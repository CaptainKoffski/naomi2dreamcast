# Moeru Casinyo (Japan) (GDL-0013) (`moeru`) — portability assessment

> **Battery v8 vram-fb-masking re-run (2026-08-08): 82.2 (S)** — spec
> `2026-08-07-vram-fb-masking-design.md`. Sidecar: flycast `f014a410c`, battery 8. No
> park, boot ok, PIO handoff at 20.0 s. Leg 1 hit an `emulator-exited` flake (the same
> known operational-flake class already documented below in §9 — a launch-time issue,
> not a game defect); the battery's automatic leg-2 retry ran the full 600 s window
> cleanly, used for all figures here. Streaming reproduces closely (1,135 DMA events,
> steady 19.93 vs v5's 19.9 MB/min). ARAM `content_total` 1,413,091 B (u=0.674) → sub
> 100.0, first content-volume measurement (v7-class keying). **VRAM: `content_total`
> 4,517,500 B + `2×fb_bytes` 1,228,800 B (`fb_bytes` 614,400 B, exactly 640×480×2) = fit
> 5,746,300 B, u=0.685 → sub 100.0** (was already 87.9 under v5's address high-water,
> 8,066,096 B, u=0.96 — a rise, as required; `nz_above_cap` stays 0, the BIOS-logo
> signature canary does not fire — see the retirement note in §4). **MAIN is
> write-truth measured for the first time (v6 instrumentation): peak 15,728,704 B**
> (v5's DMA-only figure was 11,237,600 B) — u=0.9375, sub **89.7**, now the (mild)
> binding region, just under VRAM/ARAM's 100.0. Memory axis **87.9 → 89.7**, final
> **81.6 → 82.2**, tier unchanged **S**, still #2 overall (behind cleoftp). Sanity
> clean: `fb_bytes` == 614,400, `content_total` alone equals `nz_total` exactly in the
> raw log (no bytes fell inside the masked FB region this run — `fb_masked_nz` = 0) —
> the identity holds within each sample; the sidecar's `nz_total` (4,533,046) is the
> independent run-max across all samples, not this particular sample's total.
> Coverage re-annotated `demo` (unchanged — same blackjack-demo/slot-attract loop).

> **Battery v5 re-run (2026-08-06): **81.6 (S)** — up from 80.5; still #2 overall.**
> v5's pre-`VRAMHANDOFF` sample drop (kb §9) yields a clean VRAM peak of 8,066,096 B
> (0.96×, was signature-clamped); memory axis 85.0 → 87.9 (main 11,237,600 B,
> ARAM 1,509,920 B). Coverage demo. The v4 figures below are superseded where they
> differ; identity/controls/similarity sections remain valid. Sidecar: flycast
> `ebae3b513`, battery 5.

## 1. Verdict

| | |
|---|---|
| **Final score** | **82.2** (S) — #2 overall |
| Bottom line | A Katana/Ninja2-SDK casino minigame collection from the reference maker (Altron) that fits every DC region comfortably once measured correctly; the previous "G1 broken: emulator-exited" park was an instrumentation/harness artifact stack, not the game. **(battery v8 update, see banner above:** VRAM now scores on FB-masked content + 2×FB (sub 100.0, was 87.9); write-truth main RAM, measured for the first time, becomes the mild binding region instead (sub 89.7) — final rises to 82.2.) |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; vram-fb-masking re-run 2026-08-08 · battery v8 · flycast `f014a410c` |

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
attempt of the final battery pass; retry ran the full window. Battery v8 re-run hit
the same launch-flake class again (`emulator-exited` this time, leg 1) — auto-retry
(leg 2) ran the full window cleanly, used for the v8 figures.

## 4. Memory fit (axis: 89.7)

Table refreshed 2026-08-07 (battery v8) to the region keying this doc's last commit
(v5) never had: main on write-truth peak (v6), ARAM on content volume (v7), VRAM on
FB-masked content + 2×FB budget (v8, this task). The v5-era table is retained below
for history.

| Region | Peak / fit | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth) | 15,728,704 B | 16 MB | 93.8% | 89.7 | grep `MAINPROFILE`/`MAINHIST` |
| VRAM (FB-masked content + 2×FB) | 5,746,300 B (content_total 4,517,500 + 2×fb_bytes 1,228,800) | 8 MB | 68.5% | 100.0 | grep `VRAMPROFILE` (content_* fields) |
| ARAM (content, volume-keyed) | 1,413,091 B | 2 MB | 67.4% | 100.0 | grep `ARAMPROFILE` (content_* fields) |

Memory axis = min(region sub-scores) = 89.7 (regions aren't tradeable; main now binds,
mildly — this is moeru's first write-truth main measurement, 15,728,704 B vs. the old
11,237,600 B DMA-only figure, still comfortably under cap at u=0.938).

(v5-era address-keyed table, retained as history:)

| Region | Peak | DC capacity | Utilization | Evidence |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 11,237,600 | 16,777,216 | 0.67 | `CARTDMA` in raw log |
| VRAM (write-truth diff) | 9,711,616 | 8,388,608 | 1.16 | `VRAMPROFILE` (nz_total 4,523,535; nz above cap only 57,048) |
| ARAM (content, fill-excluded) | 1,509,920 | 2,097,152 | 0.72 | `ARAMPROFILE` content fields |

VRAM's raw peak-address was 16% over the 8 MB line, but the above-cap diff was the
GD BIOS logo framebuffer signature (57,048 B @ 0x943000 — REQUIREMENTS.md's
"9.4 mb during the Naomi logo show time" caveat, proven non-game by the dragntr3
splash-only control). v5's `score.py` excluded it via `scores.vram_bios_noise_excluded`.
**v8 retirement (spec `2026-08-07-vram-fb-masking-design.md` ruling 4):** that clamp is
now obsolete — the v5 pre-`VRAMHANDOFF` gating already removed the sample-leak noise
the clamp used to correct, so an exact match on a booted title would now mean the
gating regressed, not that BIOS noise needs excluding. The clamp was promoted to a
`MetricRegression` refusal canary instead; `scores.vram_bios_noise_excluded` is no
longer written by current `score.py`, and this run's `(peak, nz_above_cap)` —
(8,066,096, 0) under the pre-v8 address keying, or the v8 content/fb fields above —
does not match the retired signature `(0x943000, 57048)`, so the canary does not fire.
The game's own content fits every region either way.

## 5. Cart streaming (axis: 55.0)

1,135 DMA events · total 198.6 MB (v8 re-run: 208.3 MB) · unique 46.5 MB (v8: 46.5 MB) ·
re-read ratio 0.766 (v8: 0.7658) · steady-state 19.9 MB/min (v8: 19.93, reproduces
within run-to-run noise) — the attract loop re-streams its minigame assets from GD
continuously; a DC port would want them resident or repacked.

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

final (current, battery v8, from `assessments/moeru.metrics.json` — quoted, not
hand-computed):
final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 89.7^.40 · 55.0^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **82.2** (S)

(v4-era formula below is retained as history; v5 already moved memory 85.0 → 87.9 via
the pre-VRAMHANDOFF gating fix, and v8 moves it again 87.9 → 89.7 via the §4
region-keying catch-up — streaming/guts/controls/similarity are unchanged throughout.)
      = 85.0^.40 · 55.1^.20 · 85.0^.20 · 100.0^.10 · 100.0^.10 = **80.5** (S)
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
