# Wave Runner GP (`wrungp`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **37.9 (C)** |
| Bottom line | All three memory regions exceed 1× — ARAM binds (content 3,798,539 B, u 1.811, sub-score 17.5, uncomfortably close to the u>2.0 gate) with main (1.338) and VRAM (1.370) also over capacity — and the ride-on jet-ski cab costs the controls axis (`pad_adaptable`, 50): the manual documents a no-motion-base configuration that reduces play to handlebar + throttle, which maps to stick X + trigger. Sega itself planned a DC port and cancelled it (GAME_FORMATS.md near-miss list). |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `wrungp` (covers clone `wrungpo` USA Rev A — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` lines 10997–10998, both `/* 0064 */`; cart ID 840-0064C per [arcade-history](https://www.arcade-history.com/?n=waverunner-gp&page=detail&id=3925)) |
| Maker / year | CRI / Sega, 2001 (MAME `GAME()` row; released August 2001 per [arcade-history](https://www.arcade-history.com/?n=waverunner-gp&page=detail&id=3925)). Cabinet co-developed with Yamaha Motor (staff roll in `guts.sdk_strings`: "Special Thanks YAMAHA MOTOR CO.,LTD.", Sega Mechanical/Electrical Design credits) |
| Genre / format | Jet-ski racing sim (sequel to *WaveRunner*, 1996 — [arcade-history](https://www.arcade-history.com/?n=waverunner-gp&page=detail&id=3925)), **cart** (`naomim2`, 48.1 MB per GAME_FORMATS.md) |
| Official DC port | **No — cancelled/unreleased.** GAME_FORMATS.md's near-miss list records `wrungp` among "cancelled-but-unreleased DC ports"; [arcade-history](https://www.arcade-history.com/?n=waverunner-gp&page=detail&id=3925) lists a Sega Dreamcast "WaveRunner: Prototype" ports row. Nothing shipped. |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Parent set (Japan); `wrungpo` is the USA Rev A of the same cart |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/wrungp.zip`
(battery log: `leg 1: wrungp.zip attempt 1 -> ran full window`)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`;
set after screenshot review). The full attract cycle runs from the first shot: `shot-060s.png`
in-engine demo on the harbor/cruise-ship course (PRESS START + FREE PLAY overlays),
`shot-121s.png` multi-rider race demo under a bridge (CRI ADX logo bug), `shot-182s.png`
title screen ("WaveRunner GP"), `shot-304s.png` canyon-course demo with Japanese caption
overlay ("波の動きも考えて操作してください。"), `shot-548s.png` dolphin-jump attract moment.
No static calibration/warning screen consumed any of the window.
Screenshots: `evidence/wrungp/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-304s.png` · `shot-548s.png` (curated from 10; `shot-243s.png` open-water transition,
`shot-365s.png`/`shot-426s.png` further demo angles, `shot-487s.png` title dup,
`shot-609s.png` canyon dup curated out)
Anomalies: none — no flake, no display blindness. The game runs its attract loop despite no
drive board being emulated (see §9).

## 4. Memory fit (axis: 17.5)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 22,449,561 | 16,777,216 | 1.3381 | 36.5 | address peak 32,247,044 (u 1.922 — address-keyed it would sit just under the gate) · `nz_above_cap` 10,117,907 · `dma_high_water` 31,453,632 (u 1.875, informational) — grep `CARTDMA` in raw log |
| VRAM (FB-masked content fit, `content_total + 2×fb_bytes`) | 11,492,890 | 8,388,608 | 1.3701 | 35.2 | `content_total` 10,264,090 + 2×`fb_bytes` 614,400 (double-buffered 640×480×2) · `nz_total` 10,840,206 (u 1.292) · address peak 15,931,286 (u 1.899) · `nz_above_cap` 5,730,125 — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 3,798,539 | 2,097,152 | 1.8113 | **17.5** | **binding region** · address peak 8,257,552 (u 3.938, position artifact) · `nz_above_cap` 1,809,715 — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 32,247,044 ·
vram 15,931,286 · aram 8,388,608 (the boot-time "DMPD" fill, not content).
Risk flag: main watermark ≈ address peak (1.92×) sits well above the scored content
volume (1.34×) — placement is spread, but the content itself is over-budget regardless.

## 5. Cart streaming (axis: 70.6)

DMA events 973 · total 137.9 MB (144,603,136 B) · unique 55.1 MB (57,755,648 B) ·
re-read ratio 0.6006 · steady-state 11.247 MB/min (`short_window: false`) ·
PIO 2,360,640 B

## 6. Guts (axis: 80.0)

Code 33,423,360 B (carve `base 0x8c020000`, entry `0x0c021000`, header title
"WAVE RUNNER GP") · functions 3,161 · MMIO refs: scif 3, rtc 3, g2ext 93 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc`+`code_over_4mb` → −20.
SDK strings: nlam Ver 0.96 / nlajamma Ver 1.02 ("NAOMI LIBRARY FOR AM"), libsnd Ver.1.03b,
CRI SPR2D Ver 0.803, zlib inflate 1.1.3, CRI ADX streamed BGM (`wr_ope_*.adx`,
`wr_pla_*.adx`) — AM-library stack plus CRI middleware, not the Katana-derived loader
family (loader match no).

## 7. Controls (axis: 50.0)

Cabinet: ride-on jet-ski body (Yamaha WaveRunner replica) the player sits on and leans —
handlebar steering with a squeeze throttle lever, VIEW button, START; motion base driven
by an air compressor with a drive board ("Air Compressor drives the Ride during game" —
owner's manual; `guts.sdk_strings`: "INITIALIZING MARINE JET / DO NOT TOUCH MARINE JET",
"DRIVE BD ERROR", "Drive Control Program" staff credit).
Input channels (primary source, Flycast fork `wrungp_inputs`,
core/hw/naomi/naomi_roms_input.h:342, wired at naomi_roms.cpp:4179/4206): analog
**HANDLE BAR** (Full, ch 0), **ROLL** (Full, ch 2), **PITCH** (Full, ch 3),
**THROTTLE LEVER** (Half, ch 4, inverted), plus VIEW + START digital. MAME assigns only
the generic `naomi` digital port set (`GAME( 2001, wrungp, naomi, naomim2, naomi, … )`,
src/mame/sega/naomi.cpp @59e7c0b line 10998) — a placeholder, not the real cab.
The owner's manual's test mode calibrates exactly three pots — HANDLE BAR VOLUME /
ROLL VOLUME / THROTTLE LEVER VOLUME — and states for the base-less cabinet variant:
"Being that this unit has no base, you will not be able to set the Roll Volume Setting"
([manual, ManualsLib #1577781](https://www.manualslib.com/manual/1577781/Sega-Waverunner-Gp.html)),
i.e. **real hardware supports a configuration without the roll/pitch motion inputs**.
`controls.device_class = pad_adaptable`: the supported reduced scheme (handle + throttle +
VIEW) maps cleanly to DC pad stick X + analog trigger + face button; it is not `awkward`
(no channel overflow in the reduced config — contrast `alpilota`'s irreducible 5 axes)
and not `stick` (the cab is not a joystick panel, and the motion axes 2/3 are simply
dropped, as Sega's own no-base cabinet drops roll).
Proposed DC mapping: stick X = handlebar, R trigger = throttle, A = VIEW, Start = Start;
optional stick Y = pitch/lean flavor.
Sources (full parity in sidecar `controls.sources`): Flycast `wrungp_inputs` descriptor ·
MAME naomi.cpp `GAME()` row ·
[Sega WaveRunner GP owner's manual](https://www.manualslib.com/manual/1577781/Sega-Waverunner-Gp.html) ·
[arcade-history](https://www.arcade-history.com/?n=waverunner-gp&page=detail&id=3925) ·
ROM-internal strings (sidecar `guts.sdk_strings`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 17.5^.40 · 70.6^.20 · 80.0^.20 · 50.0^.10 · 40.0^.10 = **37.9 (C)**
Similarity inputs: developer match no (CRI), SDK overlap partial, loader match no → 40.0.

## 9. Risks & notes

- **Every region is over budget** — this is a whole-image diet, not a single-region trim:
  main content 1.34×, VRAM content 1.37×, ARAM content 1.81×. ARAM's 1.81 is close enough
  to the u>2.0 gate that a run-to-run delta could park the title.
- **ARAM trim path**: BGM is already CRI ADX streamed from cart (`wr_*.adx` files in
  `guts.sdk_strings`), so the 3.8 MB ARAM content is largely effect/voice banks — the
  `azumanga` OSB compaction playbook applies (`tools/assess/parse_osb.py` on a
  `FLYCAST_ARAMDUMP`).
- **Drive board must be stubbed, not ported**: the ROM checks for it ("NO DRIVE BOARD",
  "WIRING TEST ERROR", "DRIVE BD NOT READY" in `guts.sdk_strings`) yet the battery run
  reached full attract with no drive board emulated — the check does not hard-block, a
  good sign for a DC build that has no motion base by definition.
- Main-RAM write-truth (v6+ metric) includes CPU writes; `dma_high_water` (1.875×) is
  informational. The address peak (1.922×) shows placement spread nearly to the 32 MB
  line — a port relocates, but the 22.4 MB of content still needs ~6 MB cut.
- Sega cancelled its own DC port (GAME_FORMATS.md near-miss list) — weak negative signal
  on feasibility circa 2001, though cancellations were commonly commercial.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 37.9 (C) | initial assessment — ARAM content u 1.811 binds (sub 17.5), main 1.338 / VRAM 1.370 also over 1×; controls researched: ride-on cab (handle/roll/pitch/throttle per Flycast `wrungp_inputs`) → `pad_adaptable` via the manual's documented no-base configuration (battery's `stick` auto-hint corrected, final moved 40.6 B → 37.9 C) |
