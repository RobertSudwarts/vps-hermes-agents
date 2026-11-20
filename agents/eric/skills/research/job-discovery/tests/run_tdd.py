"""Run real unittest output and retain each RED/GREEN transcript."""
from pathlib import Path
import subprocess
import sys
root = Path(__file__).resolve().parents[1]
phase = sys.argv[1]
test = sys.argv[2] if len(sys.argv) > 2 else 'test_discovery'
cmd = [sys.executable, '-B', '-m', 'unittest', '-v', test]
p = subprocess.run(cmd, cwd=root / 'tests', text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
text = f'\n## {phase}\n\nCommand: `{ " ".join(cmd) }`\n\n```text\n{p.stdout}```\nExit: {p.returncode}\n'
with (root / 'tests' / 'tdd-results.md').open('a', encoding='utf-8') as f:
    f.write(text)
print(text)
sys.exit(p.returncode)
