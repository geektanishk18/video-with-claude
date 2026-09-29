---
name: figuredout-reel
description: FiguredOutAI's locked brand system and reel production pipeline. Use whenever making, storyboarding, animating, editing or reviewing a FiguredOutAI video, Instagram reel, product explainer, or any FiguredOutAI-branded visual. Covers palette, type, glow rule, Peter/Stewie character assets and poses, reel frame anatomy and safe zones, camera and blur language, word-pop subtitles, dialogue-first audio mix, voiceover alignment, and the Remotion template.
---

# FiguredOutAI reel skill

Everything here was approved by the founder on the Unified AI Inbox reel (v3). Treat it as locked: follow it unless the user explicitly overrides a point in this conversation.

## Read first
- `references/brand.md`: palette, glow rule, type, wordmark, copy rules. **Never change the palette or type.**
- `references/visual-direction.md`: story rhythm, frame anatomy and safe zones, characters and poses, camera, blur, subtitles, product-UI behaviour, and how this client likes to work.
- `references/audio.md`: dialogue-first mix numbers (the funk bed was rejected), SFX palette, voiceover handling.

## Workflow
1. **Script → frame storyboard.** Break the script into 1–1.5 s frames: caption words, what moves, camera, sound. Render the frames as images and show them. **Wait for approval before writing video code.**
2. **Voiceover → master timeline.** Write a `script.json` (see `examples/unified-ai-inbox/script.json`), then:
   ```
   pip install faster-whisper
   python scripts/align_vo.py script.json --out build
   ```
   This outputs `timeline.json`, `subtitles.json`, `master_vo.wav` and `report.txt`. Tell the user about every unscripted take in the report before cutting it.
3. **Sound.** Write `cues.json` with every SFX pinned to a spoken word (see the example), then:
   ```
   python scripts/audio_mix.py build/timeline.json cues.json --vo build/master_vo.wav --out build/final_mix.wav
   ```
   Check the printed voice-over-music figure: average ≥ 16 dB, minimum ≥ 9 dB.
4. **Video.** Name the key moments the scenes react to in an events spec (see `examples/unified-ai-inbox/events_spec.json`) and run `python scripts/make_events.py build/timeline.json events_spec.json --out build/events.json`. Copy `template/` to a new project, then:
   - `npm install`
   - copy `timeline.json`, `subtitles.json` and `events.json` into `src/data/`
   - put `final_mix.wav`, `assets/characters/*` (as `peter/`, `stewie/`) and the fonts into `public/`
   - install the fonts system-wide

   Reusable parts are in `lib.tsx` and `Reel.tsx`:
   - `Camera`, `Char`, `Poses`, `Chip`, `Card`, `Room`, `Desk`, `Win`, `Cursor`, `Glow`
   - the easing helpers `pop` and `bump`
   - the shot table with blur transitions, the `Tracker`, and the word-pop `Subtitles`

   `cartoon.tsx` and `ui.tsx` hold this reel's scenes; reuse them as patterns and replace them for a new story.
5. **Review loop.** Run `npm run preview` (half-res), pull frames at every key word and every transition, fix collisions and safe-zone issues, then `npm run render`. Send the MP4 with a short change log. For audio-only fixes, remux instead of re-rendering:
   `ffmpeg -i reel.mp4 -i final_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest reel_fixed.mp4`

## Character sets (looks)
Before storyboarding, run `python scripts/lock_cast.py --project <reel>` to lock this reel's set from `looks.json`: `reveal-transform` (approved v3: Stewie turns geek on the AI line), `geek-throughout` or `smug-throughout`. It rotates across reels and writes `cast.lock.json`. Keep that look in every frame; allow at most one scripted transformation. New get-ups (Peter in a suit, and so on) need their own art first; see `art_needed` in `looks.json`.

## New poses
For a new pose sheet, run `python scripts/slice_pose_sheet.py sheet.png --out assets/characters/peter --prefix p` and check `_contact.png`. It handles transparent or white backgrounds, overlapping poses, and 2× upscaling.

## Non-negotiables
- 1080 × 1920 at 60 fps. Nothing critical outside the safe band (y 230–1440, x < 940 in the lower half).
- Ink ground, sky emphasis (one word per line), and the glow rule's exact three stops.
- Characters always have idle motion; pose swaps crossfade; the room background is softly out of focus.
- Every UI change has a visible cause; numbers land on the spoken word.
- The voice is always clearly on top. Mellow music only, unless the user asks for something else.
- Show frames before code; audio is the master timeline.
