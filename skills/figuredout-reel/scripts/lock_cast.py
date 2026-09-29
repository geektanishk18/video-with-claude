#!/usr/bin/env python3
"""Choose and lock the character set (looks) for one reel, rotating across reels.

Usage:
    python lock_cast.py --project path/to/reel               # auto-pick next unused set, write cast.lock.json
    python lock_cast.py --project path/to/reel --set evil-twin
    python lock_cast.py --project path/to/reel --set tech-launch --transform "rick:classic->tech@R3.ai"
    python lock_cast.py --list
A lock is final for that reel: re-running prints the existing lock unless --force is given.
History (for rotation) lives at ~/.claude/figuredout-reels/looks_history.json on this machine.
"""
import argparse, datetime, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CAT = json.load(open(os.path.join(HERE, '..', 'looks.json')))
HIST = os.path.expanduser(f"~/.claude/figuredout-reels/looks_history_{CAT.get('cast', 'default')}.json")

def load_hist():
    try: return json.load(open(HIST))
    except Exception: return []

ap = argparse.ArgumentParser(); ap.add_argument('--project'); ap.add_argument('--set'); ap.add_argument('--transform'); ap.add_argument('--force', action='store_true'); ap.add_argument('--list', action='store_true'); ap.add_argument('--window', type=int, default=3)
a = ap.parse_args(); hist = load_hist(); recent = [h['set'] for h in hist[-a.window:]]
if a.list or not a.project:
    for k, v in CAT['sets'].items(): print(f"{k:16s} " + ' '.join(f"{c}={v[c]:9s}" for c in CAT['characters'] if c in v) + f" {'(used recently)' if k in recent else ''} · {v.get('fits', '')}")
    sys.exit(0)
lock_path = os.path.join(a.project, 'cast.lock.json')
if os.path.exists(lock_path) and not a.force:
    print('Already locked (use --force to change):'); print(open(lock_path).read()); sys.exit(0)
name = a.set or next((k for k in CAT['sets'] if k not in recent), list(CAT['sets'])[0])
if name not in CAT['sets']: sys.exit(f'unknown set {name}; options: {", ".join(CAT["sets"])}')
s = CAT['sets'][name]
lock = {'set': name, 'looks': {c: s[c] for c in CAT['characters'] if c in s}, 'setting': s.get('setting'), 'fits': s.get('fits'),
        'transform': a.transform or s.get('transform'), 'locked_at': datetime.datetime.now().isoformat(timespec='seconds'), 'project': os.path.abspath(a.project)}
os.makedirs(a.project, exist_ok=True); json.dump(lock, open(lock_path, 'w'), indent=1)
os.makedirs(os.path.dirname(HIST), exist_ok=True); hist.append({'set': name, 'project': lock['project'], 'at': lock['locked_at']}); json.dump(hist, open(HIST, 'w'), indent=1)
print(json.dumps(lock, indent=1))
