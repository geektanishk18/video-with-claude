---
name: figuredout-reel-rick-morty
description: FiguredOutAI reel production with Rick & Morty as the cast, with built pose and look variants and a per-reel look lock that rotates character sets across reels. Use whenever making, storyboarding, animating, editing or reviewing a FiguredOutAI video or Instagram reel that features Rick and Morty (or Rick/Morty-style sci-fi comedy). Covers the locked FiguredOutAI brand system, Rick/Morty roles, required pose sheets and the pose-sheet slicer, the garage-lab setting, portal reveal and portal transitions, sci-fi sound design with a dialogue-first mix, voiceover alignment, and the Remotion template.
---

# FiguredOutAI × Rick & Morty reel skill

This is the sister skill of `figuredout-reel` (the Peter/Stewie reel). The brand, frame layout, subtitles, audio levels and workflow are the same approved system. The cast, setting, reveal device and sound palette change.

## Read first
- `references/brand.md`: locked FiguredOutAI palette, glow rule, type, wordmark, copy rules. Portal green is never a brand colour.
- `references/cast.md`: who plays which role (Morty = overwhelmed owner, Rick = the one who figured it out), the pose sheets to collect (Morty m01–m15, Rick r01–r12), staging, and voice notes.
- `references/visual-direction.md`: the story engine with the portal reveal, the garage-lab setting, the portal/blur/cut transition rules, and an example beat sheet.
- `references/audio.md`: dialogue-first mix (voice ≈ 18–21 dB over music), synth or mellow bed, sci-fi SFX, and how to handle burps and stammers.

## Workflow
0. **Cast lock.** Run `python scripts/lock_cast.py --project <reel>` to choose this reel's character set (rotates automatically; see `cast.md`). Tell the client the set and setting, and lock it before storyboarding. Every frame uses the locked looks.
   Built art: Rick (`fist`, `gun`, `flask`) and Morty (`scared`, `sweat`, `phone`, `relieved`), each in 4 looks, under `assets/characters/<char>/<look>/<pose>.png`, plus the portal at `assets/fx/portal.png`. **Never use `_src/rick.png` (middle finger).**
   New art: slice a sheet, add it to `kits/*.json`, and rebuild with `python scripts/character_kit.py kits/rick.json --out assets/characters/rick`. For sheets:
   ```
   pip install pillow scipy numpy
   python scripts/slice_pose_sheet.py morty_sheet.png --out assets/characters/morty --prefix m
   python scripts/slice_pose_sheet.py rick_sheet.png  --out assets/characters/rick  --prefix r
   ```
   Open `_contact.png` for each, and rename or reorder files to match the pose tables in `cast.md`.
1. **Script → frame storyboard.** Adapt the script to Morty's stammer and Rick's rhythm (see `examples/unified-ai-inbox-rm/script.json`). Render frame thumbnails, show them, and **wait for approval before video code.**
2. **Voiceover → master timeline:** `python scripts/align_vo.py script.json --out build`. Report unscripted words (burps, ad-libs) and let the client decide what stays.
3. **Sound:** write `cues.json` pinned to words (see the example, which uses `"bed_style": "synth"`), then run `python scripts/audio_mix.py build/timeline.json cues.json --vo build/master_vo.wav --out build/final_mix.wav`. The voice-over-music average must be ≥ 16 dB.
4. **Events:** `python scripts/make_events.py build/timeline.json events_spec.json --out build/events.json`.
5. **Video:** copy `template/`, `npm install`, and put the data JSONs in `src/data/`. Put the mix, the character folders and the fonts in `public/`, and install the fonts system-wide.
   - Reuse `lib.tsx`: `Camera`, `Char`, `Poses`, `Chip`, `Card`, `Room`, `Win`, `Cursor`, `Glow`, **`Portal`** (the drawn ring used for transitions), **`PortalSprite`** (the client's portal art, used in-world) and **`look(char, pose, t)`**, which reads `src/data/cast.lock.json` so every image follows the locked set and its one transformation.
   - Copy `cast.lock.json` into `src/data/`, and copy `assets/characters/rick`, `assets/characters/morty` and `assets/fx` into `public/`.
   - Reuse `Reel.tsx`: the shot table with the `'cut' | 'blur' | 'portal'` transitions, the `Tracker` and the `Subtitles`.
   - `cartoon.tsx` and `ui.tsx` are the Peter/Stewie reel's scenes. Keep the UI scenes as the pattern for the demo, and rebuild the cartoon scenes in the locked setting with `look('morty', …)` and `look('rick', …)`.
6. **Review:** run `npm run preview`, check frames at every key word, **every portal** and every transition, fix, then run `npm run render`. For audio-only fixes, remux instead of re-rendering.

## Non-negotiables
- 1080 × 1920 at 60 fps, and the safe zones from `visual-direction.md`.
- FiguredOutAI palette for everything except in-world sci-fi (portal, reactor, gun beam).
- Real, on-model Rick and Morty art. **One locked look set per reel** (at most one scripted transformation), and a different set each reel. Idle motion always, crossfaded pose changes, blurred background.
- The portal is the reveal. Use it at most 2–3 times per reel.
- The voice is always on top. Keep it PG: no swearing, drinking gags limited to the flask sip.
- Show frames before code; audio is the master timeline.
