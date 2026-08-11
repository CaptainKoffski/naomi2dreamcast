#!/bin/sh
# Headless Ghidra guts scan. Usage: run_guts.sh <boot.bin> <base-hex> <out.json>
# Import invocation cribbed from ../cleopatra/scripts/ghidra/run.sh (Ghidra 12.1.2).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
GHIDRA_HOME="${GHIDRA_HOME:-$REPO/../cleopatra/tools/ghidra_12.1.2_PUBLIC}"
PROJ="${ASSESS_GHIDRA_PROJ:-$REPO/tools/assess/out/ghidra-proj}"
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"   # Ghidra needs Java 21+
BOOT="$1"; BASE="$2"; OUT="$3"
[ -x "$GHIDRA_HOME/support/analyzeHeadless" ] || { echo "ERROR: no analyzeHeadless in $GHIDRA_HOME" >&2; exit 1; }
mkdir -p "$PROJ"
# Battery runs are serialized, so a leftover lock is always stale (killed run).
rm -f "$PROJ/assess.lock" "$PROJ/assess.lock~"
# One shot: import + full SH4 auto-analysis + post-script.
# GUTS_TIMEOUT caps the whole analysis (rhytngk's 4.2 MB boot ran Ghidra >2 h
# CPU without finishing, 2026-08-11); macOS has no timeout(1), so wrap in
# python with a process-group kill. On timeout the battery takes the
# guts-unavailable path (kb §4.w).
GUTS_TIMEOUT="${GUTS_TIMEOUT:-600}"
python3 -c '
import os, signal, subprocess, sys
t, cmd = int(sys.argv[1]), sys.argv[2:]
p = subprocess.Popen(cmd, start_new_session=True)
try:
    sys.exit(p.wait(t))
except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL)
    sys.stderr.write("ERROR: guts analysis timed out after %ss\n" % t)
    sys.exit(124)
' "$GUTS_TIMEOUT" \
  "$GHIDRA_HOME/support/analyzeHeadless" "$PROJ" assess \
  -import "$BOOT" -overwrite \
  -processor "SuperH4:LE:32:default" \
  -loader BinaryLoader -loader-baseAddr "$BASE" \
  -scriptPath "$HERE" -postScript GutsMetrics.java "$OUT"
[ -s "$OUT" ] || { echo "ERROR: post-script produced no output" >&2; exit 1; }
echo "OK $OUT"
