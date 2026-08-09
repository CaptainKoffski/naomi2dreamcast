# Cannon Spike / Gun Spike (`cspike`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **42.8 (B)** |
| Bottom line | ARAM is the real problem: 3.65 MB of non-fill sound content (1.742× the DC's 2 MiB, with 1.65 MB genuinely above the cap) binds the memory axis at sub-score 20.3 — main content fits at 0.50× and VRAM's FB-masked content now measured for real (3.26 MB content + 2×614 KB double-framebuffer budget = 4.49 MB, 0.535×) also fits comfortably, superseding the v7 address-peak fallback (1.254×, sub-score 39.9) — but the official 2000 DC port is shipped proof the rework is possible and is the ready-made reference. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `cspike` (no clones — `parent: null` in controls.json) |
| Maker / year | Psikyo / Capcom, 2000 (controls.json) |
| Genre / format | Shmup ★ (multi-directional arena shooter, *Gun Spike* in Japan), cart (`naomim2`, 63.6 MB) |
| Official DC port | **Yes — Cannon Spike (Dreamcast, 2000, Capcom — JP/NA/EU)** ([Wikipedia](https://en.wikipedia.org/wiki/Cannon_Spike), [Sega-16](https://www.sega-16.com/2023/11/cannon-spike/)). Assessed as reference/validation data per GAME_FORMATS.md policy. |
| Community ports | Moot — official DC port exists. |
| Representative choice | Only member of its family (MAME parent, no clones). |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/cspike.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-304s.png` is an in-game attract-demo frame
(Arthur HUD, GAME OVER card); `shot-060s.png` title, `shot-609s.png` character-art
attract screen. Sidecar `capture.coverage = "demo"`.
Screenshots: `evidence/cspike/shot-060s.png` · `evidence/cspike/shot-304s.png` ·
`evidence/cspike/shot-609s.png` (curated from 10).
Anomalies: none — DMA loader (main high-water live, unlike the gwing2/sgtetris PIO face).

## 4. Memory fit (axis: 20.3)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,435,421 | 16,777,216 | 0.5028 | 100.0 | address peak 17,948,000 (u 1.070) · 1,142,859 nonzero above cap · `dma_high_water` 17,948,000 (= peak — DMA loader) |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total` + 2×`fb_bytes`) | 4,486,431 | 8,388,608 | 0.535 | 100.0 | content_total 3,257,631 · fb_bytes 614,400 (double-buffered → 1,228,800) — v8 real measurement, replaces the v7 address-peak fallback (peak 10,516,642, u 1.254, sub-score 39.9); raw write-truth peak still 10,516,642 (nz_total 3,637,559 · 1,872,598 above cap, informational) |
| ARAM (content volume, fill-excluded, `content_total`) | 3,654,043 | 2,097,152 | 1.742 | 20.3 | address peak 8,257,552 (u 3.94, the pre-v7 gated keying) · 1,649,859 content above cap — **binding region** |

Watermarks (informational, content-scan — stale-data prone): main 17,948,000 ·
vram 10,516,642 · aram 8,388,608 (boot-time fill, not content).

## 5. Cart streaming (axis: 64.9)

DMA events 152 · total 132.7 MB · unique 34.5 MB · re-read ratio 0.7402 ·
steady-state 12.993 MB/min (`short_window: false`) · PIO 2,281,280 B

## 6. Guts (axis: 85.0)

Code 2,097,152 B · functions 1,707 · MMIO refs: scif 2, rtc 4, g2ext 50 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → 85.0.
Boot blob carved at base `0x0c020000`, entry `0x0c021000`, header title `GUN SPIKE`.
No Sega library version banners among the 500 captured `sdk_strings` — game/engine
strings dominate (including `dc_pad->id/support/on/off` debug fields).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 3 used buttons (Shoot · Mark lock-on · Attack
melee), 2 players. MAME input ports: `naomi`. Stock-pad workable; the official DC port
shipped on the standard controller (arcade stick recommended by period reviews).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=cspike)
(8-way joystick + 6-button JVS standard declaration, 2P);
[Wikipedia](https://en.wikipedia.org/wiki/Cannon_Spike) (Shoot / Mark / Attack,
three specials on combinations).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 20.3^.40 · 64.9^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **42.8 (B)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **ARAM's 1,649,859 B of real above-cap sound content is the binding cost** — a
  genuine memory problem regardless of the address-vs-volume keying (contrast
  `gwing2`, where that distinction was the entire story).
- What would raise the score: the azumanga playbook — ARAM bank-structure dump
  (`FLYCAST_ARAMDUMP` + `tools/assess/parse_osb.py`) to check whether the above-cap
  content is position-independent OSB banks + streamable BGM; plus the official DC
  port as an audio-budget reference (Capcom fit it in 2 MiB in 2000). ARAM is now
  the *only* memory region needing rework — VRAM and main both fit comfortably
  under the real (content-keyed) measurements.
- VRAM no longer needs texture reduction: the v8 FB-mask fields (`content_total`
  3,257,631 + 2×`fb_bytes` 614,400) show the real fit at 0.535×, sub-score 100.0 —
  the v7 doc's 1.254×/39.9 was the address-peak fallback, now superseded. Main
  content fits at 0.503× (`nz_total`); its raw address peak (17,948,000 B, u 1.070,
  1.14 MB nonzero above cap) still flags layout/relocation attention but doesn't
  score — content volume does.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v5 | 2026-08-06 | PARKED G3-ARAM | ARAM address-keyed peak 8,257,552 (u 3.94) gated before axes (flycast `ebae3b513`) |
| v7 | 2026-08-07 | 42.8 (B) | Un-parked: ARAM re-keyed on content volume (kb §6 checkpoint) — 3,654,043 B (u 1.742) scores instead of gating and binds memory at 20.3 |
| v9 | 2026-08-08 | 42.8 (B) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`) — 8,435,427 (u 0.503) replaces the address peak; final unchanged, ARAM still binds |
| v9 | 2026-08-09 | 42.8 (B) | ranking-groom chunk 5: fresh v9 capture (was v7) — VRAM FB-mask fields measured for real (content_total 3,257,631 + 2×fb_bytes 614,400 → u 0.535, sub-score 100.0, was fallback address-peak u 1.254/39.9); every other raw counter reproduced within noise (main nz_total ±6 B, streaming bandwidth +0.003 MB/min); ARAM still binds memory at 20.3, final unchanged 42.8 (B) |
