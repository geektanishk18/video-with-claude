import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, E, SEG, Card, Room, Desk, Char, Poses, Chip, Camera, Glow, pop, bump, shake, prog, easeOut, easeInOut, lerp, clamp, talk, CARD, DISPLAY, TEXT, BODY, LABEL, Win, Cursor, cursorAt} from './lib';

const P = (n: number) => `peter/p${String(n).padStart(2, '0')}.png`;
const ST = (v: string) => `stewie/${v}.png`;
const A = E.another;
const f0 = SEG.P1.end + 0.08, f1 = E.really - 0.1;
const FL = (i: number) => f0 + (f1 - f0) * i / 5;
// [label, sub, x, y, appear]
export const CHIPS: [string, string, number, number, number][] = [
  ['WhatsApp', 'New lead', 290, 470, 0],
  ['Instagram', 'New DM', 800, 450, A], ['Website', 'Form submitted', 250, 650, A + 0.1], ['Email', 'New enquiry', 830, 640, A + 0.2],
  ['Chat', 'Visitor waiting', 270, 830, A + 0.3], ['Call', 'Missed call', 810, 820, A + 0.4],
  ['WhatsApp', 'Is this available?', 540, 420, FL(0)], ['Instagram', 'Story reply', 250, 1010, FL(1)], ['Email', 'Re: pricing', 820, 1010, FL(2)],
  ['Website', 'Demo request', 540, 1090, FL(3)], ['Chat', 'Hello??', 190, 560, FL(4)], ['CRM', 'Task overdue', 880, 540, FL(5)],
];
const chipLayer = (t: number, o = 1, grey = false, fallFrom = 0) => CHIPS.map((c, i) => {
  if (t < c[4]) return null;
  const s = pop(t, c[4], 0.26);
  const dx = Math.sin(t * 1.3 + i) * 6, dy = Math.cos(t * 1.1 + i * 2) * 6;
  let fy = 0, rot = Math.sin(i * 7) * 3;
  if (fallFrom) { const ft = Math.max(0, t - fallFrom - i * 0.03); fy = 900 * ft * ft; rot += ft * 60 * (i % 2 ? 1 : -1); }
  const k = shake(t, E.everywhere, 14, 0.45);
  return <Chip key={i} label={c[0]} sub={c[1]} x={c[2] + dx + k[0]} y={c[3] + dy + fy + k[1]} s={s * (1 + 0.08 * bump(t, E.everywhere, 0.4))} o={o} grey={grey} rot={rot} blur={o < 0.6 ? 3 : 0} />;
});

/* A · 0 → P1 start: one chip on black */
export const Hook: React.FC<{t: number}> = ({t}) => (
  <AbsoluteFill>
    <Glow x={540} y={880} w={900} h={560} o={pop(t, 0, 0.3)} />
    <Chip label="WhatsApp" sub="New lead" x={540} y={880} s={1.6 * pop(t, 0, 0.3) * (1 + 0.1 * bump(t, 0, 0.3))} />
  </AbsoluteFill>
);

/* B + C · Peter at desk, chips escalate (P1, Really?, P2) */
export const Chaos: React.FC<{t: number}> = ({t}) => {
  const k = shake(t, E.everywhere, 10, 0.45), k2 = shake(t, FL(2), 6, 0.9);
  const whip = t >= E.actually ? 1 - easeOut(prog(t, E.actually - 0.05, 0.25)) : 0;
  const scale = 1 + 0.05 * prog(t, SEG.P1.start, 3) + 0.14 * bump(t, A, 0.4) + 0.12 * bump(t, E.really, 0.35) + 0.1 * bump(t, E.everywhere, 0.45);
  const b = talk(t, 'Peter');
  // channel ring on "coming"
  const ring = ['WHATSAPP', 'INSTAGRAM', 'WEBSITE', 'EMAIL', 'CHAT', 'CALLS'];
  return (
    <Camera s={scale} x={k[0] + k2[0] + whip * -260} y={k[1] + k2[1]} blur={whip * 14}>
      <Card><Room t={t} />
        <Poses t={t} keys={[[0, P(1), 640, 400], [E.really, P(8), 560, 430], [E.actually, P(3), 560, 400], [E.everywhere, P(4), 570, 400]]} x={400} bottom={700} h={560} b={b} />
        <Desk laptop="busy" t={t} />
      </Card>
      {chipLayer(t, t >= E.coming ? 0.55 : 1)}
      {t >= E.coming && ring.map((r, i) => {
        const a = (i / ring.length) * Math.PI * 2 - Math.PI / 2, s = pop(t, E.coming + i * 0.08, 0.25);
        const x = 540 + Math.cos(a) * 380, y = 760 + Math.sin(a) * 330;
        const col = [C.ok, C.loss, C.sky, C.amber, C.peak, C.amber][i];
        return <div key={r} style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${s * (1 + 0.1 * bump(t, E.everywhere, 0.4))})`, padding: '18px 30px', borderRadius: 40, background: C.panel, border: `4px solid ${col}`, font: `700 30px/1 ${TEXT}`, letterSpacing: 4, color: C.peak, boxShadow: `0 0 30px ${col}55`}}>{r}</div>;
      })}
    </Camera>
  );
};

/* D · Stewie enters (S1) */
export const Enter: React.FC<{t: number}> = ({t}) => {
  const whip = 1 - easeOut(prog(t, E.s1 - 0.05, 0.28));
  const push = 0.18 * easeInOut(prog(t, E.manually - 0.1, 0.5));
  return (
    <Camera s={1 + push} ox="72% 50%" x={whip * 320} blur={whip * 16}>
      <Card><Room t={t} />
        <Char src={P(9)} x={290} bottom={720} h={540} b={talk(t, 'Peter')} />
        <Desk laptop="busy" t={t} />
        <Char src={ST('smug')} x={700} bottom={612} h={330} flip b={talk(t, 'Stewie')} style={{}} />
      </Card>
      {chipLayer(t, 0.28)}
    </Camera>
  );
};

/* E · manual qualification form (P3) */
export const Manual: React.FC<{t: number}> = ({t}) => {
  const t0 = E.p3;
  const unroll = easeOut(prog(t, t0 - 0.05, 0.35));
  const fields: [string, string][] = [['NAME', 'Priya S.'], ['BUDGET', ''], ['LOCATION', '?'], ['INTENT', '?'], ['TIMELINE', '?'], ['REQUIREMENT', '?'], ['FOLLOW-UP', '?']];
  const typed = '₹2'.slice(0, Math.max(0, Math.floor((t - E.qualify - 0.25) / 0.2)));
  const cur = cursorAt(t, [[t0, 900, 1150], [t0 + 0.6, 900, 1150], [E.qualify - 0.05, 700, 588]], [E.qualify]);
  const slam = pop(t, E.first, 0.22);
  const k = shake(t, E.first, 12, 0.35);
  const zoom = 1 + 0.12 * easeInOut(prog(t, t0, 0.5)) + 0.1 * bump(t, E.first, 0.35);
  return (
    <Camera s={zoom} x={k[0]} y={k[1]} ox="50% 40%">
      <Win x={110} y={400} w={860} h={Math.max(80, 720 * unroll)} title="leads/priya-s · manual">
        {fields.map(([k2, v], i) => {
          const y = 40 + i * 86; const isB = i === 1; const active = isB && t >= E.qualify;
          return <div key={k2} style={{position: 'absolute', left: 40, right: 40, top: y, height: 70, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', borderRadius: 16,
            border: `3px solid ${active ? C.sky : 'rgba(144,194,231,.12)'}`, background: active ? 'rgba(144,194,231,.08)' : 'rgba(240,237,239,.03)'}}>
            <span style={{font: `500 24px/1 ${TEXT}`, letterSpacing: 3, color: LABEL}}>{k2}</span>
            <span style={{font: `700 32px/1 ${DISPLAY}`, color: i === 0 ? C.paper : C.amber}}>{isB ? (typed || (active ? '' : '?')) : v}{active && Math.floor(t * 3.8) % 2 === 0 ? <span style={{color: C.sky}}>|</span> : null}
              {i === 0 && <span style={{marginLeft: 14, color: C.ok}}>✓</span>}</span>
          </div>;
        })}
      </Win>
      <Char src={P(6)} x={880} bottom={1262} h={250} b={talk(t, 'Peter')} />
      {t >= t0 + 0.2 && <Cursor x={cur.x} y={cur.y} click={cur.click} />}
      {t >= E.first && <Chip label="Instagram" sub="New DM · just now" x={540} y={430} s={1.35 * slam} rot={-4} />}
    </Camera>
  );
};

/* F · Every single one? / ...Yes. / stare */
export const Beat: React.FC<{t: number}> = ({t}) => {
  if (t < SEG.S2.end) {
    const s = 1 + 0.04 * prog(t, SEG.S2.start, 1.2);
    return <Camera s={s}><Card><Room t={t} /><Char src={ST('smug')} x={474} bottom={800} h={640} b={talk(t, 'Stewie')} /></Card></Camera>;
  }
  if (t < SEG.P4.end + 0.05) {
    const s = 1 + 0.08 * easeInOut(prog(t, SEG.S2.end, 1.2));
    const slump = easeOut(prog(t, E.p4, 0.3));
    return <Camera s={s} ox="40% 40%"><Card><Room t={t} />
      <Char src={P(9)} x={420} bottom={770 + 14 * slump} h={620} rot={-2 * slump} b={talk(t, 'Peter')} />
      <div style={{position: 'absolute', left: 560, top: 180 + 60 * prog(t, SEG.S2.end + 0.2, 1.0), width: 22, height: 30, borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%', background: C.sky, opacity: 0.9 * (1 - prog(t, E.p4 + 0.3, 0.3))}} />
      <Desk laptop="busy" t={t} /></Card></Camera>;
  }
  const s = 1 + 0.05 * prog(t, SEG.P4.end, 0.9);
  return <Camera s={s}><Card><Room t={t} /><Char src={ST('smug')} x={474} bottom={800} h={660} /></Card></Camera>;
};

/* G + H · freeze, insight */
export const Insight: React.FC<{t: number}> = ({t}) => {
  const cardO = 1 - prog(t, E.s3, 0.35);
  const s = 1 + 0.05 * prog(t, E.s4, 4);
  const tangle = prog(t, E.work - 0.1, 0.9);
  const dots = [[300, 470], [780, 450], [230, 640], [850, 620], [540, 520], [400, 760], [700, 760]];
  const lines = [[0, 4, 60], [4, 1, -80], [1, 3, 90], [3, 6, -60], [6, 5, 120], [5, 2, -90], [2, 0, 70], [0, 6, 200], [1, 5, -180], [4, 3, 140], [2, 4, -120]];
  return (
    <AbsoluteFill>
      <div style={{opacity: cardO}}><Card><Room t={t} /></Card></div>
      {t < E.s4 + 0.4 && chipLayer(t, 1, true, E.s3)}
      <Camera s={s}>
        <Glow x={540} y={880} w={900} h={900} o={prog(t, E.s3 + 0.2, 0.8)} />
        {tangle > 0 && <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
          {lines.map(([a, b, bend], i) => {
            const [x0, y0] = dots[a], [x1, y1] = dots[b]; const mx = (x0 + x1) / 2 + bend, my = (y0 + y1) / 2 - bend * 0.6;
            const L = 900; const p = clamp(tangle * 1.6 - i * 0.06);
            return <path key={i} d={`M${x0},${y0} Q${mx},${my} ${x1},${y1}`} stroke={C.amber} strokeOpacity={0.75} strokeWidth={5} fill="none" strokeDasharray={L} strokeDashoffset={L * (1 - p)} strokeLinecap="round" />;
          })}
          {dots.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={16 * pop(t, E.s5 + i * 0.05, 0.25)} fill="#56666c" stroke={C.paper} strokeOpacity={0.4} strokeWidth={3} />)}
        </svg>}
        <Char src={ST('smug')} x={540} bottom={1200} h={tangle > 0 ? 440 : 560} b={talk(t, 'Stewie')} />
      </Camera>
    </AbsoluteFill>
  );
};

/* I · Let the AI handle it → reveal flow */
const CH = ['WhatsApp', 'Instagram', 'Website', 'Email', 'Chat'];
export const Reveal: React.FC<{t: number}> = ({t}) => {
  const geek = t >= E.ai;
  const flowStart = E.handle + 0.15;
  const toCorner = easeInOut(prog(t, E.s6end + 0.2, 0.7));
  const sx = lerp(540, 905, toCorner), sb = lerp(1180, 560, toCorner), sh = lerp(620, 250, toCorner);
  const fadeO = 1 - prog(t, E.s7 - 0.35, 0.2);
  const snap = 1 + 0.14 * bump(t, E.ai, 0.3);
  const fl = prog(t, flowStart, 0.9);
  return (
    <AbsoluteFill>
      <Camera s={snap}>
        <Glow x={540} y={900} w={1000} h={900} o={1 - toCorner * 0.4} />
        {fl > 0 && <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
          {CH.map((c, i) => {
            const y = 520 + i * 105; const L = 700; const p = clamp(fl * 1.4 - i * 0.08);
            const col = [C.ok, C.loss, C.sky, C.amber, C.peak][i];
            return <g key={c}><path d={`M300,${y} C520,${y} 520,780 700,780`} stroke={col} strokeWidth={7} fill="none" strokeDasharray={L} strokeDashoffset={L * (1 - p)} />
              <text x={280} y={y + 11} textAnchor="end" fontFamily={TEXT} fontWeight={600} fontSize={30} letterSpacing={3} fill={C.peak} opacity={p}>{c.toUpperCase()}</text>
              {p > 0.3 && p < 1 && <circle r={9} fill={col} cx={lerp(300, 700, (t * 1.4 + i * 0.2) % 1)} cy={lerp(y, 780, easeInOut((t * 1.4 + i * 0.2) % 1))} />}</g>;
          })}
        </svg>}
        {fl > 0 && <div style={{position: 'absolute', left: 700, top: 690, width: 270, height: 180, borderRadius: 32, background: C.panel, border: `${4 + 3 * bump(t, flowStart + 0.9, 0.5)}px solid ${C.sky}`, display: 'grid', placeItems: 'center', alignContent: 'center',
          transform: `scale(${pop(t, flowStart + 0.5, 0.35)})`, boxShadow: `0 0 ${40 + 40 * bump(t, flowStart + 0.9, 0.6)}px rgba(144,194,231,.45)`}}>
          <div style={{font: `800 50px/1 ${DISPLAY}`, color: C.sky}}>AI</div><div style={{font: `700 36px/1.2 ${DISPLAY}`, color: C.paper}}>INBOX</div></div>}
        <Poses t={t} keys={[[0, ST('smug'), sh], [E.ai, ST('geek_headset'), sh * 1.1]]} x={sx} bottom={sb} h={sh} o={fadeO} b={talk(t, 'Stewie')} rot={geek ? -2 * bump(t, E.ai, 0.4) : 0} />
      </Camera>
    </AbsoluteFill>
  );
};

/* R + S · payoff room */
export const Payoff: React.FC<{t: number}> = ({t}) => {
  const whip = 1 - easeOut(prog(t, E.p5 - 0.08, 0.3));
  const walk = prog(t, E.s15 - 0.1, 1.5);
  const sx = lerp(1050, 690, easeOut(walk));
  return (
    <Camera s={1 + 0.05 * prog(t, E.p5, 4)} x={whip * -300} blur={whip * 14}>
      <Card><Room t={t} />
        <Poses t={t} keys={[[0, P(7)], [SEG.P5.words[5][0], P(12)], [E.s15, P(11)]]} x={320} bottom={720} h={560} b={talk(t, 'Peter')} />
        <Desk laptop="clean" t={t} />
        {t >= E.s15 - 0.1 && <Char src={ST('smug')} x={sx} bottom={612 - Math.abs(Math.sin(walk * Math.PI * 4)) * 14 * (walk < 1 ? 1 : 0)} h={330} flip b={talk(t, 'Stewie')} />}
      </Card>
    </Camera>
  );
};

/* T · Oh. That's actually pretty nice. */
export const Sip: React.FC<{t: number}> = ({t}) => {
  const z = 1 + 0.06 * prog(t, E.p6, 2.4) + 0.22 * easeInOut(prog(t, E.nice - 0.1, 0.5));
  return (
    <AbsoluteFill>
    <Camera s={z} ox="36% 62%">
      <Card><Room t={t} /><Char src={P(13)} x={474} bottom={820} h={640} b={talk(t, 'Peter')} rot={-1.5 * easeOut(prog(t, E.nice - 0.15, 0.4))} /></Card>
    </Camera>
    <AbsoluteFill style={{background: '#000', opacity: easeInOut(prog(t, E.total - 0.55, 0.5))}} />
    </AbsoluteFill>
  );
};

/* U · brand frame */
export const Brand: React.FC<{t: number}> = ({t}) => {
  const a = pop(t, E.s16, 0.4), b = prog(t, E.unified - 0.05, 0.35), end = E.total;
  const tag = ['One inbox.', 'Every enquiry.', 'Already understood.'];
  const black = prog(t, end - 0.12, 0.1);
  return (
    <AbsoluteFill>
      <Camera s={1 + 0.05 * prog(t, E.s16, 4.5)}>
        <Glow x={540} y={820} w={1000} h={760} o={a} />
        <div style={{position: 'absolute', top: 700, width: '100%', textAlign: 'center', transform: `scale(${0.85 + 0.15 * a})`, opacity: clamp(a)}}>
          <span style={{font: `300 132px/1 ${DISPLAY}`, color: C.paper, letterSpacing: -2}}>figured</span><span style={{font: `700 132px/1 ${DISPLAY}`, color: C.sky, letterSpacing: -2}}>out.ai</span>
        </div>
        <div style={{position: 'absolute', top: 880, width: '100%', textAlign: 'center', font: `500 38px/1 ${TEXT}`, letterSpacing: 16, color: BODY, opacity: b, transform: `translateY(${20 * (1 - b)}px)`}}>UNIFIED AI INBOX</div>
        <div style={{position: 'absolute', top: 1010, width: '100%', display: 'flex', justifyContent: 'center', gap: 22}}>
          {tag.map((s, i) => { const p = prog(t, E.s16end + 0.05 + i * 0.2, 0.3); return <span key={s} style={{font: `${i === 2 ? 700 : 600} 34px/1 ${DISPLAY}`, color: i === 2 ? C.sky : C.paper, opacity: p, transform: `translateY(${14 * (1 - p)}px)`, display: 'inline-block'}}>{s}</span>; })}
        </div>
      </Camera>
      <AbsoluteFill style={{background: '#000', opacity: black}} />
    </AbsoluteFill>
  );
};
