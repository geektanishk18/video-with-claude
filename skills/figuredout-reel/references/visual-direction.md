# Visual direction for FiguredOutAI reels (locked)

Reference build: the Unified AI Inbox reel, v3 (approved). Format: Instagram Reels, **1080 × 1920, 60 fps**.

## Story rhythm
**Comedy → chaos → pause → insight → reveal → product demo → payoff → rest.**
- The first 15–20 s are deliberately messy. The viewer feels the pain before seeing the product.
- One big stillness (freeze, music out, stare into camera) right before the insight.
- The reveal is almost unnaturally clean: chaos → silence → product.
- From the reveal on, the language switches from cartoon to real browser behaviour.
- A dense shot is always followed by a lighter one.
- End on the character payoff. No brand end card unless asked (it was removed in v3).

## Frame anatomy (safe zones)
| Band | y range | Contents |
|---|---|---|
| Instagram top UI | 0–220 | nothing critical |
| Progress tracker | 230–345 | 5 stations (e.g. Understand → Qualify → Score → Match → Route), a small character rides the bar. Empty during chaos, fills during the demo |
| Scene card / app window | 366–1166 | rounded illustrated window (cartoon) or browser window (UI), x 66–1014 |
| Subtitles | 1250–1440 | centred, 1–4 words, max 2 lines |
| Instagram caption area | 1480–1920 | nothing critical |
| Right action rail | x > 940, y 960–1480 | nothing critical |

## Characters
- Use Peter and Stewie (Family Guy) artwork from `assets/characters/`. Peter: 15 poses (`p01` neutral … `p15` celebrating). Stewie: `smug`, `geek` (glasses), `geek_headset`, `geek_laptop`.
- Peter pose map: p01 neutral · p02 point/shout · p03 hands up "whoa" · p04 hands on head panic · p05 explaining · p06 at laptop stressed · p07 thinking · p08 shrug · p09 nervous hands · p10 fists angry · p11 happy pointing up · p12 excited idea · p13 relaxed with coffee · p14 happy hands clasped · p15 celebrating.
- Stewie turns tech-geek (glasses + headset flash on) the moment the AI is introduced, and stays that way through the demo: talking PIP bubble at the app window's top-right corner (x 905, y 430, r 88), full-body with laptop in wide shots.
- Peter reacts in a PIP bubble on the left during the demo's big numbers (92%, "best fit").
- Every character always has **idle life**: breathing (±1.1% scaleY, 2.8 s), sway (±0.8°, 3.7 s), float (±3.5 px). Each has its own phase.
- Talking = squash-bounce on each word onset (≈3.5%, 0.2 s), driven by the aligned word timings.
- Pose changes **crossfade over ~0.14 s with a tiny squash**, never hard swaps.
- Stewie faces Peter in two-shots (flip horizontally); faces camera in close-ups.

## Camera vocabulary
- **SLOW PUSH** 1.00 → 1.06 across a shot (default for talking beats).
- **SNAP** +12–14% bump on a hit word, smooth rise (smoothstep) and cosine fall ≈0.35 s.
- **HYPER ZOOM** into a detail (a field, a mug) ≈0.25–0.5 s ease-in-out.
- **WHIP** 0.25–0.3 s horizontal slide with 14–16 px blur, for the chaos section and the return to the cartoon world.
- **SHAKE** ±6–14 px decaying over 0.4 s, chaos only.
- **PULL-OUT** 1.5 → 1.0 to reveal breadth.

## Blur and depth
- Scene changes: **gaussian-blur dissolve** 0.32 s (outgoing blurs to 18 px and scales up 5%, incoming does the reverse). Keep **hard cuts** for comedy beats (the jab, the freeze) and whips.
- The illustrated room behind characters is always slightly out of focus (2.5 px). Background notification chips blur 3 px.
- Windows and chips blur in as they appear. Subtitle words focus-pull in (9 px → 0) as they pop.

## Subtitles
- Word-pop kinetic: each word springs in on its own spoken onset (easeOutBack, soft overshoot).
- Normal words: Poppins 700, 72 px, paper, sentence case. **Emphasis words:** Poppins 800 italic, uppercase, sky, soft glow. About one per chunk.
- Insight lines (the calm beat) fade in as whole sentences instead of popping.
- Chunks follow meaning, not word count ("the *same*...", not "every enquiry the / same").

## Product UI
- Looks like a real SaaS app: `app.figuredout.ai/...` URL bar, traffic lights, panel fill, real-looking rows.
- **Every UI change has a visible cause**: a cursor click, a spoken word, or the previous step's output.
- Cursor: gentle arcs, ease-in-out, hover state before click, click ring.
- Numbers count in steps (0 → 23 → 47 → 68 → 81 → 92) and land exactly on the spoken word, then hold ≥0.6 s.
- Lists physically reorder with a spring. Stamps rotate slightly (−6°).

## Process rules (how this client works)
1. Script → frame storyboard → client approves frames **before** any video code.
2. Voiceover arrives → **audio is the master timeline**: align it, report stray/unscripted takes, build the pause map. Don't estimate from text.
3. Build in Remotion, render a half-res preview, review frames at every key beat and every transition, fix, then render full-res.
4. Send the MP4 with a short change log. Audio-only changes are remuxed, not re-rendered.
