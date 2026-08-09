# Trizeal (Japan) (GDL-0026) (`trizeal`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **72.5 (A)** |
| Bottom line | The wave's only title with genuine VRAM content pressure: FB-masked content + double framebuffer is 9.39 MB (u 1.119, sub-score 63.6) — the binding region even under content keying — while main (0.34×) and ARAM (0.30×) fit outright; Triangle Service's own 2005 DC port ships the game and proves the texture trim possible. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` (see History) |

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
Screenshots (5 kept of 10):
- `evidence/trizeal/shot-060s.png` — title: TRIZEAL logo over 3D ship, EXTEND table, ©2004 TRIANGLE SERVICE
- `evidence/trizeal/shot-182s.png` — attract gameplay: enemy formation, GAME OVER overlay, missile trails
- `evidence/trizeal/shot-365s.png` — attract gameplay: enemy waves, rainbow item gem, player ship firing
- `evidence/trizeal/shot-426s.png` — attract gameplay: large explosion, twin beam lasers, GAME OVER
- `evidence/trizeal/shot-548s.png` — RANK/SCORE/STAGE/NAME 20-row ranking table

Anomalies: VRAM, ARAM, guts, controls, and screenshots reproduced byte-identical
across the v8→v9 re-capture. Two counters moved by capture-timing noise only:
main `nz_total` 5,725,402 → 5,725,400 B (−2 B) and streaming `steady_mb_per_min`
10.630 → 10.623 MB/min (streaming sub-score 69.7 → 69.8). Neither moves the
memory sub-score (still 63.6, VRAM-bound) or the final score (still 72.5 A).

## 4. Memory fit (axis: 63.6)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 5,725,400 | 16,777,216 | 0.3413 | 100.0 | address peak 32,548,960 (u 1.940, informational — 43,040 B *past* the `0x1F00040` signature, near it but not equal, so NOT counted as an instance, kb §6 item 3) · `nz_above_cap` 4,102,336 · `dma_high_water` 27,750,592 (the §6 item 3 27–30 MB GD cluster band, informational-only from v6 on) |
| VRAM (FB-masked content + 2×FB) | 9,386,488 (content_total 8,157,688 + 2×fb_bytes 614,400) | 8,388,608 | 1.119 | 63.6 | **binding region — genuine content pressure**: 8.16 MB of masked content, nz_total 8,666,757; the wave's only title over cap on content, not extent (raw address peak 16,478,358, u 1.964) |
| ARAM (content volume, fill-excluded, `content_total`) | 632,368 | 2,097,152 | 0.3015 | 100.0 | address peak 2,097,136 — the exact illvelo/karous 16-under-2-MiB value, third instance, **second developer**: reads as a GD-era SDK/sound-driver allocation constant, not an engine quirk (kb §6 item 1) |

Watermarks (informational, content-scan — stale-data prone): main 32,548,960 ·
vram 16,478,358 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 69.8)

DMA events 1,704 · total 129,357,824 B (123.4 MB) · unique 42,684,416 B (40.7 MB) ·
re-read ratio 0.6700 · steady-state 10.623 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 1,115,456 B (the ~1 MB GD DIMM bootstrap; the wave's other GD
titles carried ~2.1 MB).

## 6. Guts (axis: 85.0)

Code 1,048,576 B (carve `base 0x8c020000`, entry `0x8c021000`, header title "TRIZEAL" —
a 1 MB boot blob, half the wave's usual 2 MB) · functions 2,095 · MMIO refs: scif 9,
rtc 3, g2ext 645 · BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel, 8-way stick + 3 buttons — A = Shot, B = weapon/form
change (Wide / Missile / Laser), C = Bomb. `controls.device_class = stick`. MAME input
ports: `naomi` (INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506).
Proposed DC mapping: d-pad + 3 face buttons, 1:1 — the DC review's verdict: "the
Dreamcast D-pad is up to the job".
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Shmups Wiki](https://shmups.wiki/library/Trizeal);
[Bordersdown DC review](https://bordersdown.net/articles/retro/2740855-trizeal-review-sega-dreamcast).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 63.6^.40 · 69.8^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **72.5 (A)**
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- **Porting is redundant**: the official 2005 DC build (TATE, VGA, extra modes) is
  canonical and has a 2023 English patch. Assessment value: the only wave title where a
  real VRAM content trim (8.16 MB → 8 MB budget minus framebuffers) is part of what its
  shipped port proves possible — the binding region here is real porting work, not a
  measurement artifact.
- Main above-cap content (4,102,336 B by address) is placement, not volume, under
  content keying; the shipped DC port is proof the game fits 16 MB after a real downport.
- ROT270 vertical — solved in the official port (4 screen modes).
- Engine lineage: Triangle Service's XII Stag (hidden XII ship here), Exzeal, Shooting
  Love 2007 (`sl2007`, Naomi cart, still pending in the queue) — expect similar metric
  shapes when `sl2007` is assessed.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v8 | 2026-08-08 | 37.7 (C) | First assessment (FB-masked VRAM keying); main address-keyed peak 32.5 MB bound at u 1.940; genuine VRAM content pressure (fit-u 1.119) identified — kb §6 item 3 |
| v9 | 2026-08-08 | 72.5 (A) | Scoring-only re-key (no re-capture): main keyed on content volume `nz_total` 5,725,402 B; binding region moved to VRAM — spec `2026-08-08-main-content-rekey-design.md` |
| v9 | 2026-08-09 | 72.5 (A) | ranking-groom chunk 4: fresh v9 capture, provenance v8→v9 (scoring keys unchanged); main `nz_total` −2 B and streaming `steady_mb_per_min` 10.630→10.623 MB/min (streaming sub-score 69.7→69.8) — capture-timing noise only, final unchanged |
