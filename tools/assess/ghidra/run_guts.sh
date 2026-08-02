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
# One shot: import + full SH4 auto-analysis + post-script.
"$GHIDRA_HOME/support/analyzeHeadless" "$PROJ" assess \
  -import "$BOOT" -overwrite \
  -processor "SuperH4:LE:32:default" \
  -loader BinaryLoader -loader-baseAddr "$BASE" \
  -scriptPath "$HERE" -postScript GutsMetrics.java "$OUT"
[ -s "$OUT" ] || { echo "ERROR: post-script produced no output" >&2; exit 1; }
echo "OK $OUT"
