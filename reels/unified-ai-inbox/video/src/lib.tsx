import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import EV from './data/events.json';
import TLj from './data/timeline.json';
import SUBj from './data/subtitles.json';

export const E: Record<string, number> = EV as any;
export const TL: any = TLj;
export const SUB: any[] = SUBj as any;
export const SEG: Record<string, any> = Object.fromEntries(TL.segments.map((s: any) => [s.id, s]));
export const FPS = 60;
export const W = 1080;
export const H = 1920;
export const C = {ink: '#030A0E', panel: '#08171D', panel2: '#0C2129', teal: '#1B6579', sky: '#90C2E7', peak: '#C9E4F5', paper: '#F0EDEF', amber: '#E8A33D', loss: '#D4645A', ok: '#4FA87C'};
export const BODY = 'rgba(240,237,239,.72)';
export const LABEL = 'rgba(240,237,239,.56)';
export const DISPLAY = 'Poppins, Inter, sans-serif';
export const TEXT = 'Inter, Poppins, sans-serif';

export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;
export const prog = (t: number, a: number, d: number) => clamp((t - a) / d);
export const easeOut = (p: number) => 1 - Math.pow(1 - clamp(p), 3);
export const easeIn = (p: number) => Math.pow(clamp(p), 3);
export const easeInOut = (p: number) => { p = clamp(p); return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
/** easeOutBack pop 0→1 with overshoot */
export const pop = (t: number, a: number, d = 0.28) => {
  const p = clamp((t - a) / d); if (p <= 0) return 0;
  const c1 = 1.6, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
};
/** decaying bump after time a */
export const bump = (t: number, a: number, d = 0.35) => { const p = (t - a) / d; if (p < 0 || p > 1) return 0; if (p < 0.22) { const q = p / 0.22; return q * q * (3 - 2 * q); } return 0.5 + 0.5 * Math.cos(Math.PI * (p - 0.22) / 0.78); };
/** pseudo-random noise for shake */
export const nz = (x: number) => Math.sin(x * 12.9898) * 43758.5453 % 1;
export const shake = (t: number, a: number, amp = 12, d = 0.4) => {
  const p = (t - a) / d; if (p < 0 || p > 1) return [0, 0];
  const k = amp * Math.pow(1 - p, 2); return [Math.sin(t * 91) * k, Math.cos(t * 77) * k];
};
/** talking bounce for a character, driven by word onsets */
export const talk = (t: number, who: string) => {
  let b = 0;
  for (const s of TL.segments) {
    if (s.char !== who || t < s.start - 0.1 || t > s.end + 0.3) continue;
    for (const w of s.words) { const p = (t - w[0]) / 0.2; if (p >= 0 && p <= 1) b = Math.max(b, Math.sin(Math.PI * p) * 0.035); }
  }
  return b;
};

export const Glow: React.FC<{x: number; y: number; w: number; h: number; o?: number}> = ({x, y, w, h, o = 1}) => (
  <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, borderRadius: '50%', opacity: o, filter: 'blur(24px)', pointerEvents: 'none',
    background: 'radial-gradient(ellipse at center, rgba(144,194,231,0.30) 0%, rgba(27,101,121,0.22) 40%, rgba(3,10,14,0) 70%)'}} />
);

export const Camera: React.FC<{s?: number; x?: number; y?: number; ox?: string; blur?: number; children: React.ReactNode}> = ({s = 1, x = 0, y = 0, ox = '50% 42%', blur = 0, children}) => (
  <AbsoluteFill style={{transform: `translate(${x}px,${y}px) scale(${s})`, transformOrigin: ox, filter: blur > 0.3 ? `blur(${blur}px)` : undefined}}>{children}</AbsoluteFill>
);

/** Character image anchored at its bottom-centre, with idle breathing, sway and float */
const hsh = (s: string) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 997; return h; };
export const Char: React.FC<{src: string; x: number; bottom: number; h: number; flip?: boolean; b?: number; rot?: number; o?: number; idle?: number; blur?: number; style?: React.CSSProperties}> = ({src, x, bottom, h, flip, b = 0, rot = 0, o = 1, idle = 1, blur = 0, style}) => {
  const t = useCurrentFrame() / FPS; const ph = (hsh(src.split('/')[0]) / 997) * 6.283;
  const br = idle * 0.011 * Math.sin((t * 2 * Math.PI) / 2.8 + ph);
  const sw = idle * 0.8 * Math.sin((t * 2 * Math.PI) / 3.7 + ph);
  const fy = idle * 3.5 * Math.sin((t * 2 * Math.PI) / 2.8 + ph + 1.2);
  if (o <= 0.001) return null;
  return (
    <div style={{position: 'absolute', left: x, top: bottom - h, height: h, transform: `translateX(-50%) translateY(${fy}px) rotate(${rot + sw}deg) scale(${(flip ? -1 : 1) * (1 - b / 2 - br / 2)},${1 + b + br})`, transformOrigin: '50% 100%', opacity: o, filter: blur > 0.2 ? `blur(${blur}px)` : undefined, ...style}}>
      <Img src={staticFile(src)} style={{height: h, display: 'block', filter: 'drop-shadow(0 18px 28px rgba(0,0,0,.45))'}} />
    </div>
  );
};
/** pose track with crossfade + tiny squash on each change. keys: [time, src, h?, x?] */
export const Poses: React.FC<{t: number; keys: [number, string, number?, number?][]; x: number; bottom: number; h: number; flip?: boolean; b?: number; rot?: number; o?: number}> = ({t, keys, x, bottom, h, flip, b = 0, rot = 0, o = 1}) => {
  let i = 0; keys.forEach((k, j) => { if (t >= k[0]) i = j; });
  const cur = keys[i], prev = i > 0 ? keys[i - 1] : null;
  const p = prev ? easeInOut(prog(t, cur[0] - 0.04, 0.14)) : 1;
  const sq = prev ? 0.045 * bump(t, cur[0] - 0.02, 0.32) : 0;
  return <>
    {prev && p < 1 && <Char src={prev[1]} x={prev[3] ?? x} bottom={bottom} h={prev[2] ?? h} flip={flip} b={b} rot={rot} o={o * (1 - p)} />}
    <Char src={cur[1]} x={cur[3] ?? x} bottom={bottom} h={cur[2] ?? h} flip={flip} b={b + sq} rot={rot} o={o * p} />
  </>;
};

export const DOT: Record<string, string> = {WhatsApp: C.ok, Instagram: C.loss, Website: C.sky, Email: C.amber, Chat: C.peak, Call: C.amber, CRM: C.teal};
export const Chip: React.FC<{label: string; sub?: string; x: number; y: number; s?: number; o?: number; grey?: boolean; rot?: number; blur?: number}> = ({label, sub = 'New enquiry', x, y, s = 1, o = 1, grey, rot = 0, blur = 0}) => {
  const c = grey ? '#56666c' : (DOT[label] || C.sky);
  const bl = blur + Math.max(0, 1 - s) * 10;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 340, height: 96, transform: `translate(-50%,-50%) scale(${s}) rotate(${rot}deg)`, opacity: o, filter: bl > 0.3 ? `blur(${bl}px)` : undefined,
      background: C.panel, border: `3px solid ${c}`, borderRadius: 24, display: 'flex', alignItems: 'center', gap: 16, padding: '0 22px', boxShadow: grey ? 'none' : `0 10px 30px rgba(0,0,0,.45), 0 0 24px ${c}33`}}>
      <div style={{width: 38, height: 38, borderRadius: 19, background: c, flex: 'none'}} />
      <div style={{display: 'grid', gap: 2}}>
        <div style={{font: `600 22px/1 ${TEXT}`, letterSpacing: 3, color: grey ? '#7c8a90' : C.peak, textTransform: 'uppercase'}}>{label}</div>
        <div style={{font: `400 22px/1.2 ${TEXT}`, color: grey ? '#66767c' : BODY}}>{sub}</div>
      </div>
    </div>
  );
};

/** rounded scene card (the reference-reel window) */
export const CARD = {x: 66, y: 366, w: 948, h: 800};
export const Card: React.FC<{children: React.ReactNode; bg?: string}> = ({children, bg}) => (
  <div style={{position: 'absolute', left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, borderRadius: 48, overflow: 'hidden',
    border: '4px solid rgba(144,194,231,.32)', background: bg || C.panel, boxShadow: '0 30px 80px rgba(0,0,0,.5)'}}>{children}</div>
);

export const Room: React.FC<{t: number; night?: boolean}> = ({t, night = true}) => (
  <svg width={CARD.w} height={CARD.h} viewBox={`0 0 ${CARD.w} ${CARD.h}`} style={{position: 'absolute', inset: -8, width: CARD.w + 16, height: CARD.h + 16, filter: 'blur(2.5px)'}}>
    <defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#0E2630" /><stop offset="1" stopColor="#081820" /></linearGradient></defs>
    <rect width={CARD.w} height={CARD.h} fill="url(#wall)" />
    <rect x={600} y={70} width={290} height={230} rx={14} fill={night ? '#0A1B33' : '#16384A'} stroke="#1E4452" strokeWidth={10} />
    {night && <circle cx={830} cy={125} r={26} fill="#E8E0C8" opacity={0.85} />}
    {night && [[630, 250, 36, 45], [672, 222, 32, 73], [712, 240, 40, 55], [766, 212, 36, 83], [818, 248, 36, 47], [858, 230, 26, 65]].map((r, i) => (
      <g key={i}><rect x={r[0]} y={r[1]} width={r[2]} height={r[3]} fill="#0F2440" />
        {[0, 1, 2].map((k) => <rect key={k} x={r[0] + 8} y={r[1] + 10 + k * 16} width={6} height={6} fill="#E8A33D" opacity={((i * 3 + k + Math.floor(t * 0.7)) % 4 === 0) ? 0.8 : 0.15} />)}</g>))}
    {[0, 1, 2, 3, 4].map((i) => <polygon key={i} points={`${-100 + i * 240},${CARD.h} ${30 + i * 240},${CARD.h} ${380 + i * 240},0 ${250 + i * 240},0`} fill="#fff" opacity={0.035} />)}
    <rect y={640} width={CARD.w} height={CARD.h - 640} fill="#06131A" />
  </svg>
);
export const Desk: React.FC<{y?: number; laptop?: 'busy' | 'clean' | 'none'; t?: number}> = ({y = 600, laptop = 'busy', t = 0}) => (
  <svg width={CARD.w} height={CARD.h} viewBox={`0 0 ${CARD.w} ${CARD.h}`} style={{position: 'absolute', inset: 0}}>
    <rect x={40} y={y} width={CARD.w - 80} height={30} rx={8} fill="#1A3C48" />
    <rect x={40} y={y + 30} width={CARD.w - 80} height={CARD.h - y} fill="#0B1E25" />
    {laptop !== 'none' && (
      <g transform={`translate(600,${y})`}>
        <path d="M0,0 L240,0 L220,-160 L20,-160Z" fill="#23434F" />
        <rect x={38} y={-146} width={164} height={120} rx={4} fill={C.panel} stroke={C.sky} strokeOpacity={0.4} />
        {laptop === 'busy' ? <>
          <rect x={52} y={-132} width={62} height={20} rx={5} fill={C.loss} opacity={0.5 + 0.4 * Math.abs(Math.sin(t * 6))} />
          <rect x={122} y={-132} width={66} height={20} rx={5} fill={C.amber} opacity={0.8} />
          <rect x={52} y={-104} width={136} height={20} rx={5} fill={C.ok} opacity={0.6} />
          <rect x={52} y={-76} width={100} height={20} rx={5} fill={C.loss} opacity={0.6} />
        </> : <>
          <rect x={60} y={-118} width={110} height={10} rx={5} fill={C.sky} opacity={0.7} />
          <rect x={60} y={-96} width={80} height={10} rx={5} fill={C.ok} opacity={0.7} />
        </>}
        <rect x={-20} y={-4} width={280} height={12} rx={4} fill="#2C5A68" />
      </g>)}
  </svg>
);

export const Cursor: React.FC<{x: number; y: number; click?: number}> = ({x, y, click = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, width: 60, height: 90, pointerEvents: 'none'}}>
    {click > 0 && <div style={{position: 'absolute', left: -34 + 4, top: -34 + 4, width: 68, height: 68, borderRadius: 34, border: `5px solid ${C.sky}`, opacity: 1 - click, transform: `scale(${0.4 + click})`}} />}
    <svg width={60} height={90} style={{transform: `scale(${click > 0 && click < 0.3 ? 0.9 : 1})`, transformOrigin: '0 0'}}><path d="M2,2 L2,70 L19,55 L32,82 L45,76 L32,51 L54,51Z" fill={C.paper} stroke={C.ink} strokeWidth={4} /></svg>
  </div>
);
/** cursor path through keyframes [t,x,y] with eased arcs; returns x,y and click progress */
export const cursorAt = (t: number, keys: [number, number, number][], clicks: number[] = []) => {
  let x = keys[0][1], y = keys[0][2];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, x0, y0] = keys[i], [t1, x1, y1] = keys[i + 1];
    if (t >= t1) { x = x1; y = y1; continue; }
    if (t >= t0) { const p = easeInOut((t - t0) / (t1 - t0)); const arc = Math.sin(Math.PI * p) * 0.12 * Math.hypot(x1 - x0, y1 - y0); x = lerp(x0, x1, p) - arc * 0.3; y = lerp(y0, y1, p) - arc; }
    break;
  }
  let c = 0; for (const k of clicks) { const p = (t - k) / 0.3; if (p >= 0 && p <= 1) c = p; }
  return {x, y, click: c};
};

export const Win: React.FC<{x: number; y: number; w: number; h: number; title: string; children?: React.ReactNode; o?: number; ty?: number}> = ({x, y, w, h, title, children, o = 1, ty = 0}) => (
  <div style={{position: 'absolute', left: x, top: y + ty, width: w, height: h, opacity: o, filter: o < 0.99 ? `blur(${(1 - o) * 14}px)` : undefined, borderRadius: 30, background: C.panel, border: '3px solid rgba(144,194,231,.3)', overflow: 'hidden', boxShadow: '0 30px 80px rgba(0,0,0,.55)'}}>
    <div style={{height: 76, background: C.panel2, display: 'flex', alignItems: 'center', padding: '0 26px', gap: 12}}>
      {[C.loss, C.amber, C.ok].map((c) => <div key={c} style={{width: 18, height: 18, borderRadius: 9, background: c, opacity: 0.85}} />)}
      <div style={{marginLeft: 18, flex: 1, height: 40, borderRadius: 20, background: 'rgba(240,237,239,.05)', display: 'flex', alignItems: 'center', padding: '0 18px', font: `500 20px/1 ${TEXT}`, color: LABEL, letterSpacing: 1}}>app.figuredout.ai/<span style={{color: C.peak}}>{title}</span></div>
    </div>
    <div style={{position: 'relative', width: '100%', height: h - 76}}>{children}</div>
  </div>
);
