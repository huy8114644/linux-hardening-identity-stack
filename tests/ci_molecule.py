#!/usr/bin/env python3
import subprocess
import sys

print("=== Starting Molecule Test via Python Streaming Runner ===", flush=True)
proc = subprocess.Popen(
    ["make", "molecule"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)
lines = []
for line in proc.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()
    lines.append(line)
proc.wait()
if proc.returncode != 0:
    print("
=== MOLECULE FAILED. LAST 20 LINES ===", file=sys.stderr)
    for l in lines[-20:]:
        sys.stderr.write(l)
sys.exit(proc.returncode)
