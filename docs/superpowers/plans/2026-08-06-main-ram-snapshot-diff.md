# Main-RAM Write-Truth (Battery v6) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **EXCEPTION (kb §4.j):** Tasks 5–9 launch the assessment battery. A battery started inside a subagent is KILLED the moment that subagent yields (kurucham 2026-08-03 precedent). The coordinator/main session must launch every `run_battery.py` itself (background Bash in the main session survives turns); subagents may only do the before/after work (doc edits, analysis, table regen).

**Goal:** Replace the main-RAM footprint metric (CARTDMA dest high-water) with a snapshot+diff write-truth high-water over Naomi's 32 MB main RAM, un-blinding PIO-loading carts (sgtetris, gwing2) and retiring the spec-v1 main-RAM limitation.

**Architecture:** The fork gains a `MAINPROFILE` emitter cloned from `cartlog_vram_profile()` plus a unified one-shot handoff (`first CARTDMA` OR `cumulative PIO ROM_DATA reads ≥ 32 KB`) that baselines all three regions and tags markers `trigger=dma|pio`. The parser gates main samples on `MAINHANDOFF` and latches handoff on the markers themselves (PIO titles have no CARTDMA line at all). The scorer prefers write-truth peak, falls back to `dma_high_water` for legacy sidecars, and drops-and-flags a blind main region instead of fabricating u=0→100.

**Tech Stack:** C++ (Flycast fork at `../cleopatra/tools/flycast-src`, separate git repo), Python 3 stdlib only (`tools/assess/*.py`), plain-assert test scripts.

**Spec:** `docs/superpowers/specs/2026-08-06-main-ram-snapshot-diff-design.md`

## Global Constraints

- Python is **stdlib only**; tests are plain-assert `__main__` scripts that must print `ALL OK`.
- **Never weaken a guard/test to make a run pass** (kb §8 posture; test_metric_guards.py docstring).
- **Never commit ROMs, decrypted dumps, or `raw/` evidence** — `assessments/evidence/*/raw/` is gitignored; `tools/assess/out/` is scratch.
- Battery is **SERIAL ONLY** (one at a time) and **main-session only** (kb §4.j); launch in background, ~11 min per family.
- **Instrumentation never mutates guest state** — host-side snapshot+diff only (memory rule; moeru A/B).
- Fork work commits in `../cleopatra/tools/flycast-src` (its own git repo, currently at `ebae3b513`); this repo's sidecars pick the new hash up automatically via `flycast_commit()`.
- Constants fixed by the spec: `BATTERY_VERSION = "6"`; PIO handoff threshold **32 KB**; Naomi main window **32 MB** (`RAM_SIZE`); DC cap divisor **16 MB** (`score.py CAPS["main"]`, unchanged).
- Repo comment style: ~78-col wrapped, cite kb §s; `ponytail:` marks deliberate ceilings.

## File Structure

| File | Change |
|---|---|
| `tools/assess/score.py` | Modify `score_sidecar()`: write-truth-preferred main peak, blind-main drop+flag |
| `tools/assess/tests/test_score.py` | Add 2 tests (blind main, write-truth preferred) |
| `tools/assess/tests/test_metric_guards.py` | Add blind-main invariant (Task 1); add sgtetris PIO golden (Task 7) |
| `../cleopatra/tools/flycast-src/core/hw/naomi/cartlog.h` | Declare `cartlog_handoff`, `cartlog_pio_read` |
| `../cleopatra/tools/flycast-src/core/hw/naomi/naomi.cpp` | `cartlog_main_base`, `cartlog_main_profile()`, `cartlog_handoff()`, `cartlog_pio_read()`, wire into `cartlog_sample()`, replace DmaStart block |
| `../cleopatra/tools/flycast-src/core/hw/naomi/naomi_cart.cpp` | Hook `cartlog_pio_read(2)` in the ROM_DATA PIO read funnel |
| `tools/assess/parse_capture.py` | `_MPROF`/`_PIOC`/`_TRIG` regexes, marker-latched handoff, gated main dict, `pio_bytes` |
| `tools/assess/tests/test_parse_capture.py` | Add 2 tests (PIO face end-to-end, DMA trigger + main) |
| `tools/assess/run_battery.py` | `BATTERY_VERSION = "6"`, sidecar `memory.main` shape |
| `assessments/*.metrics.json` + `assessments/*.md` + tables | Re-run wave artifacts (Tasks 5–9) |
| `docs/kb/assessment-tooling.md` | §4.v RESOLVED note (Task 7); new v6 section (Task 10) |
| `docs/superpowers/specs/backlog-main-ram-snapshot-diff.md` | Status flip (Task 10) |

---

### Task 1: Scorer guard — blind main is unmeasured, never 100

Lands FIRST (before any fork work): kills the 100-from-nothing hazard for every
scoring run from now on, and is a permanent "Done means" invariant.

**Files:**
- Modify: `tools/assess/score.py:165-167` (the `memory_axis` call in `score_sidecar`)
- Test: `tools/assess/tests/test_score.py`, `tools/assess/tests/test_metric_guards.py`

**Interfaces:**
- Consumes: sidecar `memory.main` dict — legacy shape `{"dma_high_water": int}` or v6 shape `{"peak": int, "nz_total": int, "nz_above_cap": int, "dma_high_water": int}` (v6 shape produced by Task 4).
- Produces: `sc["scores"]["main_unmeasured"] = True` flag on scored sidecars whose main region was dropped; `memory_axis` receives a peaks dict *without* the `"main"` key in that case (it already handles arbitrary key subsets — `min(scores.values())`).

- [ ] **Step 1: Write the failing tests in `test_score.py`** — append before the `__main__` block:

```python
def test_main_unmeasured_never_100():
    # gwing2 shape (kb §4.v): PIO loader — dma_high_water 0 with real DMA
    # events means the main axis is BLIND, not "u=0 -> 100". The region drops
    # from the memory min() (spec §4.3 renormalize precedent) and a flag
    # records it in the sidecar.
    sc = {
        "set": "synth-pio",
        "boot": {"ok": True},
        "memory": {"main": {"dma_high_water": 0},
                   "vram": {"peak": 8066048, "nz_above_cap": 0},   # u=0.96
                   "aram": {"peak": 2097152, "nz_above_cap": 0}},  # u=1.0 -> 85
        "streaming": {"steady_mb_per_min": 1.155, "reread_ratio": 0.72,
                      "dma_events": 1344},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert sc["scores"]["main_unmeasured"] is True
    assert sc["scores"]["memory"] == 85.0, sc["scores"]   # min(vram, aram)

def test_main_write_truth_preferred():
    # v6 sidecar: memory.main.peak (write-truth) is the scored figure even
    # when dma_high_water is 0 (PIO loader, now measured) — no flag.
    sc = {
        "set": "synth-v6",
        "boot": {"ok": True},
        "memory": {"main": {"peak": 5 * MB, "nz_total": 4 * MB,
                            "nz_above_cap": 0, "dma_high_water": 0},
                   "vram": {"peak": 6 * MB, "nz_above_cap": 0},
                   "aram": {"peak": 1 * MB, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert "main_unmeasured" not in sc["scores"], sc["scores"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]  # all three regions fit
```

- [ ] **Step 2: Write the failing invariant in `test_metric_guards.py`** — append before the `__main__` block:

```python
def test_blind_main_shape_never_scores_100():
    """kb §4.v: dma_high_water == 0 with dma_events > 0 = main axis BLIND
    (PIO loader). score.py must drop+flag the region — a fabricated
    main u=0 -> 100 is the gwing2 100-from-nothing hazard."""
    sc = base_sc()
    sc["memory"]["main"] = {"dma_high_water": 0}
    sc["memory"]["vram"] = {"peak": 7 << 20, "nz_above_cap": 0}   # u=0.875
    sc["streaming"]["dma_events"] = 1344
    score.score_sidecar(sc)
    assert sc["scores"]["main_unmeasured"] is True
    assert sc["scores"]["memory"] < 100.0, sc["scores"]
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py`
Expected: FAIL — `KeyError: 'main_unmeasured'` (or memory == 100.0 assertion) in the first new test reached.

- [ ] **Step 4: Implement in `score.py`** — replace the `memory_axis` call block (currently lines 165–167):

```python
    mem, gated = memory_axis({"main": sc["memory"]["main"]["dma_high_water"],
                              "vram": vram_peak,
                              "aram": sc["memory"]["aram"]["peak"]})
```

with:

```python
    # v6: prefer the write-truth peak (MAINPROFILE snapshot+diff); legacy
    # pre-v6 sidecars fall back to the CARTDMA-dest high-water. A booted title
    # with NEITHER measured is a blind metric (PIO loader — gwing2, kb §4.v),
    # not a zero-footprint game: drop the region from the min() (spec §4.3
    # renormalize precedent) and flag it — u=0 must never fabricate a 100.
    main_peak = sc["memory"]["main"].get("peak") or sc["memory"]["main"]["dma_high_water"]
    peaks = {"vram": vram_peak, "aram": sc["memory"]["aram"]["peak"]}
    if main_peak:
        peaks["main"] = main_peak
    mem, gated = memory_axis(peaks)
```

and after the `sc["scores"]["tier"] = tier(f)` line add:

```python
    if not main_peak:
        sc["scores"]["main_unmeasured"] = True
```

- [ ] **Step 5: Run the full assess test suite**

Run: `python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py && python3 tools/assess/tests/test_parse_capture.py`
Expected: `ALL OK` × 3 (committed cleoftp/ikaruga anchors re-score green through the legacy fallback).

- [ ] **Step 6: Commit**

```bash
git add tools/assess/score.py tools/assess/tests/test_score.py tools/assess/tests/test_metric_guards.py
git commit -m "score: blind main axis = unmeasured (drop+flag), never 100 from nothing (kb 4.v)"
```

---

### Task 2: Fork — unified dma|pio handoff, MAINPROFILE, PIO counter

One commit in the fork repo (`../cleopatra/tools/flycast-src`, own git). No unit
tests exist there; the gate is a clean build with the Vulkan bundle intact, and
Task 5's cleoftp control run is the real validation.

**Files:**
- Modify: `../cleopatra/tools/flycast-src/core/hw/naomi/cartlog.h` (8 lines currently)
- Modify: `../cleopatra/tools/flycast-src/core/hw/naomi/naomi.cpp:193` (baseline ptrs), after `:265` (new fns), `:298-312` (`cartlog_sample`), `:373-387` (DmaStart block)
- Modify: `../cleopatra/tools/flycast-src/core/hw/naomi/naomi_cart.cpp:950-958` (ROM_DATA read case)

**Interfaces:**
- Produces (log lines the parser consumes in Task 3):
  - `MAINHANDOFF baselined size=%x trigger=%s` (and ` trigger=%s` appended to the existing `ARAMHANDOFF`/`VRAMHANDOFF` lines; safe — parser prefix-matches, battery greps substrings)
  - `MAINPROFILE high=%x nz=%x nz_below16m=%x nz_above16m=%x size=%x`
  - `MAINHIST %x %x ...` (128 × 256 KB buckets)
  - `CARTPIOCNT bytes=%llx` (cumulative)
- Produces (C symbols): `void cartlog_handoff(const char *trigger)`, `void cartlog_pio_read(unsigned bytes)`.

- [ ] **Step 1: Declare the new functions in `cartlog.h`** — append:

```c
// naomi.cpp — v6 main-RAM write-truth (2026-08-06):
void cartlog_handoff(const char *trigger);   // one-shot ARAM/VRAM/MAIN baseline; trigger = "dma" | "pio"
void cartlog_pio_read(unsigned bytes);       // ROM_DATA PIO accounting; fires cartlog_handoff("pio") at 32 KB
```

- [ ] **Step 2: Extend the baseline pointers in `naomi.cpp`** — line 193:

```cpp
static u8 *cartlog_aram_base, *cartlog_vram_base, *cartlog_main_base;   // handoff baselines (host-only)
```

- [ ] **Step 3: Add the main profile emitter** — insert directly after `cartlog_vram_profile()` (after line 265):

```cpp
// v6 (2026-08-06): main-RAM write-truth. The v1 metric (CARTDMA dest
// high-water) is blind on PIO-loading carts (sgtetris: zero DMA tags despite
// visibly running; gwing2: dma_high_water 0 with 1,344 non-main DMAs — kb
// §4.v) and misses CPU-written data above the last DMA'd asset (spec v1
// limitation). Same diff-vs-handoff-baseline method as cartlog_vram_profile:
// 32 MB Naomi window, counts split at DC's 16 MB cap. Raw diff only — no
// ARAM-style content dedup; no fill artifact is known for main, and kb §8
// discipline adds exclusion signatures only when a control run proves one.
static void cartlog_main_profile()
{
	const u8 *base = cartlog_main_base;
	if (base == nullptr)
		return;   // kb §9: a diff is only as meaningful as its baseline — never emit a vs-zero sample
	const u32 size = RAM_SIZE, BUCK = 0x40000;   // 256 KB buckets (128 for Naomi's 32 MB)
	u32 hist[128] = {0}, nb = size / BUCK;
	if (nb > 128) nb = 128;
	u32 high = 0, nz = 0, nz_below16m = 0;
	for (u32 i = 0; i < size; i++)
		if (mem_b[i] != base[i]) {
			nz++; high = i + 1;
			if (i < 0x1000000) nz_below16m++;
			u32 b = i / BUCK; if (b < 128) hist[b]++;
		}
	cartlog("MAINPROFILE high=%x nz=%x nz_below16m=%x nz_above16m=%x size=%x\n",
			high, nz, nz_below16m, nz - nz_below16m, size);
	char line[1280]; int p = 0;
	for (u32 b = 0; b < nb; b++)
		p += snprintf(line + p, sizeof(line) - p, "%x ", hist[b]);
	cartlog("MAINHIST %s\n", line);   // nz-byte count per 256 KB bucket (bucket 64+ = past 16 MB)
}

// v6: one-shot handoff baseline at the first BULK cart->RAM transfer — first
// cart DMA, or cumulative PIO ROM_DATA reads crossing 32 KB (PIO-loading
// carts fire no DMA at all; BIOS-era header pokes are bytes-to-KB while an
// image load is MBs, so any threshold in that gap separates them — chocomk
// cartlog evidence, 2026-08-06). Host-side SNAPSHOT, never a zero: v1 zeroed
// the guest arrays and broke rendering for the whole no-render class (moeru
// A/B 2026-08-03) — instrumentation must never mutate guest state.
// v4 guard note still applies: a pre-DMA ARM reset (BIOS jingle) may have
// allocated the ARAM baseline via cartlog_aram_rebaseline; the snapshot here
// refreshes it, and each *HANDOFF marker fires exactly once (the harness
// keys handoff detection on these markers).
void cartlog_handoff(const char *trigger)
{
	if (!cartlog_enabled())
		return;
	static bool logged = false;
	if (logged)
		return;
	logged = true;
	if (cartlog_aram_base == nullptr)
		cartlog_aram_base = new u8[ARAM_SIZE];
	memcpy(cartlog_aram_base, &aica::aica_ram[0], ARAM_SIZE);
	cartlog("ARAMHANDOFF baselined size=%x trigger=%s\n", ARAM_SIZE, trigger);
	cartlog_vram_base = new u8[VRAM_SIZE];
	memcpy(cartlog_vram_base, &vram[0], VRAM_SIZE);
	cartlog("VRAMHANDOFF baselined size=%x trigger=%s\n", VRAM_SIZE, trigger);
	cartlog_main_base = new u8[RAM_SIZE];
	memcpy(cartlog_main_base, &mem_b[0], RAM_SIZE);
	cartlog("MAINHANDOFF baselined size=%x trigger=%s\n", RAM_SIZE, trigger);
}

// v6: PIO ROM_DATA read accounting (called from the naomi_cart.cpp funnel).
// Cart reads are MMIO and always route through C code — unlike RAM stores,
// the dynarec fast path cannot bypass this (contrast cartlog_shimwatch).
// Doubles as the PIO-loading handoff trigger and the CARTPIOCNT lower bound.
static unsigned long long cartlog_pio_bytes;
void cartlog_pio_read(unsigned bytes)
{
	if (!cartlog_enabled())
		return;
	cartlog_pio_bytes += bytes;
	if (cartlog_pio_bytes >= (32 << 10))
		cartlog_handoff("pio");
}
```

- [ ] **Step 4: Wire into `cartlog_sample()`** — after the `cartlog_vram_profile();` line (line 303):

```cpp
	cartlog_main_profile();   // v6: main-RAM fit (write-truth, post-handoff)
	cartlog("CARTPIOCNT bytes=%llx\n", cartlog_pio_bytes);
```

- [ ] **Step 5: Replace the DmaStart handoff block** — in `Naomi_DmaStart`, delete lines 369–387 (the `// Phase 5: baseline ...` + `// v4: guards split ...` comments, the `static bool cartlog_handoff_logged` latch, and the whole `if (!cartlog_handoff_logged) { ... }` block) and replace with:

```cpp
			cartlog_handoff("dma");   // Phase 5/v6: one-shot 3-region baseline (see cartlog_handoff)
```

Keep the `static u32 cartlog_dma_count` every-64th-DMA sample block that follows it unchanged.

- [ ] **Step 6: Hook the PIO read funnel** — in `naomi_cart.cpp`, `NaomiCartridge::ReadMem` case `NAOMI_ROM_DATA_addr` (line 950; this is the single funnel — `GDCartridge`/`SystemSpCart` delegate to it):

```cpp
	case NAOMI_ROM_DATA_addr:
		{
			u32 rv = 0;
			Read(RomPioOffset, 2, &rv);
			if (RomPioAutoIncrement)
				RomPioOffset += 2;
			cartlog_pio_read(2);   // v6: PIO load accounting + bulk-transfer handoff trigger

			return rv;
		}
```

- [ ] **Step 7: Incremental build (cache already has USE_VULKAN=ON, Unix Makefiles, Homebrew cmake 4.4.0)**

```bash
cd /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
cmake --build build -j"$(sysctl -n hw.ncpu)"
ls build/Flycast.app/Contents/Frameworks/libvulkan.dylib   # Vulkan bundle intact (GL never shows CPU-FB screens, kb §7)
```

Expected: build succeeds; `libvulkan.dylib` present. If the incremental build fails at generate, re-run the full recipe in `../cleopatra/docs/kb/tooling.md` §"Configure + build".

- [ ] **Step 8: Commit in the fork repo and record the hash**

```bash
cd /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src
git add core/hw/naomi/cartlog.h core/hw/naomi/naomi.cpp core/hw/naomi/naomi_cart.cpp
git commit -m "instrumentation v6: main-RAM write-truth; unified dma|pio handoff; PIO byte counter"
git rev-parse --short HEAD
```

Note the hash — every v6 sidecar's `versions.flycast` must show it (automatic via `flycast_commit()`).

---

### Task 3: Parser — MAINPROFILE, marker-latched handoff, trigger, pio_bytes

**Files:**
- Modify: `tools/assess/parse_capture.py`
- Test: `tools/assess/tests/test_parse_capture.py`

**Interfaces:**
- Consumes: the Task 2 log lines (exact formats in Task 2's Interfaces block); tolerates legacy logs (no `trigger=`, no `MAINHANDOFF`) — then `trigger` is `None` and main peak stays 0.
- Produces (consumed by Task 4's sidecar assembly): `parse()` return gains
  `main = {"dma_high_water", "watermark_max", "peak", "nz_total", "nz_above_cap"}`,
  `streaming["pio_bytes"]` (int), `handoff = {"seen", "t", "aram_zeroed", "vram_zeroed", "main_baselined", "trigger"}`.
- CRITICAL behavior change: `handoff["seen"]` now ALSO latches on any `*HANDOFF` marker line (PIO titles emit no `CARTDMA` line ever — without this, sgtetris parses `boot_ok=False` even with the fork fix).

- [ ] **Step 1: Write the failing tests** — append to `test_parse_capture.py` before the `__main__` block, and add the two calls + prints there:

```python
def test_pio_handoff_and_main_profile():
    # v6 PIO face (sgtetris, kb §4.v): no CARTDMA line ever — handoff.seen
    # must latch on the marker lines themselves. Pre-MAINHANDOFF MAINPROFILE
    # samples diff vs a null baseline (a different measurement, kb §9) and
    # must be dropped — the exact pre-VRAMHANDOFF rule, applied to main.
    log = (
        "CARTPIO offset=00000000\n"
        "MAINPROFILE high=1d00000 nz=400000 nz_below16m=300000 nz_above16m=100000 size=2000000\n"
        "ARAMHANDOFF baselined size=800000 trigger=pio\n"
        "VRAMHANDOFF baselined size=1000000 trigger=pio\n"
        "MAINHANDOFF baselined size=2000000 trigger=pio\n"
        "MAINPROFILE high=4c0000 nz=3c0000 nz_below16m=3c0000 nz_above16m=0 size=2000000\n"
        "MAINPROFILE high=980000 nz=700000 nz_below16m=700000 nz_above16m=0 size=2000000\n"
        "VRAMPROFILE high=300000 nz=200000 nz_below8m=200000 nz_above8m=0 size=1000000\n"
        "CARTPIOCNT bytes=2f0000\n"
    )
    m = parse_capture.parse(log)
    assert m["handoff"]["seen"] is True and m["handoff"]["trigger"] == "pio"
    assert m["handoff"]["main_baselined"] is True
    assert m["main"]["peak"] == 0x980000, hex(m["main"]["peak"])
    assert m["main"]["nz_total"] == 0x700000 and m["main"]["nz_above_cap"] == 0
    assert m["main"]["dma_high_water"] == 0
    assert m["streaming"]["pio_bytes"] == 0x2f0000
    assert m["streaming"]["dma_events"] == 0
    assert m["boot_ok"] is True     # vram nz_total 0x200000 >= 0x80000

def test_dma_trigger_and_main_above_cap():
    log = (
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "ARAMHANDOFF baselined size=800000 trigger=dma\n"
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "MAINHANDOFF baselined size=2000000 trigger=dma\n"
        "MAINPROFILE high=1100000 nz=e00000 nz_below16m=d00000 nz_above16m=100000 size=2000000\n"
    )
    m = parse_capture.parse(log)
    assert m["handoff"]["trigger"] == "dma"
    assert m["main"]["peak"] == 0x1100000 and m["main"]["nz_above_cap"] == 0x100000
```

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: FAIL — `KeyError: 'trigger'` (or `main` missing `peak`).

- [ ] **Step 3: Implement in `parse_capture.py`**

Add regexes after `_VREGS` (line 15):

```python
_MPROF = re.compile(r"^MAINPROFILE high=([0-9a-f]+) nz=([0-9a-f]+) nz_below16m=[0-9a-f]+ nz_above16m=([0-9a-f]+)", re.I)
_PIOC = re.compile(r"^CARTPIOCNT bytes=([0-9a-f]+)", re.I)
_TRIG = re.compile(r"trigger=(\w+)")
```

Extend the state init (lines 29–34):

```python
    handoff = {"seen": False, "t": None, "aram_zeroed": False, "vram_zeroed": False,
               "main_baselined": False, "trigger": None}
    ...
    main = {"peak": 0, "nz_total": 0, "nz_above_cap": 0}
    pio_bytes = 0
```

Replace the `ARAMHANDOFF`/`VRAMHANDOFF` elif branches (keep `ARAMREBASE` as is) with a combined marker branch:

```python
        elif s.startswith(("ARAMHANDOFF", "VRAMHANDOFF", "MAINHANDOFF")):
            if s.startswith("ARAMHANDOFF"):
                handoff["aram_zeroed"] = True
            elif s.startswith("VRAMHANDOFF"):
                handoff["vram_zeroed"] = True
            else:
                handoff["main_baselined"] = True
            # v6: PIO-loading carts fire no CARTDMA line at all (sgtetris,
            # kb §4.v) — the handoff markers themselves are the boot signal
            if not handoff["seen"]:
                handoff["seen"] = True
                handoff["t"] = t_of(end)
            mt = _TRIG.search(s)
            if mt and handoff["trigger"] is None:
                handoff["trigger"] = mt.group(1)
```

In the profile-matching chain, replace the innermost `_VREGS` fallback
(currently the final `else:` holding `m = _VREGS.match(s)` / `if m:
vram["regs_last"] = m.group(1)`) with this extended ladder — `_MPROF` and
`_PIOC` continue the existing one-regex-per-level nesting:

```python
                    else:
                        m = _VREGS.match(s)
                        if m:
                            vram["regs_last"] = m.group(1)
                        else:
                            m = _MPROF.match(s)
                            # pre-MAINHANDOFF samples would diff vs a null
                            # baseline — a different measurement (kb §9); the
                            # fork skips them, drop any anyway
                            if m and handoff["main_baselined"]:
                                main["peak"] = max(main["peak"], int(m.group(1), 16))
                                main["nz_total"] = max(main["nz_total"], int(m.group(2), 16))
                                main["nz_above_cap"] = max(main["nz_above_cap"], int(m.group(3), 16))
                            else:
                                m = _PIOC.match(s)
                                if m:
                                    pio_bytes = max(pio_bytes, int(m.group(1), 16))
```

Extend the return dict:

```python
        "main": {"dma_high_water": main_hw, "watermark_max": wm.get("main", 0),
                 "peak": main["peak"], "nz_total": main["nz_total"],
                 "nz_above_cap": main["nz_above_cap"]},
        ...
        "streaming": {"dma_events": len(dmas), "total_bytes": total, "unique_bytes": unique,
                      "reread_ratio": round(reread, 4), "steady_mb_per_min": steady,
                      "short_window": short_window, "pio_bytes": pio_bytes},
```

- [ ] **Step 4: Run the parser tests — all must pass (old tests prove legacy-log compat)**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: `ALL OK` (old `test_parse` uses legacy `zeroed`-style marker lines with a preceding CARTDMA — its `handoff["t"] == 10.0` assert pins that CARTDMA still latches first).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/parse_capture.py tools/assess/tests/test_parse_capture.py
git commit -m "parse_capture: MAINPROFILE write-truth, marker-latched handoff + trigger, pio_bytes"
```

---

### Task 4: Battery v6 — version bump + sidecar main shape

**Files:**
- Modify: `tools/assess/run_battery.py:18` (version), `:312` (sidecar memory dict)

**Interfaces:**
- Consumes: Task 3's `cap["main"]` keys and `cap["handoff"]["trigger"]` (rides into the sidecar via the existing `"handoff": cap["handoff"]` passthrough; `pio_bytes` rides via `dict(cap["streaming"])`).
- Produces: sidecar `memory.main = {"peak", "nz_total", "nz_above_cap", "dma_high_water"}` — the shape Task 1's scorer prefers.

- [ ] **Step 1: Bump the version constant** — replace line 18 with:

```python
BATTERY_VERSION = "6"  # v6: main-RAM write-truth snapshot+diff (fork MAINPROFILE/MAINHIST; spec docs/superpowers/specs/2026-08-06-main-ram-snapshot-diff-design.md). Unified dma|pio bulk-transfer handoff un-blinds PIO-loading carts (sgtetris kb §4.v): first CARTDMA OR 32 KB cumulative PIO ROM_DATA reads baselines ARAM+VRAM+MAIN. memory.main scored from write-truth peak (dma_high_water demoted to informational); blind-main shapes renormalize+flag, never 100. CARTPIOCNT = PIO streaming lower bound. Prior sidecars' main figures stale per the re-assessment rule; v5 VRAM/ARAM figures unaffected.
```

- [ ] **Step 2: Extend the sidecar memory dict** — replace the `"memory"` entry (line 312):

```python
        "memory": {"main": {"peak": cap["main"]["peak"], "nz_total": cap["main"]["nz_total"],
                            "nz_above_cap": cap["main"]["nz_above_cap"],
                            "dma_high_water": cap["main"]["dma_high_water"]},
                   "vram": {"peak": cap["vram"]["peak"], "nz_total": cap["vram"].get("nz_total"),
                            "nz_above_cap": cap["vram"]["nz_above_cap"],
                            "regs_last": cap["vram"]["regs_last"]},
                   "aram": {"peak": cap["aram"]["peak"], "nz_above_cap": cap["aram"]["nz_above_cap"]}},
```

- [ ] **Step 3: Run the selftest suite exactly as the battery will**

Run: `python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py && python3 tools/assess/tests/test_parse_capture.py && python3 tools/assess/calibration.py`
Expected: `ALL OK` × 3 and a clean calibration pass (carve pipeline untouched — any calibration failure here is pre-existing drift; stop and diagnose per kb §10).

- [ ] **Step 4: Commit**

```bash
git add tools/assess/run_battery.py
git commit -m "battery v6: sidecar memory.main write-truth shape"
```

---

### Task 5: Validation — cleoftp anchor re-run (MAIN SESSION)

The control test (CLAUDE.md rule 2): the known-good reference through the new
path before trusting it anywhere else. kb §4.a flake warning applies (~1-in-3
launches; auto-retry built in; retry manually once more before escalating).

**Files:**
- Modify (by the battery): `assessments/cleoftp.metrics.json`, `assessments/evidence/cleoftp/`
- Modify (by hand): `assessments/cleoftp.md`, `assessments/RANKING.md`, `GAME_FORMATS.md`

- [ ] **Step 1: Launch the battery in the main session (background Bash), serial**

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast
python3 tools/assess/run_battery.py cleoftp
```

(~11 min. `selftest()` runs first and must pass — it now includes Task 1's guard.)

- [ ] **Step 2: Verify the anchor invariants**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/cleoftp.metrics.json"))
assert sc["versions"]["battery"] == "6", sc["versions"]
assert sc["versions"]["flycast"] != "ebae3b513", "fork commit did not change — wrong binary?"
assert sc["gate"] is None, ("ANCHOR PARKED — tooling regression (kb §8)", sc["gate"])
assert sc["capture"]["handoff"]["trigger"] == "dma", sc["capture"]["handoff"]
m = sc["memory"]
assert m["vram"]["peak"] == 8181717, ("vram path regressed", m["vram"])   # bit-identical across all clean runs (kb §3)
assert m["aram"]["peak"] == 2097152, ("aram path regressed", m["aram"])
assert m["main"]["dma_high_water"] == 11761888, m["main"]
assert m["main"]["peak"] >= 11761888, ("write-truth below DMA floor — impossible", m["main"])
print("main write-truth:", m["main"]["peak"], "u =", round(m["main"]["peak"] / (16 << 20), 3))
print("tier:", sc["scores"]["tier"], "final:", sc["scores"]["final"])
EOF
```

Expected: tier `S`. **If `main.peak > 16777216`:** STOP — do not weaken anything; pull `MAINHIST` from `assessments/evidence/cleoftp/raw/cartlog.txt` (buckets 64+ are above the DC cap), compare hot buckets against `CARTDMA dest` addresses to test the §6-item-3 stream-cache hypothesis, and bring the finding to the user before accepting or changing any number.

- [ ] **Step 3: Verify sampling health + record scan cost**

```bash
grep -c "MAINPROFILE" assessments/evidence/cleoftp/raw/cartlog.txt   # expect ≈ capture_s/10 (±DMA-triggered extras)
python3 -c "import json; tl=json.load(open('assessments/evidence/cleoftp/raw/timeline.json')); print([round(b[0]-a[0],1) for a,b in zip(tl,tl[1:])][:12])"
```

Expected: sample count ≈ 60+ for a 600 s run; timeline deltas steady at ~10 s (no starvation from the 32 MB scan). Note both numbers for Task 10's kb section.

- [ ] **Step 4: Update docs + tables, curate shots, commit (RUNBOOK re-assessment shape)**

Update `assessments/cleoftp.md`: v6 re-run note in the calibration banner section — new `versions` (battery 6, fork hash), main write-truth peak alongside the historical 11,761,888 B DMA figure, one line on what changed and why the anchor still validates. Curate `shot-*.png` (delete near-duplicates). Then:

```bash
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
git add assessments/cleoftp.metrics.json assessments/cleoftp.md assessments/evidence/cleoftp assessments/RANKING.md GAME_FORMATS.md
git commit -m "assess(cleoftp): battery v6 anchor re-run — main write-truth validates vs DMA floor"
```

---

### Task 6: Validation — ikaruga anchor re-run (MAIN SESSION)

**Files:** same shape as Task 5, for `ikaruga`.

- [ ] **Step 1: Launch (main session, background, after Task 5 finishes — SERIAL)**

```bash
python3 tools/assess/run_battery.py ikaruga
```

(Reminder: ikaruga spends ~330 s on its calibration-screen countdown (kb §4.b) — the 600 s window is sized for it. GD launch is via the companion zip candidate; the battery handles this.)

- [ ] **Step 2: Verify**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/ikaruga.metrics.json"))
assert sc["versions"]["battery"] == "6"
assert sc["gate"] is None, ("ANCHOR PARKED — tooling regression (kb §8)", sc["gate"])
assert sc["capture"]["handoff"]["trigger"] == "dma", sc["capture"]["handoff"]
assert sc["memory"]["main"]["peak"] > 0, "main axis still blind on a DMA title"
print("main:", sc["memory"]["main"], "\nscores:", sc["scores"])
EOF
```

- [ ] **Step 3: Docs + tables + commit**

Same RUNBOOK shape as Task 5 Step 4, for ikaruga (calibration-reference banner doc — record the v6 main figure and versions):

```bash
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
git add assessments/ikaruga.metrics.json assessments/ikaruga.md assessments/evidence/ikaruga assessments/RANKING.md GAME_FORMATS.md
git commit -m "assess(ikaruga): battery v6 anchor re-run — main axis measured"
```

---

### Task 7: sgtetris — the PIO face un-blinds; golden the shape (MAIN SESSION)

**Files:**
- Modify (battery): `assessments/sgtetris.metrics.json`, `assessments/evidence/sgtetris/`
- Modify (hand): `assessments/sgtetris.md`, `assessments/QUEUE.md`, `assessments/RANKING.md`, `GAME_FORMATS.md`, `docs/kb/assessment-tooling.md` (§4.v), `tools/assess/tests/test_metric_guards.py`

- [ ] **Step 1: Launch (main session, background, serial)**

```bash
python3 tools/assess/run_battery.py sgtetris
```

- [ ] **Step 2: Verify the PIO face end-to-end**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/sgtetris.metrics.json"))
h = sc["capture"]["handoff"]
assert h["seen"] is True, ("still no handoff — PIO trigger did not fire", h)
assert h["trigger"] == "pio", h
assert sc["memory"]["main"]["peak"] > 0
assert sc["memory"]["vram"]["peak"] > 0 and sc["memory"]["aram"]["peak"] > 0
print("gate:", sc["gate"], "\nscores:", sc["scores"], "\nmain:", sc["memory"]["main"])
print("pio_bytes:", sc["streaming"]["pio_bytes"])
EOF
```

Either verdict is a success **if the reason is real**: a score, or a park backed by measured metrics (e.g. a genuine G3). Sanity-compare `main.peak` against the stale 29.1 MB watermark — write-truth should read far lower if the watermark was BIOS/test residue (spec's expectation). Screenshots must pass the representativeness check (RUNBOOK): title + attract states as seen in the parked run.

- [ ] **Step 3: Add the PIO regression golden to `test_metric_guards.py`** — append:

```python
def test_sgtetris_pio_face_stays_measured():
    """kb §4.v RESOLVED regression control: the PIO-loading cart must stay
    measurable. If this committed sidecar's shape degrades (handoff lost,
    trigger wrong, main blind), the PIO handoff trigger has regressed."""
    sc = json.load(open(os.path.join(ASSESS, "sgtetris.metrics.json")))
    assert sc["capture"]["handoff"]["seen"] is True
    assert sc["capture"]["handoff"]["trigger"] == "pio"
    assert sc["memory"]["main"]["peak"] > 0
```

- [ ] **Step 4: Run the guards test**

Run: `python3 tools/assess/tests/test_metric_guards.py`
Expected: `ALL OK` (new golden green against the just-written sidecar).

- [ ] **Step 5: Docs — rewrite sgtetris.md, kb §4.v RESOLVED, queue + tables**

- `assessments/sgtetris.md`: from parked short-form to the TEMPLATE full form (or a parked doc with the *real* gate) — controls research is already in the old doc's §7, carry it over; cite `trigger=pio`, main/vram/aram write-truth figures, pio_bytes.
- `docs/kb/assessment-tooling.md` §4.v: append a `**RESOLVED <execution date>.**` paragraph (match §4.q's RESOLVED style): unified bulk-transfer handoff (32 KB PIO threshold), sgtetris measured end-to-end, golden test added; point to the v6 section (Task 10) and the spec.
- Flip sgtetris's `assessments/QUEUE.md` status cell if it changes class.

```bash
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
git add assessments/sgtetris.metrics.json assessments/sgtetris.md assessments/evidence/sgtetris assessments/QUEUE.md assessments/RANKING.md GAME_FORMATS.md docs/kb/assessment-tooling.md tools/assess/tests/test_metric_guards.py
git commit -m "assess(sgtetris): PIO face un-blinded under battery v6 — kb 4.v resolved, shape goldened"
```

---

### Task 8: gwing2 — partial face re-run (MAIN SESSION)

**Files:** battery artifacts + `assessments/gwing2.md`, tables.

- [ ] **Step 1: Launch (main session, background, serial)**

```bash
python3 tools/assess/run_battery.py gwing2
```

- [ ] **Step 2: Verify**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/gwing2.metrics.json"))
assert sc["memory"]["main"]["peak"] > 0, "main still blind"
print("trigger:", sc["capture"]["handoff"]["trigger"])   # dma or pio — record which
print("gate:", sc["gate"])   # G3 aram expected to stand (address-keyed; checkpoint scope)
print("main:", sc["memory"]["main"], "\npio_bytes:", sc["streaming"]["pio_bytes"])
EOF
```

Expected: still parked G3-aram (that gate's semantics are the §6 checkpoint's problem, untouched here) — but the doc's tension 2 (blind main) is now resolved with a measured figure, and `pio_bytes` bounds the PIO streaming its old doc called "partial".

- [ ] **Step 3: Docs + commit**

Update `assessments/gwing2.md` § Gate: main row gets the write-truth peak (u value) replacing "0 (blind — PIO loader)"; strike tension 2 with a resolution note; keep tension 1 (checkpoint item) as is.

```bash
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
git add assessments/gwing2.metrics.json assessments/gwing2.md assessments/evidence/gwing2 assessments/RANKING.md GAME_FORMATS.md
git commit -m "assess(gwing2): battery v6 re-run — main axis measured, tension 2 resolved"
```

---

### Task 9: Cluster re-runs — kurucham, ss2005, takoron, tetkiwam (MAIN SESSION)

The §6-item-3 question: are the old 27.4/27.5/29.4/30.5 MB main high-waters
per-title working sets or shared stream-cache placement? Four serial runs,
~45 min total. Parked-on-ARAM members (ss2005, takoron) still record main
metrics in their sidecars — the analysis works on parked sidecars too.

**Files:** battery artifacts + the four `assessments/<set>.md` docs, tables, and a findings note for kb §6 item 3.

- [ ] **Step 1: Run all four, serially, main session** (kurucham flake history: kb §4.a — retry manually once on a park with a prior clean sidecar)

```bash
python3 tools/assess/run_battery.py kurucham
python3 tools/assess/run_battery.py ss2005
python3 tools/assess/run_battery.py takoron
python3 tools/assess/run_battery.py tetkiwam
```

- [ ] **Step 2: Extract the comparison**

```bash
python3 - <<'EOF'
import json
OLD = {"kurucham": 27400000, "ss2005": 27500000, "takoron": 29400000, "tetkiwam": 30495872}
for s in ("kurucham", "ss2005", "takoron", "tetkiwam"):
    sc = json.load(open(f"assessments/{s}.metrics.json"))
    m = sc["memory"]["main"]
    print(f"{s}: old dma_hw ~{OLD[s]:,} -> v6 dma_hw {m['dma_high_water']:,}, "
          f"write-truth peak {m['peak']:,} (u={m['peak']/(16<<20):.2f}), "
          f"nz_above_cap {m['nz_above_cap']:,}, gate={sc['gate']}")
EOF
```

Also pull each `MAINHIST` from `raw/cartlog.txt` while the last set's raw
survives (earlier sets' raw dirs are deleted by the next run — kb §4.u; grab
each set's final `MAINHIST` line right after its run, before starting the next):
dense high buckets that overlap `CARTDMA` dest ranges = stream-cache
placement; scattered low-bucket density = real working set.

- [ ] **Step 3: Docs + findings + commit**

Update the four assessment docs with v6 figures (tetkiwam.md §9 gets the answer to its own clustering flag). Append the findings as a dated note under kb §6 item 3 — data only, **no scoring-rule change** (checkpoint scope). Then:

```bash
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
git add assessments/kurucham.metrics.json assessments/ss2005.metrics.json assessments/takoron.metrics.json assessments/tetkiwam.metrics.json assessments/kurucham.md assessments/ss2005.md assessments/takoron.md assessments/tetkiwam.md assessments/evidence assessments/RANKING.md GAME_FORMATS.md docs/kb/assessment-tooling.md
git commit -m "assess: battery v6 cluster re-runs — main write-truth vs the 27-30 MB dma clustering (kb 6.3 data)"
```

---

### Task 10: kb v6 section + backlog brief closure

**Files:**
- Modify: `docs/kb/assessment-tooling.md` (campaign-version header line + new section), `docs/superpowers/specs/backlog-main-ram-snapshot-diff.md`

- [ ] **Step 1: Write the kb v6 section**

Match the §7/§9 style: a `## 11. Battery v6 (<execution date>): main-RAM write-truth — the PIO blind spot closes` section covering: the two faces (sgtetris/gwing2), the unified bulk-transfer handoff rule + why 32 KB (chocomk evidence: BIOS header pokes vs image loads), rejected anchors (PC-in-RAM — BIOS relocates itself to main RAM; first-CARTPIO — BIOS-era), the marker-latched parser handoff, blind-main drop+flag rule, scan-cost numbers from Task 5 Step 3, wave results summary (anchor deltas, sgtetris verdict, cluster findings), and the standing rule that `dma_high_water` is informational-only from v6 on. Update the header line: `Campaign version: **battery v6** (...; v3 §7, v4 §7, v5 §9, v6 §11)`.

- [ ] **Step 2: Flip the brief**

In `backlog-main-ram-snapshot-diff.md`, change the Status line to: `**Status:** IMPLEMENTED <execution date> — design docs/superpowers/specs/2026-08-06-main-ram-snapshot-diff-design.md, kb §11; sgtetris goldened, wave recorded.` (Leave the body as the motivating record.) Update the kb §6 pointer sentence for this brief ("Checkpoint-independent instrumentation work") to note it landed.

- [ ] **Step 3: Commit**

```bash
git add docs/kb/assessment-tooling.md docs/superpowers/specs/backlog-main-ram-snapshot-diff.md
git commit -m "kb: battery v6 section — main-RAM write-truth, PIO handoff; close the backlog brief"
```

---

## Self-review notes (spec coverage)

- Spec "Fork" component → Task 2. "parse_capture" → Task 3 (plus the marker-latch gap the spec implies via "sgtetris assessable end-to-end" — without it, `boot_ok` stays False on PIO titles even with the fork fix). "score.py/Task-1 guard" → Task 1. "run_battery" → Task 4.
- Spec "Validation ladder" 1–5 → Tasks 5–9, same gating order. "Doc updates" → Tasks 7, 9, 10. "Done means" items map: fork emitters (T2), memory.main scored from write-truth (T1+T4), sgtetris end-to-end (T7), gwing2 measured (T8), blind-never-100 guard (T1), version bump + wave recorded (T4, T5–T10).
- Cadence/threshold/scan-cost decisions are constants in Task 2 code (600-vblank tick untouched; 32 KB literal) with the cost measurement in Task 5 Step 3 and its record in Task 10.
