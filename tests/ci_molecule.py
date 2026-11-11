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
    sys.stderr.write(os.linesep + "=== MOLECULE FAILED. SEARCHING FOR ERRORS ===" + os.linesep)
    fatal_lines = []
    for i, line in enumerate(lines):
        if "fatal:" in line.lower() or "failed:" in line.lower() or "error" in line.lower():
            start = max(0, i - 2)
            end = min(len(lines), i + 8)
            fatal_lines.extend(lines[start:end])
    if not fatal_lines:
        fatal_lines = lines[-30:]
    err_text = "".join(fatal_lines[:30]).replace(chr(13), "").replace(chr(10), "%0A")
    print(f"::error title=MoleculeFailure::{err_text}", flush=True)
sys.exit(proc.returncode)
