# Cast: Rick & Morty

Uses the real Rick and Morty artwork the client supplies, as-is. Keep the characters on-model. Don't redraw or restyle them, and don't mix in other shows' characters.

## Roles (same story engine as the Peter/Stewie reel)
| Role in the story | Character | Why it works |
|---|---|---|
| The overwhelmed business owner, drowning in manual work | **Morty** | Anxious, over-apologetic, stammers ("Aw geez", "W-wait"). The viewer's stand-in. |
| The one who already figured it out; presents the product | **Rick** | Genius, dismissive, deadpan; already a tech character, so he doesn't need a "geek" transformation |

Rick doesn't need a "geek" transformation; he is the tech character in any look. His reveal moment is the **portal gun**: he fires it and the product appears through a portal. (If the locked set is `tech-launch`, the VR visor is simply his look for that reel.)

## Art in this skill (built from the client's images)
Source cut-outs are in `assets/characters/_src/`. Variants are built by `scripts/character_kit.py` from `kits/rick.json` and `kits/morty.json`. Each character shares one canvas, so pose swaps never jump.

| Character | Poses | Looks | Files |
|---|---|---|---|
| Rick | `fist` (explaining), `gun` (portal gun, the reveal), `flask` (pauses, burps) | `classic`, `lab` (goggles on forehead), `tech` (VR visor), `space` (helmet) | `assets/characters/rick/<look>/<pose>.png` |
| Morty | `scared`, `sweat` (peak stress), `phone` (buzzing phone), `relieved` (smile) | `classic`, `evil` (Evil Morty eye patch), `tech`, `space` | `assets/characters/morty/<look>/<pose>.png` |

**Rick source warning:** the supplied Rick art raises a **middle finger**. Every Rick pose in the kit replaces that finger (fist, portal gun or flask). **Never use `_src/rick.png` directly.** The Rick art is fan art signed "KineticSquirrel" (bottom right, by his feet). The signature is left intact; for a public reel, prefer official art or the artist's OK.

Your portal image is at `assets/fx/portal.png` and used by `PortalSprite` in the template.

### Adding poses or looks
- New pose from a new image: cut it out (`slice_pose_sheet.py`), add it under `bases` in the kit, then add a pose entry with its ops.
- New look: add an entry under `looks` in the kit, made of overlay ops (goggles, visor, helmet, eyepatch, props, shapes), then run `python scripts/character_kit.py kits/<char>.json --out assets/characters/<char>`.
- Transformations from the series that change the body (Pickle Rick, Tiny Rick, Toxic Rick, Cronenberg) **need their own art**. They are listed under `art_needed` in `looks.json`. Never fake them with overlays.

## Character sets: one look per reel, a different set each reel
`looks.json` defines **sets** (a look for each character, plus the setting and the kind of story it fits):
`garage-classic`, `lab-day`, `tech-launch`, `space-mission`, `evil-twin`.
- At the storyboard stage, run `python scripts/lock_cast.py --project <reel>`. It picks the next set not used in the last 3 reels on this machine and writes `cast.lock.json`. Show the choice to the client; `--set <name>` overrides it.
- The lock is final for that reel. Every frame uses those looks through `look('rick', 'gun', t)` in the template.
- At most **one scripted transformation** per reel, e.g. `--transform "rick:classic->tech@ai"` (Rick puts the visor on at the AI line). It happens once, at that event, and holds to the end.
- Poses change freely inside a reel. Looks don't, apart from that one transformation.

## Pose sheets to collect (to extend the library)
Supply each character as a pose sheet (transparent or flat white background), then run
`python scripts/slice_pose_sheet.py sheet.png --out assets/characters/<name> --prefix <m|r>` and check `_contact.png`.
Aim for sheets at least 1,500 px wide so poses stay sharp after the 2× upscale.

**More Morty poses worth collecting (15 total)**
| # | Pose | Used for |
|---|---|---|
| m01 | Neutral standing, hands at sides | Calm opening |
| m02 | Looking at phone, worried | First notification |
| m03 | Hands up, panicking | "They're everywhere" |
| m04 | Hands on head, screaming | Peak chaos |
| m05 | Shrug, confused | "Really?" beats |
| m06 | Hunched at laptop, typing | Manual work |
| m07 | Nervous, hands clasped, sweating | Admitting it ("...Yes.") |
| m08 | Pointing, excited | "Wait, so...?" |
| m09 | Arms crossed, sulking | Being told off |
| m10 | Jaw-drop, eyes wide | Seeing the product |
| m11 | Relieved, smiling | Payoff |
| m12 | Relaxed, leaning back / feet up | Final rest |
| m13 | Thumbs up | Optional CTA beat |
| m14 | Running / flailing | Transition gags |
| m15 | Talking, one hand gesturing | Generic dialogue |

**More Rick poses worth collecting (12 total)**
| # | Pose | Used for |
|---|---|---|
| r01 | Neutral, half-lidded, arms at sides | Default |
| r02 | Arms crossed, unimpressed | "You're doing this manually?" |
| r03 | Drinking from flask | Comedic pauses, burps |
| r04 | Pointing the portal gun | The reveal |
| r05 | Pointing at viewer / explaining with one finger | Demo narration |
| r06 | Leaning on something, smug | Payoff lines |
| r07 | Typing on a holo-screen / tablet | Tech-presenter PIP |
| r08 | Shouting / annoyed | "Morty!" |
| r09 | Shrug, "obviously" | "That's the point" |
| r10 | Burp, eyes closed | Burp beats |
| r11 | Walking | Crossing frame |
| r12 | Talking, hands open | Generic dialogue |

**Props (separate transparent PNGs, optional):** portal gun, flask. The portal itself is drawn in code (`Portal` in `lib.tsx`).

## Placement and staging
- Morty is short. In two-shots put the scene-card floor at the same line for both and let Rick tower (Rick ≈ 1.35× Morty's height).
- Rick faces Morty in two-shots (flip horizontally if needed); both face camera in close-ups.
- During the product demo Rick appears as a talking **PIP bubble at the window's top-right** (pose r05 or r07, head-and-shoulders crop), and full-body on wide beats. Morty reacts in a PIP on the left at big moments (r/m10 jaw-drop at the score, m11 relieved at "best fit").
- Idle life on every character: breathing, sway, float (built into `Char`). Pose changes crossfade (`Poses`).

## Voice and delivery notes (for script writing)
- **Morty:** short, broken sentences, stammers on the first word ("W-we've got another lead"). Rising panic across the chaos section.
- **Rick:** long confident lines broken by a burp or a flask sip mid-sentence. Addresses Morty by name. Dismissive first, then explains the product crisply.
- Burps and stammers stay in the audio. Subtitles show the clean line; burps can appear as a small italic `*burp*` in peak colour, never as the emphasis word.
- Keep it PG: no swearing, no gore, no drunkenness jokes beyond the flask sip. It's a brand reel.
