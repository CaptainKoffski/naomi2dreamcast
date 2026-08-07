# Sega Tetris (`sgtetris`) — portability assessment

> **Battery v8 vram-fb-masking re-run (2026-08-07): 47.4 (B)** — spec
> `2026-08-07-vram-fb-masking-design.md`. Sidecar: flycast `f014a410c`, battery 8. No
> park, boot ok, same PIO handoff. Main (29,130,560 B) and ARAM `content_total`
> (1,604,876 B) reproduce **bit-identically** to the v7 run — the reproduction check this
> wave requires for non-VRAM regions. VRAM flips from address high-water (16,279,552 B,
> u=1.941, sub 12.4) to FB-masked content: `content_total` 8,800,955 B + `2×fb_bytes`
> 1,228,800 B (`fb_bytes` 614,400 B, exactly 640×480×2) = fit 10,029,755 B, u=1.196 → sub
> **49.8** — a rise, as required (was 12.4). This does not change which region binds:
> main RAM's write-truth peak (u=1.736, sub 20.5) is now the lowest of the three,
> exactly the design doc's "main 20.5 becomes binding" prediction — memory axis
> **12.4 → 20.5**, final **38.7 → 47.4**, tier **C → B**. VRAM is still genuinely over
> cap (not fully resolved, just no longer the worst region) — 8,800,955 B of real
> non-FB content plus two framebuffers still doesn't fit in 8 MB. Coverage re-annotated
> `demo` (unchanged — same title/how-to-play/ranking/attract-gameplay loop).

## 1. Verdict

| | |
|---|---|
| **Final score** | **47.4 (B)** — battery v8 vram-fb-masking re-run; was 38.7 (C) under v7's address-keyed VRAM |
| Bottom line | The §6 checkpoint re-keying G3-ARAM on content volume closes this title's gate: `content_total` = 1,604,876 B (u = 0.765, well under the 2 MiB cap) vs. the old content-high address u = 3.94×. But the ARAM semantics were never the whole memory story here — main RAM (29,130,560 B, u = 1.736×) and VRAM (16,279,552 B, u = 1.941×) are both genuinely over the DC caps, so the memory axis is capped at 12.4 (bound by VRAM, the worst region) and the final lands at **38.7 (C)** — a real, low but scored, result. Main RAM and VRAM (measured for the first time in battery v6) reproduce bit-identically to that run; the main write-truth peak (29,130,560 B) still matches the stale v5 watermark almost exactly, confirming those writes were real cart content, not BIOS residue. Official 2000 DC port exists regardless. **(battery v8 update, see banner above:** VRAM re-keyed on FB-masked content + 2×FB now scores 49.8 (was 12.4) — main RAM (sub 20.5) becomes the binding region instead, final rises to 47.4 (B).) |
| Assessed | 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857`; vram-fb-masking re-run 2026-08-07 · battery v8 · flycast `f014a410c` |

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
`shot-121s.png`, `shot-365s.png`, `shot-487s.png`, `shot-609s.png`. (v8 re-run:
same 5-shot curation — title/how-to-play/ranking/attract-gameplay, coverage `demo`
unchanged.)
Anomalies: kb §4.v's G1 blindness for this title is **CLOSED** — see § Gate.

## Gate

**No gate — un-parked 2026-08-07 (battery v7): ARAM re-keyed on content volume closes the last remaining region; battery v8 re-keys VRAM on FB-masked content + 2×FB, which raises VRAM's sub-score but main RAM (still genuinely over cap) becomes the new binding region — memory axis 12.4 → 20.5, final 38.7 → 47.4 (B).**

| Region | Peak / fit (write-truth) | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM | 29,130,560 | 16,777,216 | 1.736 | nz_total 7,350,605 (v8 re-run, matches v7's 7,350,612 within run-to-run noise; 3,289,898 B above cap); `dma_high_water = 0` (PIO-loaded, measured via snapshot+diff); write-truth peak reproduces **bit-identically** to v7 — now the binding region (sub-score 20.5, lowest of the three) |
| VRAM (FB-masked content + 2×FB) | 10,029,755 (content_total 8,800,955 + 2×fb_bytes 1,228,800) | 8,388,608 | **1.196** | battery v8 re-keying (this task, spec `2026-08-07-vram-fb-masking-design.md`): `fb_bytes` 614,400 B (exactly 640×480×2) — sub-score rises to 49.8 (was 12.4 under the old address high-water, 16,279,552 B, u=1.941, still genuinely over cap so not a full resolution, just no longer the worst region) |
| ARAM (content volume, fill-excluded) | 1,604,876 | 2,097,152 | **0.765** | `content_total` (§6 volume-keyed, battery v7) — reproduces bit-identically in the v8 re-run; well under cap, sub-score 100.0, not the binding region; old content-high **address** was 8,257,552 (u=3.94, pre-v7 keying), same 8 B above the 2 MB line either way (`nz_above_cap = 8`; raw nz_above2m 32,768 B, the fill-exclusion doing real work). NOT the DMPD fill canary (that requires `nz_above_cap == 0x600000` exactly, kb §8/§4) |

Streaming: `dma_events = 0` · `pio_bytes = 27,167,524` (~27 MB streamed via PIO over the
600 s window — a lower bound; the counter (`CARTPIOCNT`) is cumulative from the first PIO
read, not gated by the handoff threshold — only the main-RAM handoff *baseline* snapshot
is taken at the 32 KB crossing) · 1,078 `CARTPIO offset=` pokes logged total. The entire cart loads and streams
by PIO — zero cart-DMA traffic the whole run.

**§6 checkpoint, RESOLVED 2026-08-07 (battery v7):** sgtetris was the most extreme G3-aram
address-vs-volume divergence on record — 8 B of content above the 2 MB cap at content-high
address u=3.94, vs. marstv's previous record of 81,598 B (kb §6 item 5). The checkpoint
re-keyed the gate on content volume exactly as this divergence argued: `content_total` =
1,604,876 B (u=0.765) passes through with an effectively DC-fitting sound bank. As
predicted here, that alone does not unpark the title on its own — main RAM and VRAM are
both still measured over-cap (1.736× and 1.941×), so the memory axis lands at 12.4
(bound by VRAM) and the final score is a real but low **38.7 (C)**, not a park.

**What changed:** kb §4.v's G1 blindness (`no-handoff-120s` with the game visibly running,
zero `ARAMHANDOFF`/`CARTDMA` tags) is now **RESOLVED** — the unified `dma|pio` handoff
(fork commit `65f9f7857`, battery v6) baselines all three regions the instant cumulative
PIO `ROM_DATA` reads cross 32 KB, closing the blind spot without any cart-DMA dependency.
This title is measured end-to-end for the first time; under battery v6's address-keyed
ARAM rule it parked on a real, evidenced gate (not an instrumentation false-negative) —
battery v7's volume-keyed rule (§6 checkpoint) now un-parks it, landing at a real but low
score instead (§ Verdict). A regression golden
(`tools/assess/tests/test_metric_guards.py::test_sgtetris_pio_face_stays_measured`) now
guards this shape.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 2 rotate buttons (L/R) + start, 2 players.
MAME input ports: `naomi`. A stock DC pad maps 1:1 (d-pad + A/B rotate) — decisively,
the official DC port shipped exactly that.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sgtetris)
(8-way joystick + 6-button JVS standard declaration, 2P);
[tetris.wiki](https://tetris.wiki/Sega_Tetris) (rotate L/R buttons, left-turn-only
secret bonus, NAOMI DAS bug carried into the DC port).
