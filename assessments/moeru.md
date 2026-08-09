# Moeru Casinyo (Japan) (GDL-0013) (`moeru`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **85.9 (S)** |
| Bottom line | A Katana/Ninja2-SDK casino minigame collection from the reference maker (Altron) whose content fits every DC region outright (all three memory sub-scores 100) — the porting cost is the attract loop's 19.9 MB/min GD re-streaming, not memory. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `moeru` (no clones) |
| Maker / year | Altron, 2002 |
| Genre / format | Casino minigames (slots/blackjack), GD-ROM (GDL-0013) |
| Official DC port | None found |
| Community ports | None found |
| Representative choice | Only set in family |

This title is the debugging vehicle that exposed the battery v2/v3 defects: it was
the A/B control for the guest-zeroing regression, the bare-`.chd` DC-BIOS-menu
harness trap, and the GL-vs-Vulkan CPU-framebuffer presentation gap
(`docs/kb/assessment-tooling.md` §7).

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/moeru.zip`
Attract/demo reached: **demo** — slot-machine attract with live reels, bet/credit
counters and "GET THE CHANCE" banner at `evidence/moeru/shot-609s.png`; earlier
shots cycle the blackjack table demo.
Screenshots: `evidence/moeru/shot-060s.png` · `evidence/moeru/shot-365s.png` ·
`evidence/moeru/shot-609s.png`
Anomalies: launch-flake class only (known operational class, not a game defect) —
leg 1 ran the full 600 s window cleanly on the first attempt this run (`moeru-battery.log`:
"leg 1: moeru.zip attempt 1 -> ran full window"), unlike the v4/v8 passes which needed
the auto-retry. All three memory regions (main `peak`/`nz_total`/`nz_above_cap`/
`dma_high_water`, VRAM `peak`/`nz_total`/`content_total`/`fb_bytes`, ARAM `peak`/
`content_total`) reproduced byte-identically against the v8 sidecar
(`git show HEAD:assessments/moeru.metrics.json` pre-this-commit) — same capture is
stable frame-for-frame. Streaming reproduced near-identically (`dma_events` 1,135,
`total_bytes`/`unique_bytes`/`reread_ratio` unchanged; `steady_mb_per_min` 19.922 vs
v8's 19.93, an immaterial capture-window rounding difference, not a regression).
`shot-060s.png` and `shot-365s.png` are pixel-identical to the v8 capture (deterministic
attract loop); `shot-609s.png` differs slightly (credit/reel state at the 609 s mark)
but shows the same slot-demo screen.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 4,868,604 | 16,777,216 | 0.290 | 100.0 | address peak 15,728,704 (u 0.938, informational — was the v8 binding value) · `dma_high_water` 11,237,600 · nz_above_cap 0 |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 5,746,300 (content 4,517,500 + 2×614,400) | 8,388,608 | 0.685 | 100.0 | address peak 8,066,096 (u 0.962, informational) · nz_total 4,533,046 · nz_above_cap 0 · `fb_bytes` = exactly 640×480×2 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,413,091 | 2,097,152 | 0.674 | 100.0 | address peak 1,509,920 (u 0.720) · nz_above_cap 0 |

No region binds — all three sub-scores are 100.0.
Watermarks (informational, content-scan — stale-data prone): main 15,728,704 ·
vram 9,711,616 (includes the GD BIOS-logo sheet the retired v4-era clamp used to
exclude; the clamp is now a `MetricRegression` canary, spec
`2026-08-07-vram-fb-masking-design.md` ruling 4, and this run's values do not match
the signature) · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 55.1)

DMA events 1,135 · total 198.6 MB · unique 46.5 MB · re-read ratio 0.7658 ·
steady-state 19.922 MB/min (`short_window: false`) · PIO 1,443,136 B — the attract
loop re-streams its minigame assets from GD continuously; a DC port would want them
resident or repacked.

## 6. Guts (axis: 85.0)

Code 1,441,792 B · functions 2,072 · MMIO refs: scif 3, rtc 3, g2ext 214 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc`.
Title header `THE MOERU CASINYO` @ base `0x8c020000`, entry `0x8c056e24`.
SDK strings are the full Sega Katana stack (`syStartKn 2.07`, `Ninja2 2.01.010`,
`syChain`, `gdCi*` GD filesystem calls) — this is effectively DC-SDK code running
on Naomi, the best possible guts profile for a port.

## 7. Controls (axis: 100.0)

Cabinet: standard 1P stick + buttons (`controls.device_class = stick`). Casino menu
game — trivially pad-mappable.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 55.1^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **85.9 (S)**
Similarity inputs: developer yes (Altron is the reference maker), SDK overlap
partial, loader match yes — 100 (points cap).

## 9. Risks & notes

- 19.9 MB/min steady GD re-streaming (re-read ratio 0.766) is the main porting cost:
  the attract loop cycles minigame assets; GD-ROM seek/stream behavior on real DC
  hardware must be validated early.
- Launch flakes (dynarec-init assert, `emulator-exited`) are a known operational
  class of the harness, not a game defect — both occurrences retried clean (§3).
- The v2 "G1 broken: emulator-exited" verdict and every early screenshot (DC BIOS
  menu, black screens, frozen NOW LOADING) were artifacts of the harness and
  instrumentation, fixed in battery v3/v4 — `docs/kb/assessment-tooling.md` §7.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G1 broken: emulator-exited | Harness/instrumentation artifact stack (guest-zeroing regression, bare-`.chd` DC-BIOS-menu trap, GL-vs-Vulkan CPU-FB gap) — root-causes kb §7 |
| v4 | 2026-08-04 | 80.5 (S) | First scored run after the harness fixes; VRAM's GD BIOS-logo noise excluded via the signature clamp (kb §7) |
| v5 | 2026-08-06 | 81.6 (S) | Pre-`VRAMHANDOFF` sample drop gave a clean VRAM peak 8,066,096 (0.96×); memory 85.0 → 87.9 (kb §9) |
| v8 | 2026-08-08 | 82.2 (S) | Re-capture. VRAM re-keyed on FB-masked content (sub 100.0), first write-truth main measurement (peak 15,728,704, sub 89.7, binding) and first ARAM content-volume measurement (spec `2026-08-07-vram-fb-masking-design.md`) |
| v9 | 2026-08-08 | 85.9 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory axis 100.0, no region binding |
| v9 | 2026-08-09 | 85.9 S | ranking-groom chunk 1: fresh v9 capture, provenance v8→v9 (scoring keys unchanged) |
