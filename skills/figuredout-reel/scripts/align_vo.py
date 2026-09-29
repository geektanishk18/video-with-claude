#!/usr/bin/env python3
"""Align per-character voiceover files to an approved script and build the master timeline.

Usage:
    python align_vo.py script.json --out build/

script.json:
{
  "files": {"Peter": "audio/peter.mp3", "Stewie": "audio/stewie.mp3"},
  "lead_in": 0.5,                 # silence before the first line (hook visual)
  "tail": 1.5,                    # silence after the last line
  "lines": [
    {"id": "P1", "char": "Peter",  "text": "Stewie... we've got another lead.",
     "gap": 0.5, "subs": "Stewie...|we've got *another*|*lead.*"},
    {"id": "S1", "char": "Stewie", "text": "And you're handling all of them manually?", "gap": 0.4},
    {"id": "S2", "char": "Stewie", "text": "Every single one?", "gap": "recorded"}
  ]
}

gap   : seconds of silence before the line, or "recorded" to keep the pause the actor left
        (only valid when the previous line is from the same file).
subs  : optional subtitle plan. "|" separates on-screen chunks, *word* marks emphasis.
        Its word count must equal the spoken word count; otherwise chunks are automatic.

Outputs (in --out): timeline.json, subtitles.json, master_vo.wav, words_<char>.json, report.txt
The report lists every recorded word that is NOT in the script (ad-libs, stray takes) so they can be
reviewed. They are left out of the timeline by default.
"""
import argparse, json, os, re, subprocess, sys
from difflib import SequenceMatcher

def norm(w): return re.sub(r"[^a-z0-9%₹]", "", w.lower().replace("inquiry", "enquiry"))

def transcribe(path, model):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(path, word_timestamps=True, beam_size=5)
    return [[round(w.start, 3), round(w.end, 3), w.word.strip()] for s in segs for w in s.words]

def silences(path, db=-38, d=0.18):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(st, en))

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)

def align(lines, words):
    """Greedy in-order alignment of script lines onto the word stream. Returns spans and unscripted words."""
    toks = [norm(w[2]) for w in words]; pos = 0; spans = {}; used = set()
    for ln in lines:
        spoken = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", ln["text"])  # FiguredOutAI -> Figured Out AI
        target = [norm(x) for x in spoken.split() if norm(x)]
        best = (0, pos, pos + len(target))
        for i in range(pos, len(toks)):
            for L in range(max(1, len(target) - 3), len(target) + 4):
                j = i + L
                if j > len(toks): break
                r = SequenceMatcher(None, target, toks[i:j]).ratio()
                if r > best[0]: best = (r, i, j)
            if best[0] > 0.95: break
        r, i, j = best
        if r < 0.5: sys.exit(f"Could not find line {ln['id']} ({ln['text']!r}) in the recording (best match {r:.2f}).")
        spans[ln["id"]] = (i, j, r); used.update(range(i, j)); pos = j
    extra = [words[k] for k in range(len(words)) if k not in used]
    return spans, extra

def refine(a, b, sil, dur):
    """Snap speech edges to silence boundaries detected by ffmpeg."""
    ends = [e for s, e in sil if abs(e - a) < 0.35]      # speech starts where a silence ends
    starts = [s for s, e in sil if -0.35 < s - b < 0.45]  # speech ends where a silence starts
    na = min(ends, key=lambda e: abs(e - a)) if ends else max(0, a - 0.05)
    nb = min(starts, key=lambda s: abs(s - b)) if starts else min(dur, b + 0.12)
    return na, max(nb, na + 0.2)

def chunk_auto(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.,?!…]$", w[2]) or len(cur) >= 3 or cur[-1][1] - cur[0][0] > 1.0: out.append(cur); cur = []
    if cur: out.append(cur)
    return [dict(text=" ".join(x[2] for x in c), em=[], words=[[x[0], x[1]] for x in c]) for c in out]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--out", default="build"); ap.add_argument("--model", default="small.en")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    S = json.load(open(a.script)); base = os.path.dirname(os.path.abspath(a.script))
    files = {c: os.path.join(base, p) for c, p in S["files"].items()}
    report = []
    W, SIL, DUR, SP = {}, {}, {}, {}
    for c, p in files.items():
        W[c] = transcribe(p, a.model); SIL[c] = silences(p); DUR[c] = duration(p)
        json.dump(W[c], open(os.path.join(a.out, f"words_{c}.json"), "w"))
        spans, extra = align([l for l in S["lines"] if l["char"] == c], W[c]); SP.update(spans)
        if extra: report.append(f"{c}: unscripted words (left out): " + " ".join(f"{w[2]}@{w[0]:.2f}" for w in extra))
    t = 0; segs = []; prev = None
    for k, ln in enumerate(S["lines"]):
        c = ln["char"]; i, j, r = SP[ln["id"]]; ws = W[c][i:j]
        src_a, src_b = refine(ws[0][0], ws[-1][1], SIL[c], DUR[c])
        gap = ln.get("gap", 0.45 if k else S.get("lead_in", 0.5))
        if gap == "recorded":
            if not prev or prev["char"] != c: sys.exit(f"{ln['id']}: 'recorded' gap needs the previous line from the same file")
            before = [e - st for st, e in SIL[c] if abs(e - src_a) < 0.02]  # the actor's own pause right before this line
            gap = max(0.05, before[0] if before else src_a - prev["src"][1])
        t += gap; d = src_b - src_a
        seg = dict(id=ln["id"], char=c, file=files[c], src=[round(src_a, 3), round(src_b, 3)], start=round(t, 3), end=round(t + d, 3), dur=round(d, 3),
                   gap_before=round(gap, 3), text=ln["text"], match=round(r, 2), words=[[round(t + w[0] - src_a, 3), round(t + w[1] - src_a, 3), w[2]] for w in ws])
        seg["wps"] = round(len(ws) / d, 2); segs.append(seg); t += d; prev = seg
        if r < 0.85: report.append(f"{ln['id']}: recording differs from script (match {r:.2f}): heard {' '.join(w[2] for w in ws)!r}")
    total = round(t + S.get("tail", 1.5), 3)
    for k, s in enumerate(segs): s["gap_after"] = round((segs[k + 1]["start"] if k + 1 < len(segs) else total) - s["end"], 3)
    json.dump(dict(total=total, segments=segs), open(os.path.join(a.out, "timeline.json"), "w"), indent=1)
    subs = []
    for s, ln in zip(segs, S["lines"]):
        ws = s["words"]; plan = ln.get("subs")
        if plan and sum(len(x.split()) for x in plan.split("|")) == len(ws):
            i = 0
            for ch in plan.split("|"):
                n = len(ch.split()); part = ws[i:i + n]; i += n
                subs.append(dict(seg=s["id"], start=part[0][0], end=part[-1][1], text=ch.replace("*", ""),
                                 em=[re.sub(r"[*.,?!]", "", x) for x in re.findall(r"\*[^*]+\*", ch)], words=[[w[0], w[1]] for w in part]))
        else:
            if plan: report.append(f"{s['id']}: subs plan word count != spoken words ({len(ws)}); used automatic chunks")
            for c in chunk_auto(ws): subs.append(dict(seg=s["id"], start=c["words"][0][0], end=c["words"][-1][1], **c))
    for k, c in enumerate(subs):
        nxt = subs[k + 1]["start"] if k + 1 < len(subs) else total; c["out"] = round(min(nxt, c["end"] + 0.5), 3)
    json.dump(subs, open(os.path.join(a.out, "subtitles.json"), "w"), indent=1)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for s in segs: cmd += ["-ss", str(s["src"][0]), "-to", str(s["src"][1]), "-i", s["file"]]
    fc = ";".join(f"[{i}]adelay={int(round(s['start'] * 1000))}:all=1[a{i}]" for i, s in enumerate(segs))
    fc += ";" + "".join(f"[a{i}]" for i in range(len(segs))) + f"amix=inputs={len(segs)}:normalize=0,apad,atrim=0:{total}[m]"
    subprocess.run(cmd + ["-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "1", os.path.join(a.out, "master_vo.wav")], check=True)
    open(os.path.join(a.out, "report.txt"), "w").write("\n".join(report) or "Recording matches the script.")
    print(f"timeline {total:.2f}s · {len(segs)} lines · {len(subs)} subtitle chunks"); print("\n".join(report))

if __name__ == "__main__":
    main()
