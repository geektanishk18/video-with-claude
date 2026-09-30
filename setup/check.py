#!/usr/bin/env python3
"""Check that every tool the FiguredOutAI reel workflow needs is installed.  Run:  python setup/check.py"""
import importlib, os, shutil, subprocess, sys, glob

ok = True
def row(name, good, detail, fix=''):
    global ok; ok &= good
    print(f"{'OK ' if good else 'MISSING'}  {name:26s} {detail}" + (f"\n         -> {fix}" if not good and fix else ''))

def ver(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip().splitlines()[0]
    except Exception: return ''

print('\nFiguredOutAI reel workflow: dependency check\n')
row('Python 3.10+', sys.version_info >= (3, 10), sys.version.split()[0], 'install Python 3.11+ from python.org (tick "Add to PATH")')
for mod, pkg in [('faster_whisper', 'faster-whisper'), ('numpy', 'numpy'), ('scipy', 'scipy'), ('PIL', 'pillow')]:
    try: m = importlib.import_module(mod); row(f'python: {pkg}', True, getattr(m, '__version__', 'installed'))
    except Exception: row(f'python: {pkg}', False, 'not importable', 'pip install -r setup/requirements.txt')
for tool, fix in [('ffmpeg', 'winget install Gyan.FFmpeg   (macOS: brew install ffmpeg)'), ('ffprobe', 'comes with ffmpeg'),
                  ('node', 'winget install OpenJS.NodeJS.LTS   (macOS: brew install node)'), ('npm', 'comes with Node.js'), ('git', 'winget install Git.Git')]:
    p = shutil.which(tool); row(tool, bool(p), ver([tool, '-version' if tool.startswith('ff') else '--version']) if p else 'not on PATH', fix)
nv = ver(['node', '--version']).lstrip('v')
if nv: row('Node 18+', int(nv.split('.')[0]) >= 18, nv, 'install Node.js 20 LTS or newer')
fonts = ''
try: fonts = subprocess.run(['fc-list'], capture_output=True, text=True).stdout
except Exception:
    for d in [os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'), r'C:\Windows\Fonts', os.path.expanduser('~/Library/Fonts')]:
        fonts += ' '.join(glob.glob(os.path.join(d, '*')))
row('fonts: Poppins', 'Poppins' in fonts, 'installed' if 'Poppins' in fonts else 'not found', 'run the setup script (installs from skills/*/assets/fonts)')
row('fonts: Inter', 'Inter' in fonts, 'installed' if 'Inter' in fonts else 'not found', 'run the setup script')
sk = os.path.expanduser('~/.claude/skills')
for s in ['figuredout-reel', 'figuredout-reel-rick-morty']:
    here = os.path.exists(os.path.join(sk, s, 'SKILL.md'))
    row(f'skill: {s}', here, os.path.join(sk, s) if here else 'not in ~/.claude/skills', 'run the setup script (copies skills/ into ~/.claude/skills)')
nm = os.path.join(os.path.dirname(__file__), '..', 'reels', 'unified-ai-inbox', 'video', 'node_modules', 'remotion')
row('remotion (example reel)', os.path.exists(nm), 'installed' if os.path.exists(nm) else 'not installed', 'cd reels/unified-ai-inbox/video && npm install')
print('\n' + ('All set: the whole workflow can run on this machine.' if ok else 'Fix the MISSING items above, then run this check again.') + '\n')
sys.exit(0 if ok else 1)
