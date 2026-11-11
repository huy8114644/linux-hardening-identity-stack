#!/usr/bin/env python3
import os
import subprocess
import sys

print("=== Starting Molecule Test via Python Streaming Runner ===", flush=True)
proc = subprocess.Popen(
    ["make", "molecule"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)
lines = []
if proc.stdout:
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        lines.append(line)
proc.wait()
if proc.returncode != 0:
    sys.stderr.write(os.linesep + "=== MOLECULE FAILED. LAST 20 LINES ===" + os.linesep)
    for line in lines[-20:]:
        sys.stderr.write(line)
    err_text = "".join(lines[-25:]).replace(chr(13), "").replace(chr(10), "%0A")
    print(f"::error title=MoleculeFailure::{err_text}", flush=True)
sys.exit(proc.returncode)
