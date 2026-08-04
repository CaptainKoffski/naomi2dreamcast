# Moeru Casinyo (Japan) (GDL-0013) (`moeru`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **80.5** (S) — #2 overall |
| Bottom line | A Katana/Ninja2-SDK casino minigame collection from the reference maker (Altron) that fits every DC region comfortably once measured correctly; the previous "G1 broken: emulator-exited" park was an instrumentation/harness artifact stack, not the game. |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/moeru.zip`
Attract/demo reached: **demo** — slot-machine attract with live reels, bet/credit
counters and "GET THE CHANCE" banner at `evidence/moeru/shot-609s.png`; earlier
shots cycle the blackjack table demo.
Screenshots: `evidence/moeru/shot-060s.png` · `evidence/moeru/shot-365s.png` ·
`evidence/moeru/shot-609s.png`
Anomalies: one launch-flake leg (dynarec-init assert, known class) on the first
attempt of the final battery pass; retry ran the full window.

## 4. Memory fit (axis: 85.0)

| Region | Peak | DC capacity | Utilization | Evidence |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 11,237,600 | 16,777,216 | 0.67 | `CARTDMA` in raw log |
| VRAM (write-truth diff) | 9,711,616 | 8,388,608 | 1.16 | `VRAMPROFILE` (nz_total 4,523,535; nz above cap only 57,048) |
| ARAM (content, fill-excluded) | 1,509,920 | 2,097,152 | 0.72 | `ARAMPROFILE` content fields |

VRAM's raw peak-address is 16% over the 8 MB line, but the above-cap diff is the
GD BIOS logo framebuffer signature (57,048 B @ 0x943000 — REQUIREMENTS.md's
"9.4 mb during the Naomi logo show time" caveat, proven non-game by the dragntr3
splash-only control). `score.py` excludes it (`scores.vram_bios_noise_excluded`);
the game's own content fits every region.

## 5. Cart streaming (axis: 55.1)

1,135 DMA events · total 198.6 MB · unique 46.5 MB · re-read ratio 0.766 ·
steady-state 19.9 MB/min — the attract loop re-streams its minigame assets from
GD continuously; a DC port would want them resident or repacked.

## 6. Guts (axis: 85.0)

Code 1,441,792 B · 2,072 functions · MMIO refs: scif 3, rtc 3, g2ext 214 ·
title header `THE MOERU CASINYO` @ 0x8c020000, entry 0x8c056e24.
Penalties: `eeprom_bios`, `serial`, `rtc`.
SDK strings are the full Sega Katana stack (`syStartKn 2.07`, `Ninja2 2.01.010`,
`syChain`, `gdCi*` GD filesystem calls) — this is effectively DC-SDK code running
on Naomi, the best possible guts profile for a port.

## 7. Controls (axis: 100.0)

Cabinet: standard 1P stick + buttons (MAME `naomi.cpp` INPUT_PORTS, cited in
sidecar). Casino menu game — trivially pad-mappable.

## 8. Score computation

final = 85.0^.40 · 55.1^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **80.5** (S)
Similarity: developer match **yes** (Altron is the reference maker), SDK overlap
full, loader match yes → 100.

## 9. Risks & notes

- 19.9 MB/min steady GD re-streaming (re-read ratio 0.77) is the main porting cost:
  the attract loop cycles minigame assets; GD-ROM seek/stream behavior on real DC
  hardware must be validated early.
- Main-RAM v1 limitation: CPU-written data above the last DMA'd asset is not
  captured by the DMA high-water metric.
- History: v2 verdict "G1 broken: emulator-exited" and every early screenshot
  (DC BIOS menu, black screens, frozen NOW LOADING) were artifacts of the harness
  and instrumentation, fixed in battery v3/v4 — `docs/kb/assessment-tooling.md` §7.
