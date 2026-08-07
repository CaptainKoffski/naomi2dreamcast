# G3-ARAM Volume Re-Key Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Key the ARAM region of the portability scorer (gate + sub-score) on compacted content volume instead of the content high-water address, then re-run the 10 affected families and regenerate campaign tables.

**Architecture:** Three code changes in `tools/assess/` (parser captures an already-logged field; scorer keys ARAM on it with a conservative fallback; battery version bumps to 7), followed by a serial 10-set re-run wave and a docs/tables pass. No emulator-fork change — the fork already logs `content_below2m` on every `ARAMPROFILE` line.

**Tech Stack:** Python 3 stdlib only (repo convention: no dependencies). Plain-assert test files run directly with `python3`, no pytest.

**Spec:** `docs/superpowers/specs/2026-08-07-aram-gate-volume-design.md` — read it first; the Rulings section records the user decisions this plan implements.

## Global Constraints

- Work in the main checkout on branch `main` (repo convention: campaign commits go straight to `main`). Do NOT use a git worktree: the battery needs the gitignored `naomi/` ROM tree and the local emulator build.
- Never commit ROMs, BIOS images, or disc images — `naomi/` and `assessments/evidence/*/raw/` stay untracked/gitignored.
- Never weaken `tools/assess/tests/test_metric_guards.py` — its header says these invariants are "the strict prohibition, not advice". All existing tests stay green at every commit.
- `BATTERY_VERSION` becomes exactly `"7"`.
- One Flycast instance at a time; the wave is strictly serial (kb: headless recipe).
- ARAM keying invariant: content volume ≤ content high-water address, so the address fallback for pre-v7 sidecars may only *under*-score. Nothing in this plan may let a fallback path produce a higher score than the volume path would.
- Commit messages follow repo style: short `area: summary` subject (`git log --oneline` for examples), ending with the Claude co-author trailer.

---

### Task 1: Parser — capture `content_below2m`, emit `aram.content_total`

**Files:**
- Modify: `tools/assess/parse_capture.py:12-13` (`_APROF` regex), `:36` (aram init), `:71` (ARAMREBASE reset), `:79-88` (`_APROF` branch), `:150-151` (return dict)
- Test: `tools/assess/tests/test_parse_capture.py`

**Interfaces:**
- Consumes: fork `ARAMPROFILE` log lines, e.g. `ARAMPROFILE high=400000 nz=200000 nz_below2m=1f0000 nz_above2m=10000 content_high=400000 content_below2m=1f0000 content_above2m=10000 size=800000` (the `content_*` triple is optional — absent on pre-v4 logs).
- Produces: `parse(...)["aram"]["content_total"]` — `int` bytes (max over per-sample `content_below2m + content_above2m`) or `None` when no sample carried content fields. Task 3 copies it into the sidecar; Task 2 scores it.

- [ ] **Step 1: Write the failing test**

Append to `tools/assess/tests/test_parse_capture.py` (before the `__main__` block):

```python
def test_aram_content_total_per_sample_max():
    # §6 ruling (spec 2026-08-07-aram-gate-volume-design.md): content_total is
    # the max of PER-SAMPLE below+above totals. max(below)+max(above) across
    # different samples (here 0x1f0000+0x80000=0x270000) is a volume that never
    # existed at once and must NOT be the answer.
    log = (
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "ARAMHANDOFF baselined size=800000 trigger=dma\n"
        "ARAMPROFILE high=400000 nz=200000 nz_below2m=1f0000 nz_above2m=10000"
        " content_high=400000 content_below2m=1f0000 content_above2m=10000 size=800000\n"
        "ARAMPROFILE high=400000 nz=180000 nz_below2m=100000 nz_above2m=80000"
        " content_high=400000 content_below2m=100000 content_above2m=80000 size=800000\n"
    )
    m = parse_capture.parse(log)
    assert m["aram"]["content_total"] == 0x200000, hex(m["aram"]["content_total"])
    assert m["aram"]["peak"] == 0x400000 and m["aram"]["nz_above_cap"] == 0x80000

def test_aram_content_total_legacy_and_rebase():
    # Legacy line (no content_* fields): content_total must stay None, and
    # peak/nz_above_cap keep their raw-diff fallback semantics.
    m = parse_capture.parse(
        "ARAMPROFILE high=200000 nz=1e0000 nz_below2m=1e0000 nz_above2m=0 size=800000\n")
    assert m["aram"]["content_total"] is None
    assert m["aram"]["peak"] == 0x200000
    # ARAMREBASE restarts every running max — content_total included (samples
    # before the last rebase measured BIOS sound-RAM-test residue).
    log = (
        "ARAMPROFILE high=700000 nz=600000 nz_below2m=200000 nz_above2m=400000"
        " content_high=700000 content_below2m=200000 content_above2m=400000 size=800000\n"
        "ARAMREBASE armrst size=800000\n"
        "ARAMPROFILE high=180000 nz=150000 nz_below2m=150000 nz_above2m=0"
        " content_high=180000 content_below2m=150000 content_above2m=0 size=800000\n"
    )
    m = parse_capture.parse(log)
    assert m["aram"]["content_total"] == 0x150000, hex(m["aram"]["content_total"])
```

Register both in the `__main__` block alongside the existing calls:

```python
    test_aram_content_total_per_sample_max(); print("test_aram_content_total_per_sample_max OK")
    test_aram_content_total_legacy_and_rebase(); print("test_aram_content_total_legacy_and_rebase OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: FAIL with `KeyError: 'content_total'`

- [ ] **Step 3: Implement**

In `tools/assess/parse_capture.py`, four edits:

(a) `_APROF` regex — capture `content_below2m` (was a non-captured skip). Note the group renumbering: `content_above2m` moves from group 4 to group 5.

```python
_APROF = re.compile(r"^ARAMPROFILE high=([0-9a-f]+) nz=[0-9a-f]+ nz_below2m=[0-9a-f]+ nz_above2m=([0-9a-f]+)"
                    r"(?: content_high=([0-9a-f]+) content_below2m=([0-9a-f]+) content_above2m=([0-9a-f]+))?", re.I)
```

(b) aram init (line 36):

```python
    aram = {"peak": 0, "nz_above_cap": 0, "content_total": None}
```

(c) ARAMREBASE reset (line 71) — must reset the new field too:

```python
            aram = {"peak": 0, "nz_above_cap": 0, "content_total": None}
```

(d) `_APROF` branch (lines 85-88) — group 4 is now `content_below2m`, group 5 is `content_above2m`:

```python
                    peak_s = m.group(3) if m.group(3) is not None else m.group(1)
                    above_s = m.group(5) if m.group(5) is not None else m.group(2)
                    aram["peak"] = max(aram["peak"], int(peak_s, 16))
                    aram["nz_above_cap"] = max(aram["nz_above_cap"], int(above_s, 16))
                    if m.group(4) is not None:
                        # §6 volume keying: one coherent sample's below+above —
                        # never max(below)+max(above) across samples
                        total = int(m.group(4), 16) + int(m.group(5), 16)
                        aram["content_total"] = max(aram["content_total"] or 0, total)
```

(e) return dict (lines 150-151):

```python
        "aram": {"peak": aram["peak"], "nz_above_cap": aram["nz_above_cap"],
                 "content_total": aram["content_total"],
                 "watermark_max": wm.get("aram", 0)},
```

- [ ] **Step 4: Run the full parser test file**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: `ALL OK` (existing tests prove the group renumbering didn't break legacy fallback: `test_parse` asserts aram peak/nz from a legacy line).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/parse_capture.py tools/assess/tests/test_parse_capture.py
git commit -m "assess: parser captures content_below2m -> aram.content_total (spec 2026-08-07)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Scorer — ARAM gate + axis keyed on volume, address fallback

**Files:**
- Modify: `tools/assess/score.py:170-176` (inside `score_sidecar`)
- Test: `tools/assess/tests/test_score.py`

**Interfaces:**
- Consumes: sidecar `memory.aram.content_total` (int bytes, may be absent/None on pre-v7 sidecars) and `memory.aram.peak` (content high-water address).
- Produces: unchanged function signatures. `score_sidecar` gates ARAM with message `G3 memory: aram content > 2x DC capacity` when volume-keyed, keeps `G3 memory: aram peak > 2x DC capacity` when address-fallback-keyed. `region_score`, `memory_axis`, `CAPS`, thresholds: untouched.

- [ ] **Step 1: Write the failing tests**

Append to `tools/assess/tests/test_score.py` (before the `__main__` block; it auto-discovers `test_*` names):

```python
def _volume_sc(aram):
    # main/vram comfortably fit so the memory axis == the aram sub-score path
    return {
        "set": "synth-volume", "boot": {"ok": True},
        "memory": {"main": {"peak": 5 * MB, "nz_total": 4 * MB, "nz_above_cap": 0,
                            "dma_high_water": 0},
                   "vram": {"peak": 6 * MB, "nz_above_cap": 0},
                   "aram": aram},
        "streaming": {"steady_mb_per_min": 2.0, "reread_ratio": 0.05},
        "guts": {"dat_available": False},
        "controls": {"device_class": "stick"},
        "similarity": {"developer_match": False, "sdk_overlap": "none",
                       "cart_loader_match": False},
    }

def test_aram_small_blob_high_address_scores():
    # gwing2 shape (spec: the divergent case): 47.5 KB blob at the top of an
    # 8 MiB bank — address-u 3.99 parked it; volume-u 1.023 must score ~80.8.
    sc = _volume_sc({"peak": 8372160, "nz_above_cap": 48674,
                     "content_total": 2097152 + 48674})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 80.8, sc["scores"]

def test_aram_volume_overflow_parks_with_content_message():
    # 4.4 MB of real compacted content (takoron class): u > 2 -> park, and the
    # message says "content" because the gate keyed on measured volume.
    sc = _volume_sc({"peak": 8257552, "nz_above_cap": 2302848,
                     "content_total": 4400000})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: aram content > 2x DC capacity", sc["gate"]

def test_aram_no_content_total_falls_back_to_address():
    # Pre-v7 sidecar: no content_total -> the address keeps gating (legacy
    # message says "peak"). Volume <= address, so this only under-scores.
    sc = _volume_sc({"peak": 8257552, "nz_above_cap": 1000})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: aram peak > 2x DC capacity", sc["gate"]

def test_aram_zero_volume_is_a_measurement_not_missing():
    # content_total == 0 must key the axis (u=0 -> 100), NOT fall back to the
    # 8 MiB address — the `is not None` check, not truthiness.
    sc = _volume_sc({"peak": 8 * MB, "nz_above_cap": 0, "content_total": 0})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]
```

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python3 tools/assess/tests/test_score.py`
Expected: `test_aram_small_blob_high_address_scores` raises AssertionError (gate fired: the current scorer keys on `peak` 8372160 → u 3.99 → park). The three other new tests: the park-message test fails (no "content" wording yet), the fallback test passes already (documents current behavior), the zero-volume test fails.

- [ ] **Step 3: Implement**

In `tools/assess/score.py`, replace lines 171-176 (`peaks = ...` through the gate assignment; the `main_peak` line above stays):

```python
    # §6 checkpoint ruling (2026-08-07, spec 2026-08-07-aram-gate-volume-design.md):
    # ARAM keys on compacted content VOLUME — OSB banks are position-independent
    # (azumanga live verification), so the high-water ADDRESS is a porting
    # artifact. content_total <= content_high always, so the address fallback
    # for pre-v7 sidecars can only under-score, never over-score.
    aram_ct = sc["memory"]["aram"].get("content_total")
    aram_fit = aram_ct if aram_ct is not None else sc["memory"]["aram"]["peak"]
    peaks = {"vram": vram_peak, "aram": aram_fit}
    if main_peak:
        peaks["main"] = main_peak
    mem, gated = memory_axis(peaks)
    if mem is None:
        metric = "content" if (gated == "aram" and aram_ct is not None) else "peak"
        sc["gate"] = f"G3 memory: {gated} {metric} > 2x DC capacity"
```

- [ ] **Step 4: Run the scorer and guard suites**

Run: `python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py`
Expected: both print `ALL OK`. The guard file's synthetic sidecars carry no `content_total`, so they exercise the fallback path and must be untouched-green (Global Constraints: never weaken them).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/score.py tools/assess/tests/test_score.py
git commit -m "assess: G3-ARAM gate+axis keyed on content volume, address fallback (§6 ruling)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Battery — sidecar field + `BATTERY_VERSION = "7"`

**Files:**
- Modify: `tools/assess/run_battery.py:18` (version), `:318` (sidecar aram block)

**Interfaces:**
- Consumes: `cap["aram"]["content_total"]` from Task 1's parser.
- Produces: sidecar `memory.aram.content_total` (key present only when measured — spec: "no zero-fill") and `versions.battery == "7"`. The wave (Task 4) relies on both.

- [ ] **Step 1: Bump the version constant**

Replace line 18 of `tools/assess/run_battery.py` with:

```python
BATTERY_VERSION = "7"  # v7: G3-ARAM keyed on content VOLUME (spec docs/superpowers/specs/2026-08-07-aram-gate-volume-design.md). Parser captures the fork's already-logged content_below2m; sidecar gains memory.aram.content_total = max over per-sample (below+above); score.py gates+scores aram on volume with address fallback for pre-v7 sidecars (volume <= address, so fallback only under-scores). No fork change; capture format identical to v6 — the bump marks the schema+semantics change for RANKING provenance (user ruling at spec review).
```

- [ ] **Step 2: Write `content_total` into the sidecar**

Replace the aram line of the `"memory"` block (line 318):

```python
                   "aram": {"peak": cap["aram"]["peak"], "nz_above_cap": cap["aram"]["nz_above_cap"],
                            **({"content_total": cap["aram"]["content_total"]}
                               if cap["aram"]["content_total"] is not None else {})}},
```

- [ ] **Step 3: Run the whole assess test suite**

Run: `for t in tools/assess/tests/test_*.py; do python3 "$t" || break; done`
Expected: every file prints `ALL OK`. (No unit test covers `run_battery.main()` — the wave's first run is its verification: Task 4 Step 2 asserts `versions.battery == "7"` and a present `content_total`.)

- [ ] **Step 4: Commit**

```bash
git add tools/assess/run_battery.py
git commit -m "assess: battery v7 — sidecar carries aram.content_total

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Re-run wave — 10 sets, serial

**Files:**
- Modify (per set): `assessments/<set>.metrics.json`, `assessments/<set>.md`, `assessments/evidence/<set>/shot-*.png`
- Reference: `assessments/RUNBOOK.md` (per-family flow), `assessments/gwing2.md` § Gate (doc-update template)

**Interfaces:**
- Consumes: Tasks 1-3 landed (the battery's preflight self-test runs `test_score.py` + `test_metric_guards.py` and refuses to start if red).
- Produces: 10 sidecars with `versions.battery == "7"` and measured `aram.content_total`; updated per-set assessment docs. Task 5 regenerates tables from these.

Wave order and expectations (spec § Expected outcomes — bounds, the measurement decides):

| # | Set | Expected gate | Expected aram volume-u |
|---|---|---|---|
| 1 | gwing2 | un-parks, scores | ≈ 1.02 |
| 2 | sgtetris | un-parks, scores | ≤ 1.0 |
| 3 | ausfache | stays scored, memory axis 85 → up to 100 | ≤ 1.0 |
| 4 | cleoftp | stays scored (ANCHOR — a park here crashes the battery by design; stop and debug, never override) | ≤ 1.0 |
| 5 | azumanga | un-parks, low memory axis | ≤ 1.81 |
| 6 | cspike | un-parks, low memory axis | ≤ 1.79 |
| 7 | zerogu2 | borderline — measurement decides park vs floor-score | ≈ 2.02 bound |
| 8 | takoron | stays parked ("content" message) | ≥ 3.1 |
| 9 | inunoos | stays parked | ≈ 3.3 |
| 10 | pokasuka | stays parked | ≈ 3.4 |

Per set, repeat this cycle (strictly one at a time; ~12-15 min each):

- [ ] **Step 1: Record the prior coverage annotation** (a re-run resets `capture.coverage` to null — gwing2 2026-08-07 precedent):

```bash
git show HEAD:assessments/<set>.metrics.json | python3 -c "import json,sys; sc=json.load(sys.stdin); print(sc['capture'].get('coverage'), (sc.get('scores') or {}), sc.get('gate'))"
```

- [ ] **Step 2: Run the battery and verify the sidecar**

```bash
python3 tools/assess/run_battery.py <set>
python3 - <<'EOF'
import json, sys
sc = json.load(open("assessments/<set>.metrics.json"))
a = sc["memory"]["aram"]
assert sc["versions"]["battery"] == "7", sc["versions"]
assert "content_total" in a, "parser/battery pipeline lost content_total"
print(sc["set"], "| gate:", sc.get("gate"), "| content_total:", a["content_total"],
      "| volume-u:", round(a["content_total"] / (2 << 20), 3),
      "| final:", (sc.get("scores") or {}).get("final"))
EOF
```

Compare the printed gate/u against the expectations table. A result outside its bound (e.g. gwing2 still parked, or takoron un-parked) is NOT hand-adjusted — stop the wave and debug the instrumentation first (kb §7 posture; use superpowers:systematic-debugging).

- [ ] **Step 3: Re-annotate `capture.coverage`** — inspect the run's `assessments/evidence/<set>/shot-*.png` per RUNBOOK's representativeness check ("demo" if any frame shows in-game/demo footage, "title" if only title/attract cards) and set the field in the sidecar JSON. Use Step 1's prior value as the reference point; if the new run's screenshots reach less than the prior run did, keep the conservative lower of the two.

- [ ] **Step 4: Update `assessments/<set>.md`** — following the structure visible in `assessments/gwing2.md`:
  - §1 header status row: append `; aram-volume re-run 2026-08-07 · battery v7 · flycast <commit printed by the battery>`.
  - § Gate: update the ARAM row of the region table to the volume-keyed u (`content_total` / 2,097,152), state the new verdict (un-parked score or re-confirmed park with the "content" message), and for gwing2 mark tension 1 **RESOLVED** (mirror how tension 2 was struck through and resolved in that same file).
  - Final-score/verdict lines: the new `scores.final`/`tier`, or the new park string.

- [ ] **Step 5: Commit the set**

```bash
git add assessments/<set>.metrics.json assessments/<set>.md assessments/evidence/<set>/
git commit -m "assess: <set> aram-volume re-run (battery v7) — <one-line outcome>

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Then move to the next set in the table.

---

### Task 5: Blanket re-score + regenerate tables

**Files:**
- Modify: `assessments/RANKING.md`, `assessments/QUEUE.md`, `GAME_FORMATS.md` (status cells only)

**Interfaces:**
- Consumes: all 10 wave sidecars committed; scorer from Task 2.
- Produces: campaign tables consistent under one scorer version. Task 6 cites them.

- [ ] **Step 1: Re-score every sidecar under the new scorer**

```bash
for f in assessments/*.metrics.json; do
  python3 tools/assess/score.py "$f" || echo "NOT RESCORED: $f"
done
```

`score.py` refuses sidecars whose controls research is pending (`device_class`
None/"review") — every currently-committed sidecar has researched controls, so
expect zero `NOT RESCORED` lines; if one appears, report it, don't force it.

- [ ] **Step 2: Verify the no-change proof**

Run: `git diff --stat assessments/`
Expected: **zero modified files.** Non-wave sidecars lack `content_total`, take the address fallback, and reproduce their committed scores byte-for-byte; wave sidecars were already scored by the v7 battery. Any diff here means the fallback changed a score it must not touch — stop and debug before proceeding (the Global Constraints invariant).

- [ ] **Step 3: Regenerate tables and flip queue statuses**

```bash
python3 tools/assess/gen_tables.py ranking
python3 tools/assess/gen_tables.py patch
```

Then hand-edit `assessments/QUEUE.md` status cells (it is hand-curated; never regenerate it): `gwing2`, `sgtetris`, `azumanga`, `cspike` → `done` (plus `zerogu2` if it un-parked); `takoron`, `inunoos`, `pokasuka` stay `parked`.

- [ ] **Step 4: Sanity-check RANKING.md**

Read the regenerated `assessments/RANKING.md`: wave sets show battery `v7` in the provenance column; un-parked sets appear as scored rows; still-parked ARAM sets show the new `content` gate wording.

- [ ] **Step 5: Commit**

```bash
git add assessments/RANKING.md assessments/QUEUE.md GAME_FORMATS.md
git commit -m "tables: regenerate under aram-volume scorer (battery v7 wave)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Knowledge base entry, backlog briefs, final verification

**Files:**
- Modify: `docs/kb/assessment-tooling.md` §6, `docs/superpowers/specs/backlog-aram-gate-volume.md`
- Create: `docs/superpowers/specs/backlog-aram-p16-discount.md`

**Interfaces:**
- Consumes: wave results (Task 4 sidecars), regenerated tables (Task 5).
- Produces: the §6 checkpoint record; the maybe-marked follow-up brief; the closed motivating brief.

- [ ] **Step 1: Write the kb §6 checkpoint entry**

In `docs/kb/assessment-tooling.md` §6:

(a) Update the intro's backlog-brief line (the one listing `backlog-aram-gate-volume.md` as queued) to mark it **landed 2026-08-07 as battery v7** — mirror the phrasing already used there for the snapshot-diff brief.

(b) Append a new numbered item (after item 5) recording, with the actual measured numbers pulled from the wave sidecars:

- The ruling: checkpoint opened at 25 families (user decision); G3-ARAM gate + axis re-keyed on `content_total`; address fallback for pre-v7 sidecars (volume ≤ address ⇒ under-scores only); battery v7.
- The evidence pair: gwing2 (48,674 B above cap, address-u 3.99 vs measured volume-u) vs takoron (4,347,346 B above cap, still parked) — plus the sgtetris addendum: the brief said seven parked sets, but sgtetris was the eighth and most extreme (8 B above cap).
- The measured volume-u distribution across all 10 wave sets, extracted with:

```bash
python3 - <<'EOF'
import json
for s in ("gwing2","sgtetris","ausfache","cleoftp","azumanga","cspike","zerogu2","takoron","inunoos","pokasuka"):
    sc = json.load(open(f"assessments/{s}.metrics.json"))
    a = sc["memory"]["aram"]
    print(f"{s}: content_total={a['content_total']:,} u={a['content_total']/(2<<20):.3f} "
          f"gate={sc.get('gate')} final={(sc.get('scores') or {}).get('final')}")
EOF
```

- The item-1 deferral: the 2× ARAM multiple itself (ikaruga's official port trimmed a genuine 4× bank) is now decidable against this measured distribution — explicitly still open, next §6 ruling.
- Update item 5 (marstv peak-vs-content) with a closing note: the content rule it argued for is now the shipped rule.

- [ ] **Step 2: Create `docs/superpowers/specs/backlog-aram-p16-discount.md`**

```markdown
# Backlog (maybe): discount GD-streamable raw .p16 BGM before the ARAM volume gate

**Status:** proposed 2026-08-07 at the §6 checkpoint, marked **maybe** — user
ruling: not implemented with the volume re-key; revisit only if the evidence
bar below is met.

## Idea

Raw `.p16` BGM sitting in inter-bank ARAM gaps (headerless, GD-streamable —
azumanga finding, `assessments/azumanga.md`) is content a real port would
stream from disc, not resident sound RAM. Subtract identified `.p16` runs
from `aram.content_total` before gating/scoring.

## Pros

- More faithful to porting reality: the DC streams BGM from GD-ROM routinely;
  resident ARAM is for SFX/voice banks.
- Could move heavy-but-streamable titles (azumanga class) from the
  10-13 memory-axis band into scoreable range, or un-park volume-parked sets
  whose overflow is mostly BGM.

## Cons

- Needs automated bank-map carving + a headerless-format classifier inside
  the deterministic scorer (`parse_osb.py`-grade analysis per title) — a big
  step up in scorer complexity and a new false-positive surface.
- Evidenced on ONE title (azumanga). No second data point yet.
- Double-counts against the §6 item-1 threshold question: if the ARAM
  multiple is softened instead, most of the same titles are reachable with
  zero new analysis code.

## Possible ranking impact (from the 2026-08-07 v7 wave)

Fill from wave data: for each still-parked or low-band set (azumanga, cspike,
zerogu2, takoron, inunoos, pokasuka), how much of `content_total` is `.p16`
gap content (requires an ARAM dump + `parse_osb.py` pass per title — the
azumanga § ARAM bank-structure method). A set moves only if the discounted
volume crosses a scoring band edge (2.0 park line, or the 1.25/1.0/0.8 knees).

## Evidence bar (do not start before this)

- ≥ 3 titles where a `parse_osb.py`-verified `.p16` share would flip a park
  or move a memory-axis band, AND
- the §6 item-1 threshold ruling has landed (it may make this moot).
```

- [ ] **Step 3: Close the motivating brief**

Edit `docs/superpowers/specs/backlog-aram-gate-volume.md`'s Status line to:

```markdown
**Status:** LANDED 2026-08-07 as battery v7 — design
`2026-08-07-aram-gate-volume-design.md`, kb §6 checkpoint entry records the
ruling and wave results. Kept as the motivating brief.
```

- [ ] **Step 4: Final verification**

```bash
for t in tools/assess/tests/test_*.py; do python3 "$t" || break; done
git status --short
```

Expected: every test file `ALL OK`; no unexpected untracked/modified files (evidence `raw/` dirs are gitignored).

- [ ] **Step 5: Commit**

```bash
git add docs/kb/assessment-tooling.md docs/superpowers/specs/backlog-aram-p16-discount.md docs/superpowers/specs/backlog-aram-gate-volume.md
git commit -m "kb: §6 aram-volume checkpoint entry; p16-discount maybe-brief; close motivating brief

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```
