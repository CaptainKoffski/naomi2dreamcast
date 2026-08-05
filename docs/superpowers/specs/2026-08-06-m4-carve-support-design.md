# M4 static-scan support: mask the encryption flag bit in carve_boot

**Date:** 2026-08-06
**Status:** approved (design), pending implementation

## Problem

Five M4 cart titles fail the static scan with `load entry out of file:
rom=0x40000000` (kb §4.q: zunou, illvelo, radirgyn, ausfache, mamonoro).
Four of them are *scored*, so their guts axis is silently dropped and
weights renormalize (spec §4.3), skewing finals:

| set      | final | tier |
|----------|-------|------|
| ausfache | 71.3  | A    |
| radirgyn | 46.1  | B    |
| mamonoro | 36.8  | C    |
| illvelo  | 34.1  | C    |

zunou is G1-parked (bad key-PIC dump) and stays parked.

## Root cause

Not missing M4 decryption — `cart2dat.py` has assembled+decrypted M4
carts since e027619 (2026-08-01, `m4dec.c` transcribed from Flycast).
The failure is one step later: M4 load-table entries set **bit 30 of the
rom offset as an "encrypted read" flag**, not an address bit, and
`carve_boot.py` treats the raw value as a file offset.

Primary sources (both agree):

- MAME `src/mame/sega/naomim4.cpp:124-125` @59e7c0b:
  `rom_cur_address = address & 0x1ffffffe; encryption = rom_offset & 0x40000000;`
- Flycast `core/hw/naomi/m4cartridge.cpp:115,131` @ebae3b513:
  `encryption = pio_offset & 0x40000000;` … `rom_cur_address = RomPioOffset & 0x1ffffffe;`

Cart address space is 29-bit (`& 0x1ffffffe`); any offset with bit 30
set is definitionally flagged, never a real position. Since `m4dec`
already produces the fully-decrypted flat image, masking the flag is
sufficient — no decrypt-on-read emulation needed in the carver.

## Design

### 1. Fix — `tools/assess/carve_boot.py`

In the entry loop of `carve()`, **only when `hdr == 0`** (cart image),
mask each entry's rom offset with `0x1ffffffe` before the bounds check.
One line plus a citation comment naming both emulator sources above.

Why cart-only: GD .dats put the header at 0x800000 and use plain file
offsets (sometimes hdr-relative, already handled); a GD data track can
in principle exceed 512 MB, where the mask would corrupt a legitimate
offset. Header position is the discriminator we already trust.

The `0xFFFFFFFF` terminator check in `_entries()` runs on the raw value
before any masking — unchanged.

Also: fix the stale `cart2dat.py` docstring claiming the tool "refuses"
M1/M4 (it hasn't since e027619). That stale line is why this task was
initially framed as "add M4 support".

### 2. Test — `tools/assess/tests/test_carve_boot.py`

New case `test_carve_m4_encrypted_entry`: synthetic cart header
(`hdr_at=0`) with a load entry whose rom offset is `0x40000000 | real`,
assert the payload carves correctly. Existing four cases stay green.
Runner stays the plain `__main__` assert style already used there.

### 3. Re-score driver — `tools/assess/rescore_static.py` (new, committed)

Committed rather than scratchpad: reproducibility rule — the method that
changed four recorded scores must be on record. ~30 lines, reusing
existing functions only:

1. Load `assessments/<set>.metrics.json`.
2. `run_battery.static_scan(set, keep_dat=False)` → fresh guts
   (cart2dat assemble+decrypt → carve → `run_guts.sh` Ghidra pass;
   decrypted .dat deleted afterward as today, never committed).
3. `run_battery.guts_flags(...)` and `run_battery.similarity(...)`
   recomputed — **similarity moves too**: `cart_loader_match` requires
   `dat_available`, `sdk_overlap` requires sdk_strings.
4. Merge into the sidecar (same field shape run_battery writes,
   sdk_strings excluded from the stored guts block as today).
5. `score.score_sidecar(...)`, write back.

Sidecar `versions`/`assessed`/capture fields stay untouched — the
capture is not re-run and its provenance must not be overwritten. The
re-scan is recorded in each title's `.md` instead.

### 4. Rollout

Run the driver for ausfache, radirgyn, mamonoro, illvelo. For each:
update the axes line and add a re-scan note (date, cause, both citation
lines) in `assessments/<set>.md`. Resolve kb §4.q: root cause was the
flag bit in the carver, not missing M4 support in cart2dat; note that
future M4 titles now scan normally with no extra step.

### Error handling

Unchanged: `carve()` still raises `ValueError` on genuinely
out-of-file entries; `static_scan()` still degrades to
`dat_available=false` instead of crashing the battery.

## Out of scope

- zunou (G1-parked, bad dump — guts moot).
- Mixed encrypted/plaintext M4 load tables (none observed; the planned
  byte-compare calibration guard in carve_boot's comments is the
  catch-all if one appears).
- M1 asset LZSS decompression (boot region is plaintext; scans fine).

## Success criteria

- New test passes; existing carve/score/battery tests stay green.
- All four titles re-score with `guts.dat_available = true`, a numeric
  guts axis, and updated finals/tiers in sidecar + `.md`.
- kb §4.q closed with citations; no decrypted dumps left on disk or in git.
