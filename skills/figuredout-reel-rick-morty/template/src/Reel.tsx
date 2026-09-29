import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame} from 'remotion';
import {C, E, SEG, SUB, FPS, DISPLAY, TEXT, LABEL, prog, pop, bump, clamp, easeOut, easeInOut, talk, Portal} from './lib';
import {Hook, Chaos, Enter, Manual, Beat, Insight, Reveal, Payoff, Sip} from './cartoon';
import {Understand, Qualify, Score, Sort, Industries, Criteria, Route, PIP} from './ui';

// [start, end, component, transition-in: 'blur' | 'cut' | 'portal']
const SHOTS: [number, number, React.FC<{t: number}>, string][] = [
  [0, SEG.P1.start, Hook, 'cut'],
  [SEG.P1.start, E.s1 - 0.07, Chaos, 'blur'],
  [E.s1 - 0.07, E.p3 - 0.07, Enter, 'cut'],
  [E.p3 - 0.07, E.s2 - 0.07, Manual, 'blur'],
  [E.s2 - 0.07, E.s3, Beat, 'cut'],
  [E.s3, E.s6 - 0.07, Insight, 'cut'],
  [E.s6 - 0.07, E.s7 - 0.2, Reveal, 'blur'],
  [E.s7 - 0.2, E.s8 - 0.07, Understand, 'blur'],
  [E.s8 - 0.07, E.s9 - 0.07, Qualify, 'blur'],
  [E.s9 - 0.07, E.s10 - 0.2, Score, 'blur'],
  [E.s10 - 0.2, E.s12 - 0.07, Sort, 'blur'],
  [E.s12 - 0.07, E.s13 - 0.2, Industries, 'blur'],
  [E.s13 - 0.2, E.s14 - 0.07, Criteria, 'blur'],
  [E.s14 - 0.07, E.p5 - 0.1, Route, 'blur'],
  [E.p5 - 0.1, E.p6 - 0.07, Payoff, 'cut'],
  [E.p6 - 0.07, E.total + 1, Sip, 'blur'],
];
const TD = 0.32;

const STN = ['UNDERSTAND', 'QUALIFY', 'SCORE', 'MATCH', 'ROUTE'];
const trackerK = (t: number) => {
  if (t < E.s7) return 0;
  if (t < E.s8) return prog(t, E.s7, E.s8 - E.s7);
  if (t < E.s9) return 1 + prog(t, E.s8, E.s9 - E.s8);
  if (t < E.s10) return 2 + prog(t, E.s9, E.score + 0.3 - E.s9);
  if (t < E.s14) return 3 + prog(t, E.s10, E.s14 - E.s10);
  return 4 + prog(t, E.s14, E.best + 0.3 - E.s14);
};
const Tracker: React.FC<{t: number}> = ({t}) => {
  const vis = t >= 0.5 && t < E.s3 ? prog(t, 0.5, 0.4) * (1 - prog(t, E.s3 - 0.2, 0.2)) : t >= E.handle + 0.9 ? prog(t, E.handle + 0.9, 0.4) * (1 - prog(t, E.total - 0.8, 0.4)) : 0;
  if (vis <= 0) return null;
  const k = trackerK(t), x0 = 150, x1 = 930, y = 262;
  const mx = x0 + (x1 - x0) * clamp(k, 0, 4) / 4;
  const geek = t > E.ai;
  return (
    <div style={{position: 'absolute', inset: 0, opacity: vis, transform: `translateY(${-30 * (1 - vis)}px)`}}>
      <div style={{position: 'absolute', left: x0, top: y - 6, width: x1 - x0, height: 12, borderRadius: 6, background: 'rgba(144,194,231,.16)'}} />
      <div style={{position: 'absolute', left: x0, top: y - 6, width: (x1 - x0) * clamp(k, 0, 4) / 4, height: 12, borderRadius: 6, background: C.sky, boxShadow: '0 0 16px rgba(144,194,231,.6)'}} />
      {STN.map((s, i) => {
        const x = x0 + (x1 - x0) * i / 4, done = k >= i + 1 || (i === 4 && k >= 5), cur = !done && k > i - 0.001 && k > 0 && Math.floor(k) === i;
        const b = done ? pop(t, 0, 0.01) : 1;
        return <React.Fragment key={s}>
          <div style={{position: 'absolute', left: x - 22, top: y - 22, width: 44, height: 44, borderRadius: 22, background: done ? C.ok : cur ? C.sky : C.panel, border: done || cur ? 'none' : '3px solid rgba(144,194,231,.45)', display: 'grid', placeItems: 'center', font: `800 24px/1 ${DISPLAY}`, color: C.ink, transform: `scale(${b})`}}>{done ? '✓' : ''}</div>
          <div style={{position: 'absolute', left: x - 90, width: 180, top: y + 32, textAlign: 'center', font: `600 17px/1 ${TEXT}`, letterSpacing: 2, color: done || cur ? C.peak : 'rgba(240,237,239,.45)'}}>{s}</div>
        </React.Fragment>;
      })}
      <Img src={staticFile(geek ? 'stewie/geek_headset.png' : 'stewie/smug.png')} style={{position: 'absolute', left: mx - 40, top: y - 112, height: 100, transform: `translateY(${-Math.abs(Math.sin(t * 9)) * (k > 0 && k < 5 && k % 1 > 0.02 ? 8 : 0)}px)`}} />
    </div>
  );
};

const clean = (w: string) => w.toLowerCase().replace(/[^a-z0-9%]/g, '');
const SENTENCE = new Set(['S3', 'S4', 'S5']);
const Subtitles: React.FC<{t: number}> = ({t}) => {
  const c = SUB.find((s) => t >= s.start - 0.04 && t < s.out);
  if (!c) return null;
  const words = c.text.split(' ');
  const em = new Set((c.em as string[]).flatMap((e) => e.split(' ').map(clean)));
  const exit = 1 - prog(t, c.out - 0.12, 0.12);
  const sentence = SENTENCE.has(c.seg);
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1250, height: 190, display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center', alignContent: 'center', gap: '4px 20px', opacity: exit}}>
      {words.map((w: string, i: number) => {
        const wt = c.words[i] ? c.words[i][0] : c.start;
        const isEm = em.has(clean(w));
        const s = sentence ? 1 : pop(t, wt - 0.03, 0.22);
        const o = sentence ? prog(t, c.start - 0.04, 0.3) : clamp(s * 3);
        if (!sentence && t < wt - 0.03) return <span key={i} style={{visibility: 'hidden', font: `700 72px/1.15 ${DISPLAY}`}}>{w}</span>;
        const bl = sentence ? (1 - o) * 10 : Math.max(0, 1 - prog(t, wt - 0.03, 0.14)) * 9;
        return <span key={i} style={{display: 'inline-block', transform: `scale(${s})`, opacity: o, filter: bl > 0.3 ? `blur(${bl}px)` : undefined,
          font: isEm ? `italic 800 76px/1.15 ${DISPLAY}` : `700 72px/1.15 ${DISPLAY}`, textTransform: isEm ? 'uppercase' : 'none',
          color: isEm ? C.sky : C.paper, textShadow: isEm ? '0 0 26px rgba(144,194,231,.55), 0 4px 18px rgba(0,0,0,.85)' : '0 4px 18px rgba(0,0,0,.85)'}}>{w}</span>;
      })}
    </div>
  );
};

export const Reel: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let idx = SHOTS.findIndex((s) => t >= s[0] && t < s[1]); if (idx < 0) idx = SHOTS.length - 1;
  const [s0, , Comp, tr] = SHOTS[idx];
  let scene: React.ReactNode = <Comp t={t} />;
  const PD = 0.7; // portal transition: a portal opens mid-frame and the next scene appears inside it
  if (idx > 0 && tr === 'portal' && t < s0 + PD) {
    const p = easeInOut((t - s0) / PD), Prev = SHOTS[idx - 1][2], R = 1300 * p;
    scene = <>
      <AbsoluteFill style={{filter: `blur(${6 * p}px)`, transform: `scale(${1 + 0.08 * p}) rotate(${-4 * p}deg)`}}><Prev t={t} /></AbsoluteFill>
      <AbsoluteFill style={{clipPath: `circle(${R}px at 540px 820px)`}}><Comp t={t} /></AbsoluteFill>
      <Portal x={540} y={820} r={Math.max(2, R / 0.92)} t={t} ring={clamp((p - 0.12) / 0.2)} o={1 - prog(t, s0 + PD * 0.55, PD * 0.4)} />
    </>;
  }
  if (idx > 0 && tr === 'blur' && t < s0 + TD) {
    const p = easeInOut((t - s0) / TD), Prev = SHOTS[idx - 1][2];
    scene = <>
      <AbsoluteFill style={{opacity: 1 - p, filter: `blur(${18 * p}px)`, transform: `scale(${1 + 0.05 * p})`}}><Prev t={t} /></AbsoluteFill>
      <AbsoluteFill style={{opacity: p, filter: p < 0.98 ? `blur(${18 * (1 - p)}px)` : undefined, transform: `scale(${1.05 - 0.05 * p})`}}><Comp t={t} /></AbsoluteFill>
    </>;
  }
  const ui = t >= E.s7 - 0.2 && t < E.p5 - 0.1;
  const industries = t >= E.s12 - 0.07 && t < E.s13 - 0.2;
  const leak = bump(t, E.handle, 0.8);
  const white = 0.18 * bump(t, E.ai, 0.2) + 0.1 * bump(t, E.first, 0.15) + 0.1 * bump(t, E.everywhere, 0.15) + 0.12 * bump(t, E.score, 0.2);
  return (
    <AbsoluteFill style={{background: C.ink, backgroundImage: 'radial-gradient(rgba(144,194,231,.06) 1.2px, transparent 1.2px)', backgroundSize: '24px 24px', overflow: 'hidden'}}>
      {scene}
      {ui && !industries && <PIP src="stewie/geek_headset.png" t={t} at={E.s7 - 0.15} x={905} y={430} r={88} ih={250} b={talk(t, 'Stewie')} />}
      {industries && <div style={{position: 'absolute', left: 175, top: 1262 - 270, transform: `translateX(-50%) translateY(${60 * (1 - easeOut(prog(t, E.s12, 0.4)))}px) scale(${1 - talk(t, 'Stewie') / 2},${1 + talk(t, 'Stewie')})`, transformOrigin: '50% 100%'}}>
        <Img src={staticFile('stewie/geek_laptop.png')} style={{height: 270, filter: 'drop-shadow(0 16px 26px rgba(0,0,0,.5))'}} /></div>}
      <Tracker t={t} />
      <Subtitles t={t} />
      {leak > 0 && <AbsoluteFill style={{mixBlendMode: 'screen', opacity: leak, background: 'radial-gradient(circle at 30% 35%, rgba(255,246,224,.95) 0%, rgba(201,228,245,.75) 30%, rgba(144,194,231,.35) 60%, rgba(3,10,14,0) 85%)'}} />}
      {white > 0 && <AbsoluteFill style={{background: '#fff', opacity: white}} />}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.45) 100%)', pointerEvents: 'none'}} />
      <Audio src={staticFile('final_mix.wav')} />
    </AbsoluteFill>
  );
};
