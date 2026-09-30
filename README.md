# video-with-claude

FiguredOutAI animated reels, built in code with Claude Code (Remotion + Python + ffmpeg).

## Contents
| Path | What it is |
|---|---|
| `skills/figuredout-reel/` | Claude Code skill: locked FiguredOutAI brand + reel pipeline with Peter & Stewie. Copy to `~/.claude/skills/`. |
| `skills/figuredout-reel-rick-morty/` | Sister skill with Rick & Morty: pose/look variants, per-reel look lock, portal reveal, sci-fi sound. |
| `reels/unified-ai-inbox/renders/` | Rendered reels: v1 (30 fps), v2 (60 fps, funk bed), **v3 (approved: mellow bed, dialogue-first)** |
| `reels/unified-ai-inbox/video/` | Remotion project for that reel (`npm install`, then `npm run preview` / `npm run render`) |
| `reels/unified-ai-inbox/audio/` | Voiceovers, alignment (`timeline.json`, `subtitles.json`, `events.json`), sound design script, final mixes |
| `reels/unified-ai-inbox/storyboard/` | Frame-by-frame storyboard page and the 58 rendered storyboard frames |
| `reels/unified-ai-inbox/plan/` | Audio-first master-timeline plan page |
| `reels/unified-ai-inbox/assets/` | Brand fonts, Peter pose cut-outs, Stewie variants, source images |
| `character-art/rick-morty/` | Rick & Morty source cut-outs, kits and all 28 generated variants |

## Setup (new machine)
Windows: `powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1` · macOS/Linux: `bash setup/setup.sh` · verify: `python setup/check.py`.
The full dependency list and every script in order: [`setup/WORKFLOW.md`](setup/WORKFLOW.md).

## Pipeline (per reel)
1. Script → frame storyboard → approval
2. Voiceover → `align_vo.py` → master timeline + subtitles
3. `audio_mix.py` → dialogue-first mix (voice ≈ 18 dB above music)
4. Remotion build → half-res preview → review → full render (1080×1920, 60 fps)

Full details live in the skills' `SKILL.md` files.

## Notes
- Character artwork (Family Guy, Rick & Morty) belongs to its owners; the Rick base image is fan art signed "KineticSquirrel". Keep this repo private.
- `skills/figuredout-reel-rick-morty/assets/characters/_src/rick.png` contains an offensive hand gesture. Use only the generated variants.
