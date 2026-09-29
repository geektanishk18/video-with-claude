#!/usr/bin/env python3
"""Dialogue-first sound design: synthesised SFX + a mellow music bed, ducked under the voiceover.

Usage:
    python audio_mix.py build/timeline.json cues.json --vo build/master_vo.wav --out build/final_mix.wav

cues.json:
{
  "sfx": [
    ["ding", "0", 0, 1.0],                      # [sound, when, pitch semitones, gain]
    ["ding", "P1.another", 0, 0.55],             # SEG.word  -> start of that word
    ["ding", "P1.another+0.1", 2, 0.55],         # offsets in seconds
    ["confirm", "S9.score", 0, 0.9],
    ["drop", "S6.handle", 0, 1.0],
    ["whoosh", "S7.start-0.15", 0, 0.7],         # SEG.start / SEG.end
    ["key", "S7.start+0.1", 0, 0.5, {"repeat": 18, "every": 0.07}]
  ],
  "bed": [                                        # music plays only inside these sections
    {"from": "0.5", "to": "P4.start", "drums": true},
    {"from": "S6.handle", "to": "P5.start", "drums": true},
    {"from": "P5.start", "to": "P6.end+0.2", "drums": false}
  ],
  "end_chord": "P6.end+0.25",
  "room_tone": [["P4.start", "S6.handle"]]
}

Mix rules (approved on the Unified AI Inbox reel, v3):
  voice ≈ 18 dB above music on average, never less than ~10 dB
  music ducks 65% under speech with a slow 150 ms release; SFX a little under the voice
  final loudness −15 LUFS integrated, true peak −1.2 dBTP
Sounds: ding pop click key whoosh whooshdown drop riser confirm stamp slide tick scribble tap thud step sip
"""
import argparse, json, re, subprocess
import numpy as np

SR = 48000
rng = np.random.default_rng(7)

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
def tone(f, d, a=0.004, r=0.25, h=(1, .3, .1)):
    n = int(d * SR); t = np.arange(n) / SR; return sum(amp * np.sin(2 * np.pi * f * (i + 1) * t) for i, amp in enumerate(h)) * env(n, a, r)
def bp_noise(d, f0, f1):
    n = int(d * SR); X = np.fft.rfft(rng.standard_normal(n)); fr = np.fft.rfftfreq(n, 1 / SR); X[(fr < f0) | (fr > f1)] = 0; return np.fft.irfft(X, n)
def sweep(d, f0, f1):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); seg = int(0.02 * SR)
    for i in range(0, n, seg):
        f = f0 + (f1 - f0) * i / n; X = np.fft.rfft(x[i:i + seg]); fr = np.fft.rfftfreq(len(x[i:i + seg]), 1 / SR); X[(fr < f * .6) | (fr > f * 1.6)] = 0; out[i:i + seg] = np.fft.irfft(X, len(x[i:i + seg]))
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
def L(d): return int(d * SR)
SFX = {
 'ding': lambda p=0: tone(1318.5 * 2 ** (p / 12), .6, r=.18, h=(1, .25, .08)) + .6 * tone(1975.5 * 2 ** (p / 12), .6, r=.12),
 'pop': lambda p=0: tone(620 * 2 ** (p / 12), .12, a=.002, r=.03, h=(1, .5)),
 'click': lambda p=0: bp_noise(.02, 2500, 7000) * env(L(.02), .0005, .004) * 1.5,
 'key': lambda p=0: bp_noise(.03, 1500, 5000) * env(L(.03), .0005, .006) * (.8 + .4 * rng.random()),
 'whoosh': lambda p=0: sweep(.35, 400, 4000) * .9,
 'whooshdown': lambda p=0: sweep(.5, 3000, 300) * .9,
 'drop': lambda p=0: np.sin(2 * np.pi * np.cumsum(np.linspace(90, 38, L(1.2))) / SR) * env(L(1.2), .003, .45) * 1.4 + bp_noise(1.2, 40, 180) * env(L(1.2), .002, .2) * .5,
 'riser': lambda p=0: sweep(1.2, 300, 6000) * np.linspace(.2, 1, L(1.2)) * .7,
 'confirm': lambda p=0: sum(tone(f, 1.1, r=.5, h=(1, .2)) for f in [523.25, 659.25, 783.99, 1046.5]) * .35,
 'stamp': lambda p=0: bp_noise(.18, 60, 900) * env(L(.18), .001, .05) * 1.6 + tone(110, .18, r=.06) * .8,
 'slide': lambda p=0: bp_noise(.18, 800, 3000) * np.sin(np.linspace(0, np.pi, L(.18))) * .5,
 'tick': lambda p=0: tone(1800 * 2 ** (p / 12), .06, a=.001, r=.015, h=(1,)),
 'scribble': lambda p=0: bp_noise(.9, 1500, 6000) * (.5 + .5 * np.abs(np.sin(np.linspace(0, 40, L(.9))))) * .35,
 'tap': lambda p=0: tone(880, .15, a=.001, r=.04, h=(1, .6)) * .8,
 'thud': lambda p=0: tone(70, .5, a=.002, r=.15, h=(1, .4)) * 1.2,
 'step': lambda p=0: bp_noise(.08, 100, 1200) * env(L(.08), .001, .02) * 1.1,
 'sip': lambda p=0: bp_noise(.45, 2000, 8000) * np.sin(np.linspace(0, np.pi, L(.45))) ** 2 * .45,
}

def resolver(T):
    SEG = {s['id']: s for s in T['segments']}
    clean = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
    def at(ref):
        m = re.match(r'^\s*([^+\-]+?)\s*([+\-]\s*[\d.]+)?\s*$', str(ref)); base, off = m.group(1), float((m.group(2) or '0').replace(' ', ''))
        if re.match(r'^[\d.]+$', base): return float(base) + off
        if base == 'total': return T['total'] + off
        seg, _, key = base.partition('.'); s = SEG[seg]
        if key in ('start', 'end'): return s[key] + off
        k, _, n = key.partition('#'); n = int(n or 1); c = 0
        for w in s['words']:
            if clean(w[2]) == clean(k):
                c += 1
                if c == n: return w[0] + off
        raise KeyError(f'word {key!r} not found in {seg}')
    return at

def mellow_bed(N, sections, at, end_chord=None, bpm=86):
    beat = 60 / bpm; mus = np.zeros(N)
    def add(x, t, g=1.0):
        i = int(t * SR); j = min(N, i + len(x))
        if 0 <= i < N and j > i: mus[i:j] += g * x[:j - i]
    def ep(fs, d):
        n = L(d); t = np.arange(n) / SR; o = sum(np.sin(2 * np.pi * f * t + .5 * np.exp(-t / .3) * np.sin(2 * np.pi * f * t)) for f in fs)
        return o * np.exp(-t / 1.6) * np.minimum(1, t / .02) * .07
    kick = lambda: (lambda n, t: np.sin(2 * np.pi * np.cumsum(np.linspace(110, 50, n)) / SR) * np.exp(-t / .07) * .6)(L(.3), np.arange(L(.3)) / SR)
    rim = lambda: bp_noise(.08, 1500, 5000) * np.exp(-np.arange(L(.08)) / SR / .015) * .25
    brush = lambda: bp_noise(.12, 5000, 11000) * np.exp(-np.arange(L(.12)) / SR / .04) * .08
    sub = lambda f, d: np.sin(2 * np.pi * f * np.arange(L(d)) / SR) * np.minimum(1, np.arange(L(d)) / SR / .03) * np.exp(-np.arange(L(d)) / SR / 1.2) * .28
    PROG = [([261.63, 329.63, 392, 493.88], 65.41), ([220, 261.63, 329.63, 392], 55.0), ([174.61, 220, 261.63, 329.63], 43.65), ([196, 246.94, 293.66, 349.23], 49.0)]
    gate = np.zeros(N)
    for sec in sections:
        t0, t1 = at(sec['from']), at(sec['to']); t = t0; b = 0
        while t < t1 - 1e-6:
            ch, root = PROG[(b // 4) % 4]
            if b % 4 == 0: add(ep(ch, min(beat * 4, t1 - t) + .4), t); add(sub(root, beat * 3.8), t)
            if sec.get('drums', True):
                if b % 4 in (0, 2): add(kick(), t)
                if b % 4 in (1, 3): add(rim(), t)
                add(brush(), t + beat / 2)
            t += beat; b += 1
        i0, i1 = int(t0 * SR), min(N, int((t1 + 1.6) * SR)); gate[i0:i1] = 1
        r = min(L(.4), i1 - i0); gate[i0:i0 + r] *= np.linspace(0, 1, r)
    if end_chord is not None:
        tc = at(end_chord); add(ep([261.63, 329.63, 392, 493.88, 587.33], 2.5), tc, 1.2); gate[int(tc * SR):] = 1
    mus *= np.convolve(gate, np.ones(L(.05)) / L(.05), 'same')
    fr = np.fft.rfftfreq(N, 1 / SR); return np.fft.irfft(np.fft.rfft(mus) / (1 + (fr / 3500) ** 4), N)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('timeline'); ap.add_argument('cues'); ap.add_argument('--vo', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--music', type=float, default=0.24, help='music gain (0.24 = approved v3 level)'); ap.add_argument('--sfx', type=float, default=0.22)
    a = ap.parse_args(); T = json.load(open(a.timeline)); Q = json.load(open(a.cues)); at = resolver(T)
    N = int(T['total'] * SR)
    vo = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', a.vo, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).astype(np.float64)
    vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
    sfx = np.zeros(N)
    for cue in Q.get('sfx', []):
        name, when, p, g = cue[:4]; opt = cue[4] if len(cue) > 4 else {}
        for k in range(opt.get('repeat', 1)):
            s = SFX[name](p + k * opt.get('pitch_step', 0)); i = int(max(0, at(when) + k * opt.get('every', 0)) * SR); j = min(N, i + len(s))
            if i < N: sfx[i:j] += g * s[:j - i]
    for a0, a1 in Q.get('room_tone', []):
        i0, i1 = int(at(a0) * SR), int(at(a1) * SR); sfx[i0:i1] += bp_noise((i1 - i0) / SR, 80, 900)[:i1 - i0] * .02
    mus = mellow_bed(N, Q.get('bed', []), at, Q.get('end_chord'))
    e = np.sqrt(np.convolve(vo ** 2, np.ones(2400) / 2400, 'same'))
    duck = np.convolve(1 - .65 * np.clip(e / .03, 0, 1), np.ones(7200) / 7200, 'same')
    mix = vo + mus * duck * a.music + sfx * a.sfx
    mix /= max(1e-9, np.abs(mix).max()) / .9
    raw = a.out + '.f32'; mix.astype(np.float32).tofile(raw)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', raw, '-af', 'loudnorm=I=-15:TP=-1.2:LRA=9', '-ar', '48000', '-ac', '2', a.out], check=True)
    import os; os.remove(raw)
    r = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
    gaps = [r(vo[int(s['start'] * SR):int(s['end'] * SR)]) - r((mus * duck * a.music)[int(s['start'] * SR):int(s['end'] * SR)]) for s in T['segments']]
    gaps = [g for g in gaps if g < 150]
    if gaps: print(f'voice over music: avg {np.mean(gaps):.1f} dB, min {np.min(gaps):.1f} dB (target avg ≥ 16, min ≥ 9)')
    print('wrote', a.out)

if __name__ == '__main__':
    main()
