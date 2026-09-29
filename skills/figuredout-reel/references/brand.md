# FiguredOutAI brand system (locked)

Source of truth: the FiguredoutAI Visual System (Drive → `HANDOFF.md`). The founders signed it off twice. Palette, type, glow logic, card treatment and spacing are frozen. Change language and structure, never the system.

## Colour
| Token | Hex | Use |
|---|---|---|
| ink | `#030A0E` | Page / video ground. Every frame starts here. |
| panel | `#08171D` | Raised surfaces: app windows, scene cards, chips |
| panel2 | `#0C2129` | Window title bars |
| teal | `#1B6579` | Structural: selected tab, highlights, headers |
| sky | `#90C2E7` | Glows, accents, focus, links, **one emphasis word per line** |
| peak | `#C9E4F5` | Specular only: labels, roles, small caps text |
| paper | `#F0EDEF` | Primary text |
| amber | `#E8A33D` | Warning, secondary metric, "?" unknowns |
| loss | `#D4645A` | Negative |
| ok | `#4FA87C` | Positive: confirmed, qualified, ticks |

Text opacity on ink: 100% headings, 72% body, 56% labels. 56% is the floor.

## The glow rule (non-negotiable)
```css
background: radial-gradient(ellipse at center,
  rgba(144,194,231,0.30) 0%, rgba(27,101,121,0.22) 40%, rgba(3,10,14,0) 70%);
filter: blur(24px);
```
Sky first, then teal, then transparent. Teal alone goes murky green-grey on ink. Blur never exceeds 24px for glows. Glows sit behind content.

## Type
- **Poppins**: display, subtitles, big numbers. 700 regular; 800 italic for emphasis words.
- **Inter**: UI text, labels (500–600, uppercase labels get 0.14–0.2em tracking).
- Font files ship in `assets/fonts/`. Install them system-wide before rendering so headless Chrome finds them by name.

## Wordmark
Live text, never an image: thin **"figured"** (Poppins 300, paper) + bold **"out.ai"** (Poppins 700, sky). Name in copy: **FiguredOutAI**.

## Surfaces
- Cards/windows: panel fill, `1–4px rgba(144,194,231,.12–.32)` border, radius 20–48, deep soft shadow.
- Buttons outlined, never filled (UI mock exceptions: a selected sort pill may fill sky).
- Dot-grid texture on the ground: 1px dots, `rgba(144,194,231,.04–.06)`, 24px pitch.

## Voice and copy
- Short declarative sentences. Specific over intense. No exclamation marks. "We", never "I".
- British/Indian spelling: **enquiry**, prioritise. Currency in **₹** (₹30L), India-first examples (Gurgaon, Noida).
- Never invent client names, logos, testimonials, prices or statistics as facts. Demo data is clearly demo data (first-name + initial leads).
- Never state or imply company age or size.
