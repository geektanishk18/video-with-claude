#!/usr/bin/env python3
"""Build the live research graph page from the agents' real tool-call logs + their result JSON."""
import json, os, re, time
from urllib.parse import urlparse

# Portable paths: results live in ../data, the page is written next to this script.
# Optional: TASKS_DIR=<folder of agent transcript .jsonl/.output files> to draw live search/visit nodes for new agents.
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'data'); OUT = HERE; TASKS = os.environ.get('TASKS_DIR', os.path.join(HERE, '..', 'logs'))
# To add relaunched agents, set their transcript id here (or leave as-is and drop agent_<X>.json + steps_<X>.json into ../data).
AGENTS = [
    ('A', 'abd9d96dab2e3b5e9', 'AI-native unified inboxes', 'Kinso AI + AI inbox startups'),
    ('B', 'a5c435613585f82d1', 'Omnichannel CRM incumbents', 'HighLevel, Kommo, respond.io, Trengo, Zoho, HubSpot'),
    ('C', 'a85477514d13985bf', 'India WhatsApp-first', 'Interakt, Wati, AiSensy, Gallabox, LimeChat, Gupshup, Yellow.ai'),
    ('D', 'a429bdc50483958fc', 'Voice AI & AI SDRs', 'Vapi, Retell, Bland, Synthflow + AI SDRs'),
    ('E', 'a9586f73926390acb', 'Enterprise AI platforms', 'Intercom, Zendesk, Salesforce, Freshworks, Sprinklr, Meta'),
    ('F', 'aac5f294c40d5e143', 'Comment-to-DM funnel', 'ManyChat, SuperProfile, Meta rules, Cal.com/Calendly, benchmarks'),
]
STATUS_OVERRIDE = json.load(open(OUT + '/status.json')) if os.path.exists(OUT + '/status.json') else {}
URL_RE = re.compile(r'https?://[^\s\'"<>)\]]+')

def host(u):
    try: return urlparse(u).netloc.replace('www.', '')
    except Exception: return u[:40]

def steps_from_log(path):
    steps = []
    if not os.path.exists(path): return steps
    for line in open(path, errors='ignore'):
        try: d = json.loads(line)
        except Exception: continue
        if d.get('type') != 'assistant': continue
        msg = d.get('message') or {}
        content = msg.get('content') if isinstance(msg, dict) else None
        if not isinstance(content, list): continue
        for c in content:
            if not isinstance(c, dict) or c.get('type') != 'tool_use': continue
            name, inp = c.get('name'), c.get('input') or {}
            ts = d.get('timestamp', '')
            if name == 'WebSearch':
                steps.append({'t': ts, 'kind': 'search', 'label': inp.get('query', '')[:120]})
            elif name == 'WebFetch':
                u = inp.get('url', ''); steps.append({'t': ts, 'kind': 'fetch', 'label': u[:160], 'host': host(u)})
            elif name == 'Bash':
                cmd = inp.get('command', '')
                urls = URL_RE.findall(cmd)
                kind = 'browser' if ('node ' in cmd and ('.cjs' in cmd or 'playwright' in cmd)) else ('fetch' if 'curl' in cmd else 'shell')
                if kind == 'browser' and not urls:
                    # urls live inside the script file the agent wrote; pick them up from heredocs
                    urls = URL_RE.findall(cmd)
                if urls:
                    for u in urls[:6]: steps.append({'t': ts, 'kind': kind, 'label': u[:160], 'host': host(u)})
                elif kind in ('browser',):
                    steps.append({'t': ts, 'kind': 'browser', 'label': 'headless Chromium run'})
            elif name == 'Write':
                fp = inp.get('file_path', '')
                if fp.endswith('.json') and '/research/' in fp: steps.append({'t': ts, 'kind': 'write', 'label': 'wrote results ' + os.path.basename(fp)})
                else:
                    urls = URL_RE.findall(inp.get('content', '') or '')
                    for u in urls[:8]: steps.append({'t': ts, 'kind': 'browser', 'label': u[:160], 'host': host(u)})
    return steps

graph = {'nodes': [], 'links': [], 'agents': [], 'feed': [], 'built': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
N = graph['nodes']; L = graph['links']; seen = {}
def node(id_, **kw):
    if id_ in seen: return seen[id_]
    n = {'id': id_, **kw}; N.append(n); seen[id_] = n; return n
def link(a, b, kind='flow'): L.append({'s': a, 't': b, 'k': kind})

node('ORCH', type='orch', label='Orchestrator', detail='Claude (main session): planned the study, split it into 6 research agents, will synthesise the verdict, funnel and SOP.')
VD = json.load(open(OUT + '/verdict.json')) if os.path.exists(OUT + '/verdict.json') else {}
node('VERDICT', type='verdict', label=VD.get('label', 'Verdict: is the Unified AI Inbox already built?'), detail=VD.get('detail', 'Synthesis node. Filled once all agents report.'))
node('SOP', type='verdict', label='Funnel + SOP', detail='Comment "INBOX" → auto-DM → qualify → book 20-min audit. Built from agent F + competitor gaps.')
link('VERDICT', 'ORCH', 'synth'); link('SOP', 'ORCH', 'synth')
host_count = {}
for letter, aid, seg, scope in AGENTS:
    res_path = f'{RES}/agent_{letter}.json'
    done = os.path.exists(res_path)
    status = STATUS_OVERRIDE.get(letter) or ('done' if done else 'running')
    steps = steps_from_log(f'{TASKS}/{aid}.output')
    if not steps and os.path.exists(os.path.join(RES, f'steps_{letter}.json')):
        steps = json.load(open(os.path.join(RES, f'steps_{letter}.json')))  # full step log exported from the cloud session
    A = f'AG_{letter}'
    node(A, type='agent', label=f'Agent {letter} · {seg}', detail=scope, status=status, steps=len(steps))
    link('ORCH', A, 'spawn')
    res = None
    if done:
        try: res = json.load(open(res_path))
        except Exception: res = None
    counts = {'search': 0, 'fetch': 0, 'browser': 0}
    for i, s in enumerate(steps):
        if s['kind'] in ('shell', 'write'): continue
        counts[s['kind']] = counts.get(s['kind'], 0) + 1
        graph['feed'].append({'agent': letter, **s})
        if s['kind'] == 'search':
            sid = f'S_{letter}_{i}'; node(sid, type='search', label=s['label'], detail=f'Agent {letter} searched: {s["label"]}'); link(A, sid)
        else:
            h = s.get('host') or 'page'; hid = f'H_{h}'
            n = node(hid, type='site', label=h, detail='', urls=[], agents=[])
            if s['label'] not in n['urls']: n['urls'].append(s['label'])
            if letter not in n['agents']: n['agents'].append(letter); link(A, hid, s['kind'])
            n['detail'] = f'{len(n["urls"])} page(s) visited by agent(s) {", ".join(n["agents"])}'
            if 'instagram.com' in h or 'linkedin.com' in h: n['social'] = True
    graph['agents'].append({'letter': letter, 'seg': seg, 'scope': scope, 'status': status, **counts})
    if res:
        for c in res.get('competitors', []) + res.get('tools', []):
            cid = 'C_' + re.sub(r'\W+', '_', c.get('name', '?').lower())
            close = c.get('closeness') or c.get('verdict', {}).get('closeness') if isinstance(c.get('verdict'), dict) else c.get('closeness')
            node(cid, type='competitor', label=c.get('name', '?'), detail=(c.get('positioning') or c.get('india_notes') or '')[:300], close=close, agent=letter)
            link(A, cid, 'finding'); link(cid, 'VERDICT' if letter != 'F' else 'SOP', 'feeds')
            for ev in (c.get('evidence') or [])[:6]:
                h = host(ev.get('url', '')); hid = f'H_{h}'
                if hid in seen: link(cid, hid, 'evidence')
        for k, nl in enumerate(res.get('needs_login', []) or []):
            lid = f'L_{letter}_{k}'; node(lid, type='login', label='Needs login: ' + host(nl.get('url', '')), detail=f'{nl.get("url","")} | check: {nl.get("what_to_check","")}'); link(A, lid, 'login')
graph['feed'].sort(key=lambda s: s.get('t', ''))
graph['feed'] = graph['feed'][-80:]
json.dump(graph, open(OUT + '/graph.json', 'w'))
page = open(OUT + '/template.html').read().replace('/*__DATA__*/null', json.dumps(graph))
open(OUT + '/index.html', 'w').write(page)
print(f"nodes {len(N)} links {len(L)} | " + ' '.join(f"{a['letter']}:{a['status']}:{a['search']}s/{a['fetch']}f/{a['browser']}b" for a in graph['agents']))
