# Giga Wing 2 (`gwing2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **79.0 (A)** |
| Bottom line | Clean full-window cart shmup whose official 2001 DC port already proves the fit — under content keying every region is under cap (ARAM binds at 0.964×, and its 48,674 B above the 2 MB address line is placement, not volume) — assessed as reference/validation data per GAME_FORMATS.md policy since the DC port exists regardless. |
| Assessed | capture 2026-08-07 · battery v7 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `gwing2` (no clones — `parent: null` in controls.json) |
| Maker / year | Takumi / Capcom, 2000 (controls.json) |
| Genre / format | Shmup ★ (vertical shooter, score/reflect system), cart (`naomim2`, 57.6 MB) |
| Official DC port | **Yes — Giga Wing 2 (Dreamcast, 2001, Capcom — JP+NA release)** ([shmups.wiki](https://shmups.wiki/library/Giga_Wing_2), [GameFAQs](https://gamefaqs.gamespot.com/dreamcast/479801-giga-wing-2)). Assessed as reference/validation data per GAME_FORMATS.md policy. |
| Community ports | Moot — official DC port exists. |
| Representative choice | Only member of its family (MAME parent, no clones). |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/gwing2.zip`
(single clean zip leg)
Attract/demo reached: **title (conservative lower bound)** — the attract loop verifiably
cycles (title `shot-060s` → red title card → Capcom logo → ... → character-intro art
`shot-487s` → TAG SCORE RANKING `shot-609s`), but no sampled frame caught in-game demo
footage, so `capture.coverage = "title"`.
Screenshots: `evidence/gwing2/shot-060s.png` · `shot-487s.png` · `shot-609s.png`
(curated from 10).
Anomalies: the cart→main-RAM load path is PIO — `dma_high_water = 0` despite 1,370
cart-DMA events (kb §4.v, resolved in battery v6: the unified `dma|pio` handoff baselines
main RAM directly, so main is write-truth measured, not blind). Streaming figures below
count non-main DMA only; `pio_bytes` 57,520,864 B is the measured lower bound for the
PIO-streamed traffic they don't cover.

## 4. Memory fit (axis: 87.7)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,050,490 | 16,777,216 | 0.480 | 100.0 | address peak 16,433,920 (u 0.980, informational) — equals the old informational watermark byte-for-byte: real game writes all along (kb §4.v) · `nz_above_cap` 0 · `dma_high_water` 0 (PIO loader) |
| VRAM (write-truth peak, post-handoff) | 8,066,048 | 8,388,608 | 0.9615 | 87.9 | nz_total 3,444,253 · 0 above cap · pre-v8 sidecar (no FB-masked `content_total`) — the peak fallback can only under-score |
| ARAM (content volume, fill-excluded, `content_total`) | 2,021,207 | 2,097,152 | 0.9638 | 87.7 | **binding region** · content-high address 8,372,160 (u 3.99 — the pre-v7 park driver) · `nz_above_cap` 48,674 B, the smallest observed by far (zerogu2: 2.1 MB, azumanga: 1.7 MB); OSB banks are position-independent, so compaction covers it |

Watermarks (informational, content-scan — stale-data prone): main 16,433,920 ·
vram 9,692,984 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 74.6)

Partial — non-main DMA only (PIO loader, §3): DMA events 1,370 · total 11.2 MB ·
unique 3.1 MB · re-read ratio 0.7255 · steady-state 1.159 MB/min (`short_window: false`) ·
PIO 57,520,864 B (57.5 MB over the window, first measured in battery v6 — a lower bound
for the main-RAM loader traffic the DMA figures don't count)

## 6. Guts (axis: 85.0)

Code 1,572,864 B · functions 1,560 · MMIO refs: scif 2, rtc 2, g2ext 52 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc` → 85.0
Carved at base `0x0c021000`, entry `0x0c021000`, header title `GIGAWING2 JAPAN`.
SDK strings (sidecar `guts.sdk_strings`): NAOMI LIBRARY Ver 0.9 AM R&D (Apr 2000 build),
NLOBJPUT 0.99, NLSPRITE 0.2, nlam 1.00, plus NEC's KAMUI2 Ver 16,3,2,0 and
KAMUI-Darkness (kmdk 1,3,0,0) graphics libraries.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 2 used buttons (shot · bomb), 2 players. MAME
input ports: `naomi`. Stock-pad trivial; the official DC port shipped A=shot / B=bomb
and added a dedicated autofire on R.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=gwing2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC systems FAQ](https://gamefaqs.gamespot.com/dreamcast/479801-giga-wing-2/faqs/12525)
(A shot / B bomb / R autofire).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 87.7^.40 · 74.6^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **79.0 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Port-planning takeaway: everything fits — and the official DC port (2001) already
  proved it.** This assessment is reference/validation data for the pipeline, not a port
  candidate ranking.
- **ARAM is the binding region at 0.964× as content volume.** The 48,674 B sitting above
  the 2 MB address line is placement, not volume — OSB banks are position-independent
  (azumanga live verification), so a rebuild-and-move compaction covers it.
- **Main RAM is address-sparse:** content 8.05 MB (0.480×) against an address peak of
  16,433,920 B (0.980× cap) — volume fits easily; layout/relocation attention for the
  high-address writes.
- **The streaming axis sees non-main DMA only.** The PIO loader moved 57.5 MB over the
  window (measured lower bound) — a real port's streaming budget is higher than §5's DMA
  figures suggest.
- Coverage is a conservative `title` annotation: the attract loop cycles but no sampled
  frame verified in-game demo footage, so measured figures may understate gameplay
  pressure.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v5 | 2026-08-06 | PARKED `G3 memory: aram peak > 2x DC capacity` | ARAM content high-water *address* read 3.99× cap under address keying while above-cap volume was only 48,662 B — the divergent case that drove the §6 checkpoint (kb §6 item 5) |
| v6 | 2026-08-07 | PARKED (gate re-run) | Unified `dma|pio` handoff measured main for the first time: write-truth peak 16,433,920 (u 0.980, fits — old watermark was real writes); `pio_bytes` 57.5 MB first measured; tiny-volume ARAM class reproduced (48,674 B, 12 B run-to-run delta) — kb §4.v resolved |
| v7 | 2026-08-07 | 78.6 (A) | §6 checkpoint re-keyed G3-ARAM on content volume (spec `2026-08-07-aram-gate-volume-design.md`): `content_total` 2,021,207 (u 0.964) — un-parked; memory 86.5, main binding |
| v9 | 2026-08-08 | 79.0 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` 8,050,490 (u 0.480); memory axis 87.7, binding moved to ARAM (spec `2026-08-08-main-content-rekey-design.md`) |
