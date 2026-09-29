# Visual direction: Rick & Morty reels

Everything from the approved FiguredOutAI reel system still applies: brand palette, safe zones, word-pop subtitles, dialogue-first audio, show frames before code, and audio as the master timeline. This file lists what is the same and what changes for this cast.

Format: Instagram Reels, **1080 × 1920, 60 fps**.

## Story rhythm (same engine)
**Comedy → chaos → pause → insight → portal reveal → product demo → payoff → rest.**
- Morty drowns in notifications for the first 15–20 s. Rick watches, unimpressed.
- One big stillness before the insight: Rick takes a flask sip. The silence and the stare into camera are the comedic pause.
- **The reveal is a portal.** Rick fires the portal gun on the reveal line; the product UI appears through a portal. This replaces the Stewie "glasses snap on" moment.
- The demo is real browser behaviour (identical rules to the base reel).
- End on the character payoff (Morty relaxed, Rick deadpan). No brand end card unless asked.

Example beat sheet (Unified AI Inbox, Rick & Morty version):
| Beat | Line (draft) | Visual |
|---|---|---|
| Hook | MORTY: "R-Rick... we've got another lead." | Notifications land on Morty in the garage |
| Chaos | MORTY: "Aw geez, they're coming from everywhere!" | Chips flood, shake, whip |
| Jab | RICK: "You're doing this *burp* manually, Morty?" | Rick with flask, arms crossed |
| Admit | MORTY: "...Yes." | Pause, Morty sweats |
| Insight | RICK: "The problem isn't the leads, Morty. It's the work between them." | Freeze, garage darkens, one glow |
| Reveal | RICK: "Let the AI handle it." | **Portal gun → portal opens → inbox appears** |
| Demo | RICK narrates understand → qualify → score → sort → route | Browser UI, Rick PIP top-right |
| Payoff | MORTY: "So I don't have to do all that anymore?" / RICK: "That's the whole point, Morty." | Morty feet up, Rick walks off |

## Setting
- **Rick's garage lab** replaces Peter's room: cluttered workbench, pegboard with tools, a green-glowing tube or reactor, a spaceship silhouette under a tarp. Drawn in code in the `Room` style: ink/teal wall gradient, background blurred 2.5 px, diagonal light shafts.
- **Portal green `#97CE4C`** (light `#D4F58C`, dark `#2F6B1A`) is allowed **only for in-world sci-fi elements**: the portal, the reactor glow, the portal gun beam. **Never** for UI, subtitles, tracker or text. The brand palette owns everything else.

## Frame anatomy (unchanged)
Tracker y 230–345 (a tiny Rick rides the bar; before the reveal, Morty) · scene card or app window y 366–1166 · subtitles y 1250–1440 · nothing critical in Instagram's top 220 px, bottom 440 px, or right rail (x > 940, y 960–1480).

## Transitions
| Moment | Transition |
|---|---|
| Cartoon ↔ product UI (the reveal, and the return to the garage) | **Portal** (`'portal'` in the shot table): 0.7 s, portal opens at centre, the next scene grows inside the ring, outgoing scene blurs and rotates −4° |
| Between demo steps | Gaussian-blur dissolve, 0.32 s (unchanged) |
| Comedy beats (the jab, the admission, the freeze) | Hard cut |
| Chaos | Whip with 14–16 px blur (unchanged) |
Use the portal at most 2–3 times per reel so it stays special.

## Characters on screen
- Real Rick & Morty art, on-model, with idle breathing, sway and float, and word-driven talk bounce.
- Rick ≈ 1.35× Morty's height when they share a floor line.
- Rick burp beats: a 0.1 s squash on r10 plus a small `*burp*` in the subtitle band. Treat each burp as a comedic pause, never cut it.
- Morty stammers: slight shake (±3 px) on the stammered word.

## Camera, blur, subtitles, product UI
Identical to the base FiguredOutAI reel:
- **Camera:** slow push, snap, hyper zoom, whip, shake in chaos only, pull-out.
- **Blur and depth:** blurred room, blur-in windows, focus-pull subtitles.
- **Subtitles:** one sky emphasis word per chunk, Poppins 800 italic uppercase.
- **Product UI:** every change has a visible cause, and numbers land on the spoken word.

## Process rules (how this client works)
1. Script → frame storyboard → client approves frames **before** video code.
2. Voiceover → `align_vo.py` → report stray takes (Rick ad-libs are common: ask before cutting a funny one).
3. Remotion build → half-res preview → review frames at every key beat and every portal → full render.
4. Audio-only fixes are remuxed, not re-rendered.
