# Sega Tetris (`sgtetris`) — portability assessment (parked)

## 1. Verdict

| | |
|---|---|
| **Final score** | **parked** (G1 as recorded — see § Gate: instrumentation false-negative, game itself boots) |
| Bottom line | The game demonstrably boots and reaches its attract demo, but the battery cannot measure it: both legs emitted zero `CARTDMA`/`ARAMHANDOFF` tags, so no handoff was detected and no memory/streaming metrics exist. Unblocking is a tooling task, not a game problem. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: **yes (visually)** · handoff **never detected** (no `ARAMHANDOFF`/`CARTDMA` tag in either leg) · both legs aborted `no-handoff-120s` · rom: `naomi/sgtetris.zip`
Attract/demo reached: **demo** — `shot-060s.png` (Sega Tetris title, FREE PLAY) and `shot-121s.png` (how-to-play attract demo with gameplay board) prove the game runs.
Screenshots: `assessments/evidence/sgtetris/shot-060s.png`, `assessments/evidence/sgtetris/shot-121s.png`.
Anomalies: this is **not** the kb §4.a launch flake (that class shows the DC BIOS home menu; here the game itself is on screen). Content watermarks (informational, stale-data-prone) show real activity: main 29,130,560 / vram 15,230,976 / aram 8,388,608 (full-ARAM value is the known DMPD-style fill pattern class).

## Gate

**G1 `no-handoff-120s` — instrumentation false-negative (new class, kb §4.v).**
Evidence: sidecar `capture.handoff.seen = false` with `boot.mame_not_working = false`;
screenshots above show title + attract demo inside the same 120 s window that
"failed" boot. The battery's handoff detector keys exclusively on
`ARAMHANDOFF`/`CARTDMA` log tags; this 1999 cart appears to load without cart DMA
(PIO reads), so neither tag ever fires and every downstream metric
(DMA high-water, VRAM/ARAM write-truth peaks, streaming) is undefined — the title
cannot be scored, only parked.
What would unblock: a handoff signal that does not depend on cart DMA — e.g.
instrumenting PIO cart reads (`RomPioOffset` path in the fork's cart code) or
detecting PC leaving the BIOS region — then re-run the battery.

## 7. Controls (research done, for when unblocked)

Cabinet: standard Naomi 8-way stick + 2 rotate buttons (L/R) + start, 2 players.
MAME input ports: `naomi`. A stock DC pad maps 1:1 (d-pad + A/B rotate) — decisively,
the official DC port shipped exactly that.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sgtetris)
(8-way joystick + 6-button JVS standard declaration, 2P);
[tetris.wiki](https://tetris.wiki/Sega_Tetris) (rotate L/R buttons, left-turn-only
secret bonus, NAOMI DAS bug carried into the DC port).
