# Portability Assessment Tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and calibrate the automated battery that scores every never-officially-ported Naomi game for ease of Dreamcast porting, per `docs/superpowers/specs/2026-08-02-portability-assessment-design.md`.

**Architecture:** A serial per-game pipeline: instrumented-Flycast attract capture (existing fork binary, no C++ changes) → log parsing → `.dat` static scan via headless Ghidra → deterministic scoring (`score.py` is the only implementation of the spec's §4 formulas) → machine-readable sidecar (`<set>.metrics.json`) from which all docs and tables derive. Two control-test calibrations (Cleopatra, Ikaruga) gate the real campaign.

**Tech Stack:** Python 3 stdlib only (no pip deps; tests are plain `assert` scripts, runnable directly and pytest-compatible), POSIX sh, one Ghidra Java post-script (Ghidra 12.1.2 dropped Jython headless).

## Global Constraints

- Python 3 **stdlib only** — no new dependencies anywhere.
- **Never commit copyrighted bytes:** no ROMs, no `.chd`, no `.dat`, no carved `boot.bin`, no raw capture logs (they embed dumped data). Screenshots and extracted metrics are fine.
- **Serial execution only** — never two Flycast instances at once (spec §8).
- GitHub-flavoured Markdown for all docs.
- Toolchain pins: instrumented Flycast = `../cleopatra/tools/flycast-src/build/Flycast.app` (record `git -C ../cleopatra/tools/flycast-src rev-parse --short HEAD` in every sidecar) · Ghidra `12.1.2_PUBLIC` at `../cleopatra/tools/ghidra_12.1.2_PUBLIC` · MAME source = `../cleopatra/tools/mame` (commit `59e7c0b`) · `battery_version = "1"`.
- Every hardware/behavioral claim in generated docs carries a citation (log grep tag, screenshot path, or URL; primary sources outrank wikis).
- Repo root in examples: `/Users/captainkoffski/AntigravityProjects/naomi2dreamcast`. All new tools live in `tools/assess/`. Run commands from repo root unless stated.
- Delete `tools/dat-extract/out/<set>.dat` and carved `boot.bin` when the static scan finishes (SSD hygiene, spec §8).

## File Structure

```
tools/assess/
  score.py               ← spec §4 formulas: the ONLY place breakpoints/penalties/weights/tiers live
  parse_capture.py       ← cartlog + timeline → metrics fragment (JSON)
  controls_extract.py    ← MAME naomi.cpp → per-set identity/input JSON
  carve_boot.py          ← .dat header → boot.bin + meta (base addr, entry) for Ghidra
  run_battery.py         ← per-family orchestrator (launch/kill Flycast, parsers, static scan, sidecar)
  gen_tables.py          ← QUEUE.md / RANKING.md generators + GAME_FORMATS.md status-cell patcher
  ghidra/run_guts.sh     ← headless Ghidra wrapper (import+analyze+post-script, one shot)
  ghidra/GutsMetrics.java← post-script: code size, MMIO/BIOS refs, SDK strings → JSON
  tests/test_*.py        ← plain-assert test scripts (one per pure-logic tool)
  out/                   ← gitignored scratch (controls.json, guts JSONs, ghidra proj, carved bins)
assessments/
  RUNBOOK.md TEMPLATE.md ← procedure + doc template (Task 8)
  QUEUE.md               ← generated once in Task 11, hand-curated afterwards
  RANKING.md             ← regenerated from sidecars
  reference/similarity-reference.json  ← built from Cleopatra calibration (Task 9)
  <set>.md <set>.metrics.json          ← per-family outputs (calibration produces 2)
  evidence/<set>/shot-*.png            ← committed; evidence/<set>/raw/ gitignored
docs/kb/assessment-tooling.md          ← versions + lessons (Task 11)
```

Dependency order: Task 1 (score) and Task 3 (controls) and Task 4 (carve) are independent; Task 2 needs nothing but is used by 6; Task 5 needs 4; Task 6 needs 1–5; Task 7 is independent (file-format work); Tasks 9–10 need 6+7+8; Task 11 needs 9–10.

---

### Task 1: Scaffolding + `score.py` (the spec §4 formulas)

**Files:**
- Create: `tools/assess/score.py`
- Create: `tools/assess/tests/test_score.py`
- Modify: `.gitignore` (append scratch/evidence ignores)

**Interfaces:**
- Consumes: a sidecar dict shaped per spec §5.2 (see `score_sidecar` docstring below — Task 6 builds exactly this shape).
- Produces: `region_score(peak, cap) -> float|None`, `memory_axis(peaks: dict) -> (float|None, gated_region|None)`, `streaming_axis(steady_mb_per_min, reread_ratio) -> float`, `guts_axis(flags: set, extra_bios_classes: int) -> float`, `controls_axis(device_class: str) -> float|None`, `similarity_axis(dev_match, sdk_overlap, cart_loader_match) -> float`, `final_score(axes: dict) -> float`, `tier(score) -> str`, `score_sidecar(sidecar: dict) -> dict` (mutates+returns), CLI `python3 tools/assess/score.py <sidecar.json>` (rewrites file in place, prints `<set> <final> <tier>` or `<set> PARKED <gate>`).

- [ ] **Step 1: Append ignores to `.gitignore`**

Append these lines (create the file if absent; skip lines already present):

```
# assessment battery scratch + raw evidence (regenerable; may embed dumped bytes)
tools/assess/out/
assessments/evidence/*/raw/
```

- [ ] **Step 2: Write the failing test**

`tools/assess/tests/test_score.py`:

```python
#!/usr/bin/env python3
"""Plain-assert tests for score.py (spec §4). Run: python3 tools/assess/tests/test_score.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import score

MB = 1 << 20

def test_region_bands():
    cap = 16 * MB
    assert score.region_score(int(0.5 * cap), cap) == 100.0
    assert score.region_score(int(0.80 * cap), cap) == 100.0
    assert round(score.region_score(cap, cap), 4) == 85.0            # u=1.00 exactly -> 85 (spec §4.1)
    assert round(score.region_score(int(1.25 * cap), cap), 4) == 40.0
    assert round(score.region_score(2 * cap, cap), 4) == 10.0
    assert score.region_score(2 * cap + 1, cap) is None              # gate G3

def test_memory_axis_min_and_gate():
    ax, gated = score.memory_axis({"main": 8 * MB, "vram": 2 * MB, "aram": 2 * MB})  # aram u=1.0
    assert round(ax, 4) == 85.0 and gated is None
    ax, gated = score.memory_axis({"main": 40 * MB, "vram": MB, "aram": MB})
    assert ax is None and gated == "main"

def test_streaming():
    assert score.streaming_axis(2.0, 0.05) == 100.0
    assert round(score.streaming_axis(24.0, 0.1), 4) == round(0.6 * 60 + 0.4 * 100, 4)

def test_guts():
    assert score.guts_axis({"serial", "eeprom_bios"}, 0) == 90.0     # the Cleopatra profile
    assert score.guts_axis({"network"}, 6) == 100 - 25 - 10          # bios-class penalty capped at 10
    assert score.guts_axis(set(PENALTY_ALL), 9) == 35.0              # 100 - 55 - 10 (all penalties + cap)

PENALTY_ALL = ("serial", "eeprom_bios", "eeprom_direct", "rtc", "network", "code_over_4mb")

def test_controls_similarity_tiers():
    assert score.controls_axis("stick") == 100.0
    assert score.controls_axis("card_reader") is None                # gate G2: not on the ladder
    assert score.similarity_axis(True, "full", True) == 100.0        # 20+30+40+30 capped
    assert score.similarity_axis(False, "none", False) == 20.0
    assert score.tier(80.0) == "S" and score.tier(79.9) == "A" and score.tier(19.9) == "D"

def test_final_anchor():
    # Cleopatra anchor (spec §4.6): mem 85, stream 100, guts 90, ctrl 100, sim 100 -> 91.8 S
    axes = {"memory": 85.0, "streaming": 100.0, "guts": 90.0, "controls": 100.0, "similarity": 100.0}
    assert score.final_score(axes) == 91.8
    # no-.dat renormalization (spec §4.3): drop guts -> weights x1.25
    axes2 = {"memory": 85.0, "streaming": 100.0, "guts": None, "controls": 100.0, "similarity": 100.0}
    import math
    exp = math.exp(0.5 * math.log(85) + 0.25 * math.log(100) + 0.125 * math.log(100) + 0.125 * math.log(100))
    assert score.final_score(axes2) == round(exp, 1)

def test_score_sidecar_anchor():
    sc = {
        "set": "cleoftp",
        "boot": {"ok": True},
        "memory": {"main": {"dma_high_water": 11761888}, "vram": {"peak": 8181717, "nz_above_cap": 0},
                   "aram": {"peak": 2097152, "nz_above_cap": 0}},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": True, "flags": ["serial", "eeprom_bios"], "extra_bios_classes": 0},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": True, "sdk_overlap": "full", "cart_loader_match": True},
    }
    out = score.score_sidecar(sc)
    assert out["gate"] is None
    assert out["scores"]["final"] == 91.8 and out["scores"]["tier"] == "S"

def test_score_sidecar_gates():
    base = {"set": "x", "boot": {"ok": True},
            "memory": {"main": {"dma_high_water": 40 << 20}, "vram": {"peak": 1}, "aram": {"peak": 1}},
            "streaming": {"steady_mb_per_min": 1, "reread_ratio": 0}, "guts": {"dat_available": True, "flags": [], "extra_bios_classes": 0},
            "controls": {"device_class": "stick"}, "similarity": {"developer_match": False, "sdk_overlap": "none", "cart_loader_match": False}}
    assert score.score_sidecar(dict(base))["gate"].startswith("G3")
    b2 = dict(base); b2["boot"] = {"ok": False}
    assert score.score_sidecar(b2)["gate"].startswith("G1")
    b3 = dict(base); b3["memory"] = {"main": {"dma_high_water": 1}, "vram": {"peak": 1}, "aram": {"peak": 1}}
    b3["controls"] = {"device_class": "card_reader"}
    assert score.score_sidecar(b3)["gate"].startswith("G2")

if __name__ == "__main__":
    for n, f in sorted(globals().items()):
        if n.startswith("test_") and callable(f):
            f(); print(f"{n} OK")
    print("ALL OK")
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 tools/assess/tests/test_score.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'score'`

- [ ] **Step 4: Write `tools/assess/score.py`**

```python
#!/usr/bin/env python3
"""Deterministic Naomi->DC portability scoring — the ONLY implementation of spec §4
(docs/superpowers/specs/2026-08-02-portability-assessment-design.md).
CLI: score.py <sidecar.json>  — rewrites the sidecar in place with scores/gate."""
import json, math, sys

CAPS = {"main": 16 << 20, "vram": 8 << 20, "aram": 2 << 20}
WEIGHTS = {"memory": 0.40, "streaming": 0.20, "guts": 0.20, "controls": 0.10, "similarity": 0.10}
AXIS_FLOOR = 10.0   # spec §4: axes live in [10,100]; a 0 would annihilate the geometric mean


def _lerp(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def region_score(peak, cap):
    """Spec §4.1 piecewise map. None => gate G3 (u > 2)."""
    u = peak / cap
    if u > 2.0:
        return None
    if u <= 0.80:
        return 100.0
    if u <= 1.00:
        return _lerp(u, 0.80, 1.00, 100.0, 85.0)
    if u <= 1.25:
        return _lerp(u, 1.00, 1.25, 85.0, 40.0)
    return _lerp(u, 1.25, 2.00, 40.0, 10.0)


def memory_axis(peaks):
    """peaks: {'main'|'vram'|'aram': bytes}. Returns (axis, None) or (None, gated_region)."""
    scores = {}
    for region, peak in peaks.items():
        s = region_score(peak, CAPS[region])
        if s is None:
            return None, region
        scores[region] = s
    return max(AXIS_FLOOR, min(scores.values())), None   # min: regions aren't tradeable


def bandwidth_score(mb_per_min):
    b = mb_per_min
    if b <= 6:
        return 100.0
    if b <= 24:
        return _lerp(b, 6, 24, 100.0, 60.0)
    if b <= 60:
        return _lerp(b, 24, 60, 60.0, 20.0)
    return 10.0


def reread_score(r):
    if r <= 0.1:
        return 100.0
    if r <= 0.5:
        return _lerp(r, 0.1, 0.5, 100.0, 50.0)
    return _lerp(min(r, 1.0), 0.5, 1.0, 50.0, 20.0)


def streaming_axis(steady_mb_per_min, reread_ratio):
    return max(AXIS_FLOOR, 0.6 * bandwidth_score(steady_mb_per_min) + 0.4 * reread_score(reread_ratio))


PENALTIES = {"serial": 5, "eeprom_bios": 5, "eeprom_direct": 10, "rtc": 5,
             "network": 25, "code_over_4mb": 5}


def guts_axis(flags, extra_bios_classes=0):
    p = sum(PENALTIES[f] for f in flags)
    p += min(10, 2 * extra_bios_classes)
    return max(AXIS_FLOOR, 100.0 - p)


CONTROLS = {"stick": 100.0, "dc_peripheral": 75.0, "pad_adaptable": 50.0, "awkward": 25.0}


def controls_axis(device_class):
    """None => gate G2 (class not on the ladder = physically unmappable)."""
    return CONTROLS.get(device_class)


def similarity_axis(dev_match, sdk_overlap, cart_loader_match):
    pts = 20 + (30 if dev_match else 0) \
             + {"full": 40, "partial": 20, "none": 0}[sdk_overlap] \
             + (30 if cart_loader_match else 0)
    return float(min(100, pts))


TIERS = [(80, "S"), (60, "A"), (40, "B"), (20, "C")]


def tier(score):
    for lo, t in TIERS:
        if score >= lo:
            return t
    return "D"


def final_score(axes):
    """axes: {name: value | None}; None drops the axis and renormalizes weights (spec §4.3)."""
    used = {k: v for k, v in axes.items() if v is not None}
    wsum = sum(WEIGHTS[k] for k in used)
    s = math.exp(sum(WEIGHTS[k] / wsum * math.log(v) for k, v in used.items()))
    return round(s, 1)


def score_sidecar(sc):
    """Fill sc['scores'] / sc['gate'] from a spec-§5.2 sidecar. Mutates and returns sc."""
    sc["gate"] = None
    sc["scores"] = None
    if not sc["boot"]["ok"]:
        sc["gate"] = "G1 broken: " + sc["boot"].get("failure_class", "no boot")
        return sc
    mem, gated = memory_axis({"main": sc["memory"]["main"]["dma_high_water"],
                              "vram": sc["memory"]["vram"]["peak"],
                              "aram": sc["memory"]["aram"]["peak"]})
    if mem is None:
        sc["gate"] = f"G3 memory: {gated} peak > 2x DC capacity"
        return sc
    ctrl = controls_axis(sc["controls"]["device_class"])
    if ctrl is None:
        sc["gate"] = "G2 controls: " + str(sc["controls"]["device_class"])
        return sc
    guts = None
    if sc["guts"]["dat_available"]:
        guts = guts_axis(set(sc["guts"]["flags"]), sc["guts"]["extra_bios_classes"])
    axes = {"memory": mem,
            "streaming": streaming_axis(sc["streaming"]["steady_mb_per_min"],
                                        sc["streaming"]["reread_ratio"]),
            "guts": guts,
            "controls": ctrl,
            "similarity": similarity_axis(sc["similarity"]["developer_match"],
                                          sc["similarity"]["sdk_overlap"],
                                          sc["similarity"]["cart_loader_match"])}
    f = final_score(axes)
    sc["scores"] = {k: (round(v, 1) if v is not None else None) for k, v in axes.items()}
    sc["scores"]["final"] = f
    sc["scores"]["tier"] = tier(f)
    return sc


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as fh:
        sc = json.load(fh)
    if sc.get("controls", {}).get("device_class") in (None, "review"):
        sys.exit(f"{sc.get('set')}: controls research required — set controls.device_class first")
    sc = score_sidecar(sc)
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    if sc["gate"]:
        print(sc["set"], "PARKED", sc["gate"])
    else:
        print(sc["set"], sc["scores"]["final"], sc["scores"]["tier"])
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python3 tools/assess/tests/test_score.py`
Expected: `ALL OK` (each `test_* OK` line printed)

- [ ] **Step 6: Commit**

```bash
git add .gitignore tools/assess/score.py tools/assess/tests/test_score.py
git commit -m "assess: score.py — spec §4 formulas + gates + tiers (anchor 91.8/S)"
```

---

### Task 2: `parse_capture.py` (cartlog → metrics fragment)

**Files:**
- Create: `tools/assess/parse_capture.py`
- Create: `tools/assess/tests/test_parse_capture.py`

**Interfaces:**
- Consumes: a cartlog text file (tags per the flycast fork: `CARTDMA src= dest= len=`, `WATERMARK region= used= size=`, `ARAMPROFILE high= nz= nz_below2m= nz_above2m=`, `VRAMPROFILE high= nz= nz_below8m= nz_above8m=`, `ARAMHANDOFF`/`VRAMHANDOFF`, `VRAMREGS …`, `SERIALPOKE …`; regexes adapted from `../cleopatra/scripts/parse_cart_log.py`) + optional timeline JSON `[[t_seconds, log_byte_size], …]` (written by Task 6's orchestrator every 10 s).
- Produces: `parse(text, timeline=None, handoff_window=120) -> dict` and CLI `python3 tools/assess/parse_capture.py <cartlog> [--timeline t.json]` printing that dict as JSON:

```json
{"handoff": {"seen": true, "t": 12.0, "aram_zeroed": true, "vram_zeroed": true},
 "main": {"dma_high_water": 0, "watermark_max": 0},
 "vram": {"peak": 0, "nz_above_cap": 0, "watermark_max": 0, "regs_last": ""},
 "aram": {"peak": 0, "nz_above_cap": 0, "watermark_max": 0},
 "streaming": {"dma_events": 0, "total_bytes": 0, "unique_bytes": 0, "reread_ratio": 0.0,
               "steady_mb_per_min": null, "short_window": true},
 "serial_pokes": 0, "boot_ok": false}
```

- [ ] **Step 1: Write the failing test**

`tools/assess/tests/test_parse_capture.py`:

```python
#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_parse_capture.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import parse_capture

# Synthetic capture: handoff at first CARTDMA; one re-read; one DMA outside main RAM.
LOG = (
    "WATERMARK region=main used=1fff60b size=2000000\n"      # stale-content scan: informational only
    "CARTDMA src=00010000 dest=0c020000 len=100000\n"        # handoff DMA, 1 MiB to main
    "ARAMHANDOFF zeroed size=800000\n"
    "VRAMHANDOFF zeroed size=1000000\n"
    "CARTDMA src=00200000 dest=0cb00000 len=80000\n"         # high-water: 0xb80000 above base
    "CARTDMA src=00200000 dest=0cb00000 len=80000\n"         # exact re-read (0x80000 re-bytes)
    "CARTDMA src=00300000 dest=10000000 len=1000\n"          # not main RAM: streams, no high-water
    "ARAMPROFILE high=200000 nz=1e0000 nz_below2m=1e0000 nz_above2m=0 size=800000\n"
    "VRAMPROFILE high=7cd7d5 nz=400000 nz_below8m=400000 nz_above8m=0 size=1000000\n"
    "VRAMREGS isp_base=0 isp_limit=0 ol_base=0 ol_limit=0 fb_w_sof1=0 fb_w_sof2=0 fb_r_sof1=0\n"
    "SERIALPOKE addr=ffe80000 data=00000041\n"
)
# Timeline: line offsets — first CARTDMA line ends within the first 10s sample.
def offsets():
    total, offs = 0, []
    for i, line in enumerate(LOG.splitlines(keepends=True)):
        total += len(line)
        offs.append(total)
    return offs

def test_parse():
    offs = offsets()
    # samples at t=10 (through line 2: handoff seen), t=200, t=360 (all bytes)
    timeline = [[10.0, offs[1]], [200.0, offs[6]], [360.0, offs[-1]]]
    m = parse_capture.parse(LOG, timeline=timeline)
    assert m["handoff"]["seen"] and m["handoff"]["aram_zeroed"] and m["handoff"]["vram_zeroed"]
    assert m["handoff"]["t"] == 10.0
    assert m["main"]["dma_high_water"] == 0x0cb80000 - 0x0c000000
    assert m["main"]["watermark_max"] == 0x1fff60b
    assert m["vram"]["peak"] == 0x7cd7d5 and m["vram"]["nz_above_cap"] == 0
    assert m["aram"]["peak"] == 0x200000 and m["aram"]["nz_above_cap"] == 0
    st = m["streaming"]
    assert st["dma_events"] == 4 and st["total_bytes"] == 0x100000 + 0x80000 + 0x80000 + 0x1000
    assert st["unique_bytes"] == 0x100000 + 0x80000 + 0x1000
    assert round(st["reread_ratio"], 4) == round(0x80000 / st["total_bytes"], 4)
    # steady window = t >= 10+120=130; only DMAs sampled after that fall in it. Events at
    # offsets <= offs[6] have t<=200... the window exists (360-130=230s >= 60) so not short.
    assert st["short_window"] is False and st["steady_mb_per_min"] is not None
    assert m["serial_pokes"] == 1
    assert m["boot_ok"] is True     # handoff seen + vram nz_below8m >= 0x10000

def test_no_timeline_no_boot():
    m = parse_capture.parse("WATERMARK region=main used=5 size=2000000\n")
    assert m["handoff"]["seen"] is False and m["boot_ok"] is False
    assert m["streaming"]["steady_mb_per_min"] is None and m["streaming"]["short_window"] is True

if __name__ == "__main__":
    test_parse(); print("test_parse OK")
    test_no_timeline_no_boot(); print("test_no_timeline_no_boot OK")
    print("ALL OK")
```

- [ ] **Step 2: Run to verify it fails** — `python3 tools/assess/tests/test_parse_capture.py` → `ModuleNotFoundError`

- [ ] **Step 3: Write `tools/assess/parse_capture.py`**

```python
#!/usr/bin/env python3
"""Instrumented-Flycast cartlog -> metrics fragment (JSON on stdout).
Regexes adapted from ../cleopatra/scripts/parse_cart_log.py (the Phase 2/3 parser).
The cartlog has no timestamps; time comes from the orchestrator's timeline file
([[t_seconds, log_byte_size], ...] sampled every ~10 s) via byte-offset lookup.
Usage: parse_capture.py <cartlog> [--timeline timeline.json] [--handoff-window 120]"""
import bisect, json, re, sys

MAIN_LO, MAIN_HI = 0x0c000000, 0x0e000000    # Naomi main-RAM physical window
_DMA = re.compile(r"^CARTDMA src=([0-9a-f]+) dest=([0-9a-f]+) len=([0-9a-f]+)", re.I)
_WM = re.compile(r"^WATERMARK region=(\w+) used=([0-9a-f]+) size=([0-9a-f]+)", re.I)
_APROF = re.compile(r"^ARAMPROFILE high=([0-9a-f]+) nz=[0-9a-f]+ nz_below2m=[0-9a-f]+ nz_above2m=([0-9a-f]+)", re.I)
_VPROF = re.compile(r"^VRAMPROFILE high=([0-9a-f]+) nz=[0-9a-f]+ nz_below8m=([0-9a-f]+) nz_above8m=([0-9a-f]+)", re.I)
_VREGS = re.compile(r"^VRAMREGS (.+)$")


def parse(text, timeline=None, handoff_window=120):
    ts = [t for t, _ in timeline] if timeline else []
    offs = [o for _, o in timeline] if timeline else []

    def t_of(byte_off):
        if not offs:
            return None
        i = bisect.bisect_left(offs, byte_off)
        return ts[i] if i < len(ts) else ts[-1]

    pos = 0
    handoff = {"seen": False, "t": None, "aram_zeroed": False, "vram_zeroed": False}
    wm = {}
    vram = {"peak": 0, "nz_above_cap": 0, "nz_below_max": 0, "regs_last": ""}
    aram = {"peak": 0, "nz_above_cap": 0}
    dmas = []           # (t, src, dest, length)
    serial = 0
    for line in text.splitlines(keepends=True):
        end = pos + len(line)
        s = line.rstrip("\n")
        m = _DMA.match(s)
        if m:
            src, dest, length = (int(g, 16) for g in m.groups())
            if not handoff["seen"]:
                handoff["seen"] = True
                handoff["t"] = t_of(end)
            dmas.append((t_of(end), src, dest, length))
        elif s.startswith("ARAMHANDOFF"):
            handoff["aram_zeroed"] = True
        elif s.startswith("VRAMHANDOFF"):
            handoff["vram_zeroed"] = True
        elif s.startswith("SERIALPOKE"):
            serial += 1
        else:
            m = _WM.match(s)
            if m:
                wm[m.group(1)] = max(wm.get(m.group(1), 0), int(m.group(2), 16))
            else:
                m = _APROF.match(s)
                if m:
                    aram["peak"] = max(aram["peak"], int(m.group(1), 16))
                    aram["nz_above_cap"] = max(aram["nz_above_cap"], int(m.group(2), 16))
                else:
                    m = _VPROF.match(s)
                    if m:
                        vram["peak"] = max(vram["peak"], int(m.group(1), 16))
                        vram["nz_below_max"] = max(vram["nz_below_max"], int(m.group(2), 16))
                        vram["nz_above_cap"] = max(vram["nz_above_cap"], int(m.group(3), 16))
                    else:
                        m = _VREGS.match(s)
                        if m:
                            vram["regs_last"] = m.group(1)
        pos = end

    main_hw = max((dest + n - MAIN_LO for _, _, dest, n in dmas if MAIN_LO <= dest < MAIN_HI),
                  default=0)
    total = sum(n for _, _, _, n in dmas)
    seen, unique = set(), 0
    for _, src, _, n in dmas:
        if (src, n) not in seen:            # ponytail: overlap-blind unique sum; exact interval
            seen.add((src, n))              # union not needed at MB/min granularity
            unique += n
    reread = (total - unique) / total if total else 0.0

    steady, short_window = None, True
    if handoff["t"] is not None and ts:
        w0 = handoff["t"] + handoff_window
        dur = ts[-1] - w0
        if dur >= 60:
            in_w = sum(n for t, _, _, n in dmas if t is not None and t >= w0)
            steady = round(in_w / (1 << 20) / (dur / 60.0), 3)
            short_window = False
        elif ts[-1] > handoff["t"]:
            # run too short for a clean window: fall back to whole post-handoff rate, flagged
            dur = ts[-1] - handoff["t"]
            in_w = sum(n for t, _, _, n in dmas if t is not None and t >= handoff["t"])
            steady = round(in_w / (1 << 20) / (dur / 60.0), 3)

    return {
        "handoff": handoff,
        "main": {"dma_high_water": main_hw, "watermark_max": wm.get("main", 0)},
        "vram": {"peak": vram["peak"], "nz_above_cap": vram["nz_above_cap"],
                 "watermark_max": wm.get("vram", 0), "regs_last": vram["regs_last"]},
        "aram": {"peak": aram["peak"], "nz_above_cap": aram["nz_above_cap"],
                 "watermark_max": wm.get("aram", 0)},
        "streaming": {"dma_events": len(dmas), "total_bytes": total, "unique_bytes": unique,
                      "reread_ratio": round(reread, 4), "steady_mb_per_min": steady,
                      "short_window": short_window},
        "serial_pokes": serial,
        "boot_ok": bool(handoff["seen"] and vram["nz_below_max"] >= 0x10000),
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    tl = None
    if "--timeline" in args:
        i = args.index("--timeline")
        with open(args[i + 1]) as fh:
            tl = json.load(fh)
        del args[i:i + 2]
    with open(args[0]) as fh:
        print(json.dumps(parse(fh.read(), timeline=tl), indent=2))
```

- [ ] **Step 4: Run to verify it passes** — `python3 tools/assess/tests/test_parse_capture.py` → `ALL OK`

- [ ] **Step 5: Commit**

```bash
git add tools/assess/parse_capture.py tools/assess/tests/test_parse_capture.py
git commit -m "assess: parse_capture.py — cartlog + timeline -> metrics fragment"
```

---

### Task 3: `controls_extract.py` (MAME → identity/input JSON)

**Files:**
- Create: `tools/assess/controls_extract.py`
- Create: `tools/assess/tests/test_controls_extract.py`

**Interfaces:**
- Consumes: `../cleopatra/tools/mame/src/mame/sega/naomi.cpp` (override with env `MAME_NAOMI`).
- Produces: CLI `python3 tools/assess/controls_extract.py > tools/assess/out/controls.json` — a dict `{set: {"year", "parent" (str|null), "machine", "input_ports", "maker", "title", "not_working" (bool), "device_class_hint"}}`, BIOS-root entries excluded. Task 6 reads one row per set; Task 11's queue uses `parent`.

- [ ] **Step 1: Write the failing test**

`tools/assess/tests/test_controls_extract.py`:

```python
#!/usr/bin/env python3
"""Integration test against the pinned local MAME checkout (commit 59e7c0b).
Run: python3 tools/assess/tests/test_controls_extract.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import controls_extract as ce

def test_real_file():
    path = ce.default_mame_path()
    assert os.path.isfile(path), f"pinned MAME source missing: {path}"
    rows = ce.extract(open(path, encoding="utf-8", errors="replace").read())
    assert "naomi" not in rows                      # BIOS roots excluded
    assert rows["cleoftp"]["maker"].startswith("Taito")
    assert rows["cleoftp"]["parent"] is None        # parent set
    assert rows["ikaruga"]["maker"] == "Treasure"
    assert rows["cvs2mf"]["parent"] == "cvs2"       # clone linkage
    assert len(rows) >= 140                          # the Naomi library
    assert all("device_class_hint" in r for r in rows.values())

if __name__ == "__main__":
    test_real_file(); print("test_real_file OK"); print("ALL OK")
```

- [ ] **Step 2: Run to verify it fails** — `ModuleNotFoundError`

- [ ] **Step 3: List the actual INPUT_PORTS names, then write the tool**

First enumerate the port definitions to fill the hints table with real names:

Run: `grep -o 'INPUT_PORTS_START( *[a-z0-9_]*' ../cleopatra/tools/mame/src/mame/sega/naomi.cpp`

Write `tools/assess/controls_extract.py` — complete `DEVICE_HINTS` with every name that grep printed, using this rubric (spec §4.4 ladder): joystick/button panels → `"stick"`; light-gun ports → `"dc_peripheral"` (DC light gun exists); fishing rod / keyboard / maracas / twin-stick / wheel → `"dc_peripheral"`; mahjong panels → `"pad_adaptable"`; anything card/medal/hopper-flavoured → `"card_reader"` (not on the ladder ⇒ score.py gates G2); a name you cannot classify from the port definition → `"review"` (forces the assessing agent to research before scoring — score.py refuses to score `review`):

```python
#!/usr/bin/env python3
"""Parse MAME's naomi.cpp GAME() rows -> per-set identity/input JSON on stdout.
Pinned source: ../cleopatra/tools/mame (commit 59e7c0b). Override: env MAME_NAOMI."""
import json, os, re, sys

# GAME( 1999, set, parent, machine, input, class, init, rot, "Maker", "Title", flags )
_GAME = re.compile(
    r'GAME\(\s*(\d{4}),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*\w+,\s*\w+,\s*\w+,\s*'
    r'"([^"]*)",\s*"([^"]*)",\s*([^)]*)\)')

# INPUT_PORTS name -> spec §4.4 ladder class. Filled from:
#   grep -o 'INPUT_PORTS_START( *[a-z0-9_]*' naomi.cpp
# "review" = hint unknown; the assessing agent must research + set the class by hand.
DEVICE_HINTS = {
    "naomi": "stick",
    "hotd2": "dc_peripheral",        # light gun — DC gun exists
    # ... one line per INPUT_PORTS_START name from the grep above, classified per rubric ...
}


def default_mame_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.environ.get("MAME_NAOMI", os.path.normpath(os.path.join(
        here, "../../../..", "cleopatra/tools/mame/src/mame/sega/naomi.cpp")))


def extract(text):
    rows = {}
    for m in _GAME.finditer(text):
        year, setname, parent, machine, inp, maker, title, flags = m.groups()
        if "MACHINE_IS_BIOS_ROOT" in flags:
            continue
        rows[setname] = {
            "year": year,
            "parent": None if parent == "0" else parent,
            "machine": machine,
            "input_ports": inp,
            "maker": maker,
            "title": title,
            "not_working": "MACHINE_NOT_WORKING" in flags,
            "device_class_hint": DEVICE_HINTS.get(inp, "review"),
        }
    return rows


if __name__ == "__main__":
    with open(default_mame_path(), encoding="utf-8", errors="replace") as fh:
        print(json.dumps(extract(fh.read()), indent=2, sort_keys=True))
```

- [ ] **Step 4: Run to verify it passes** — `python3 tools/assess/tests/test_controls_extract.py` → `ALL OK`. If `_GAME` misses rows (multi-line GAME entries), extend the regex with `re.S` and `\s*` liberally until the count assertion passes — the source is the pinned checkout, so this converges once.

- [ ] **Step 5: Generate the artifact and eyeball it**

Run: `mkdir -p tools/assess/out && python3 tools/assess/controls_extract.py > tools/assess/out/controls.json && python3 -c "import json;d=json.load(open('tools/assess/out/controls.json'));print(len(d),'sets');print(d['cleoftp'])"`
Expected: ≥140 sets; cleoftp row sane.

- [ ] **Step 6: Commit**

```bash
git add tools/assess/controls_extract.py tools/assess/tests/test_controls_extract.py
git commit -m "assess: controls_extract.py — MAME GAME rows -> identity/input JSON"
```

---

### Task 4: `carve_boot.py` (.dat → Ghidra-loadable boot image)

**Files:**
- Create: `tools/assess/carve_boot.py`
- Create: `tools/assess/tests/test_carve_boot.py`

**Interfaces:**
- Consumes: a `.dat` (NAOMI header at offset 0 or 0x800000; field offsets per `../cleopatra/scripts/parse_header.py`, cross-checked against DragonMinded's netboot `rom.py`: main load entries at hdr+0x360 (8 × `<III` rom,ram,len; stop on 0xFFFFFFFF or all-zero), entrypoints at hdr+0x420).
- Produces: `carve(data: bytes) -> (blob: bytes, meta: dict)` with `meta = {"base": "0x8c020000", "entry": "0x…", "size": n, "entries": [[rom, ram, len], …], "hdr_at": 0|0x800000, "title": str}`; CLI `python3 tools/assess/carve_boot.py <dat> <outstem>` writing `<outstem>.boot.bin` + `<outstem>.meta.json`. Task 5 imports the blob at `meta["base"]`.

- [ ] **Step 1: Write the failing test** (synthetic image)

`tools/assess/tests/test_carve_boot.py`:

```python
#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_carve_boot.py"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import carve_boot

def synth(hdr_at=0):
    img = bytearray(hdr_at + 0x2000)
    img[hdr_at:hdr_at + 5] = b"NAOMI"
    img[hdr_at + 0x30:hdr_at + 0x36] = b"TESTGM"                      # Japan title
    # two load entries: rom -> ram (absolute file offsets for rom)
    struct.pack_into("<III", img, hdr_at + 0x360, hdr_at + 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<III", img, hdr_at + 0x360 + 12, hdr_at + 0x1800, 0x8c020200, 0x80)
    struct.pack_into("<I", img, hdr_at + 0x360 + 24, 0xFFFFFFFF)      # terminator
    struct.pack_into("<II", img, hdr_at + 0x420, 0x8c020000, 0x8c020100)
    img[hdr_at + 0x1000:hdr_at + 0x1100] = b"A" * 0x100
    img[hdr_at + 0x1800:hdr_at + 0x1880] = b"B" * 0x80
    return bytes(img)

def test_carve_at_0():
    blob, meta = carve_boot.carve(synth(0))
    assert meta["hdr_at"] == 0 and meta["title"] == "TESTGM"
    assert meta["base"] == "0x8c020000" and meta["entry"] == "0x8c020000"
    assert len(blob) == 0x280                       # span 0x8c020000..0x8c020280
    assert blob[0:0x100] == b"A" * 0x100
    assert blob[0x100:0x200] == b"\x00" * 0x100     # gap zero-filled
    assert blob[0x200:0x280] == b"B" * 0x80

def test_carve_at_800000():
    blob, meta = carve_boot.carve(synth(0x800000))
    assert meta["hdr_at"] == 0x800000 and blob[0:0x100] == b"A" * 0x100

if __name__ == "__main__":
    test_carve_at_0(); print("test_carve_at_0 OK")
    test_carve_at_800000(); print("test_carve_at_800000 OK")
    print("ALL OK")
```

- [ ] **Step 2: Run to verify it fails** — `ModuleNotFoundError`

- [ ] **Step 3: Write `tools/assess/carve_boot.py`**

```python
#!/usr/bin/env python3
"""Carve a Naomi .dat's main load image into one Ghidra-loadable blob.
Header layout per ../cleopatra/scripts/parse_header.py (netboot rom.py cross-check):
magic@hdr+0, Japan title@hdr+0x30, main load entries@hdr+0x360, entrypoints@hdr+0x420.
ROM offsets are absolute file offsets; if an entry runs past EOF we retry hdr-relative
(GD .dat images place the header at 0x800000).
Usage: carve_boot.py <dat> <outstem>   -> <outstem>.boot.bin + <outstem>.meta.json"""
import json, struct, sys


def _entries(data, hdr):
    out = []
    for i in range(8):
        rom, ram, n = struct.unpack_from("<III", data, hdr + 0x360 + 12 * i)
        if rom == 0xFFFFFFFF or (rom == 0 and n == 0):
            break
        out.append((rom, ram, n))
    return out


def carve(data):
    hdr = 0 if data[0:5] == b"NAOMI" else 0x800000
    if data[hdr:hdr + 5] != b"NAOMI":
        raise ValueError("no NAOMI header at 0 or 0x800000")
    title = data[hdr + 0x30:hdr + 0x50].decode("ascii", "replace").rstrip("\x00 ")
    entries = _entries(data, hdr)
    if not entries:
        raise ValueError("no main load entries")
    fixed = []
    for rom, ram, n in entries:
        if rom + n > len(data) and hdr + rom + n <= len(data):
            rom = hdr + rom                       # hdr-relative fallback
        if rom + n > len(data):
            raise ValueError(f"load entry out of file: rom=0x{rom:x} len=0x{n:x}")
        fixed.append((rom, ram, n))
    base = min(ram for _, ram, _ in fixed)
    top = max(ram + n for _, ram, n in fixed)
    blob = bytearray(top - base)
    for rom, ram, n in fixed:
        blob[ram - base:ram - base + n] = data[rom:rom + n]
    entry, _test_ep = struct.unpack_from("<II", data, hdr + 0x420)
    meta = {"base": f"0x{base:08x}", "entry": f"0x{entry:08x}", "size": len(blob),
            "entries": [[r, m, n] for r, m, n in fixed], "hdr_at": hdr, "title": title}
    return bytes(blob), meta


if __name__ == "__main__":
    dat, stem = sys.argv[1], sys.argv[2]
    with open(dat, "rb") as fh:
        blob, meta = carve(fh.read())
    with open(stem + ".boot.bin", "wb") as fh:
        fh.write(blob)
    with open(stem + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(f"OK {meta['title']} base={meta['base']} entry={meta['entry']} size=0x{meta['size']:x}")
```

- [ ] **Step 4: Run to verify it passes** — `python3 tools/assess/tests/test_carve_boot.py` → `ALL OK`

- [ ] **Step 5: Commit**

```bash
git add tools/assess/carve_boot.py tools/assess/tests/test_carve_boot.py
git commit -m "assess: carve_boot.py — .dat main load entries -> Ghidra blob + meta"
```

---

### Task 5: Headless Ghidra guts metrics

**Files:**
- Create: `tools/assess/ghidra/run_guts.sh`
- Create: `tools/assess/ghidra/GutsMetrics.java`

**Interfaces:**
- Consumes: `<set>.boot.bin` + base address from Task 4's meta; Ghidra 12.1.2 at `../cleopatra/tools/ghidra_12.1.2_PUBLIC` (override env `GHIDRA_HOME`); import invocation cribbed from `../cleopatra/scripts/ghidra/run.sh`.
- Produces: `sh tools/assess/ghidra/run_guts.sh <boot.bin> <base-hex> <out.json>` → JSON `{"code_bytes": n, "functions": n, "mmio_refs": {"scif": n, "rtc": n, "g2ext": n}, "bios_refs": {"0x8c0000b0": n, …}, "sdk_strings": [str, …]}`. Task 6 maps these to guts flags.

- [ ] **Step 1: Cross-check the BIOS vector list**

Read `../cleopatra/docs/kb/boot-binary.md` and list the Naomi BIOS entry addresses it documents (the boot/EEPROM syscall vectors). Update the `BIOS_VEC` array below if that doc names vectors beyond the defaults `0x8c0000b0, 0x8c0000b8, 0x8c0000bc, 0x8c0000c0, 0x8c0000e0`. Cite the kb section in a comment.

- [ ] **Step 2: Write `tools/assess/ghidra/GutsMetrics.java`**

```java
// GutsMetrics.java — Ghidra post-script: guts metrics for one Naomi boot image.
// args[0] = output JSON path. Ghidra 12.1.2 headless (Jython is gone; Java only).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.scalar.Scalar;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class GutsMetrics extends GhidraScript {
    // {lo, hi} physical (addr & 0x1FFFFFFF). SCIF = SH4 on-chip serial 0xFFE8xxxx.
    static final long[][] MMIO = {
        {0x00710000L, 0x0071FFFFL},   // rtc: AICA RTC registers
        {0x01000000L, 0x01FFFFFFL},   // g2ext: G2 add-on board window (DIMM/net) — informational
        {0x1FE80000L, 0x1FE8FFFFL},   // scif
    };
    static final String[] MMIO_NAMES = {"rtc", "g2ext", "scif"};
    // Naomi BIOS syscall vectors — cross-checked against ../cleopatra/docs/kb/boot-binary.md
    static final long[] BIOS_VEC = {0x8c0000b0L, 0x8c0000b8L, 0x8c0000bcL, 0x8c0000c0L, 0x8c0000e0L};

    Map<String, Integer> mmio = new LinkedHashMap<>();
    Map<String, Integer> bios = new LinkedHashMap<>();

    void tally(long v) {
        long p = v & 0x1FFFFFFFL;
        for (int i = 0; i < MMIO.length; i++)
            if (p >= MMIO[i][0] && p <= MMIO[i][1])
                mmio.merge(MMIO_NAMES[i], 1, Integer::sum);
        for (long vec : BIOS_VEC)
            if (v == vec || p == (vec & 0x1FFFFFFFL))
                bios.merge(String.format("0x%08x", vec), 1, Integer::sum);
    }

    static String esc(String s) {
        StringBuilder b = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '"' || c == '\\') b.append('\\').append(c);
            else if (c >= 0x20 && c < 0x7f) b.append(c);
        }
        return b.toString();
    }

    @Override
    public void run() throws Exception {
        for (String n : MMIO_NAMES) mmio.put(n, 0);
        long codeBytes = 0;
        for (MemoryBlock b : currentProgram.getMemory().getBlocks())
            if (b.isInitialized()) codeBytes += b.getSize();
        int functions = currentProgram.getFunctionManager().getFunctionCount();

        InstructionIterator it = currentProgram.getListing().getInstructions(true);
        while (it.hasNext() && !monitor.isCancelled()) {
            Instruction ins = it.next();
            for (int op = 0; op < ins.getNumOperands(); op++)
                for (Object o : ins.getOpObjects(op))
                    if (o instanceof Scalar) tally(((Scalar) o).getUnsignedValue());
        }
        // SH4 reaches MMIO via literal pools -> defined 4-byte data and pointers
        List<String> strs = new ArrayList<>();
        DataIterator dit = currentProgram.getListing().getDefinedData(true);
        while (dit.hasNext() && !monitor.isCancelled()) {
            Data d = dit.next();
            Object v = d.getValue();
            if (d.getLength() == 4 && v instanceof Scalar)
                tally(((Scalar) v).getUnsignedValue());
            else if (v instanceof ghidra.program.model.address.Address)
                tally(((ghidra.program.model.address.Address) v).getOffset());
            else if (d.hasStringValue() && strs.size() < 500) {
                String s = d.getDefaultValueRepresentation();
                if (s.length() >= 10) strs.add(esc(s));
            }
        }

        try (PrintWriter w = new PrintWriter(getScriptArgs()[0])) {
            w.printf("{\"code_bytes\": %d, \"functions\": %d,%n", codeBytes, functions);
            w.print("\"mmio_refs\": {");
            boolean first = true;
            for (Map.Entry<String, Integer> e : mmio.entrySet()) {
                if (!first) w.print(", ");
                w.printf("\"%s\": %d", e.getKey(), e.getValue()); first = false;
            }
            w.print("},%n\"bios_refs\": {".replace("%n", System.lineSeparator()));
            first = true;
            for (Map.Entry<String, Integer> e : bios.entrySet()) {
                if (!first) w.print(", ");
                w.printf("\"%s\": %d", e.getKey(), e.getValue()); first = false;
            }
            w.print("},");
            w.println();
            w.print("\"sdk_strings\": [");
            for (int i = 0; i < strs.size(); i++)
                w.printf("%s\"%s\"", i == 0 ? "" : ", ", strs.get(i));
            w.println("]}");
        }
        println("GutsMetrics: wrote " + getScriptArgs()[0]);
    }
}
```

- [ ] **Step 3: Write `tools/assess/ghidra/run_guts.sh`**

```sh
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
```

Then: `chmod +x tools/assess/ghidra/run_guts.sh`

- [ ] **Step 4: Smoke-test on the Cleopatra .dat (real end-to-end check)**

```bash
cd tools/dat-extract && ./chd2dat.sh cleoftp && cd ../..
python3 tools/assess/carve_boot.py tools/dat-extract/out/cleoftp.dat tools/assess/out/cleoftp
sh tools/assess/ghidra/run_guts.sh tools/assess/out/cleoftp.boot.bin \
   $(python3 -c "import json;print(json.load(open('tools/assess/out/cleoftp.meta.json'))['base'])") \
   tools/assess/out/cleoftp.guts.json
python3 -c "import json; g=json.load(open('tools/assess/out/cleoftp.guts.json')); print(g['functions'], g['code_bytes'], g['mmio_refs'])"
```

Expected: valid JSON; `functions` > 100; `code_bytes` ≈ 1 MB; `mmio_refs.scif` ≥ 1 (this game pokes serial — `phase2-measurements.md`). Also compare the carve against the known-good slice: `cmp tools/assess/out/cleoftp.boot.bin ../cleopatra/tools/boot.bin && echo IDENTICAL` — if not identical, diff sizes: cleopatra's `boot.bin` may be a first-entry-only slice; identical prefix (`cmp -n <cleopatra-size> …`) is acceptable, document which. Fix Java compile errors by iterating (analyzeHeadless prints javac output). Keep the `.dat` for Task 9; the carved bin stays in gitignored `out/`.

- [ ] **Step 5: Commit**

```bash
git add tools/assess/ghidra/run_guts.sh tools/assess/ghidra/GutsMetrics.java
git commit -m "assess: headless Ghidra guts metrics (code size, MMIO/BIOS refs, SDK strings)"
```

---

### Task 6: `run_battery.py` (orchestrator)

**Files:**
- Create: `tools/assess/run_battery.py`

**Interfaces:**
- Consumes: everything above — `parse_capture.parse`, `carve_boot`, `run_guts.sh`, `score.score_sidecar`, `tools/assess/out/controls.json`, the flycast binary, `naomi/<set>.zip` / `naomi/<set>/*.chd`, `tools/dat-extract/{chd2dat.sh,cart2dat.py}`, optional `assessments/reference/similarity-reference.json`.
- Produces: CLI `python3 tools/assess/run_battery.py <set> [--secs 360] [--skip-static] [--keep-dat] [--rom <path>]` → writes `assessments/<set>.metrics.json` (spec §5.2 shape — exactly the dict `score_sidecar` consumes, plus `versions`, `params`, `capture`, identity fields), `assessments/evidence/<set>/shot-*.png`, `assessments/evidence/<set>/raw/{cartlog.txt,timeline.json,stdout.log}`. Prints one verdict line. Exit 0 even when parked (parking is a result); exit ≠0 only on tooling failure.

- [ ] **Step 1: Write `tools/assess/run_battery.py`**

```python
#!/usr/bin/env python3
"""One-family assessment battery (spec §2). SERIAL ONLY — never run two at once.
Usage: run_battery.py <set> [--secs 360] [--skip-static] [--keep-dat] [--rom PATH]
Env overrides: FLYCAST_BIN, NAOMI_DIR, MAME_NAOMI."""
import glob, json, os, shutil, signal, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import carve_boot, parse_capture, score  # noqa: E402

NAOMI = os.environ.get("NAOMI_DIR", os.path.join(REPO, "naomi"))
CLEO = os.path.normpath(os.path.join(REPO, "..", "cleopatra"))
BIN = os.environ.get("FLYCAST_BIN", os.path.join(
    CLEO, "tools/flycast-src/build/Flycast.app/Contents/MacOS/Flycast"))
ASSESS = os.path.join(REPO, "assessments")
OUT = os.path.join(HERE, "out")
BATTERY_VERSION = "1"
HANDOFF_TAGS = (b"ARAMHANDOFF", b"CARTDMA")
# Sets whose disc/feature set is network-bound (netpic/WCCF/satellite — GAME_FORMATS.md
# Completeness section). Drives the guts 'network' penalty (spec §4.3).
NETWORK_SETS = {"wccf116", "wccf1dup", "wccf212e", "wccf234j", "wccf310j", "wccf322e",
                "wccf341j", "wccf331e", "wccf331j", "dragntr", "dragntra", "dragntr2",
                "dragntr3", "quizqgd"}


def rom_candidates(setname):
    cands = []
    z = os.path.join(NAOMI, setname + ".zip")
    if os.path.isfile(z):
        cands.append(z)
    cands += sorted(glob.glob(os.path.join(NAOMI, setname, "*.chd")))
    return cands


def flycast_commit():
    try:
        return subprocess.run(["git", "-C", os.path.join(CLEO, "tools/flycast-src"),
                               "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        return "unknown"


def handoff_seen(logpath):
    try:
        with open(logpath, "rb") as fh:
            data = fh.read()
        return any(t in data for t in HANDOFF_TAGS)
    except OSError:
        return False


def capture(setname, rom, secs):
    ev = os.path.join(ASSESS, "evidence", setname)
    raw = os.path.join(ev, "raw")
    os.makedirs(raw, exist_ok=True)
    log = os.path.join(raw, "cartlog.txt")
    shot = os.path.join(raw, "shot.png")
    for p in (log, shot):
        if os.path.exists(p):
            os.remove(p)
    # macOS: suppress the "reopen windows?" modal that blocks boot after a killed run
    # (root-caused in ../cleopatra/scripts/capture.sh)
    for k, v in (("ApplePersistenceIgnoreState", "YES"), ("NSQuitAlwaysKeepsWindows", "false")):
        subprocess.run(["defaults", "write", "com.flyinghead.Flycast", k, "-bool", v],
                       check=False, capture_output=True)
    env = dict(os.environ, FLYCAST_CARTLOG=log, FLYCAST_SHOT=shot, FLYCAST_SHOT_EVERY="300")
    with open(os.path.join(raw, "stdout.log"), "wb") as so:
        # vsync off so the emu thread doesn't deadlock unfocused (capture.sh finding)
        p = subprocess.Popen([BIN, "-config", "config:rend.vsync=no", rom],
                             env=env, stdout=so, stderr=subprocess.STDOUT)
    t0 = time.time()
    timeline, next_shot, shots, aborted = [], 60, [], None
    while True:
        time.sleep(10)
        t = round(time.time() - t0, 1)
        size = os.path.getsize(log) if os.path.exists(log) else 0
        timeline.append([t, size])
        if t >= next_shot and p.poll() is None:
            os.kill(p.pid, signal.SIGUSR1)
            time.sleep(1)                       # copy-then-open: fwrite isn't atomic
            if os.path.exists(shot):
                dst = os.path.join(ev, f"shot-{int(t):03d}s.png")
                shutil.copyfile(shot, dst)
                shots.append(os.path.relpath(dst, REPO))
            next_shot += 60
        if p.poll() is not None:
            aborted = "emulator-exited"
            break
        if t >= 120 and not handoff_seen(log):
            aborted = "no-handoff-120s"          # spec §2 early abort
            break
        if t >= secs:
            break
    if p.poll() is None:
        p.terminate()
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            p.kill()
    with open(os.path.join(raw, "timeline.json"), "w") as fh:
        json.dump(timeline, fh)
    return log, timeline, shots, aborted


def static_scan(setname, keep_dat):
    de = os.path.join(REPO, "tools", "dat-extract")
    is_gd = bool(glob.glob(os.path.join(NAOMI, setname, "*.chd")) or
                 glob.glob(os.path.join(NAOMI, "*", setname + "*.chd")))
    cmd = ["./chd2dat.sh", setname] if is_gd else ["python3", "cart2dat.py", setname]
    r = subprocess.run(cmd, cwd=de, capture_output=True, text=True)
    dat = os.path.join(de, "out", setname + ".dat")
    if r.returncode != 0 or not os.path.isfile(dat):
        return {"dat_available": False, "error": (r.stdout + r.stderr)[-500:]}
    try:
        stem = os.path.join(OUT, setname)
        os.makedirs(OUT, exist_ok=True)
        with open(dat, "rb") as fh:
            blob, meta = carve_boot.carve(fh.read())
        with open(stem + ".boot.bin", "wb") as fh:
            fh.write(blob)
        guts_json = stem + ".guts.json"
        g = subprocess.run(["sh", os.path.join(HERE, "ghidra", "run_guts.sh"),
                            stem + ".boot.bin", meta["base"], guts_json],
                           capture_output=True, text=True)
        if g.returncode != 0 or not os.path.isfile(guts_json):
            return {"dat_available": False, "error": "ghidra: " + (g.stdout + g.stderr)[-500:]}
        with open(guts_json) as fh:
            guts = json.load(fh)
        guts["dat_available"] = True
        guts["carve_meta"] = meta
        return guts
    finally:
        if not keep_dat:
            for p in (dat, os.path.join(OUT, setname + ".boot.bin")):
                if os.path.exists(p):
                    os.remove(p)                 # SSD hygiene + never keep decrypted dumps


def guts_flags(setname, guts, serial_pokes):
    flags = ["eeprom_bios"]                      # every Naomi game reads settings via BIOS
    if serial_pokes > 0 or guts.get("mmio_refs", {}).get("scif", 0) > 0:
        flags.append("serial")
    if guts.get("mmio_refs", {}).get("rtc", 0) > 0:
        flags.append("rtc")
    if setname in NETWORK_SETS:
        flags.append("network")
    if guts.get("code_bytes", 0) > 4 << 20:
        flags.append("code_over_4mb")
    extra = max(0, sum(1 for v in guts.get("bios_refs", {}).values() if v) - 2)
    return flags, extra


def similarity(row, fmt, guts):
    ref_path = os.path.join(ASSESS, "reference", "similarity-reference.json")
    if not os.path.isfile(ref_path):
        return {"developer_match": False, "sdk_overlap": "none", "cart_loader_match": False,
                "note": "no reference yet (pre-calibration)"}
    with open(ref_path) as fh:
        ref = json.load(fh)
    ours = set(guts.get("sdk_strings", []))
    theirs = set(ref["sdk_strings"])
    overlap = "full" if theirs and theirs <= ours else ("partial" if ours & theirs else "none")
    return {"developer_match": row["maker"] in ref["makers"],
            "sdk_overlap": overlap,
            "cart_loader_match": fmt == ref["format"] and guts.get("dat_available", False)}


def main():
    args = sys.argv[1:]
    setname = args[0]
    secs = int(args[args.index("--secs") + 1]) if "--secs" in args else 360
    skip_static = "--skip-static" in args
    keep_dat = "--keep-dat" in args
    rom = args[args.index("--rom") + 1] if "--rom" in args else None

    with open(os.path.join(OUT, "controls.json")) as fh:
        controls = json.load(fh)
    row = controls[setname]
    cands = [rom] if rom else rom_candidates(setname)
    if not cands:
        sys.exit(f"no rom for {setname} under {NAOMI}")
    fmt = "GD-ROM" if any(c.endswith(".chd") for c in rom_candidates(setname)) else "cart"

    log = timeline = shots = None
    aborted, rom_used = "no-candidates", None
    for cand in cands:
        log, timeline, shots, aborted = capture(setname, cand, secs)
        rom_used = cand
        if aborted is None:                      # clean full run; else try the next launch file
            break                                # (zip may show BIOS-only for GD sets — chd next)

    with open(log) as fh:
        cap = parse_capture.parse(fh.read(), timeline=timeline)

    boot_ok = cap["boot_ok"] and aborted is None
    guts = {"dat_available": False, "error": "skipped (--skip-static or no boot)"}
    if boot_ok and not skip_static:
        guts = static_scan(setname, keep_dat)
    flags, extra = guts_flags(setname, guts, cap["serial_pokes"])

    sc = {
        "set": setname, "title": row["title"], "maker": row["maker"], "year": row["year"],
        "format": fmt, "assessed": time.strftime("%Y-%m-%d"),
        "versions": {"flycast": flycast_commit(), "battery": BATTERY_VERSION,
                     "ghidra": "12.1.2_PUBLIC", "mame_src": "59e7c0b"},
        "params": {"capture_s": secs, "steady_after_s": 120, "shot_interval_s": 60,
                   "boot_timeout_s": 120, "rom_used": os.path.relpath(rom_used, REPO)},
        "boot": {"ok": boot_ok,
                 "failure_class": aborted if not boot_ok else None,
                 "mame_not_working": row["not_working"]},
        "capture": {"handoff": cap["handoff"], "screenshots": shots,
                    "watermarks_info": {r: cap[r]["watermark_max"] for r in ("main", "vram", "aram")}},
        "memory": {"main": {"dma_high_water": cap["main"]["dma_high_water"]},
                   "vram": {"peak": cap["vram"]["peak"], "nz_above_cap": cap["vram"]["nz_above_cap"],
                            "regs_last": cap["vram"]["regs_last"]},
                   "aram": {"peak": cap["aram"]["peak"], "nz_above_cap": cap["aram"]["nz_above_cap"]}},
        "streaming": dict(cap["streaming"]),
        "guts": {**{k: v for k, v in guts.items() if k != "sdk_strings"},
                 "flags": flags, "extra_bios_classes": extra,
                 "sdk_strings": guts.get("sdk_strings", [])},
        "serial_pokes": cap["serial_pokes"],
        "controls": {"device_class": row["device_class_hint"], "input_ports": row["input_ports"],
                     "sources": [f"MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS "
                                 f"'{row['input_ports']}'"]},
        "similarity": similarity(row, fmt, guts),
    }
    if sc["controls"]["device_class"] == "review":
        sc["gate"] = None
        sc["scores"] = None
        verdict = "UNSCORED (controls research required — set device_class, rerun score.py)"
    else:
        score.score_sidecar(sc)
        verdict = (f"PARKED {sc['gate']}" if sc["gate"]
                   else f"{sc['scores']['final']} {sc['scores']['tier']}")
    path = os.path.join(ASSESS, setname + ".metrics.json")
    with open(path, "w") as fh:
        json.dump(sc, fh, indent=2)
    print(f"{setname}: {verdict}  -> {os.path.relpath(path, REPO)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Sanity-check the glue without an emulator run**

Run: `python3 -c "import sys; sys.path.insert(0,'tools/assess'); import run_battery; print(run_battery.rom_candidates('cleoftp')); print(run_battery.flycast_commit())"`
Expected: a non-empty candidate list (`naomi/cleoftp.zip` first) and a short commit hash. Real end-to-end exercise is Task 9 (calibration) — that is this task's true test.

- [ ] **Step 3: Commit**

```bash
git add tools/assess/run_battery.py
git commit -m "assess: run_battery.py — per-family orchestrator (capture->parse->static->score->sidecar)"
```

---

### Task 7: `gen_tables.py` (QUEUE / RANKING / GAME_FORMATS patch)

**Files:**
- Create: `tools/assess/gen_tables.py`
- Create: `tools/assess/tests/test_gen_tables.py`

**Interfaces:**
- Consumes: `GAME_FORMATS.md` per-set table rows (8 cells: `| Title | \`set\` | Format | parent/clone of \`x\` | Size | Genre | DC port | status |`), `tools/assess/out/controls.json`, `assessments/*.metrics.json`.
- Produces: CLI `python3 tools/assess/gen_tables.py queue|ranking|patch`. `queue` writes `assessments/QUEUE.md` (refuses if it exists — hand-curated after birth; `--force` overrides). `ranking` rewrites `assessments/RANKING.md`. `patch` rewrites only the 8th cell of matching `GAME_FORMATS.md` rows.

- [ ] **Step 1: Write the failing test**

`tools/assess/tests/test_gen_tables.py`:

```python
#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_gen_tables.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gen_tables as gt

FIXTURE = """| Some Game (GDL-1) | `aaa` | **GD-ROM** | parent | 10 MB | Puzzle ★ | No | not assessed |
| Some Game (Japan) (GDL-1J) | `aaaj` | **GD-ROM** | clone of `aaa` | 10 MB | Puzzle ★ | No | not assessed |
| Ported Game (GDL-2) | `bbb` | **GD-ROM** | parent | 20 MB | Fighting | Yes (2001) | not assessed |
| Ported Clone (GDL-2J) | `bbbj` | **GD-ROM** | clone of `bbb` | 20 MB | Fighting | No | not assessed |
| Cleopatra Fortune Plus (GDL-0012) | `cleoftp` | **GD-ROM** | parent | 65.8 MB | Puzzle ★ | No | not assessed |
"""

def test_parse_rows():
    rows = gt.parse_rows(FIXTURE)
    assert rows["aaa"]["parent"] is None and rows["aaaj"]["parent"] == "aaa"
    assert rows["bbb"]["dc_port"].startswith("Yes")

def test_families_scope():
    rows = gt.parse_rows(FIXTURE)
    fams = gt.families(rows)
    scope = gt.in_scope(fams, rows)
    assert "aaa" in scope                        # family all-No -> in scope
    assert "bbb" not in scope                    # any member Yes -> whole family out
    assert "cleoftp" not in scope                # EXCLUDE: already fan-ported reference

def test_patch_cell():
    sidecars = {"aaa": {"scores": {"final": 72.5, "tier": "A"}, "gate": None}}
    out = gt.patch_text(FIXTURE, sidecars, clones={"aaaj": "aaa"})
    assert "| **72.5** A · [assessment](assessments/aaa.md) |" in out
    assert "| see [`aaa`](assessments/aaa.md) |" in out
    assert out.count("not assessed") == 3        # untouched rows stay untouched
    parked = {"aaa": {"scores": None, "gate": "G2 controls: card_reader"}}
    assert "| parked G2 · [notes](assessments/aaa.md) |" in gt.patch_text(FIXTURE, parked, clones={})

if __name__ == "__main__":
    test_parse_rows(); print("test_parse_rows OK")
    test_families_scope(); print("test_families_scope OK")
    test_patch_cell(); print("test_patch_cell OK")
    print("ALL OK")
```

- [ ] **Step 2: Run to verify it fails** — `ModuleNotFoundError`

- [ ] **Step 3: Write `tools/assess/gen_tables.py`**

```python
#!/usr/bin/env python3
"""Summary-table generators (spec §5.3). Subcommands:
  queue    -> assessments/QUEUE.md   (once; hand-curated afterwards; --force to regen)
  ranking  -> assessments/RANKING.md (regenerated from assessments/*.metrics.json)
  patch    -> rewrite ONLY the status cell of matching GAME_FORMATS.md rows"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
GF = os.path.join(REPO, "GAME_FORMATS.md")
ASSESS = os.path.join(REPO, "assessments")
# Families kept out of the queue with a reason (spec §1 + calibration refs)
EXCLUDE = {"cleoftp": "reference — already fan-ported (`../cleopatra`)"}

_ROW = re.compile(r"^\| (.+?) \| `(\w+)` \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|\s*$")
_CLONE = re.compile(r"clone of `(\w+)`")


def parse_rows(text):
    rows = {}
    for line in text.splitlines():
        m = _ROW.match(line)
        if not m:
            continue
        title, setname, fmt, rel, size, genre, dc, status = m.groups()
        cm = _CLONE.search(rel)
        rows[setname] = {"title": title, "format": fmt, "parent": cm.group(1) if cm else None,
                         "size": size, "genre": genre, "dc_port": dc, "status": status}
    return rows


def families(rows):
    fams = {}
    for s, r in rows.items():
        fams.setdefault(r["parent"] or s, []).append(s)
    return fams


def in_scope(fams, rows):
    """Spec §1: family in scope iff NO member has an official DC port, minus EXCLUDE."""
    return {rep: members for rep, members in fams.items()
            if rep not in EXCLUDE
            and not any(rows[m]["dc_port"].startswith("Yes") for m in members)}


def load_sidecars():
    out = {}
    for p in glob.glob(os.path.join(ASSESS, "*.metrics.json")):
        with open(p) as fh:
            sc = json.load(fh)
        out[sc["set"]] = sc
    return out


def queue(force=False):
    path = os.path.join(ASSESS, "QUEUE.md")
    if os.path.isfile(path) and not force:
        sys.exit("QUEUE.md exists (hand-curated) — use --force to regenerate")
    rows = parse_rows(open(GF).read())
    fams = families(rows)
    scope = in_scope(fams, rows)
    lines = ["# Assessment queue", "",
             "Generated by `tools/assess/gen_tables.py queue` from `GAME_FORMATS.md`; "
             "hand-curated afterwards (representative overrides, ordering).", "",
             "| Representative | Family members | Genre | Size | Status |", "|---|---|---|---|---|"]
    def key(rep):
        g = rows[rep]["genre"]
        return (0 if "★" in g else (2 if "⚠" in g else 1), g, rep)
    for rep in sorted(scope, key=key):
        members = ", ".join(f"`{m}`" for m in sorted(scope[rep]))
        r = rows[rep]
        lines.append(f"| `{rep}` — {r['title']} | {members} | {r['genre']} | {r['size']} | pending |")
    excl = ", ".join(f"`{k}` ({v})" for k, v in EXCLUDE.items())
    lines += ["", f"Excluded beyond official DC ports: {excl}.", ""]
    open(path, "w").write("\n".join(lines))
    print(f"QUEUE.md: {len(scope)} families")


def ranking():
    scs = load_sidecars()
    scored = [s for s in scs.values() if s.get("scores")]
    parked = [s for s in scs.values() if s.get("gate")]
    unscored = [s for s in scs.values() if not s.get("scores") and not s.get("gate")]
    scored.sort(key=lambda s: -s["scores"]["final"])
    lines = ["# Portability ranking", "",
             "Generated by `tools/assess/gen_tables.py ranking` from `assessments/*.metrics.json`. "
             "Do not edit by hand.", "",
             "| # | Game | Set | Final | Tier | Mem | Stream | Guts | Ctrl | Sim |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(scored, 1):
        sc = s["scores"]
        lines.append(f"| {i} | {s['title']} | [`{s['set']}`]({s['set']}.md) | **{sc['final']}** "
                     f"| {sc['tier']} | {sc['memory']} | {sc['streaming']} | {sc['guts']} "
                     f"| {sc['controls']} | {sc['similarity']} |")
    if parked:
        lines += ["", "## Parked", ""] + [
            f"- [`{s['set']}`]({s['set']}.md) — {s['gate']}" for s in parked]
    if unscored:
        lines += ["", "## Awaiting controls research", ""] + [
            f"- [`{s['set']}`]({s['set']}.md)" for s in unscored]
    open(os.path.join(ASSESS, "RANKING.md"), "w").write("\n".join(lines) + "\n")
    print(f"RANKING.md: {len(scored)} scored, {len(parked)} parked, {len(unscored)} unscored")


def patch_text(text, sidecars, clones):
    out = []
    for line in text.splitlines(keepends=True):
        m = _ROW.match(line.rstrip("\n"))
        if m:
            setname = m.group(2)
            cell = None
            if setname in sidecars:
                sc = sidecars[setname]
                if sc.get("scores"):
                    cell = (f"**{sc['scores']['final']}** {sc['scores']['tier']} · "
                            f"[assessment](assessments/{setname}.md)")
                elif sc.get("gate"):
                    cell = f"parked {sc['gate'].split()[0]} · [notes](assessments/{setname}.md)"
            elif setname in clones and clones[setname] in sidecars:
                rep = clones[setname]
                cell = f"see [`{rep}`](assessments/{rep}.md)"
            if cell:
                head = line.rstrip("\n").rsplit("|", 2)[0]
                line = f"{head}| {cell} |\n"
        out.append(line)
    return "".join(out)


def patch():
    text = open(GF).read()
    rows = parse_rows(text)
    clones = {s: r["parent"] for s, r in rows.items() if r["parent"]}
    open(GF, "w").write(patch_text(text, load_sidecars(), clones))
    print("GAME_FORMATS.md patched")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "queue":
        queue("--force" in sys.argv)
    elif cmd == "ranking":
        ranking()
    elif cmd == "patch":
        patch()
    else:
        sys.exit("usage: gen_tables.py queue|ranking|patch")
```

- [ ] **Step 4: Run to verify it passes** — `python3 tools/assess/tests/test_gen_tables.py` → `ALL OK`

- [ ] **Step 5: Verify against the real table (read-only)**

Run: `python3 -c "import sys;sys.path.insert(0,'tools/assess');import gen_tables as gt;rows=gt.parse_rows(open('GAME_FORMATS.md').read());print(len(rows),'rows');fams=gt.families(rows);scope=gt.in_scope(fams,rows);print(len(fams),'families,',len(scope),'in scope')"`
Expected: 152 rows; families ≈ 136; in-scope ≈ 75–80. If row count < 152, the `_ROW` regex missed real rows — print non-matching `| ` lines and adjust.

- [ ] **Step 6: Commit**

```bash
git add tools/assess/gen_tables.py tools/assess/tests/test_gen_tables.py
git commit -m "assess: gen_tables.py — queue/ranking generators + GAME_FORMATS status patch"
```

---

### Task 8: RUNBOOK + assessment template

**Files:**
- Create: `assessments/RUNBOOK.md`
- Create: `assessments/TEMPLATE.md`

**Interfaces:**
- Consumes: every CLI from Tasks 1–7 (exact commands below).
- Produces: the verbatim procedure each assessing agent follows (spec §8) and the doc skeleton (spec §5.1). Tasks 9–10 follow this runbook to produce the first two docs.

- [ ] **Step 1: Write `assessments/RUNBOOK.md`**

```markdown
# Assessment runbook (battery v1)

Follow verbatim, one family at a time, SERIAL ONLY (never two Flycast instances).
Spec: `docs/superpowers/specs/2026-08-02-portability-assessment-design.md`.

## Once per session

1. `python3 tools/assess/tests/test_score.py` → must print `ALL OK` (toolchain sanity).
2. If `tools/assess/out/controls.json` is missing:
   `mkdir -p tools/assess/out && python3 tools/assess/controls_extract.py > tools/assess/out/controls.json`
3. Naomi BIOS must be at `~/Library/Application Support/Flycast/data/naomi.zip`
   (else: `cp ../cleopatra/bios/naomi.zip ~/Library/Application\ Support/Flycast/data/`).

## Per family (representative set from QUEUE.md)

1. **Battery:** `python3 tools/assess/run_battery.py <set>`
   (~6 min unattended; writes `assessments/<set>.metrics.json` + evidence).
   - `PARKED G1 …` → verify it is the game, not tooling: check `assessments/evidence/<set>/raw/stdout.log`,
     the screenshots, and `boot.mame_not_working` in the sidecar. Write the short-form doc (§ Parked below).
   - `UNSCORED (controls research required)` → continue; scoring happens in step 3.
2. **Controls research:** determine the real cabinet controls. Sources in priority order:
   MAME `naomi.cpp` input ports (already cited in the sidecar) > game manual/flyer scans >
   Sega Retro/System16 hardware pages > wikis. Record ≥2 sources with URLs.
   Set `controls.device_class` in the sidecar to one of: `stick`, `dc_peripheral`,
   `pad_adaptable`, `awkward` — or, for physically unmappable hardware (card reader/printer,
   medal/hopper, mandatory multi-cabinet), leave the raw name (e.g. `card_reader`): score.py
   turns any off-ladder value into gate G2. Append your sources to `controls.sources`.
   Also research **existing community/fan DC ports** of the game; note findings for the doc.
3. **Score:** `python3 tools/assess/score.py assessments/<set>.metrics.json`
4. **Write the doc:** copy `assessments/TEMPLATE.md` → `assessments/<set>.md`; fill every
   `{{…}}` from the sidecar and your research. Never hand-edit a number the sidecar owns —
   quote it. Every claim needs its citation (log tag, screenshot path, or URL).
5. **Tables:** `python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch`
6. **Update QUEUE.md** status cell for the family (`pending` → `done` / `parked`).
7. **Commit:** `git add assessments/<set>.md assessments/<set>.metrics.json
   assessments/evidence/<set>/*.png assessments/RANKING.md assessments/QUEUE.md GAME_FORMATS.md`
   then commit `assess(<set>): <final> <tier>` (or `parked <gate>`).
   NEVER add `evidence/<set>/raw/` or anything under `tools/assess/out/` or `tools/dat-extract/out/`.
8. **Lessons:** anything surprising (tool quirk, new failure class, scoring edge) →
   append to `docs/kb/assessment-tooling.md`.

## Parked short-form doc

Use TEMPLATE sections 1–3 only, plus a `## Gate` section: which gate, the evidence
(log line / screenshot / source), and what would unblock the game.

## Re-assessment rule

If instrumentation or `score.py` changes materially, bump `BATTERY_VERSION` in
`run_battery.py`; sidecars with an older version are stale — re-run them before
comparing scores (spec §7).
```

- [ ] **Step 2: Write `assessments/TEMPLATE.md`**

```markdown
# {{Title}} (`{{set}}`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **{{final}}** ({{tier}}) |
| Bottom line | {{one sentence: why this rank}} |
| Assessed | {{date}} · battery v{{battery}} · flycast `{{flycast_commit}}` · Ghidra {{ghidra}} · MAME `{{mame_src}}` |

## 2. Identity

| | |
|---|---|
| Set / family | `{{set}}` (covers: {{clone list or "no clones"}}) |
| Maker / year | {{maker}}, {{year}} |
| Genre / format | {{genre}}, {{cart or GD-ROM}} |
| Official DC port | {{No / Partial + note}} |
| Community ports | {{none found / links}} |
| Representative choice | {{why this set represents the family}} |

## 3. Boot & run evidence

Boots: {{yes/no}} · handoff at {{t}} s · run {{secs}} s · rom: `{{rom_used}}`
Screenshots: {{links to evidence/<set>/shot-*.png}}
Anomalies: {{none / description}}

## 4. Memory fit (axis: {{memory score}})

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | {{bytes}} | 16 MB | {{u}} | {{s}} | grep `CARTDMA` in raw log |
| VRAM (write-truth) | {{bytes}} | 8 MB | {{u}} | {{s}} | grep `VRAMPROFILE` |
| ARAM (write-truth) | {{bytes}} | 2 MB | {{u}} | {{s}} | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): {{main/vram/aram}}.
{{Risk flag if main watermark ≫ high-water.}}

## 5. Cart streaming (axis: {{streaming score}})

DMA events {{n}} · total {{MB}} · unique {{MB}} · re-read ratio {{r}} ·
steady-state {{MB/min}} {{(short-window flag?)}}

## 6. Guts (axis: {{guts score or "n/a — no .dat"}})

Code {{bytes}} · functions {{n}} · MMIO refs: scif {{n}}, rtc {{n}}, g2ext {{n}} ·
BIOS vector refs: {{map}} · penalties applied: {{flags → numbers}}

## 7. Controls (axis: {{controls score or gate}})

Cabinet: {{description}}. MAME input ports: `{{input_ports}}`.
Proposed DC mapping: {{pad/peripheral proposal}}.
Sources: {{≥2 citations, URLs}}

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = {{m}}^.40 · {{st}}^.20 · {{g}}^.20 · {{c}}^.10 · {{si}}^.10 = **{{final}}**
{{If guts dropped: note renormalized weights .50/.25/.125/.125.}}
Similarity inputs: developer {{y/n}}, SDK overlap {{full/partial/none}}, loader match {{y/n}}.

## 9. Risks & notes

- {{main-RAM v1 limitation: CPU-written data above DMA assets not captured}}
- {{anything odd; what a port project should verify first}}
```

- [ ] **Step 3: Verify template/spec coverage**

Check TEMPLATE.md against spec §5.1's nine sections — every one present, none empty. Check RUNBOOK command names against the actual CLIs from Tasks 1–7 (run each command with no args; each must fail with its usage line, not `No such file`).

- [ ] **Step 4: Commit**

```bash
git add assessments/RUNBOOK.md assessments/TEMPLATE.md
git commit -m "assess: RUNBOOK + assessment doc template"
```

---

### Task 9: Calibration A — Cleopatra Fortune Plus (the control test)

**Files:**
- Create: `assessments/cleoftp.metrics.json`, `assessments/cleoftp.md`, `assessments/reference/similarity-reference.json`, `assessments/evidence/cleoftp/shot-*.png`

**Interfaces:**
- Consumes: the full battery; known-good numbers from `../cleopatra/docs/kb/phase2-measurements.md`.
- Produces: the calibration verdict (battery trustworthy or not) + the similarity reference all later runs use.

- [ ] **Step 1: Prerequisites**

```bash
mkdir -p tools/assess/out
python3 tools/assess/controls_extract.py > tools/assess/out/controls.json
ls ~/Library/Application\ Support/Flycast/data/naomi.zip || cp ../cleopatra/bios/naomi.zip ~/Library/Application\ Support/Flycast/data/
```

- [ ] **Step 2: Run the battery**

Run: `python3 tools/assess/run_battery.py cleoftp --keep-dat`
Expected: ~6 min; verdict line ends `S` (device hint for `naomi` ports is `stick`, so it scores immediately).

- [ ] **Step 3: Verify against the known-good numbers — fix the battery, never the numbers**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/cleoftp.metrics.json"))
ref = {"main": 11761888, "vram": 8181717, "aram": 2097152}   # phase2-measurements.md
main = sc["memory"]["main"]["dma_high_water"]
vram = sc["memory"]["vram"]["peak"]; aram = sc["memory"]["aram"]["peak"]
assert abs(main - ref["main"]) / ref["main"] < 0.05, f"main {main:#x} vs {ref['main']:#x}"
assert abs(vram - ref["vram"]) / ref["vram"] < 0.05, f"vram {vram:#x}"
assert aram == ref["aram"], f"aram {aram:#x} must be exactly 2 MiB"
assert sc["memory"]["vram"]["nz_above_cap"] == 0 and sc["memory"]["aram"]["nz_above_cap"] == 0
assert sc["capture"]["handoff"]["aram_zeroed"] and sc["capture"]["handoff"]["vram_zeroed"]
assert sc["scores"]["tier"] == "S", sc["scores"]
print("CALIBRATION A PASS", sc["scores"])
EOF
```

Troubleshooting (from the Cleopatra project's findings): no window / instant exit → check `evidence/cleoftp/raw/stdout.log` for missing BIOS; black screenshots → vsync/persistence flags (both already set by `run_battery.py` — check the `defaults write` succeeded); zip launch fails → `--rom naomi/cleoftp/<disc>.chd`, and if that also fails `--rom` the `.dat` (record which worked; update RUNBOOK if zip isn't the universal answer). If VRAM peak ≈ 9.4 MB, the handoff-zero didn't fire — the BIOS-logo false positive is back; check `VRAMHANDOFF` in the raw log.

- [ ] **Step 4: Determinism spot-check**

Re-run `python3 tools/assess/run_battery.py cleoftp` and re-run the Step 3 verifier. Both passes within tolerance → battery stable. (Second run's sidecar overwrites the first — fine.)

- [ ] **Step 5: Build the similarity reference**

```bash
mkdir -p assessments/reference
python3 - <<'EOF'
import json
sc = json.load(open("assessments/cleoftp.metrics.json"))
json.dump({"makers": [sc["maker"]], "format": sc["format"],
           "sdk_strings": sc["guts"]["sdk_strings"]},
          open("assessments/reference/similarity-reference.json", "w"), indent=2)
print("reference written:", len(sc["guts"]["sdk_strings"]), "strings")
EOF
# Bake similarity vs itself into the sidecar (dev match + full overlap + loader match = 100):
python3 tools/assess/run_battery.py cleoftp && python3 - <<'EOF'
import json; sc = json.load(open("assessments/cleoftp.metrics.json"))
assert sc["similarity"] == {"developer_match": True, "sdk_overlap": "full", "cart_loader_match": True}, sc["similarity"]
# Spec anchor predicts ~92 with guts 90; real static-scan penalties (rtc refs, extra BIOS
# classes) are DATA, not battery error — accept any S-tier result.
assert sc["scores"]["final"] >= 85 and sc["scores"]["tier"] == "S", sc["scores"]
print("ANCHOR PASS", sc["scores"]["final"], sc["scores"]["tier"])
EOF
```

- [ ] **Step 6: Write `assessments/cleoftp.md` from TEMPLATE.md**

Fill every `{{…}}`; mark prominently in §1: *"Calibration reference — already fan-ported (`../cleopatra`); not a queue entry."* This doubles as the template's usability test: any section that can't be filled from sidecar + research means TEMPLATE or sidecar needs a field — fix it now.

- [ ] **Step 7: Clean up and commit**

```bash
rm -f tools/dat-extract/out/cleoftp.dat
git add assessments/cleoftp.md assessments/cleoftp.metrics.json assessments/reference/ assessments/evidence/cleoftp/*.png
git commit -m "assess: calibration A — cleoftp reproduces phase2/5 numbers, scores ~92/S"
```

---

### Task 10: Calibration B — Ikaruga (GD-ROM path verification)

**Files:**
- Create: `assessments/ikaruga.metrics.json`, `assessments/ikaruga.md`, `assessments/evidence/ikaruga/shot-*.png`

**Interfaces:**
- Consumes: the battery; the spec's claim that GD/DIMM reads route through the logged `CARTDMA` path (to be proven here).
- Produces: GD-path verdict; the second calibration doc. Contingency: the one C++ change this plan allows.

- [ ] **Step 1: Run the battery**

Run: `python3 tools/assess/run_battery.py ikaruga`
Expected: verdict line with a score (Ikaruga's official DC port proves the game fits — memory axes should be comfortable).

- [ ] **Step 2: Verify the GD/DIMM streaming path is visible**

```bash
python3 - <<'EOF'
import json
sc = json.load(open("assessments/ikaruga.metrics.json"))
st = sc["streaming"]
assert st["dma_events"] > 0, "NO CARTDMA EVENTS — GD/DIMM reads bypass the logged path (see contingency)"
assert sc["boot"]["ok"], sc["boot"]
assert sc["memory"]["vram"]["nz_above_cap"] == 0 and sc["memory"]["aram"]["nz_above_cap"] == 0
print("CALIBRATION B PASS:", st["dma_events"], "DMA events,",
      sc["scores"]["final"] if sc["scores"] else sc["gate"])
EOF
```

**Contingency (only if `dma_events == 0`):** GD-ROM sets bypass `Naomi_DmaStart`'s logging. Locate the GD cart read path in the fork: `grep -n "DmaOffset\|AdvancePtr" ../cleopatra/tools/flycast-src/core/hw/naomi/gdcartridge.cpp` and add the same `cartlog("CARTDMA src=%08x dest=%08x len=%x\n", …)` call used in `naomi.cpp`'s `Naomi_DmaStart` (include `cartlog.h`). Rebuild: `cmake --build ../cleopatra/tools/flycast-src/build`. Then re-run **both** calibrations (Task 9 Step 2 onward, then this task) — instrumentation changed, so all captures must be uniform (spec §7). Commit the fork change in the fork repo with a message referencing this plan.

- [ ] **Step 3: Write `assessments/ikaruga.md`**

From TEMPLATE.md, marked *"Calibration reference — official DC port exists (2002); not a queue entry."* Controls: `stick` (2-button shmup; cite MAME input ports + the DC port's existence).

- [ ] **Step 4: Commit**

```bash
git add assessments/ikaruga.md assessments/ikaruga.metrics.json assessments/evidence/ikaruga/*.png
git commit -m "assess: calibration B — ikaruga; GD/DIMM streaming visible via CARTDMA"
```

---

### Task 11: Queue, tables, knowledge base — campaign-ready

**Files:**
- Create: `assessments/QUEUE.md`, `assessments/RANKING.md`, `docs/kb/assessment-tooling.md`
- Modify: `GAME_FORMATS.md` (status cells for `cleoftp`/`ikaruga` + a one-line pointer to RANKING/QUEUE under the table intro)

**Interfaces:**
- Consumes: everything; both calibration sidecars.
- Produces: the campaign's work list and the reproducibility record. After this task the assessment campaign is pure RUNBOOK execution.

- [ ] **Step 1: Generate queue and tables**

```bash
python3 tools/assess/gen_tables.py queue
python3 tools/assess/gen_tables.py ranking
python3 tools/assess/gen_tables.py patch
```

Expected: QUEUE.md with ~75–80 families (★ genres first); RANKING.md with the two calibration entries; `GAME_FORMATS.md` rows for `cleoftp`/`ikaruga` now carry score links, everything else untouched (`git diff GAME_FORMATS.md` must show only those cells).

- [ ] **Step 2: Add the pointer line to GAME_FORMATS.md**

Under the intro paragraph (after the "DC port column" bullet list ends), insert:

```markdown
- **Assessment status:** per-set cell in the last column; sorted scores in [assessments/RANKING.md](assessments/RANKING.md), work queue in [assessments/QUEUE.md](assessments/QUEUE.md), method in the [spec](docs/superpowers/specs/2026-08-02-portability-assessment-design.md).
```

- [ ] **Step 3: Write `docs/kb/assessment-tooling.md`**

Record (reproducibility rule — exact versions, flags, steps):
- Toolchain pins: flycast fork commit (from a calibration sidecar), Ghidra `12.1.2_PUBLIC` (+ install source per `../cleopatra/docs/kb/tooling.md`), MAME `59e7c0b`, battery v1, macOS version (`sw_vers -productVersion`).
- The battery invocation and its env knobs (`FLYCAST_BIN`, `NAOMI_DIR`, `MAME_NAOMI`, `GHIDRA_HOME`).
- Calibration results: both verdict lines, the reproduced Cleopatra numbers, GD-path outcome (incl. contingency taken or not), zip-vs-chd launch findings.
- Lessons learned during Tasks 1–10 (each troubleshooting hit that cost >10 minutes).

- [ ] **Step 4: Full test sweep + commit**

```bash
for t in tools/assess/tests/test_*.py; do python3 "$t" || exit 1; done
git add assessments/QUEUE.md assessments/RANKING.md GAME_FORMATS.md docs/kb/assessment-tooling.md
git commit -m "assess: queue + tables + tooling kb — battery calibrated, campaign ready"
```

---

## Plan Self-Review (performed at write time)

1. **Spec coverage:** §2 pipeline → Tasks 2/5/6; §3 gates + §4 axes/tiers → Task 1; §5.1 template → Task 8; §5.2 sidecar → Task 6; §5.3 tables → Task 7; §6 tooling rows → Tasks 2–7 (flycast row: no C++, contingency in Task 10); §7 calibration → Tasks 9–10; §8 policies → RUNBOOK (Task 8) + `.gitignore` (Task 1) + `.dat` deletion (Task 6); §1 queue/scope → Tasks 7/11. Deferred items (§10) have no tasks by design.
2. **Placeholders:** the one intentionally in-task-derived datum is `DEVICE_HINTS` (Task 3) — derived from a named grep against a pinned file with a complete classification rubric; everything else is concrete code/commands.
3. **Type consistency:** sidecar keys used in `score_sidecar` (Task 1) match what `run_battery.py` builds (Task 6) and what the calibration verifiers read (Tasks 9–10); `parse_capture` output keys match `run_battery`'s consumption; `carve_boot.meta["base"]` (hex string) matches `run_guts.sh $2` usage; `gen_tables.patch_text(text, sidecars, clones)` matches its test.
