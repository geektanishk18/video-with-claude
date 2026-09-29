import json, html
T = json.load(open('timeline.json')); SUB = json.load(open('subtitles.json'))
SEG = {s['id']: s for s in T['segments']}
e = html.escape
def ts(t): return f"{int(t//60):02d}:{t%60:06.3f}"

# ---------- per-segment direction ----------
DIR = {
 'P1': dict(delivery='Casual, slightly weary. Stresses "got" (+5 dB).', intent='Set up the everyday problem', vis='Peter at his desk, calm, coffee in hand. On "another" five notification chips burst in 3 frames apart. On "lead." hyper zoom into his phone.', chars='Peter idle breathing, 2% bob. Glance toward phone on "another".', cam='SLOW PUSH 1.00→1.06, SNAP on "another", HYPER on "lead."', ui='—', sfx='ding at 0.00; ding ×5 rising pitch from "another"', music='Pulse bed fades in at 0.5 s, low', dens='M → H', trans='Cut in from the black DING frame'),
 'P2': dict(delivery='Quick realisation, faster second half. Peak on "everywhere".', intent='Escalate: it is not one lead, it is all channels', vis='On "Actually," tabs whip past (WhatsApp, inbox, form). On "coming from" six channel labels pop in a ring. On "everywhere." every chip lands at once.', chars='Peter swaps to panic pose, sweat drop, phone in hand', cam='WHIP on "Actually,", SHAKE ±6 px on "everywhere."', ui='Tab stack whip', sfx='tab click ×3, pop ×6, ding cluster', music='Bed continues', dens='H', trans='Whip'),
 'S1': dict(delivery='Dry, even, slightly clipped. Lands on "them manually".', intent='Stewie questions the method', vis='Stewie is suddenly there, frame right, arms folded. Chips keep drifting slowly behind Peter.', chars='Stewie still; slow blink at "all of them"', cam='WHIP-PAN from Peter to Stewie on "And", PUSH on "manually"', ui='—', sfx='chips muffle (low-pass) while he talks', music='Bed ducks −6 dB', dens='M', trans='Whip pan'),
 'P3': dict(delivery='Defensive. "Well," then accents on "qualify".', intent='Peter justifies the manual work', vis='The comically tall manual checklist unrolls. Cursor clicks Budget, types one letter at a time. A new chip slams over the form on "first."', chars='Peter off-screen (UI shot)', cam='HYPER into form on "Well,", SNAP on the new chip', ui='Manual form: Name ticked, six empty "?" fields; cursor to Budget; typing', sfx='paper unroll, key clicks ×6, ding', music='Bed', dens='H', trans='Hard cut'),
 'S2': dict(delivery='Deadpan, falling. Quiet on "one?"', intent='The jab', vis='Cut to Stewie close. Nothing moves.', chars='Stewie locked', cam='Locked', ui='—', sfx='none', music='Bed ducks −10 dB', dens='L', trans='Hard cut'),
 'P4': dict(delivery='Defeated, soft, slow (1.85 words/s)', intent='Admission', vis='Two-shot. Peter has slowly turned to Stewie during the 0.80 s pause, then "...Yes."', chars='Peter head turn over 0.8 s, slumps 3% on "Yes"', cam='Slow PUSH on Peter', ui='—', sfx='none', music='Bed out on "Yes."', dens='L', trans='Hard cut'),
 'S3': dict(delivery='Understated, fast (3.5 words/s), quieter than average', intent='Diagnosis, the turn of the video', vis='Freeze. Chips drain to grey and fall. Background clears to ink. This is the visual rest.', chars='Stewie stares into camera through the 0.90 s silence before the line', cam='Locked', ui='—', sfx='all sound cut, room tone', music='Silence', dens='L', trans='Freeze frame'),
 'S4': dict(delivery='Measured. Leans on "problem isn\'t" (+2 dB)', intent='Reframe', vis='Stewie steps forward into one soft glow. Line fades in as a sentence, not word-pop.', chars='Stewie steps 40 px forward', cam='PUSH 1.00→1.06', ui='—', sfx='room tone', music='Silence', dens='L', trans='Fade'),
 'S5': dict(delivery='Weight on "work" (+3 dB)', intent='The insight', vis='Grey lead dots appear with tangled hand-drawn lines between them: the "work between them".', chars='Stewie still', cam='Locked', ui='Tangle of lines between dots', sfx='pencil scribble', music='Silence', dens='L → M', trans='Line swap'),
 'S6': dict(delivery='Fastest line (4.8 words/s), punchy. "Let" and "AI" +5 dB, "it." drops away', intent='The command', vis='Stewie points and taps; ripple. On "handle it." light-leak flash.', chars='Stewie tap gesture', cam='SNAP on "AI"', ui='—', sfx='tap, then DROP on "handle"', music='Silence until the drop', dens='M', trans='Light-leak flash'),
 'S7': dict(delivery='Explanatory, lifts on "understands"', intent='Mechanism 1: understand', vis='Browser slides up. A new enquiry types in. On "understands" phrases highlight. On "person actually wants" they lift into Intent, Location, Budget, Timeline.', chars='—', cam='WHIP in, then PUSH; HYPER on ₹30L', ui='Conversation view, extraction', sfx='type ticks, whoosh per field', music='Bed back at full after the drop', dens='H', trans='Whip into browser'),
 'S8': dict(delivery='Continuous with S7, even', intent='Mechanism 2: qualify', vis='Fields slide into a Qualification panel. On "criteria" a criteria column appears and five ticks land.', chars='—', cam='micro SNAP per tick', ui='Qualification panel', sfx='tick ×5 rising', music='Bed', dens='H', trans='Slide'),
 'S9': dict(delivery='Even, "score." falls away', intent='Mechanism 3: score', vis='Everything collapses into the ring. Counter runs 0→23→47→68→81→92 across the line and lands exactly on "score."', chars='—', cam='HYPER in, then locked', ui='Match score ring', sfx='counter ticks, confirm chord on 92', music='Bed', dens='M', trans='Collapse'),
 'S10': dict(delivery='Conversational, builds to "same"', intent='Contrast', vis='Five leads, unsorted. Cursor travels to Sort, clicks, dropdown opens, selects "Match score ↓" on "same".', chars='—', cam='PULL back to show list', ui='Inbox list + sort dropdown', sfx='hover tick, click, dropdown open', music='Bed', dens='M', trans='Cut'),
 'S11': dict(delivery='Warm, "know" +3 dB, soft landing', intent='Payoff of sorting', vis='Rows physically reorder on "you know". Top row glows. HIGH PRIORITY stamps on "attention."', chars='—', cam='SNAP on stamp', ui='Sorted list + badge', sfx='card slide ×5, stamp', music='Bed', dens='M', trans='—'),
 'S12': dict(delivery='Bright opening "And" (+4 dB)', intent='Breadth', vis='Pull out. The lead card morphs through six industries, about every 0.33 s. On "industry." the labels settle in an orbit around the inbox.', chars='—', cam='PULL 2.0→1.0, slow rotate 4°', ui='Industry morph', sfx='whoosh per morph', music='Bed', dens='H', trans='Pull-out'),
 'S13': dict(delivery='"Your" stressed (+5 dB), "like." trails off', intent='You control it', vis='Criteria editor. Cursor edits a rule; the good-lead card updates live.', chars='—', cam='PUSH', ui='Criteria editor, live edit', sfx='type ticks', music='Bed', dens='M', trans='Cut'),
 'S14': dict(delivery='Three beats with natural 0.2 s and 0.3 s breaths', intent='Whole flow in one sentence', vis='Pipeline: Enquiry → AI (on "understands") → 92% (on "scores it") → Match (on "match") → Best fit, Assigned to Sales (on "best fit."). Tracker completes.', chars='—', cam='Track down the pipeline', ui='Pipeline + assignment card', sfx='pulse per stage, confirm', music='Bed peaks', dens='M', trans='—'),
 'P5': dict(delivery='Fastest Peter line (3.9 words/s), hopeful disbelief, "all" +5 dB', intent='Relief', vis='Back in the room. Clean desk, silent phone, calm laptop.', chars='Peter relaxed, leans back', cam='Wide, slow PUSH', ui='—', sfx='room tone', music='Bed softens', dens='L', trans='Whip back to cartoon'),
 'S15': dict(delivery='Flat, deadpan, "point." drops -8 dB', intent='Button', vis='Stewie walks past Peter without looking.', chars='Stewie slides across frame', cam='Locked', ui='—', sfx='footsteps ×3', music='Bed', dens='L', trans='—'),
 'P6': dict(delivery='"Oh." then a genuine stumble "that\'s... that\'s" before "actually pretty nice"', intent='Warm comedic landing', vis='Peter considers it, then sips his coffee.', chars='Peter mug rises on "nice."', cam='HYPER to mug on "nice."', ui='—', sfx='sip', music='Bed resolves', dens='L', trans='—'),
 'S16': dict(delivery='Slowest line (1.8 words/s), announcer read', intent='Brand', vis='Wordmark lands on "FiguredOutAI." "UNIFIED AI INBOX" lands on "Unified AI Inbox." Tagline "One inbox. Every enquiry. Already understood." fades in during the 1.3 s tail. Cut to black on the final frame.', chars='—', cam='Slow PUSH, hard cut', ui='—', sfx='final chord, click to black', music='Ends on the cut', dens='L', trans='Fade to brand'),
}
UI = [
 ('P3', 'Manual form', [('"Well,"', 'Form unrolls from top, 10 frames, ease-out'), ('"I have to"', 'Cursor glides from bottom-right to Budget field, 14 frames, ease-in-out with a slight arc'), ('"qualify"', 'Click: field outline goes sky; caret blinks'), ('"them first."', 'Typing "₹2" then stops; new Instagram chip slams over the top of the form')]),
 ('S7', 'Conversation view', [('0.0 s', 'Browser slides up 120 px + fades in, 12 frames'), ('"It"', 'Enquiry types in at 40 chars/s: "Hi, I\'m looking for a 3BHK in Gurgaon. Budget around ₹30L. Moving in 2 months."'), ('"understands"', 'Four key phrases underline in teal, 4 frames apart'), ('"the person"', 'Phrase "3BHK" lifts and flies to Intent: HIGH'), ('"actually"', '"₹30L" flies to Budget (hyper zoom on this one)'), ('"wants"', 'Gurgaon and 2 months fly to Location and Timeline')]),
 ('S8', 'Qualification panel', [('"qualifies them"', 'The four fields slide right into a Qualification panel; Requirement row joins'), ('"against your"', 'A second column "Your criteria" slides in: 3BHK · Gurgaon · ≤ ₹35L · < 3 months'), ('"criteria"', 'Ticks land row by row, 5 frames apart, each pops 1.15× then settles')]),
 ('S9', 'Match score', [('"and gives"', 'Panel collapses into a ring at centre'), ('"every enquiry"', 'Counter 0 → 23 → 47'), ('"a match"', 'Counter → 68 → 81'), ('"score."', 'Lands on 92 exactly on the word; ring completes; holds through the 0.68 s pause')]),
 ('S10', 'Inbox list + sort', [('"So instead of"', 'List of five leads appears unsorted: 42, 67, 91, 38, 86'), ('"treating"', 'Cursor moves to "Sort" button top-right, hover state'), ('"every enquiry"', 'Click: dropdown opens with Newest, Channel, Match score ↓'), ('"the same"', 'Cursor hovers and clicks "Match score ↓"')]),
 ('S11', 'Reorder', [('"you know"', 'Rows animate to new order with spring (stiffness 180, damping 18): 91, 86, 67, 42, 38'), ('"which ones"', 'Top row glows sky'), ('"attention."', 'HIGH PRIORITY badge stamps on at −6°')]),
 ('S12', 'Industry morph', [('"And it isn\'t"', 'Camera pulls out; one lead card in centre'), ('"limited to"', 'Card title morphs: Real estate → Recruitment → Home services → Agencies'), ('"one industry."', 'Education → Healthcare; then six labels fly out into an orbit')]),
 ('S13', 'Criteria editor', [('"Your criteria"', 'Criteria editor slides in; cursor clicks the Budget rule'), ('"define what"', 'Rule edits live: "≤ ₹35L" → "≤ ₹50L"'), ('"a good lead"', 'A lead card below re-scores from 74% → 92% and turns green'), ('"looks like."', 'Hold')]),
 ('S14', 'Routing pipeline', [('"It understands"', 'Enquiry → AI stage lights'), ('"scores it,"', '92% stage lights'), ('"and helps match it"', 'Match stage lights, cursor-free (automatic)'), ('"best fit."', 'Assigned to Sales card slides in with a check')]),
]

# ---------- pause map ----------
def gap_type(why):
    w = why.lower()
    if 'comedic' in w: return ('Comedic', '#E8A33D')
    if 'reveal' in w: return ('Reveal hold', '#90C2E7')
    if 'recorded' in w: return ('Recorded', '#4FA87C')
    if 'lead-in' in w or 'brand' in w or 'scene' in w: return ('Structural', '#C9E4F5')
    return ('Turn-taking', 'rgba(240,237,239,.56)')

rows_tl = ''.join(f"<tr><td class='m'>{s['id']}</td><td>{s['char']}</td><td>{e(s['text'])}</td><td class='m r'>{s['start']:.3f}</td><td class='m r'>{s['end']:.3f}</td><td class='m r'>{s['dur']:.2f}</td><td class='m r'>{s['gap_after']:.2f}</td><td class='m r'>{s['wps']}</td><td>{e(DIR[s['id']]['delivery'])}</td></tr>" for s in T['segments'])

chron = [f"<li><span class='m'>00:00.000–00:00.500</span> <em>silence · DING on black</em></li>"]
for i, s in enumerate(T['segments']):
    chron.append(f"<li class='{s['char'].lower()}'><span class='m'>{ts(s['start'])}–{ts(s['end'])}</span> <b>{s['char']}</b> “{e(s['text'])}”</li>")
    nxt = T['segments'][i+1]['start'] if i+1 < len(T['segments']) else T['total']
    gt = gap_type(T['segments'][i+1]['gap_why'] if i+1 < len(T['segments']) else 'structural')
    chron.append(f"<li class='gap'><span class='m'>{ts(s['end'])}–{ts(nxt)}</span> <em>silence {nxt-s['end']:.2f} s · {gt[0].lower()}</em></li>")

pause_rows = ''
for i, s in enumerate(T['segments']):
    gt = gap_type(s['gap_why'])
    prev = T['segments'][i-1]['id'] if i else 'start'
    pause_rows += f"<tr><td class='m'>{prev} → {s['id']}</td><td class='m r'>{s['gap_before']:.2f} s</td><td><span class='pill' style='color:{gt[1]};border-color:{gt[1]}'>{gt[0]}</span></td><td>{e(s['gap_why'])}</td></tr>"

sub_rows = ''.join(f"<tr><td class='m'>{c['seg']}</td><td class='m r'>{c['start']:.2f}</td><td class='m r'>{c['out']:.2f}</td><td class='cap'>{''.join(('<i>'+e(w)+'</i> ' if any(w.strip('.,?!…').lower()==x.lower() or w.strip('.,?!…').lower() in x.lower().split() for x in c['em']) else e(w)+' ') for w in c['text'].split())}</td></tr>" for c in SUB)

story = ''
for s in T['segments']:
    d = DIR[s['id']]
    story += f"""<article class='sb' id='sb-{s['id']}'><header><span class='m sky'>{ts(s['start'])}–{ts(s['end'])}</span><h3>{s['id']} · {s['char']}</h3><span class='pill'>density {d['dens']}</span></header>
<p class='quote'>“{e(s['text'])}”</p>
<dl>
<dt>Intent</dt><dd>{e(d['intent'])}</dd><dt>Visual</dt><dd>{e(d['vis'])}</dd><dt>Character</dt><dd>{e(d['chars'])}</dd><dt>Camera</dt><dd>{e(d['cam'])}</dd><dt>UI state</dt><dd>{e(d['ui'])}</dd><dt>Transition</dt><dd>{e(d['trans'])}</dd><dt>Sound</dt><dd>{e(d['sfx'])}</dd><dt>Music</dt><dd>{e(d['music'])}</dd>
</dl></article>"""

ui_html = ''
for sid, name, steps in UI:
    s = SEG[sid]
    ui_html += f"<div class='card'><span class='eyebrow'>{sid} · {ts(s['start'])}</span><h3>{e(name)}</h3><ol class='steps'>" + ''.join(f"<li><span class='m peak'>{e(a)}</span><span>{e(b)}</span></li>" for a, b in steps) + "</ol></div>"

# timeline bar
bar = ''
for s in T['segments']:
    l = s['start']/T['total']*100; w = s['dur']/T['total']*100
    bar += f"<a href='#sb-{s['id']}' class='seg {s['char'].lower()}' style='left:{l:.3f}%;width:{w:.3f}%' title='{s['id']} {e(s['text'])}'><span>{s['id']}</span></a>"

frames_total = round(T['total']*30)
DATA = json.dumps(dict(seg=[dict(id=s['id'],c=s['char'],a=s['start'],b=s['end'],t=s['text']) for s in T['segments']], sub=[dict(a=c['start'],b=c['out'],t=c['text'],em=c['em']) for c in SUB], total=T['total']))

page = open('template.html').read()
for k, v in dict(ROWS_TL=rows_tl, CHRON=''.join(chron), PAUSES=pause_rows, SUBS=sub_rows, STORY=story, UI=ui_html, BAR=bar, TOTAL=f"{T['total']:.2f}", FRAMES=str(frames_total), NSUB=str(len(SUB)), DATA=DATA).items():
    page = page.replace('{{'+k+'}}', v)
open('index.html', 'w').write(page)
print('ok', len(page))
