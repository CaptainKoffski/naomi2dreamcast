# Cleopatra Fortune Plus (GDL-0012) (`cleoftp`) — portability assessment

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
| **Final score** | **84.7** (S) |
| Bottom line | The battery reproduces `../cleopatra`'s phase2/phase5 known-good RAM figures byte-for-byte across two independent clean runs, and — once the similarity reference is baked from this run's own static-scan output (self-match by construction) — lands S-tier. The 84.7 vs. a naively-expected ~92 is explained entirely by real static-scan penalties (`serial`, `rtc`, `eeprom_bios` flags on the actual cart code), not battery error. |
| Assessed | 2026-08-02 · battery v1 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 30.0 s · run 360 s · rom: `naomi/cleoftp.zip`
Screenshots:
- `assessments/evidence/cleoftp/shot-060s.png` — title screen ("Cleopatra Fortune+", PRESS START BUTTON)
- `assessments/evidence/cleoftp/shot-121s.png` — attract "how to play" demo (tile-clearing rules)
- `assessments/evidence/cleoftp/shot-183s.png` — attract RANKING TOP10 screen

Anomalies: Of the 4 launches run this session (run 1 "keep-dat", run 2 determinism re-run, run 3 similarity-bake, and a retry of run 3), **run 3 parked `G1 broken: no-handoff-120s`**: Flycast booted to the stock Dreamcast BIOS home menu (swirl logo, Play/File/Music/Settings) instead of loading the cart at all, and the automatic rom-candidate fallback (`.zip` → `naomi/cleoftp/gdl-0012.chd`) landed on the same failure within that run (`rom_used: naomi/cleoftp/gdl-0012.chd`, still no handoff). An immediate retry of the identical command (`python3 tools/assess/run_battery.py cleoftp`, no flags) succeeded cleanly via the default `.zip` path (`rom_used: naomi/cleoftp.zip`, handoff at 30.0 s) with every memory/guts number matching runs 1 and 2 exactly. Runs 1, 2, and the retry (3 of 4 launches) are byte-identical on every measured figure; only run 3 hung at the BIOS menu. Judged a one-off Flycast launch flake, not a battery defect — see §9.

## 4. Memory fit (axis: 85.0)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 11,761,888 B (`0xb378e0`) | 16 MB | 70.1% | 100.0 | grep `CARTDMA` in raw log (1104 hits, retry run) |
| VRAM (write-truth) | 8,181,717 B (`0x7cd7d5`) | 8 MB | 97.5% | 86.8 | grep `VRAMPROFILE`/`VRAMHANDOFF` (9 profile snapshots, 1 handoff-zero) |
| ARAM (write-truth) | 2,097,152 B (`0x200000`, exactly 2 MiB) | 2 MB | 100.0% | 85.0 | grep `ARAMPROFILE`/`ARAMHANDOFF` (9 profile snapshots, 1 handoff-zero) |

Memory axis = min(region sub-scores) = 85.0 (regions aren't tradeable).
Watermarks (informational, content-scan — stale-data prone): main 16,252,992 B · vram 8,181,717 B · aram 2,097,152 B.
Risk flag: main watermark (~15.5 MB) is well above the DMA high-water (~11.2 MB) — this is exactly the known stale/uninitialized-data effect documented in `../cleopatra/docs/kb/phase2-measurements.md` (the WATERMARK scan hit was confirmed stale, not a real high-address stack, by Phase 3 disassembly + dynamic SP logging). `nz_above_cap` is 0 for both VRAM and ARAM in this run, confirming no genuine game write lands above DC capacity in either region.

Cross-check vs. `../cleopatra/docs/kb/phase2-measurements.md`: main DMA high-water 11,761,888 (11.2 MB), VRAM write-truth peak 8,181,717 (7.8 MB, `0x7cd7d5`), ARAM write-truth peak exactly 2,097,152 (2 MB, `0x200000`) — **all three reproduce exactly**, run 1 → run 2 → retry, with `nz_above_cap == 0` and `handoff.{aram,vram}_zeroed == true` in every clean run.

## 5. Cart streaming (axis: 70.8)

DMA events 552 · total 62,101,504 B (59.2 MB) · unique 22,827,008 B (21.8 MB) · re-read ratio 0.6324 ·
steady-state 10.487 MB/min (short-window flag: false)

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
      = 85.0^.40 · 70.8^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **84.7**

Similarity inputs (self-match, by construction — the reference was built from this run's own guts scan): developer y (`Altron / Taito` ∈ reference makers), SDK overlap full (500/500 `sdk_strings` ⊆ reference), loader match y (`GD-ROM` == reference format, `dat_available: true`) → similarity axis 100.0.

## 9. Risks & notes

- Main-RAM v1 limitation (carried from spec): the DMA high-water measure only sees cart-DMA'd data; CPU-written data placed above the last DMA'd asset (e.g. dynamically-allocated heap/stack past that point) is not captured. `../cleopatra`'s own Phase 3 dynamic-SP logging closed this gap for this specific title (SP confirmed at `~0x8c00e-f xxx`, nowhere near the 32 MB watermark) — see `../cleopatra/docs/kb/phase2-measurements.md`. The generic battery (v1) does not do per-title dynamic SP logging, so this residual gap applies to every other assessed set until/unless a future battery version adds it.
- One of four Flycast launches this session hung at the stock DC BIOS home menu instead of loading the cart (§3). Recommend adding to `RUNBOOK.md`: on `PARKED G1 broken: no-handoff-120s` for a title known to work (prior clean sidecar exists), retry once with the identical command before treating it as a real boot failure or reaching for the `--rom` fallback chain.
- The literal "final ≥ 85" anchor line from the calibration brief misses by 0.3 (84.7). This is fully explained by the `guts` axis landing at the real, deterministic value of 85.0 (rtc + serial + eeprom_bios penalties genuinely present in the cart's code, confirmed identically across all three clean runs) rather than the brief's naive ~90 estimate — the brief itself flags this as expected "DATA, not battery error" and instructs accepting any S-tier result. Tier S (≥80) holds with a 4.7-point margin; this is treated as calibration PASS.
- `bios_refs: {}` (empty) — no extra BIOS-vector classes penalized this run; `extra_bios_classes: 0`.
