import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, E, SEG, Win, Camera, Glow, Cursor, cursorAt, pop, bump, prog, easeOut, easeInOut, lerp, clamp, DISPLAY, TEXT, BODY, LABEL} from './lib';

const Row: React.FC<{y: number; k: string; v: React.ReactNode; on?: number; col?: string; hl?: boolean; right?: React.ReactNode}> = ({y, k, v, on = 1, col = C.paper, hl, right}) => (
  <div style={{position: 'absolute', left: 36, right: 36, top: y, height: 66, borderRadius: 16, display: 'flex', alignItems: 'center', padding: '0 26px', gap: 20,
    border: `3px solid ${hl ? C.sky : 'rgba(144,194,231,.12)'}`, background: hl ? 'rgba(144,194,231,.1)' : 'rgba(240,237,239,.03)', boxShadow: hl ? '0 0 30px rgba(144,194,231,.25)' : 'none'}}>
    <span style={{font: `500 23px/1 ${TEXT}`, letterSpacing: 3, color: LABEL, width: 190}}>{k}</span>
    <span style={{font: `700 32px/1 ${DISPLAY}`, color: col, opacity: on, transform: `translateX(${-30 * (1 - on)}px)`, flex: 1}}>{v}</span>
    {right}
  </div>
);
const Tick: React.FC<{s: number}> = ({s}) => (
  <div style={{width: 46, height: 46, borderRadius: 23, background: C.ok, display: 'grid', placeItems: 'center', transform: `scale(${s})`, font: `800 28px/1 ${DISPLAY}`, color: C.ink}}>✓</div>
);
export const PIP: React.FC<{src: string; t: number; at: number; x?: number; y?: number; r?: number; ih?: number; b?: number}> = ({src, t, at, x = 860, y = 480, r = 115, ih = 300, b = 0}) => {
  const s = pop(t, at, 0.35); if (s <= 0) return null;
  return <div style={{position: 'absolute', left: x - r, top: y - r, width: 2 * r, height: 2 * r, borderRadius: r, overflow: 'hidden', background: C.panel2, border: `5px solid ${C.sky}`, transform: `scale(${s})`, boxShadow: '0 16px 40px rgba(0,0,0,.5)'}}>
    <Img src={staticFile(src)} style={{position: 'absolute', height: ih, left: '50%', top: r * 0.16, transform: `translateX(-50%) scale(${1 - b / 2},${1 + b})`, transformOrigin: '50% 100%'}} />
  </div>;
};

/* J · It understands what the person actually wants */
export const Understand: React.FC<{t: number}> = ({t}) => {
  const t0 = E.s7;
  const inW = easeOut(prog(t, t0 - 0.2, 0.35));
  const bubble = pop(t, t0 + 0.05, 0.3);
  const scan = prog(t, E.understands, 0.6);
  const hl = (k: string) => t >= E[k];
  const H = (txt: string, k: string) => <span style={{background: hl(k) ? 'rgba(27,101,121,.35)' : 'transparent', color: hl(k) ? C.teal : C.ink, fontWeight: 800, borderRadius: 6, padding: '0 4px', boxShadow: hl(k) ? `inset 0 -4px 0 ${C.teal}` : 'none'}}>{txt}</span>;
  const f = (k: string) => easeOut(prog(t, E[k], 0.3));
  const zoom = 1 + 0.3 * easeInOut(prog(t, E.actually2 - 0.05, 0.25)) - 0.3 * easeInOut(prog(t, E.wants - 0.05, 0.3));
  return (
    <Camera s={zoom} ox="50% 47%">
      <Win x={90} y={390} w={900} h={700} title="inbox/priya-s" ty={200 * (1 - inW)} o={inW}>
        <div style={{position: 'absolute', left: 36, top: 24, font: `600 20px/1 ${TEXT}`, letterSpacing: 3, color: C.ok}}>● WHATSAPP · JUST NOW</div>
        <div style={{position: 'absolute', left: 36, top: 64, width: 720, padding: '24px 30px', borderRadius: '8px 30px 30px 30px', background: '#CFE3E8', font: `500 33px/1.45 ${TEXT}`, color: C.ink, transform: `scale(${bubble})`, transformOrigin: '0 0', overflow: 'hidden'}}>
          Hi, I'm looking for a {H('3BHK', 'person')} in {H('Gurgaon', 'wants')}. Budget around {H('₹30L', 'actually2')}. Looking to move in {H('2 months', 'wants')}.
          {scan > 0 && scan < 1 && <div style={{position: 'absolute', top: 0, bottom: 0, left: `${scan * 110 - 10}%`, width: 60, background: 'linear-gradient(90deg, rgba(144,194,231,0), rgba(144,194,231,.7), rgba(144,194,231,0))'}} />}
        </div>
        <div style={{position: 'absolute', left: 36, top: 292, font: `600 20px/1 ${TEXT}`, letterSpacing: 3, color: scan > 0 ? C.sky : LABEL}}>AI · UNDERSTOOD</div>
        <Row y={326} k="INTENT" v="HIGH · 3BHK" col={C.ok} on={f('person')} hl={t >= E.person && t < E.actually2} />
        <Row y={398} k="BUDGET" v="₹30L" on={f('actually2')} hl={t >= E.actually2 && t < E.wants} />
        <Row y={470} k="LOCATION" v="Gurgaon" on={f('wants')} hl={t >= E.wants} />
        <Row y={542} k="TIMELINE" v="2 months" on={easeOut(prog(t, E.wants + 0.15, 0.3))} hl={t >= E.wants + 0.15} />
      </Win>
    </Camera>
  );
};

/* K · qualifies them against your criteria */
export const Qualify: React.FC<{t: number}> = ({t}) => {
  const rows: [string, string, string][] = [['INTENT', 'HIGH', 'High'], ['NEEDS', '3BHK', '2–3 BHK'], ['LOCATION', 'Gurgaon', 'Gurgaon, Noida'], ['BUDGET', '₹30L', '≤ ₹35L'], ['TIMELINE', '2 months', '< 3 months']];
  const crit = easeOut(prog(t, E.against - 0.05, 0.35));
  const all = t >= E.criteria + 4 * 0.17 + 0.2;
  return (
    <Camera s={1 + 0.03 * prog(t, E.s8, 2)}>
      <Glow x={540} y={780} w={1000} h={800} o={all ? 0.9 : 0} />
      <Win x={90} y={390} w={900} h={700} title="inbox/priya-s/qualify">
        <div style={{position: 'absolute', left: 36, top: 26, right: 36, display: 'flex', font: `600 20px/1 ${TEXT}`, letterSpacing: 3, color: LABEL}}>
          <span style={{width: 250}}>FIELD</span><span style={{width: 220}}>EXTRACTED</span><span style={{opacity: crit, color: C.sky}}>YOUR CRITERIA</span></div>
        {rows.map(([k, v, c], i) => {
          const tk = pop(t, E.criteria + i * 0.17, 0.25);
          return <div key={k} style={{position: 'absolute', left: 36, right: 36, top: 70 + i * 100, height: 88, borderRadius: 18, display: 'flex', alignItems: 'center', padding: '0 24px',
            border: `3px solid ${tk > 0.5 ? 'rgba(79,168,124,.55)' : 'rgba(144,194,231,.12)'}`, background: tk > 0.5 ? 'rgba(79,168,124,.08)' : 'rgba(240,237,239,.03)'}}>
            <span style={{width: 226, font: `500 23px/1 ${TEXT}`, letterSpacing: 3, color: LABEL}}>{k}</span>
            <span style={{width: 220, font: `700 32px/1 ${DISPLAY}`, color: i === 0 ? C.ok : C.paper}}>{v}</span>
            <span style={{flex: 1, font: `600 28px/1 ${TEXT}`, color: C.peak, opacity: crit, transform: `translateX(${60 * (1 - crit)}px)`}}>{c}</span>
            {tk > 0 && <Tick s={tk * (1 - 0.13 * bump(t, E.criteria + i * 0.17 + 0.12, 0.2))} />}
          </div>;
        })}
        <div style={{position: 'absolute', left: 36, right: 36, top: 578, font: `700 30px/1 ${DISPLAY}`, color: C.ok, opacity: all ? 1 : 0, textAlign: 'center', letterSpacing: 2}}>QUALIFIED · 5 / 5</div>
      </Win>
    </Camera>
  );
};

/* L · match score */
const STEPS = [0, 23, 47, 68, 81, 92];
export const Score: React.FC<{t: number}> = ({t}) => {
  const p = prog(t, E.gives, E.score - E.gives + 0.1);
  const seg = p * (STEPS.length - 1), i = Math.min(STEPS.length - 2, Math.floor(seg));
  const v = Math.round(lerp(STEPS[i], STEPS[i + 1], easeOut(seg - i)));
  const val = p >= 1 ? 92 : v;
  const r = 250, L = 2 * Math.PI * r, s = pop(t, E.s9 - 0.05, 0.4);
  const land = bump(t, E.score, 0.5);
  return (
    <Camera s={1 + 0.04 * prog(t, E.s9, 3)}>
      <Glow x={540} y={820} w={900} h={900} o={0.6 + 0.4 * land} />
      <div style={{position: 'absolute', top: 440, width: '100%', textAlign: 'center', font: `600 40px/1 ${TEXT}`, letterSpacing: 12, color: C.peak}}>MATCH SCORE</div>
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, transform: `scale(${s * (1 + 0.05 * land)})`, transformOrigin: '540px 820px'}}>
        <circle cx={540} cy={820} r={r} fill="none" stroke="rgba(144,194,231,.14)" strokeWidth={30} />
        <circle cx={540} cy={820} r={r} fill="none" stroke={val >= 90 ? C.sky : C.teal} strokeWidth={30} strokeLinecap="round" strokeDasharray={`${L * val / 100} ${L}`} transform="rotate(-90 540 820)" />
        <text x={540} y={880} textAnchor="middle" fontFamily={DISPLAY} fontWeight={700} fontSize={170} fill={C.paper}>{val}%</text>
      </svg>
      <div style={{position: 'absolute', top: 1110, width: '100%', textAlign: 'center', font: `500 30px/1 ${TEXT}`, color: BODY}}>Priya S. · 3BHK · Gurgaon · ₹30L</div>
      <PIP src="peter/p12.png" t={t} at={E.score + 0.05} x={190} y={520} />
    </Camera>
  );
};

/* M + N · sort by match score, reorder, stamp */
const LEADS: Record<string, [string, string, number]> = {A: ['Anita R.', 'Website', 42], B: ['Rahul M.', 'Email', 67], C: ['Priya S.', 'WhatsApp', 91], D: ['Karan J.', 'Chat', 38], E: ['Meera K.', 'Instagram', 86]};
const CHC: Record<string, string> = {WhatsApp: C.ok, Instagram: C.loss, Website: C.sky, Email: C.amber, Chat: C.peak};
const BEFORE = ['A', 'B', 'C', 'D', 'E'], AFTER = ['C', 'E', 'B', 'A', 'D'];
export const Sort: React.FC<{t: number}> = ({t}) => {
  const ro = easeOut(prog(t, E.know, 0.55));
  const over = (p: number) => { const c1 = 1.4, c3 = c1 + 1; return p <= 0 ? 0 : 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
  const rp = over(prog(t, E.know, 0.6));
  const WX = 90, WY = 390, top = WY + 76;
  const open = t >= E.every10 && t < E.same + 0.15;
  const cur = cursorAt(t, [[E.s10, 1010, 1230], [E.treating, 850, top + 44], [E.every10 + 0.25, 850, top + 44], [E.same - 0.06, 830, top + 88 + 2 * 58 + 30], [E.same + 0.8, 900, top + 640]], [E.every10, E.same]);
  const stamp = pop(t, E.attention, 0.22);
  const inW = easeOut(prog(t, E.s10 - 0.25, 0.35));
  return (
    <Camera s={1 - 0.04 * prog(t, E.s10, 1) + 0.08 * bump(t, E.attention, 0.35)}>
      <Win x={WX} y={WY} w={900} h={700} title="inbox" o={inW} ty={120 * (1 - inW)}>
        <div style={{position: 'absolute', left: 36, top: 26, font: `700 32px/1 ${DISPLAY}`, color: C.paper}}>Inbox <span style={{font: `500 24px/1 ${TEXT}`, color: LABEL, marginLeft: 12}}>24 new</span></div>
        <div style={{position: 'absolute', right: 36, top: 14, height: 56, padding: '0 22px', borderRadius: 14, display: 'flex', alignItems: 'center', gap: 10, font: `600 24px/1 ${TEXT}`,
          color: t >= E.same ? C.ink : C.peak, background: t >= E.same ? C.sky : (t >= E.treating ? 'rgba(144,194,231,.18)' : 'rgba(240,237,239,.05)'), border: '2px solid rgba(144,194,231,.35)'}}>
          Sort{t >= E.same ? ': Match ↓' : ' ▾'}</div>
        {BEFORE.map((k) => {
          const i0 = BEFORE.indexOf(k), i1 = AFTER.indexOf(k); const y = 100 + lerp(i0, i1, rp) * 104;
          const [name, ch, sc] = LEADS[k]; const topRow = k === 'C' && t >= E.which;
          const col = sc >= 80 ? C.ok : sc >= 60 ? C.amber : C.loss;
          return <div key={k} style={{position: 'absolute', left: 36, right: 36, top: y, height: 92, borderRadius: 18, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 20,
            background: topRow ? 'rgba(144,194,231,.13)' : 'rgba(240,237,239,.035)', border: `3px solid ${topRow ? C.sky : 'rgba(144,194,231,.12)'}`, boxShadow: topRow ? '0 0 36px rgba(144,194,231,.35)' : 'none', zIndex: k === 'C' ? 2 : 1}}>
            <div style={{width: 56, height: 56, borderRadius: 28, background: C.teal, display: 'grid', placeItems: 'center', font: `700 26px/1 ${DISPLAY}`, color: C.paper}}>{name[0]}</div>
            <div style={{flex: 1}}><div style={{font: `700 30px/1.1 ${DISPLAY}`, color: C.paper}}>{name}</div><div style={{font: `500 20px/1.3 ${TEXT}`, letterSpacing: 2, color: CHC[ch]}}>● {ch.toUpperCase()}</div></div>
            <div style={{font: `700 38px/1 ${DISPLAY}`, color: col, fontVariantNumeric: 'tabular-nums'}}>{sc}%</div>
          </div>;
        })}
        {open && <div style={{position: 'absolute', right: 36, top: 80, width: 320, borderRadius: 16, background: C.panel2, border: '2px solid rgba(144,194,231,.35)', padding: 8, zIndex: 5, boxShadow: '0 20px 40px rgba(0,0,0,.5)', transform: `scaleY(${easeOut(prog(t, E.every10, 0.15))})`, transformOrigin: 'top'}}>
          {['Newest', 'Channel', 'Match score ↓'].map((o, i) => <div key={o} style={{height: 58, borderRadius: 10, display: 'flex', alignItems: 'center', padding: '0 18px', font: `600 24px/1 ${TEXT}`, color: i === 2 ? C.sky : BODY, background: i === 2 && t >= E.same - 0.15 ? 'rgba(144,194,231,.16)' : 'transparent'}}>{o}</div>)}
        </div>}
        {stamp > 0 && <div style={{position: 'absolute', right: 150, top: 72, transform: `rotate(-6deg) scale(${stamp})`, padding: '12px 22px', borderRadius: 12, background: C.sky, font: `800 26px/1 ${TEXT}`, letterSpacing: 3, color: C.ink, zIndex: 6, boxShadow: '0 10px 30px rgba(144,194,231,.5)'}}>HIGH PRIORITY</div>}
      </Win>
      {t >= E.s10 + 0.1 && t < E.know && <Cursor x={cur.x} y={cur.y} click={cur.click} />}
    </Camera>
  );
};

/* O · any industry */
const IND = ['REAL ESTATE', 'RECRUITMENT', 'HOME SERVICES', 'AGENCIES', 'EDUCATION', 'HEALTHCARE'];
export const Industries: React.FC<{t: number}> = ({t}) => {
  const pull = 1.5 - 0.5 * easeOut(prog(t, E.s12 - 0.1, 0.9));
  const idx = t < E.limited ? 0 : Math.min(5, Math.floor((t - E.limited) / 0.26));
  const orbit = easeOut(prog(t, E.industry, 0.6));
  return (
    <Camera s={pull}>
      <Glow x={540} y={760} w={900} h={760} />
      {IND.map((l, i) => {
        const a = (i / IND.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(t * 0.6) * 0.06;
        const x = 540 + Math.cos(a) * 320 * orbit, y = 740 + Math.sin(a) * 380 * orbit;
        return orbit > 0 ? <div key={l} style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${0.6 + 0.4 * orbit})`, padding: '18px 28px', borderRadius: 40, border: '3px solid rgba(144,194,231,.45)', background: C.panel, font: `600 24px/1 ${TEXT}`, letterSpacing: 3, color: C.peak, whiteSpace: 'nowrap', opacity: orbit}}>{l}</div> : null;
      })}
      <div style={{position: 'absolute', left: 540 - 260, top: 740 - 150, width: 520, height: 300, borderRadius: 34, background: C.panel, border: `4px solid ${C.sky}`, display: 'grid', placeItems: 'center', alignContent: 'center', gap: 16, boxShadow: '0 0 60px rgba(144,194,231,.3)'}}>
        {orbit < 0.5 ? <>
          <div style={{font: `600 22px/1 ${TEXT}`, letterSpacing: 5, color: LABEL}}>NEW ENQUIRY</div>
          <div key={idx} style={{font: `700 52px/1 ${DISPLAY}`, color: C.paper, transform: `translateY(${-14 * (1 - easeOut(((t - E.limited) % 0.26) / 0.12))}px)`}}>{IND[idx]}</div>
          <div style={{padding: '10px 22px', borderRadius: 30, background: C.ok, font: `700 26px/1 ${TEXT}`, color: C.ink}}>{[92, 88, 90, 85, 91, 89][idx]}% MATCH</div>
        </> : <>
          <div style={{font: `800 58px/1 ${DISPLAY}`, color: C.paper}}>AI <span style={{color: C.sky}}>INBOX</span></div>
          <div style={{font: `500 28px/1 ${TEXT}`, color: C.sky}}>any industry · your rules</div>
        </>}
      </div>
    </Camera>
  );
};

/* P · your criteria define what a good lead looks like */
export const Criteria: React.FC<{t: number}> = ({t}) => {
  const t0 = E.s13;
  const bs = t < E.define ? '≤ ₹35L' : t < E.define + 0.35 ? '≤ ₹' : '≤ ₹' + '50L'.slice(0, Math.floor((t - E.define - 0.35) / 0.11) + 1);
  const editing = t >= t0 + 0.5;
  const WX = 90, WY = 390, top = WY + 76;
  const cur = cursorAt(t, [[t0, 1000, 1200], [t0 + 0.5, 700, top + 70 + 2 * 88 + 34], [E.good + 0.6, 1000, 1230]], [t0 + 0.5]);
  const sc = t >= E.good ? Math.round(lerp(74, 92, easeOut(prog(t, E.good, 0.4)))) : 74;
  const good = sc >= 90;
  const inW = easeOut(prog(t, t0 - 0.2, 0.35));
  return (
    <Camera s={1 + 0.04 * prog(t, t0, 3)}>
      <Win x={WX} y={WY} w={900} h={700} title="settings/criteria" o={inW} ty={120 * (1 - inW)}>
        <div style={{position: 'absolute', left: 36, top: 22, font: `700 30px/1 ${DISPLAY}`, color: C.paper}}>Your criteria <span style={{font: `500 22px/1 ${TEXT}`, color: LABEL, marginLeft: 10}}>Real estate · Gurgaon team</span></div>
        {[['REQUIREMENT', '2–3 BHK'], ['LOCATION', 'Gurgaon, Noida'], ['BUDGET', bs], ['TIMELINE', '< 3 months']].map(([k, v], i) => (
          <Row key={k} y={70 + i * 88} k={k} v={<>{v}{i === 2 && editing && t < E.good && Math.floor(t * 3.8) % 2 === 0 ? <span style={{color: C.sky}}>|</span> : null}</>} col={i === 2 && editing ? C.sky : C.peak} hl={i === 2 && editing && t < E.good + 0.3} />
        ))}
        <div style={{position: 'absolute', left: 36, right: 36, top: 436, height: 170, borderRadius: 22, padding: '22px 28px', display: 'flex', alignItems: 'center', gap: 22,
          background: good ? 'rgba(79,168,124,.1)' : 'rgba(240,237,239,.035)', border: `3px solid ${good ? C.ok : 'rgba(232,163,61,.5)'}`, boxShadow: good ? `0 0 ${40 * (1 - prog(t, E.good + 0.6, 1)) + 10}px rgba(79,168,124,.4)` : 'none'}}>
          <div style={{width: 70, height: 70, borderRadius: 35, background: C.teal, display: 'grid', placeItems: 'center', font: `700 32px/1 ${DISPLAY}`, color: C.paper}}>A</div>
          <div style={{flex: 1}}><div style={{font: `700 32px/1.2 ${DISPLAY}`, color: C.paper}}>Arjun P.</div><div style={{font: `500 24px/1.4 ${TEXT}`, color: BODY}}>3BHK · Noida · budget ₹45L</div>
            <div style={{font: `600 20px/1.6 ${TEXT}`, letterSpacing: 3, color: good ? C.ok : C.amber}}>{good ? 'GOOD LEAD' : 'OUTSIDE BUDGET'}</div></div>
          <div style={{font: `700 56px/1 ${DISPLAY}`, color: good ? C.ok : C.amber, transform: `scale(${1 + 0.15 * bump(t, E.good + 0.35, 0.4)})`}}>{sc}%</div>
        </div>
      </Win>
      {t >= t0 && t < E.good + 0.6 && <Cursor x={cur.x} y={cur.y} click={cur.click} />}
    </Camera>
  );
};

/* Q · routing pipeline */
const STG = ['ENQUIRY', 'AI UNDERSTANDS', 'SCORED · 92%', 'MATCHED', 'BEST FIT'];
export const Route: React.FC<{t: number}> = ({t}) => {
  const at = [E.s14, E.understands2, E.scores, E.match14, E.best];
  const k = at.filter((a) => t >= a).length - 1;
  const CX = 580, Y0 = 400, GAP = 150;
  let ty = Y0 + 50; for (let i = 1; i < at.length; i++) ty = lerp(ty, Y0 + 50 + i * GAP, easeInOut(prog(t, at[i], 0.35)));
  const asg = pop(t, E.best + 0.25, 0.35);
  return (
    <Camera s={1 + 0.04 * prog(t, E.s14, 4)}>
      <Glow x={CX} y={ty} w={700} h={320} />
      {STG.map((s, i) => {
        const on = i <= k, cur = i === k; const y = Y0 + i * GAP;
        return <React.Fragment key={s}>
          {i < STG.length - 1 && <div style={{position: 'absolute', left: CX - 3, top: y + 100, width: 6, height: GAP - 100, background: i < k ? C.sky : 'rgba(144,194,231,.2)'}} />}
          <div style={{position: 'absolute', left: CX - 230, top: y, width: 460, height: 100, borderRadius: 26, display: 'grid', placeItems: 'center', font: `700 36px/1 ${DISPLAY}`,
            color: on ? (i === 2 ? C.sky : C.paper) : 'rgba(240,237,239,.35)', background: cur ? 'rgba(144,194,231,.16)' : C.panel, border: `${cur ? 5 : 3}px solid ${on ? C.sky : 'rgba(144,194,231,.2)'}`,
            transform: `scale(${1 + 0.08 * bump(t, at[i], 0.35)})`, boxShadow: cur ? '0 0 40px rgba(144,194,231,.35)' : 'none'}}>{s}</div>
        </React.Fragment>;
      })}
      <div style={{position: 'absolute', left: CX + 250, top: ty - 30, width: 60, height: 60, borderRadius: 30, background: C.teal, border: `4px solid ${C.sky}`, display: 'grid', placeItems: 'center', font: `700 28px/1 ${DISPLAY}`, color: C.paper}}>P</div>
      {asg > 0 && <div style={{position: 'absolute', left: CX - 240, top: Y0 + 4 * GAP + 130, width: 480, height: 96, borderRadius: 24, background: C.ok, display: 'grid', placeItems: 'center', font: `700 34px/1 ${TEXT}`, color: C.ink, transform: `scale(${asg})`}}>Assigned to Sales ✓</div>}
      <PIP src="peter/p15.png" t={t} at={E.best + 0.4} x={190} y={560} />
    </Camera>
  );
};
