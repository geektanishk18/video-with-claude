#!/usr/bin/env python3
"""Turn named word references into events.json for the Remotion scenes.

Usage: python make_events.py build/timeline.json events_spec.json --out build/events.json
events_spec.json: {"another": "P1.another", "s7": "S7.start", "score": "S9.score", "p6end": "P6.end"}
"total" is always added.
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from audio_mix import resolver
ap = argparse.ArgumentParser(); ap.add_argument('timeline'); ap.add_argument('spec'); ap.add_argument('--out', required=True); a = ap.parse_args()
T = json.load(open(a.timeline)); at = resolver(T)
E = {k: round(at(v), 3) for k, v in json.load(open(a.spec)).items()}; E['total'] = T['total']
json.dump(E, open(a.out, 'w'), indent=1); print(f'{len(E)} events -> {a.out}')
