# Cleopatra Fortune Plus (GDL-0012) (`cleoftp`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **85.8 (S)** |
| Bottom line | Calibration A — the already fan-ported, real-hardware-verified control title: every region fits with zero nonzero bytes above any DC cap (ARAM is the tightest at 0.936× content), and every clean run reproduces `../cleopatra`'s known-good instrumentation bit-for-bit, which is what makes the battery trustworthy on every other set. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `cleoftp` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | Altron / Taito, 2002 |
| Genre / format | Puzzle, GD-ROM |
| Official DC port | No. Only the unrelated original *Cleopatra Fortune* (non-"Plus") shipped on Dreamcast; this Naomi "Plus" revision never got an official DC release (`GAME_FORMATS.md:196`). |
| Community ports | Yes — this exact title. `../cleopatra` is a from-scratch Naomi→DC static-binary conversion of this cart, currently Phase 5: "GAME FULLY PLAYABLE ON REAL HARDWARE" as of 2026-08-02, 1P and 2P at full speed (`../cleopatra/docs/kb/00-status.md`), validated over 18 real-hardware rounds with no wrong/missing textures (`../cleopatra/docs/kb/phase2-measurements.md` §Video RAM). |
| Representative choice | Not a representative pick — this is the calibration control (not a queue entry). `../cleopatra`'s own instrumented measurements are the known-good numbers the battery must reproduce before it can be trusted on any other set; per project rule, a mismatch means **fix the battery**, never the reference numbers. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"` — the GD DIMM boot PIO-loads its
~1 MB boot segment before the first cart DMA) · run 600 s · rom: `naomi/cleoftp.zip`
Attract/demo reached: **demo** — sustains its attract "how to play" loop end-to-end
with a visibly evolving board (the attract sequence fades to black between segments —
screen wipes, not faults). Sidecar `capture.coverage = "demo"`.
Screenshots: `evidence/cleoftp/shot-060s.png` · `evidence/cleoftp/shot-243s.png` ·
`evidence/cleoftp/shot-426s.png` · `evidence/cleoftp/shot-609s.png` (curated from 10 —
all four show the attract "how to play" demo loop).
Anomalies: none this run — clean single zip leg (`leg 1: cleoftp.zip attempt 1 -> ran
full window`, battery log). All three calibration anchors reproduced bit-identically on
this v9 re-capture vs. the v8 sidecar: main `dma_high_water` 11,761,888 · VRAM address
peak 8,181,717 · ARAM address peak 2,094,512 (the −2,640 B vs. the historical exact
2,097,152 is the documented since-v5 baseline race, §4 below — not new drift).
Historical: the v1/v2 sessions flaked `no-handoff-120s` (Flycast lands on the DC BIOS
home menu, clears on a plain re-run) on 2 of 6 launches; `RUNBOOK.md` documents the
auto-retry and flake pattern.

## 4. Memory fit (axis: 89.8)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 10,537,841 | 16,777,216 | 0.6281 | 100.0 | address peak 16,252,992 (u 0.9688) · 0 above cap · `dma_high_water` 11,761,888 (informational floor) |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 6,022,568 | 8,388,608 | 0.7180 | 100.0 | content_total 4,793,768 + 2×fb_bytes 1,228,800 (`fb_bytes` 614,400, exactly 640×480×2) · address peak 8,181,717 (u 0.9753) · 0 above cap |
| ARAM (content volume, fill-excluded, `content_total`) | 1,963,359 | 2,097,152 | 0.9362 | 89.8 | address peak 2,094,512 · 0 above cap — **binding region** |

Watermarks (informational, content-scan — stale-data prone): main 16,252,992 ·
vram 9,711,616 · aram 8,388,608 (boot-time fill, not content).
Cross-check vs. `../cleopatra/docs/kb/phase2-measurements.md`: main DMA high-water
11,761,888, VRAM address peak 8,181,717 and the ~2 MiB ARAM bank reproduce across every
clean run v1 → v9 (ARAM address peak 2,094,512 since v5 — −2,640 B from the historical
exact 2,097,152, a baseline race at the last ARM-reset rebase, stable 70/70 samples,
not a regression). This v9 re-capture reproduced all three anchors bit-identically
against the v8 sidecar (see §3). `nz_above_cap = 0` in all three regions: no genuine
game write lands above any DC capacity.

## 5. Cart streaming (axis: 68.0)

DMA events 894 · total 100.1 MB · unique 21.8 MB · re-read ratio 0.7824 ·
steady-state 9.908 MB/min (`short_window: false`) · PIO 1,049,920 B
Durable invariant: `unique_bytes` (22,827,008 B) is identical at 360 s and 600 s
capture lengths — the real streamed-asset footprint doesn't grow with capture length,
only how many times it gets re-touched does.

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 1,645 · MMIO refs: scif 3, rtc 3, g2ext 166 ·
BIOS vector refs: none (`bios_refs: {}`, `extra_bios_classes: 0`) · flags:
`eeprom_bios`, `serial`, `rtc` → 85.0.
Boot binary carved via the GD-ROM chd2dat→carve_boot pipeline, base `0x8c020000`,
entry `0x8c04ae2c`, title string `CLEOPATRA FORTUNE PLUS`. `functions=1645` and
`scif=3` reproduce Task 5's smoke-test Ghidra pass exactly.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi JAMMA panel — 8-way joystick + 6 buttons per player, 2 players, 2 coin slots, no free-play by default (this cabinet is set to FREE PLAY in the captured runs, visible bottom-right of every screenshot).
MAME input ports: `naomi` (the shared default Naomi panel fragment — `PORT_INCLUDE(naomi_mie)` + per-player `IPT_JOYSTICK_{UP,DOWN,LEFT,RIGHT}` with `PORT_8WAY` + `IPT_BUTTON1..6` + `IPT_START{1,2}`).
Proposed DC mapping: DC digital pad (or analog stick, either works for 8-way input) → joystick; DC face buttons A/B/X/Y → buttons 1-4 (the puzzle-tile-clearing gameplay visible in the attract screenshots needs at most a cursor move + 1-2 action buttons; buttons 5/6 are the shared panel's unused remainder for this title); Start → Start. `device_class: stick` → controls axis 100.0 (no gate).
Sources:
- MAME `src/mame/sega/naomi.cpp @59e7c0b` (pinned copy at `../cleopatra/tools/mame`), `INPUT_PORTS_START( naomi )`, lines 1506-1565 — primary source, the exact bit-level port definition used by every "naomi"-input-port cart.
- adb.arcadeitalia.net cabinet database entry for Cleopatra Fortune Plus (GDL-0012) — corroborating manual/flyer-level source: 8-way joystick, 6 buttons, up to 2 players, 2 coin slots (`http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=cleoftp`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 89.8^.40 · 68.0^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **85.8 (S)**
Similarity inputs: developer yes (`Altron / Taito` ∈ reference makers), SDK overlap
full (500/500 `sdk_strings` ⊆ reference), loader match yes — a self-match by
construction against `assessments/reference/similarity-reference.json`.

## 9. Risks & notes

- **Calibration role:** per project rule, any mismatch with `../cleopatra`'s
  real-hardware reference numbers means fix the battery, never the reference. Every
  clean run to date passes; the anchor must never gate (control test, CLAUDE.md
  rule 2).
- **Flycast boot-menu flake:** 2 of 6 launches across the v1+v2 sessions, always the
  same signature (`no-handoff-120s`, DC BIOS home menu, clears on re-run). v4–v8 runs
  have been clean, but it is more frequent than a true one-off — keep watching
  (`RUNBOOK.md` line 26).
- ARAM is the tight region (0.936× content, 89.8 sub-score); the fan port's completed
  real-hardware audio work is the existing reference for the remaining headroom.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v1 | — | 84.7 (S) | Initial Calibration A (360 s capture): memory/handoff/guts invariants match `../cleopatra`'s real-hardware measurements bit-identically; one launch flake noted |
| v2 | 2026-08-02 | 84.2 (S) | 600 s uniformity re-run (per `RUNBOOK.md`'s stale-sidecar rule); only streaming moved (70.8 → 69.0, window dilution); flake needed one manual retry beyond the new auto-retry |
| v4 | 2026-08-04 | 84.0 (S) | Interim 71.4 was wrong — GD BIOS logo framebuffer at 0x943000 charged to the game (proven non-game by the dragntr3 control); score.py gained the signature exclusion + anchor-park refusal (root-cause kb §7) |
| v5 | 2026-08-06 | 84.0 (S) | Pre-handoff VRAMPROFILE samples dropped (kb §9) — true VRAM peak 8,181,717 without the score-side clamp |
| v6 | 2026-08-07 | 84.0 (S) | Main write-truth measured for the first time: 16,252,992 (u 0.969, 0 above cap); handoff trigger found to be `pio`, not the predicted `dma`; ARAM −2,640 B baseline-race caveat recorded |
| v7 | 2026-08-07 | 84.8 (S) | ARAM re-keyed on content volume (kb §6 checkpoint): 1,963,361 B (u 0.936); VRAM became binding |
| v8 | 2026-08-07 | 84.9 (S) | VRAM re-keyed on FB-masked content + 2×FB (spec `2026-08-07-vram-fb-masking-design.md`); v4-era BIOS-signature clamp retired to a MetricRegression canary (ruling 4); main bound |
| v9 | 2026-08-08 | 85.8 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); ARAM binds at 89.8 |
| v9 | 2026-08-09 | 85.8 S | ranking-groom chunk 2: fresh v9 capture, provenance v8→v9 (scoring keys unchanged); calibration anchors reproduced bit-identically |
