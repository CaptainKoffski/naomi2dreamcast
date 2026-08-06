# Cannon Spike / Gun Spike (`cspike`) — portability assessment (parked)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Bottom line | Clean demo-coverage run; genuine G3: ARAM content peaks at 7.87 MB (3.94× DC) with 1,649,859 B of real (non-fill) sound content above the 2 MiB cap — zerogu2/azumanga class. VRAM (1.25×) and main RAM (1.07×, properly measured here) are also over budget but scoreable; ARAM alone gates. The official 2000 DC port is shipped proof the rework is possible and is the ready-made reference. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

**G3 `aram peak > 2x DC capacity` — genuine sound-content overflow.**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 17,948,000 | 16,777,216 | 1.07 | watermark equal — mild overrun |
| VRAM (write-truth diff) | 10,516,642 | 8,388,608 | 1.25 | nz_total 3,608,767 · above cap 1,872,598 |
| ARAM (content, fill-excluded) | 8,257,552 | 2,097,152 | **3.94** | content above cap 1,649,859 |

Streaming (informational): 152 DMA events · total 132.7 MB · unique 34.5 MB ·
re-read 0.7402 · steady 12.99 MB/min.

Had ARAM not gated, this title would still have scored low on memory (main 1.07×,
VRAM 1.25×) — the park is consistent with the measurements, not a semantics artifact
(contrast gwing2).

What would unblock: the azumanga playbook — ARAM bank-structure dump
(`FLYCAST_ARAMDUMP` + `tools/assess/parse_osb.py`) to check whether the 1.65 MB
above-cap content is position-independent OSB banks + streamable BGM; plus the
official DC port as an audio-budget reference (Capcom fit it in 2 MiB in 2000).

## 7. Controls (research done, informational)

Cabinet: standard Naomi 8-way stick + 3 used buttons (Shoot · Mark lock-on · Attack
melee), 2 players. MAME input ports: `naomi`. Stock-pad workable; the official DC port
shipped on the standard controller (arcade stick recommended by period reviews).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=cspike)
(8-way joystick + 6-button JVS standard declaration, 2P);
[Wikipedia](https://en.wikipedia.org/wiki/Cannon_Spike) (Shoot / Mark / Attack,
three specials on combinations).
