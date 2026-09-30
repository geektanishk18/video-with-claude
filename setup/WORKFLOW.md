# Reel workflow: what to install and what runs when

## Install once
| Need | Version | Used for | Install (Windows) |
|---|---|---|---|
| Python | 3.10+ | all pipeline scripts | `winget install Python.Python.3.12` |
| faster-whisper, numpy, scipy, pillow | see `requirements.txt` | alignment, audio, character art | `pip install -r setup/requirements.txt` |
| ffmpeg + ffprobe | any recent | audio cutting/mixing, frame checks, remuxing | `winget install Gyan.FFmpeg` |
| Node.js + npm | 18+ (20 LTS recommended) | Remotion video rendering | `winget install OpenJS.NodeJS.LTS` |
| Remotion | 4.x (per project) | building/rendering the video | `npm install` inside the reel's `video/` folder |
| Git | any | saving work to this repo | `winget install Git.Git` |
| Fonts: Poppins, Inter | files in `skills/*/assets/fonts` | brand type in renders | setup script installs them |
| Claude Code skills | this repo's `skills/` | brand + pipeline knowledge for Claude | setup script copies to `~/.claude/skills` |

Downloaded automatically on first use: the Whisper `small.en` model (~480 MB, first alignment) and Remotion's headless browser (~100 MB, first render).
Optional: `yt-dlp` (download reference reels for research) → `winget install yt-dlp.yt-dlp`.

**One command:** `powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1` (or `bash setup/setup.sh` on macOS/Linux), then `python setup/check.py`.

## Scripts, in workflow order (inside each skill's `scripts/`)
| Step | Script | Input → output |
|---|---|---|
| 0. Characters (when new art arrives) | `slice_pose_sheet.py` | pose sheet → transparent, upscaled poses + `_contact.png` |
| 0. Variants (Rick & Morty) | `character_kit.py` | `kits/<char>.json` → `assets/characters/<char>/<look>/<pose>.png` |
| 0. Look lock | `lock_cast.py` | picks this reel's character set, rotating across reels → `cast.lock.json` |
| 1. Storyboard | (Claude builds frames, you approve) | script → frame board |
| 2. Voiceover | `align_vo.py` | `script.json` + VO files → `timeline.json`, `subtitles.json`, `master_vo.wav`, `report.txt` |
| 3. Sound | `audio_mix.py` | timeline + `cues.json` → `final_mix.wav` (checks voice ≥16 dB over music) |
| 4. Events | `make_events.py` | timeline + `events_spec.json` → `events.json` for the scenes |
| 5. Video | `npm run preview` / `npm run render` | Remotion project → MP4 (1080×1920, 60 fps) |
| Fix audio only | `ffmpeg -i reel.mp4 -i final_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest fixed.mp4` | swap the soundtrack without re-rendering |
