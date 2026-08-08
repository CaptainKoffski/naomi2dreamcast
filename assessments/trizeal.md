# Trizeal (Japan) (GDL-0026) (`trizeal`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 72.5 (A), was 37.7 (C)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 5,725,402 B (content-u 0.341) replaces peak 32,548,960 B (u 1.940).
> Memory axis 63.6, binding region now **vram** (was memory 12.4). Verdict section below is the capture-time (v≤8) record.

## 1. Verdict

| | |
|---|---|
| **Final score** | **37.7** (C) |
| Bottom line | Boots and demos cleanly; the binding axis is main RAM at u=1.940 (address-keyed peak 32.5 MB, 43 KB past — but not equal to — the `0x1F00040` shared-structure value, with 4.1 MB of real above-cap content). Distinctive in this wave: **the first title with genuine VRAM content pressure** — 8.16 MB of FB-masked content gives fit-u 1.119 (sub 63.6) even after v8 masking — and its ARAM address peak is the exact 16-under-2-MiB value (2,097,136 B) illvelo/karous carry, now seen across two unrelated developers. Triangle Service's own 2005 DC port ships the game regardless. |
| Assessed | 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `trizeal` (no clones — single GAME line, MAME naomi.cpp @59e7c0b line 11265; ROM_START 8695–8710, PIC `317-5103-JPN`, ships `trizeal-default-eeprom.bin` line 8700) |
| Maker / year | Triangle Service, 2004 |
| Genre / format | Shmup ★ (vertical, ROT270), **GD-ROM** GDL-0026, machine `naomigd` |
| Official DC port | **Yes** — JP 2005-04-07, published by Triangle Service; adds Score Attack + two minigames, 4 screen modes incl. **TATE**, VGA-compatible ([Wikipedia](https://en.wikipedia.org/wiki/Trizeal), [LaunchBox](https://gamesdb.launchbox-app.com/games/details/9588-trizeal), [shmups forum DC TATE list](https://shmups.system11.org/viewtopic.php?f=1&t=33531)). Later: PS2 *Trizeal Remix* 2006, X360 *Shooting Love, 200X* 2009, Steam *TRIZEAL Remix* 2016 (Degica) |
| Community ports | No Naomi→DC conversion found (searched 2026-08-08) — moot given the official port. Scene work targets the DC release: English translation patch v1.0 by Derek Pascarella, 2023-10-10 ([GitHub](https://github.com/DerekPascarella/Trizeal-EnglishPatchDreamcast), [dreamcast-talk t=16907](https://www.dreamcast-talk.com/forum/viewtopic.php?f=52&t=16907), [romhacking](https://www.romhacking.net/translations/7073/)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/trizeal.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle across the 10 shots: title (rotating 3D ship display, multiple angles) → live demo gameplay (enemy formations, item gem, GAME OVER frames) → 20-row score ranking.
Screenshots kept (5 of 10):
- `assessments/evidence/trizeal/shot-060s.png` — title: TRIZEAL logo over 3D ship, EXTEND table, ©2004 TRIANGLE SERVICE
- `assessments/evidence/trizeal/shot-182s.png` — attract gameplay: enemy formation, GAME OVER overlay, missile trails
- `assessments/evidence/trizeal/shot-365s.png` — attract gameplay: enemy waves, rainbow item gem, player ship firing
- `assessments/evidence/trizeal/shot-426s.png` — attract gameplay: large explosion, twin beam lasers, GAME OVER
- `assessments/evidence/trizeal/shot-548s.png` — RANK/SCORE/STAGE/NAME 20-row ranking table

Deleted surplus (5): three additional title-screen angles of the rotating ship, one near-duplicate gameplay frame, one transition frame.
Anomalies: none.

## 4. Memory fit (axis: 12.4)

| Region | Peak / fit | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth) | 32,548,960 (`0x1F0A860`) | 16,777,216 | 1.940 | 12.4 (binding) | `MAINPROFILE`; 43,040 B *past* the `0x1F00040` signature — near it, not equal, so NOT counted as an instance |
| VRAM (FB-masked content + 2×FB) | 9,386,488 (content_total 8,157,688 + 2×fb_bytes 614,400) | 8,388,608 | 1.119 | 63.6 | `VRAMPROFILE`; **genuine content pressure**: 8.16 MB of masked content, nz_total 8,666,757 — the wave's only title over cap on content, not extent (raw peak 16,478,358, u 1.964) |
| ARAM (content, volume-keyed) | 632,368 | 2,097,152 | 0.302 | 100.0 | `ARAMPROFILE`; address peak 2,097,136 — the exact illvelo/karous 16-under-2-MiB value, third instance, **second developer** |

**Checkpoint notes:**
1. Main: `nz_total` 5,725,402 B with `nz_above_cap` 4,102,336 B of real above-cap
   content — substantial, like karous (not an illvelo/sgtetris-style near-empty
   divergence). `dma_high_water` 27,750,592 B sits in the §6 item 3 27–30 MB GD cluster
   band (informational-only from v6 on).
2. VRAM is the wave's counter-example: after FB masking the content alone is 8.16 MB —
   fit-u 1.119 is real texture pressure a DC port must trim, unlike every other wave
   title where the raw peak was pure extent artifact. The official DC port evidently
   did that trim.
3. ARAM address peak 2,097,136 B (16 B under the DC cap) now appears on **two unrelated
   developers** (Milestone: illvelo/karous; Triangle Service: trizeal) — it reads as a
   GD-era SDK/sound-driver allocation constant, not an engine quirk; content here is
   only 632 KB (u 0.302). Relevant to the §6 item 1 ARAM-multiple discussion.
Watermarks (informational, content-scan — stale-data prone): main 32,548,960 · vram 16,478,358 · aram 8,388,608.

## 5. Cart streaming (axis: 69.7)

DMA events 1,704 · total 129,357,824 B (123.4 MB) · unique 42,684,416 B (40.7 MB) ·
re-read ratio 0.6700 · steady-state 10.630 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 1,115,456 B (the ~1 MB GD DIMM bootstrap; the wave's other GD
titles carried ~2.1 MB).

## 6. Guts (axis: 85.0)

Code 1,048,576 B (carve `base 0x8c020000`, entry `0x8c021000`, header title "TRIZEAL" —
a 1 MB boot blob, half the wave's usual 2 MB) · functions 2,095 · MMIO refs: scif 9,
rtc 3, g2ext 645 · BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0 — `stick`)

Cabinet: standard Naomi 2P panel, 8-way stick + 3 buttons — A = Shot, B = weapon/form
change (Wide / Missile / Laser), C = Bomb. MAME input ports: `naomi`
(INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506).
Proposed DC mapping: d-pad + 3 face buttons, 1:1 — the DC review's verdict: "the
Dreamcast D-pad is up to the job".
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Shmups Wiki](https://shmups.wiki/library/Trizeal);
[Bordersdown DC review](https://bordersdown.net/articles/retro/2740855-trizeal-review-sega-dreamcast).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 12.4^.40 · 69.7^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **37.7** (C)
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- **Porting is redundant**: the official 2005 DC build (TATE, VGA, extra modes) is
  canonical and has a 2023 English patch. Assessment value: with karous, a second
  DC-shipped ground-truth title scoring C on the address-keyed main axis — and the only
  wave title where a real VRAM content trim (8.16 MB → 8 MB budget minus framebuffers)
  is part of what its shipped port proves possible.
- ROT270 vertical — solved in the official port (4 screen modes).
- Engine lineage: Triangle Service's XII Stag (hidden XII ship here), Exzeal, Shooting
  Love 2007 (`sl2007`, Naomi cart, still pending in the queue) — expect similar metric
  shapes when `sl2007` is assessed.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.
