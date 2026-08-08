# Cannon Spike / Gun Spike (`cspike`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 42.8 (B), unchanged** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v7 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 8,435,427 B (content-u 0.503) replaces peak 17,948,000 B (u 1.070).
> Memory axis 20.3, binding region now **aram** (was memory 20.3). Verdict section below is the capture-time (v≤8) record.

## 1. Verdict

| | |
|---|---|
| **Final score** | **42.8 (B)** — un-parked 2026-08-07 (battery v7); was `PARKED — G3 memory: aram peak > 2x DC capacity` under the old address-keyed rule |
| Bottom line | Clean demo-coverage run. The §6 checkpoint re-keys G3-ARAM on content volume: `content_total` = 3,654,043 B (u = 1.742, under the u>2.0 gate) — but the real 1,649,859 B of non-fill sound content above the 2 MiB cap doesn't disappear, it just scores instead of gating, landing the lowest sub-score (20.3) and binding the memory axis. VRAM (1.25×, sub-score ~39.9) and main RAM (1.07×, sub-score ~72.4, properly measured here) are also over budget but milder. Final **42.8 (B)**. The official 2000 DC port is shipped proof the rework is possible and is the ready-made reference. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |

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

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/cspike.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-304s.png` is an in-game attract-demo frame
(Arthur HUD, GAME OVER card); `shot-060s.png` title, `shot-609s.png` character-art
attract screen. Sidecar `capture.coverage = "demo"`.
Screenshots: `assessments/evidence/cspike/shot-060s.png`, `shot-304s.png`, `shot-609s.png` (curated from 10).
Anomalies: none — DMA loader (main high-water live, unlike the gwing2/sgtetris PIO face).

## Gate

**No gate — un-parked 2026-08-07 (battery v7): ARAM re-keyed on content volume, but the real above-cap sound content still binds the memory axis at its lowest sub-score (20.3) — final 42.8 (B).**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth diff) | 17,948,000 | 16,777,216 | 1.07 | nz_total 8,435,427 · above cap 1,142,859; sub-score ~72.4 |
| VRAM (write-truth diff) | 10,516,642 | 8,388,608 | 1.25 | nz_total 3,608,767 · above cap 1,872,598; sub-score ~39.9 |
| ARAM (content volume, fill-excluded) | 3,654,043 | 2,097,152 | **1.742** | `content_total` (§6 volume-keyed, battery v7) — sub-score 20.3, the binding region; old content-high address peak 8,257,552 (u=3.94, pre-v7 keying, gated) unchanged, same 1,649,859 B above the 2 MB line either way |

Streaming (informational): 152 DMA events · total 132.7 MB · unique 34.5 MB ·
re-read 0.7402 · steady 12.99 MB/min.

Un-parked but still the low axis in the sidecar: main 1.07× (sub-score ~72.4) and VRAM
1.25× (sub-score ~39.9) are both moderately over cap, but ARAM's real 1.65 MB
above-cap content computes the lowest sub-score (20.3, u=1.742) and binds the axis — this
was a real memory problem regardless of the ARAM address-vs-volume semantics (contrast
gwing2, where that distinction was the entire story).

What would still raise the score: the azumanga playbook — ARAM bank-structure dump
(`FLYCAST_ARAMDUMP` + `tools/assess/parse_osb.py`) to check whether the 1.65 MB
above-cap content is position-independent OSB banks + streamable BGM; plus the
official DC port as an audio-budget reference (Capcom fit it in 2 MiB in 2000).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 3 used buttons (Shoot · Mark lock-on · Attack
melee), 2 players. MAME input ports: `naomi`. Stock-pad workable; the official DC port
shipped on the standard controller (arcade stick recommended by period reviews).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=cspike)
(8-way joystick + 6-button JVS standard declaration, 2P);
[Wikipedia](https://en.wikipedia.org/wiki/Cannon_Spike) (Shoot / Mark / Attack,
three specials on combinations).
