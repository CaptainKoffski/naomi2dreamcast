# Sega Tetris (`sgtetris`) — portability assessment (parked)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Bottom line | First-ever end-to-end measurement of this title — battery v6's unified `dma\|pio` handoff fires at 20.0 s (trigger `pio`), closing kb §4.v's G1 blindness (`no-handoff-120s` with the game visibly running). The park is now real: ARAM content-high address reaches 3.94× the DC cap, but only **8 bytes** of content sit above the 2 MB line (`nz_above_cap = 8`) — the most extreme address-vs-volume divergence recorded, ahead of marstv's 81,598 B (kb §6 item 5). Main RAM (measured for the first time) and VRAM also read over-cap; the main write-truth peak (29,130,560 B) matches the stale v5 watermark almost exactly, confirming those writes were real cart content, not BIOS residue. Official 2000 DC port exists regardless. |
| Assessed | 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `sgtetris` (no clones — `parent: null` in controls.json). `tetkiwam` (Tetris Kiwamemichi, Success 2004, GD-ROM) is a separate family. |
| Maker / year | Sega, 1999 (controls.json; [tetris.wiki](https://tetris.wiki/Sega_Tetris)) |
| Genre / format | Puzzle ★ (Tetris variant), cart (`naomim2`, 33.7 MB) |
| Official DC port | **Yes — Sega Tetris (Dreamcast, Japan, 2000), with online play** ([tetris.wiki](https://tetris.wiki/Sega_Tetris), [MobyGames](https://www.mobygames.com/game/71419/sega-tetris/)). Assessment done as reference/validation data per GAME_FORMATS.md policy (a `Yes` is not a skip reason). |
| Community ports | Moot — official DC port exists; no community port needed. |
| Representative choice | Only member of its family (MAME parent, no clones). |

## 3. Boot & run evidence

Boots: **yes (measured)** · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/sgtetris.zip`
Attract/demo reached: **demo** — `shot-060s.png` (title, beach backdrop), `shot-121s.png`
(how-to-play attract overlay with a live gameplay board, beach backdrop), `shot-365s.png`
(online RANKING table), `shot-487s.png` (how-to-play attract overlay, Shibuya-crossing
backdrop), `shot-609s.png` (attract auto-play gameplay board, safari backdrop). The title
screen and how-to-play overlay each rotate through multiple 3D backdrops across the 600 s
window. `capture.coverage` was `null` in the raw sidecar; set to `"demo"` by this task —
the curated shots show live gameplay boards and a ranking screen, not just an idle title
loop.
Screenshots (curated from 10): `assessments/evidence/sgtetris/shot-060s.png`,
`shot-121s.png`, `shot-365s.png`, `shot-487s.png`, `shot-609s.png`.
Anomalies: kb §4.v's G1 blindness for this title is **CLOSED** — see § Gate.

## Gate

**G3 `aram peak > 2x DC capacity` — a real park, with the most extreme address-vs-volume divergence recorded.**

| Region | Peak (write-truth) | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM | 29,130,560 | 16,777,216 | 1.736 | nz_total 7,350,612 (3.87 MB changed below the cap, 3.14 MB above — `nz_above_cap = 3,289,898`; top nonzero 256 KB bucket at 27.75–28.0 MB); `dma_high_water = 0` (PIO-loaded, now measured via snapshot+diff instead); the write-truth peak matches the stale v5 CARTDMA-era watermark (29,130,560 B) almost exactly — those writes were real cart content, not BIOS residue |
| VRAM (write-truth) | 16,279,552 | 8,388,608 | 1.941 | nz_total 9,283,220 · above cap 5,634,894 |
| ARAM (content, fill-excluded) | 8,257,552 | 2,097,152 | **3.94** | content above cap **8 bytes only** (`nz_above_cap = 8`); raw nz_above2m is 32,768 B — the fill-exclusion is doing real work here. NOT the DMPD fill canary (that requires `nz_above_cap == 0x600000` exactly, kb §8/§4) |

Streaming: `dma_events = 0` · `pio_bytes = 27,167,524` (~27 MB streamed via PIO over the
600 s window — a lower bound; the counter (`CARTPIOCNT`) is cumulative from the first PIO
read, not gated by the handoff threshold — only the main-RAM handoff *baseline* snapshot
is taken at the 32 KB crossing) · 1,078 `CARTPIO offset=` pokes logged total. The entire cart loads and streams
by PIO — zero cart-DMA traffic the whole run.

**§6 checkpoint data point:** sgtetris is now the most extreme G3-aram address-vs-volume
divergence on record — 8 B of content above the 2 MB cap at content-high address u=3.94,
vs. marstv's previous record of 81,598 B (kb §6 item 5). Under a volume-keyed gate this
title would pass through with an effectively DC-fitting sound bank; under the current
address-keyed rule (kept for the whole v6 wave per the 2026-08-07 user ruling — checkpoint
decision deferred until all planned games are processed) it parks. Main RAM and VRAM are
both also measured over-cap here (1.74× and 1.94×), so even a softened ARAM rule would not
by itself unpark this title without also revisiting those two axes.

**What changed:** kb §4.v's G1 blindness (`no-handoff-120s` with the game visibly running,
zero `ARAMHANDOFF`/`CARTDMA` tags) is now **RESOLVED** — the unified `dma|pio` handoff
(fork commit `65f9f7857`, battery v6) baselines all three regions the instant cumulative
PIO `ROM_DATA` reads cross 32 KB, closing the blind spot without any cart-DMA dependency.
This title is measured end-to-end for the first time and parks on a real, evidenced gate
instead of an instrumentation false-negative. A regression golden
(`tools/assess/tests/test_metric_guards.py::test_sgtetris_pio_face_stays_measured`) now
guards this shape.

## 7. Controls (research done, for when unblocked)

Cabinet: standard Naomi 8-way stick + 2 rotate buttons (L/R) + start, 2 players.
MAME input ports: `naomi`. A stock DC pad maps 1:1 (d-pad + A/B rotate) — decisively,
the official DC port shipped exactly that.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sgtetris)
(8-way joystick + 6-button JVS standard declaration, 2P);
[tetris.wiki](https://tetris.wiki/Sega_Tetris) (rotate L/R buttons, left-turn-only
secret bonus, NAOMI DAS bug carried into the DC port).
