# M4 Static-Scan Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the static scan work on M4 carts by masking the bit-30 encryption flag in `carve_boot.py`, then re-score the four affected titles (ausfache, radirgyn, mamonoro, illvelo).

**Architecture:** One-line semantic fix in the carve (cart images only, exact hardware mask `& 0x1ffffffe`), a small committed rescore driver that reuses `run_battery.static_scan`/`guts_flags`/`similarity` + `score.score_sidecar` against existing sidecars (no capture re-run), then per-title doc updates and kb §4.q resolution.

**Tech Stack:** Python 3 stdlib only. External steps already in place: `cart2dat.py`+`m4dec` (decrypt), Ghidra 12.1.2 headless via `tools/assess/ghidra/run_guts.sh`.

**Spec:** `docs/superpowers/specs/2026-08-06-m4-carve-support-design.md`

## Global Constraints

- Never commit or leave on disk decrypted ROM dumps: `static_scan(..., keep_dat=False)` deletes the `.dat` and `boot.bin`; keep it that way. `naomi/` and `tools/dat-extract/out/` stay out of git.
- Hardware/behavioral claims carry citations; these two are the load-bearing ones, copy them verbatim where the plan says so:
  - MAME `src/mame/sega/naomim4.cpp:124-125` @59e7c0b: `rom_cur_address = address & 0x1ffffffe; encryption = rom_offset & 0x40000000;`
  - Flycast `core/hw/naomi/m4cartridge.cpp:115,131` @ebae3b513: `encryption = pio_offset & 0x40000000;` / `rom_cur_address = RomPioOffset & 0x1ffffffe;`
- Sidecar fields `versions`, `assessed`, `params`, `boot`, `capture`, `memory`, `streaming`, `serial_pokes`, `controls` are capture provenance — the rescore must not touch them. Only `guts`, `similarity`, `gate`, `scores` are recomputed.
- Run rescores serially, one set at a time.
- Repo convention: commit directly on `main`, message style `<tool>: <what>` or `assess(<set>): <what>`.
- Tests are plain `assert` + `__main__` runners (no pytest): run with `python3 tools/assess/tests/test_carve_boot.py`.

---

### Task 1: carve_boot bit-30 mask (TDD)

**Files:**
- Modify: `tools/assess/carve_boot.py` (entry loop in `carve()`, lines 29-38, + docstring)
- Modify: `tools/dat-extract/cart2dat.py` (stale docstring lines 13-14 only)
- Test: `tools/assess/tests/test_carve_boot.py`

**Interfaces:**
- Consumes: `carve_boot.carve(data: bytes) -> (bytes, dict)` — existing signature, unchanged.
- Produces: same signature; for cart images (`hdr == 0`) each load entry's rom offset is now decoded as `rom & 0x1ffffffe` before bounds-checking, and `meta["entries"]` records the masked offsets. Task 2 relies on this making M4 .dats carveable.

- [ ] **Step 1: Write the failing test**

Append to `tools/assess/tests/test_carve_boot.py` (before the `__main__` block):

```python
def test_carve_m4_encrypted_entry():
    # M4 load entries set bit 30 of the rom offset as the "read via decryption
    # stream" flag, not an address bit (kb §4.q: rom=0x40000000 across 5 sets).
    # For cart images (hdr at 0) carve must apply the hardware address decode.
    img = bytearray(0x2000)
    img[0:5] = b"NAOMI"
    img[0x30:0x36] = b"M4TEST"
    struct.pack_into("<III", img, 0x360, 0x40000000 | 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<I", img, 0x360 + 12, 0xFFFFFFFF)      # terminator
    struct.pack_into("<II", img, 0x420, 0x8c020000, 0x8c020000)
    img[0x1000:0x1100] = b"M" * 0x100
    blob, meta = carve_boot.carve(bytes(img))
    assert meta["hdr_at"] == 0 and meta["title"] == "M4TEST"
    assert blob[0:0x100] == b"M" * 0x100
    assert meta["entries"] == [[0x1000, 0x8c020000, 0x100]]   # masked offset recorded
```

And add to the `__main__` block, before `print("ALL OK")`:

```python
    test_carve_m4_encrypted_entry(); print("test_carve_m4_encrypted_entry OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/assess/tests/test_carve_boot.py`
Expected: first four cases print OK, then `ValueError: load entry out of file: rom=0x40001000 len=0x100`

- [ ] **Step 3: Implement the mask**

In `tools/assess/carve_boot.py`, `carve()`, replace the `fixed` loop head:

```python
    fixed = []
    for rom, ram, n in entries:
        if hdr == 0:
            # Cart images: bit 30 of a load-entry rom offset is the M4
            # encrypted-read flag, and cart addressing is 29-bit — apply the
            # hardware decode. MAME naomim4.cpp:124-125 @59e7c0b
            # (rom_cur_address = address & 0x1ffffffe; encryption =
            # rom_offset & 0x40000000), Flycast m4cartridge.cpp:115,131
            # @ebae3b513. cart2dat's m4dec already wrote plaintext, so the
            # masked value is a plain file offset.
            rom &= 0x1ffffffe
        # GD-ROM .dat entries may use small hdr-relative offsets; try hdr-relative for small values.
        # hdr-relative rom that is accidentally in-bounds under absolute read is undetectable here;
        # calibration byte-compares against known-good boot.bin (planned Task 9) is the real guard.
        if hdr > 0 and rom < 0x100000:
            rom = hdr + rom                       # Small rom values are hdr-relative
        if rom + n > len(data):
            raise ValueError(f"load entry out of file: rom=0x{rom:x} len=0x{n:x}")
        fixed.append((rom, ram, n))
```

(The existing two comment lines about hdr-relative offsets stay as-is; only the `hdr == 0` branch is new. The `0xFFFFFFFF` terminator check in `_entries()` runs on raw values before masking — leave it untouched.)

Update the module docstring's last sentence to mention the flag, e.g. append: `Cart images decode load-entry offsets with the M4 mask (bit 30 = encrypted-read flag, naomim4.cpp:124-125 / m4cartridge.cpp:115,131).`

- [ ] **Step 4: Run tests to verify all pass**

Run: `python3 tools/assess/tests/test_carve_boot.py`
Expected: five `... OK` lines + `ALL OK`

Also run the neighbors that import carve semantics indirectly:
`python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py`
Expected: their usual `ALL OK`/pass output, unchanged.

- [ ] **Step 5: Fix the stale cart2dat docstring**

In `tools/dat-extract/cart2dat.py` replace lines 13-14:

```
M1/M4 carts encrypt the WHOLE ROM (stream cipher) -> assembly alone yields
garbage; this refuses them. GD-ROM games use chd2dat.sh instead.
```

with:

```
M1/M4 carts encrypt the WHOLE ROM (stream cipher): M4 is assembled then
stream-decrypted in place via m4dec (subkeys from the PIC Key blob); M1 boot
code is plaintext (asset data stays LZSS-compressed). GD-ROM uses chd2dat.sh.
```

- [ ] **Step 6: Commit**

```bash
git add tools/assess/carve_boot.py tools/assess/tests/test_carve_boot.py tools/dat-extract/cart2dat.py
git commit -m "carve_boot: decode M4 bit-30 encrypted-read flag on cart load entries

kb §4.q root cause: M4 load-table rom offsets carry bit 30 as a flag
(MAME naomim4.cpp:124-125 @59e7c0b, Flycast m4cartridge.cpp:115,131
@ebae3b513); carve read it as a file offset and bounds-failed. Cart
images (hdr at 0) now apply the hardware mask & 0x1ffffffe; GD path
unchanged. Also un-stale cart2dat's docstring (M4 decrypt exists since
e027619)."
```

---

### Task 2: rescore driver, validated end-to-end on ausfache

**Files:**
- Create: `tools/assess/rescore_static.py`
- Modify: `assessments/ausfache.metrics.json` (via the driver — never by hand)
- Modify: `assessments/ausfache.md`

**Interfaces:**
- Consumes: `run_battery.static_scan(setname, keep_dat) -> dict` (guts or `{"dat_available": False, "error": ...}`), `run_battery.guts_flags(setname, guts, serial_pokes) -> (flags, extra)`, `run_battery.similarity(row, fmt, guts) -> dict` (only reads `row["maker"]`), `score.score_sidecar(sc) -> sc` (mutates; raises `score.MetricRegression` on poisoned metrics).
- Produces: CLI `python3 tools/assess/rescore_static.py <set> [<set> ...]` that rewrites `assessments/<set>.metrics.json` in place. Task 3 runs it for the remaining three sets.

- [ ] **Step 1: Write the driver**

Create `tools/assess/rescore_static.py`:

```python
#!/usr/bin/env python3
"""rescore_static.py <set> [<set> ...]

Re-run the static scan (cart2dat assemble+decrypt -> carve -> Ghidra guts)
for an already-captured family and re-score its sidecar in place. Capture
provenance (versions/assessed/params/boot/capture/memory/streaming/
serial_pokes/controls) is left untouched; guts, similarity, gate and scores
are recomputed. Written for the kb §4.q M4 cohort (ausfache/radirgyn/
mamonoro/illvelo) after the carve_boot bit-30 fix: guts is static-only, so
no 600 s capture re-run is needed. If the scan still fails, the sidecar is
left byte-identical (keeps the historical error string)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_battery, score  # noqa: E402


def rescore(setname):
    path = os.path.join(run_battery.ASSESS, setname + ".metrics.json")
    with open(path) as fh:
        sc = json.load(fh)
    guts = run_battery.static_scan(setname, False)
    if not guts.get("dat_available"):
        sys.exit(f"{setname}: static scan still failing, sidecar untouched: "
                 f"{guts.get('error')}")
    flags, extra = run_battery.guts_flags(setname, guts, sc["serial_pokes"])
    # same field shape run_battery.main() writes (sidecar guts block)
    sc["guts"] = {**{k: v for k, v in guts.items() if k != "sdk_strings"},
                  "flags": flags, "extra_bios_classes": extra,
                  "sdk_strings": guts.get("sdk_strings", [])}
    sc["similarity"] = run_battery.similarity({"maker": sc["maker"]},
                                              sc["format"], guts)
    score.score_sidecar(sc)
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    v = (f"PARKED {sc['gate']}" if sc["gate"]
         else f"{sc['scores']['final']} {sc['scores']['tier']} "
              f"(guts {sc['scores']['guts']})")
    print(f"{setname}: {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__.splitlines()[0])
    for s in sys.argv[1:]:
        rescore(s)
```

- [ ] **Step 2: Run it on ausfache (this is the driver's end-to-end test)**

Run: `python3 tools/assess/rescore_static.py ausfache`
Expected: a single final line like `ausfache: <new final> <tier> (guts <value>)`. Takes minutes (Ghidra headless). Note: cart2dat/Ghidra stdout is captured by `static_scan`, not shown — on failure the captured tail comes back in the error message.

Failure modes: exits with `static scan still failing` → the carve fix didn't take, stop and debug Task 1; `score.MetricRegression` traceback → stop, do not retry, diagnose per kb §7.

- [ ] **Step 3: Verify the sidecar diff is surgical**

Run: `git diff --stat assessments/ausfache.metrics.json && git diff assessments/ausfache.metrics.json | head -80`
Expected: changes confined to `guts` (now `dat_available: true`, `carve_meta`, mmio/code counters, no `error` key), `similarity` (`cart_loader_match` may flip true; `sdk_overlap` per actual sdk_strings), and `scores` (`guts` numeric, new `final`/`tier`). `versions`, `assessed`, `capture`, `memory`, `streaming`, `controls` byte-identical. Confirm `guts.flags` still contains `eeprom_bios`.

Also confirm no decrypted bytes remain: `ls tools/dat-extract/out/ tools/assess/out/*.boot.bin 2>&1`
Expected: no `.dat`, no `boot.bin` (only `.guts.json` and existing battery outputs).

- [ ] **Step 4: Update ausfache.md**

Edit `assessments/ausfache.md`:
- Line 31 axes line: replace `guts None` with the new value and update the final/tier to match the sidecar.
- Lines 114-116 ("Guts **unavailable**..."): rewrite to state guts was re-scanned 2026-08-06 after the carve_boot bit-30 fix — bit 30 is the M4 encrypted-read flag, citing MAME `naomim4.cpp:124-125` @59e7c0b and Flycast `m4cartridge.cpp:115,131` @ebae3b513 — and give the new axis values (guts, similarity, final/tier). Keep the original capture provenance text intact.
- Lines 130-132 ("M4 guts gap" caveat): replace with a note that the gap is closed (rescore via `tools/assess/rescore_static.py`, capture not re-run).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/rescore_static.py assessments/ausfache.metrics.json assessments/ausfache.md
git commit -m "assess(ausfache): guts axis filled via static rescore (carve bit-30 fix)

New committed driver tools/assess/rescore_static.py re-runs static_scan
+ guts_flags + similarity + score_sidecar against the existing sidecar;
capture provenance untouched, decrypted .dat deleted as always."
```

---

### Task 3: re-score radirgyn, mamonoro, illvelo

**Files:**
- Modify: `assessments/radirgyn.metrics.json`, `assessments/mamonoro.metrics.json`, `assessments/illvelo.metrics.json` (via the driver)
- Modify: `assessments/radirgyn.md`, `assessments/mamonoro.md`, `assessments/illvelo.md`

**Interfaces:**
- Consumes: `python3 tools/assess/rescore_static.py <set>` from Task 2.
- Produces: three updated sidecars + `.md`s; final list of before/after scores for the Task 4 kb note.

- [ ] **Step 1: Run the driver serially**

Run: `python3 tools/assess/rescore_static.py radirgyn && python3 tools/assess/rescore_static.py mamonoro && python3 tools/assess/rescore_static.py illvelo`
Expected: one result line per set. If any set exits with `static scan still failing`, stop — its sidecar is untouched by design; diagnose before continuing (the remaining sets can still be run individually).

- [ ] **Step 2: Verify each diff is surgical**

Run: `git diff --stat assessments/*.metrics.json`
Expected: only the three sidecars, and per-file the same shape as ausfache's diff in Task 2 Step 3 (guts/similarity/scores only). Spot-check one: `git diff assessments/radirgyn.metrics.json | head -60`.

- [ ] **Step 3: Update the three .md files**

For each set, mirror the ausfache.md edit (Task 2 Step 4): axes line updated with numeric guts + new final/tier, and the guts-unavailable paragraph replaced with the same re-scan note (date 2026-08-06, bit-30 root cause, both citations, `rescore_static.py`, capture not re-run). Locate the spots with: `grep -n "guts" assessments/radirgyn.md assessments/mamonoro.md assessments/illvelo.md`.

- [ ] **Step 4: Commit**

```bash
git add assessments/radirgyn.metrics.json assessments/radirgyn.md \
        assessments/mamonoro.metrics.json assessments/mamonoro.md \
        assessments/illvelo.metrics.json assessments/illvelo.md
git commit -m "assess(radirgyn,mamonoro,illvelo): guts axes filled via static rescore"
```

---

### Task 4: resolve kb §4.q

**Files:**
- Modify: `docs/kb/assessment-tooling.md` (§4 lesson q, lines 326-336)

**Interfaces:**
- Consumes: before/after finals from Tasks 2-3.
- Produces: closed kb entry; nothing downstream.

- [ ] **Step 1: Rewrite lesson q**

Keep the original five-instance history, then append a resolution paragraph stating:
- **RESOLVED 2026-08-06.** Root cause was not missing M4 support in cart2dat (decrypt exists since e027619) but the carver reading the load-entry rom offset raw: bit 30 is the M4 encrypted-read flag and cart addressing is 29-bit — MAME `naomim4.cpp:124-125` @59e7c0b (`rom_cur_address = address & 0x1ffffffe; encryption = rom_offset & 0x40000000`), Flycast `m4cartridge.cpp:115,131` @ebae3b513. `carve_boot.py` now applies the hardware mask for cart images.
- The four scored titles were re-scored with `tools/assess/rescore_static.py` (capture untouched); list before → after finals/tiers from Tasks 2-3.
- Future M4 titles scan normally, no extra step. zunou stays G1-parked (bad key-PIC dump), guts moot.

- [ ] **Step 2: Commit**

```bash
git add docs/kb/assessment-tooling.md
git commit -m "kb: resolve §4.q — M4 carve flag bit fixed, four titles re-scored"
```
