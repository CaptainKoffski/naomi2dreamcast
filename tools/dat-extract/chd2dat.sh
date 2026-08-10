#!/usr/bin/env bash
# chd2dat.sh <set> [outdir]
# Produce a decrypted flat Naomi .dat (Flycast/Ghidra input) from a GD-ROM set
# in ../../naomi/. Self-contained: uses the set's own .chd + PIC, no external romset.
# Method proven byte-exact vs the known-good Cleopatra .dat (SHA1 08c2666b...).
#
# GD-ROM sets only. Cart sets use a different decrypt path (not handled here yet).
# netpic!=0 games (e.g. some dragntr) not handled yet — extract_dat reports and skips.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
LIB="$(cd "$HERE/../../naomi" && pwd)"
SET="${1:?usage: chd2dat.sh <set> [outdir]}"
OUT="${2:-$HERE/out}"; mkdir -p "$OUT"
EXTRACT="$HERE/extract_dat"
[ -x "$EXTRACT" ] && [ "$EXTRACT" -nt "$HERE/extract_dat.cpp" ] || clang++ -O2 -std=c++17 -w "$HERE/extract_dat.cpp" -o "$EXTRACT"

# locate the disc chd (in the set's folder, or a parent's for merged clones)
CHD="$(find "$LIB/$SET" -name '*.chd' 2>/dev/null | head -1 || true)"
[ -n "$CHD" ] || { echo "no .chd for set '$SET' (cart set, or clone whose disc lives in the parent folder)"; exit 1; }

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
# PICs: from the set zip, else the naomigd BIOS zip
ZIP="$LIB/$SET.zip"; [ -f "$ZIP" ] || ZIP="$(find "$LIB" -maxdepth 1 -name '*.zip' | head -1)"
7zz e -y -o"$WORK/pics" "$ZIP" '*.pic' >/dev/null 2>&1 || true
[ -n "$(ls "$WORK/pics" 2>/dev/null)" ] || { echo "no PICs in $ZIP"; exit 1; }

# extract disc; take the high-density data track (LBA base 45000).
# Sector size comes from the GDI (chdman preserves the dump's stored format):
# 2352 = MODE1_RAW (user data at +16), 2048 = plain MODE1 (e.g. lupinsho).
chdman extractcd -f -i "$CHD" -o "$WORK/disc.gdi" >/dev/null 2>&1
TRACK="$(awk '$2==45000{print $5}' "$WORK/disc.gdi")"
SECSZ="$(awk '$2==45000{print $4}' "$WORK/disc.gdi")"
[ -n "$TRACK" ] || { echo "no 45000 data track in $CHD"; exit 1; }

# try each PIC; keep the one that yields a NAOMI-headed image (the game's real key)
for pic in "$WORK"/pics/*.pic; do
  if "$EXTRACT" "$pic" "$WORK/$TRACK" "$OUT/$SET.dat" "$SECSZ" 2>"$WORK/log"; then
    if head -c16 "$OUT/$SET.dat" | grep -q NAOMI; then
      echo "OK  $SET  <- $(basename "$pic")  $(wc -c <"$OUT/$SET.dat") bytes -> $OUT/$SET.dat"
      exit 0
    fi
  fi
done
echo "FAIL $SET: no PIC produced a NAOMI image"; cat "$WORK/log" >&2; exit 2
