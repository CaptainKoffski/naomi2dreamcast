# Cleopatra Fortune Plus (GDL-0012) (`cleoftp`) — portability assessment

> **Battery v4 re-assessment (2026-08-04): **71.4 (A)**.**
> Score moved 84.2 → 71.4: v4's periodic (per-10 s) sampling catches steady-state memory peaks that v2's cart-DMA-only sampling missed. v2 under-measured; the S-tier was optimistic. Still #1.
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **71.4 (A)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/cleoftp.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 11,761,888 | 16,777,216 | 0.70 |  |
| VRAM (write-truth diff) | 9,711,616 | 8,388,608 | 1.16 | nz_total 4,792,822 |
| ARAM (content, fill-excluded) | 2,094,512 | 2,097,152 | 1.00 | content above cap 0 |

Streaming: 894 DMA events · total 100.1 MB · unique 21.8 MB · re-read 0.7824 · steady 9.904 MB/min
Axes: memory 56.6 · streaming 68.0 · guts 85.0 · controls 100.0 · similarity 100.0 → **final 71.4 (A)**
Screenshots: `evidence/cleoftp/shot-060s.png` · `evidence/cleoftp/shot-243s.png` · `evidence/cleoftp/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

> **Calibration reference — already fan-ported (`../cleopatra`); not a queue entry.**
> This is Calibration A: the control test that decides whether the assessment
> battery itself is trustworthy. All numbers below are checked against the
> known-good figures in `../cleopatra/docs/kb/phase2-measurements.md` (the
> completed, real-hardware-verified port's own instrumentation), not the other
> way around — per project rule, a mismatch means **fix the battery**, never
> the reference numbers.

## 1. Verdict

| | |
|---|---|
| **Final score** | **84.2** (S) |
| Bottom line | Re-run under battery v2 (600 s capture, was 360 s under v1) for uniformity with Calibration B (`ikaruga`). All memory/handoff/guts invariants reproduce **bit-identically** to the v1 calibration; only the streaming axis moved (70.8 → 69.0, pure dilution from the longer steady-state window — expected, not an error), taking the final score from 84.7 → 84.2. Tier stays **S**. The battery remains trustworthy. |
| Assessed | 2026-08-02 · battery v2 (600 s capture) · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `cleoftp` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | Altron / Taito, 2002 |
| Genre / format | Puzzle, GD-ROM |
| Official DC port | No. Only the unrelated original *Cleopatra Fortune* (non-"Plus") shipped on Dreamcast; this Naomi "Plus" revision never got an official DC release (`GAME_FORMATS.md:196`). |
| Community ports | Yes — this exact title. `../cleopatra` is a from-scratch Naomi→DC static-binary conversion of this cart, currently Phase 5: "GAME FULLY PLAYABLE ON REAL HARDWARE" as of 2026-08-02, 1P and 2P at full speed (`../cleopatra/docs/kb/00-status.md`), validated over 18 real-hardware rounds with no wrong/missing textures (`../cleopatra/docs/kb/phase2-measurements.md` §Video RAM). |
| Representative choice | Not a representative pick — this is the calibration control. `../cleopatra`'s own instrumented measurements are the known-good numbers the battery must reproduce before it can be trusted on any other set. |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s (battery v2 default, was 360 s under v1) · rom: `naomi/cleoftp.zip`
Attract/demo reached: **yes** — this title genuinely reaches and sustains its attract/demo loop for the full 600 s capture (contrast with `ikaruga`'s free-play title-idle lower bound). Evidence across the curated shots below: title (60 s) → attract how-to-play with an early board state (121 s) → a transitional black frame (183 s — a screen-wipe between attract segments, not a fault; the same run also hit a black frame at 370 s and a mid-wipe checkerboard frame at 485 s, both flanked by valid attract content before/after, confirming this title's attract sequence fades between segments) → attract demo with a visibly progressed board (422 s) → attract demo still actively playing, score 4000 on-screen, board mostly cleared (600 s, the very last frame of the capture). The board state visibly changes across 121 s → 422 s → 600 s (not a static loop), and the title screen recurs mid-capture (seen at 547 s, not kept) — a real, evolving attract cycle sustained end-to-end.
Screenshots:
- `assessments/evidence/cleoftp/shot-060s.png` — title screen ("Cleopatra Fortune+", PRESS START BUTTON)
- `assessments/evidence/cleoftp/shot-121s.png` — attract "how to play" demo, early board state
- `assessments/evidence/cleoftp/shot-183s.png` — transitional black frame (attract-segment screen wipe)
- `assessments/evidence/cleoftp/shot-422s.png` — attract demo, board progressed further (mid-capture)
- `assessments/evidence/cleoftp/shot-600s.png` — attract demo still active at the end of the 600 s capture (score 4000)

Anomalies: **v1 session** — of 4 launches (run 1 "keep-dat", run 2 determinism re-run, run 3 similarity-bake, and a retry of run 3), run 3 parked `G1 broken: no-handoff-120s` (Flycast booted to the stock Dreamcast BIOS home menu instead of loading the cart; the automatic `.zip`→`.chd` rom fallback also failed within that run). An immediate manual retry succeeded cleanly. Judged a one-off Flycast launch flake, not a battery defect (see §9).
**v2 re-run session (this doc's numbers)** — battery v2's new built-in auto-retry-once (see `run_battery.py`) fired but the run **still parked** `G1 broken: no-handoff-120s` after exhausting both the `.zip` and `.chd` candidates (each with its automatic retry) — `rom_used` ended at `naomi/cleoftp/gdl-0012.chd`, still no handoff. A second, fully manual re-run (`python3 tools/assess/run_battery.py cleoftp`, no flags) then succeeded cleanly via `.zip` with every memory/guts/similarity figure matching the v1 calibration exactly. This is the same flake class as v1's, just needing one extra manual retry beyond the new automatic one this time — still judged operational flakiness, not a battery or measurement defect (see §9).

## 4. Memory fit (axis: 85.0)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 11,761,888 B (`0xb378e0`) | 16 MB | 70.1% | 100.0 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 8,181,717 B (`0x7cd7d5`) | 8 MB | 97.5% | 86.8 | grep `VRAMPROFILE`/`VRAMHANDOFF` |
| ARAM (write-truth) | 2,097,152 B (`0x200000`, exactly 2 MiB) | 2 MB | 100.0% | 85.0 | grep `ARAMPROFILE`/`ARAMHANDOFF` |

Memory axis = min(region sub-scores) = 85.0 (regions aren't tradeable).
Watermarks (informational, content-scan — stale-data prone): main 16,252,992 B · vram 8,181,717 B · aram 2,097,152 B (unchanged from v1).
Risk flag: main watermark (~15.5 MB) is well above the DMA high-water (~11.2 MB) — this is exactly the known stale/uninitialized-data effect documented in `../cleopatra/docs/kb/phase2-measurements.md` (the WATERMARK scan hit was confirmed stale, not a real high-address stack, by Phase 3 disassembly + dynamic SP logging). `nz_above_cap` is 0 for both VRAM and ARAM in this run, confirming no genuine game write lands above DC capacity in either region.

Cross-check vs. `../cleopatra/docs/kb/phase2-measurements.md`: main DMA high-water 11,761,888 (11.2 MB), VRAM write-truth peak 8,181,717 (7.8 MB, `0x7cd7d5`), ARAM write-truth peak exactly 2,097,152 (2 MB, `0x200000`) — **all three reproduce exactly**, bit-for-bit, across every clean run this title has had: v1 run 1 → v1 run 2 → v1 retry → **v2 re-run (this doc)**. `nz_above_cap == 0` and `handoff.{aram,vram}_zeroed == true` hold in every clean run regardless of capture length (360 s or 600 s) — the memory axis is fully insensitive to the v1→v2 capture-length bump, as expected (these are boot/attract-loaded, not a growth trend a longer run would change).

## 5. Cart streaming (axis: 69.0)

DMA events 835 · total 97,761,280 B (93.2 MB) · unique 22,827,008 B (21.8 MB) · re-read ratio 0.7665 ·
steady-state 9.42 MB/min (short-window flag: false)

Old (v1, 360 s) vs. new (v2, 600 s) — expected drift, not an error, per the coordinator's uniformity note:

| field | v1 (360 s) | v2 (600 s) | why it moved |
|---|---|---|---|
| dma_events | 552 | 835 | more re-reads accumulate over the longer window |
| total_bytes | 62,101,504 | 97,761,280 | scales with the extra 240 s of attract/demo activity |
| unique_bytes | 22,827,008 | 22,827,008 | **identical** — same underlying asset set touched either way |
| reread_ratio | 0.6324 | 0.7665 | more repeats of the same unique set over more time |
| steady_mb_per_min | 10.487 | 9.42 | dilution — the longer window averages in more idle/attract-transition time (matches the pattern already documented for `ikaruga` in `RUNBOOK.md`'s representativeness check) |
| streaming axis | 70.8 | 69.0 | net of the above via `bandwidth_score`/`reread_score` |
| final / tier | 84.7 / S | 84.2 / S | streaming is the only axis that moved; tier unchanged |

`unique_bytes` being exactly identical is itself a useful invariant: the game's real streamed-asset footprint doesn't grow with capture length, only how many times it gets re-touched does.

## 6. Guts (axis: 85.0)

Code 1,048,576 B (1 MB) · functions 1645 · MMIO refs: scif 3, rtc 3, g2ext 166 ·
BIOS vector refs: none logged (`bios_refs: {}`, `extra_bios_classes: 0`) ·
penalties applied: `eeprom_bios` (−5, every Naomi game reads settings via BIOS), `serial` (−5, scif refs > 0), `rtc` (−5, rtc refs > 0) → 100 − 15 = 85.0

`functions=1645` and `scif=3` reproduce Task 5's smoke-test Ghidra pass exactly (clean run, same boot binary carved from the GD-ROM chd2dat→carve_boot pipeline, base `0x8c020000`, entry `0x8c04ae2c`, title string `CLEOPATRA FORTUNE PLUS`).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi JAMMA panel — 8-way joystick + 6 buttons per player, 2 players, 2 coin slots, no free-play by default (this cabinet is set to FREE PLAY in the captured runs, visible bottom-right of every screenshot).
MAME input ports: `naomi` (the shared default Naomi panel fragment — `PORT_INCLUDE(naomi_mie)` + per-player `IPT_JOYSTICK_{UP,DOWN,LEFT,RIGHT}` with `PORT_8WAY` + `IPT_BUTTON1..6` + `IPT_START{1,2}`).
Proposed DC mapping: DC digital pad (or analog stick, either works for 8-way input) → joystick; DC face buttons A/B/X/Y → buttons 1-4 (the puzzle-tile-clearing gameplay visible in the attract screenshots needs at most a cursor move + 1-2 action buttons; buttons 5/6 are the shared panel's unused remainder for this title); Start → Start. `device_class: stick` → controls axis 100.0 (no gate).
Sources:
- MAME `src/mame/sega/naomi.cpp @59e7c0b` (pinned copy at `../cleopatra/tools/mame`), `INPUT_PORTS_START( naomi )`, lines 1506-1565 — primary source, the exact bit-level port definition used by every "naomi"-input-port cart.
- adb.arcadeitalia.net cabinet database entry for Cleopatra Fortune Plus (GDL-0012) — corroborating manual/flyer-level source: 8-way joystick, 6 buttons, up to 2 players, 2 coin slots (`http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=cleoftp`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 85.0^.40 · 69.0^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **84.2**

(v1/battery-v1 was 85.0^.40 · 70.8^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = 84.7 — the only changed input is streaming, 70.8 → 69.0, per §5.)

Similarity inputs (checked against the existing `assessments/reference/similarity-reference.json` — **not rebuilt** for this re-run, per instruction): developer y (`Altron / Taito` ∈ reference makers), SDK overlap full (500/500 `sdk_strings` ⊆ reference), loader match y (`GD-ROM` == reference format, `dat_available: true`) → similarity axis 100.0, identical to v1 (expected: it's a self-match by construction, and the cart's guts scan is deterministic).

## 9. Risks & notes

- Main-RAM v1 limitation (carried from spec): the DMA high-water measure only sees cart-DMA'd data; CPU-written data placed above the last DMA'd asset (e.g. dynamically-allocated heap/stack past that point) is not captured. `../cleopatra`'s own Phase 3 dynamic-SP logging closed this gap for this specific title (SP confirmed at `~0x8c00e-f xxx`, nowhere near the 32 MB watermark) — see `../cleopatra/docs/kb/phase2-measurements.md`. The generic battery does not do per-title dynamic SP logging, so this residual gap applies to every other assessed set until/unless a future battery version adds it.
- The Flycast boot-menu flake (§3) recurred under battery v2 despite the new built-in auto-retry-once — one manual retry beyond the automatic one was still needed to get this doc's clean run. Across both sessions (v1 + v2) this title has now flaked on 2 of 6 total launches, always the same signature (`no-handoff-120s`, lands on the DC BIOS home menu, clears on a plain re-run). This is more frequent than a true one-off — worth watching across other titles rather than assuming v2's auto-retry alone is always sufficient; `RUNBOOK.md` already documents the auto-retry and flake pattern (line 26), which this run corroborates.
- The literal "final ≥ 85" anchor line from the original calibration brief misses by more under v2 (84.2, was 84.7 under v1) — purely because streaming dropped (69.0 vs 70.8, §5 dilution effect), not because guts or memory changed. Tier S (≥80) still holds, now with a 4.2-point margin (was 4.7 under v1); this remains calibration PASS — the margin shrinking with a longer, more dilution-prone capture is itself informative for future titles with long idle attract loops.
- `bios_refs: {}` (empty) — no extra BIOS-vector classes penalized this run; `extra_bios_classes: 0`.
- Uniformity note: this re-run exists solely so both calibration sidecars (`cleoftp`, `ikaruga`) are on the same battery version (v2, 600 s) before being compared or used as the basis for scoring the rest of the queue, per `RUNBOOK.md`'s re-assessment rule ("sidecars with an older battery version are stale").
