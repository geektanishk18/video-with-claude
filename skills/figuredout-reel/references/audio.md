# Audio direction (locked after v3)

**Dialogue first.** The client rejected an upbeat funk bed in v2 as "very loud, dialogues aren't clear". Approved v3 settings:

- Music: calm, mellow bed. 86 BPM electric piano (Cmaj7 → Am7 → Fmaj7 → G7), soft sub bass, soft kick, rim click, brushed hat. Top end low-passed around 3.5 kHz. **Not upbeat, not funk.**
- Levels: voice ≈ **18 dB above music on average**, never less than ~9–10 dB. Music gain 0.24, SFX 0.22 (in `audio_mix.py`).
- Ducking: music drops 65% under speech, 150 ms smoothing.
- Loudness: −15 LUFS integrated, true peak −1.2 dBTP.
- Music drops out entirely for the comedic stillness (room tone only, never digital silence), and returns on the reveal word with a sub drop.
- Ends on one soft chord after the last line; no hard stop.

SFX palette (all synthesised, no downloaded audio): ding (rising pitch for notification floods), pop, click, key, whoosh, whooshdown, riser, drop, confirm chord, stamp, slide, tick, scribble, tap, thud, step, sip. Pin every cue to a spoken word (`"S9.score"`), not to a guessed time.

Voiceover handling:
- Keep the actor's recorded pauses inside a character's file (`"gap": "recorded"`).
- Choose gaps where the two characters' files meet: 0.35–0.45 s turn-taking, 0.8–0.9 s comedic beats, +0.9 s reveal hold.
- Keep genuine stumbles if they're funny (subtitle shows the clean line).
- Unscripted takes get reported and are cut unless the client keeps them (v3 kept Peter's "Really?", cut Stewie's "Introducing the broader capability.").
