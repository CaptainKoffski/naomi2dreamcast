# Sega Tetris (`sgtetris`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **67.6 (A)** |
| Bottom line | Official 2000 DC port exists (assessed as reference/validation data): under content keying main RAM fits easily (0.438× cap) and ARAM fits (0.765×) — VRAM is the one genuinely over-cap region (FB-masked fit 1.196×, 8.8 MB of real non-FB content plus two framebuffers doesn't fit 8 MB), and it binds the memory axis at 49.8. |
| Assessed | capture 2026-08-09 · battery v9 (verified re-run) · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/sgtetris.zip`
Attract/demo reached: **demo** — `shot-060s.png` (title, beach backdrop), `shot-121s.png`
(how-to-play attract overlay with a live gameplay board, mesa/canyon backdrop), `shot-365s.png`
(online RANKING table), `shot-487s.png` (how-to-play attract overlay, Shibuya-crossing
backdrop), `shot-609s.png` (attract logo/board transition, grassland backdrop with iguana). The
title screen and how-to-play overlay each rotate through multiple 3D backdrops across the 600 s
window. (`capture.coverage` was `null` in the raw v9 sidecar; set to `"demo"` at assessment —
the curated shots show live gameplay boards and a ranking screen, not just an idle title loop.)
Screenshots: `evidence/sgtetris/shot-060s.png` · `shot-121s.png` · `shot-365s.png` ·
`shot-487s.png` · `shot-609s.png`
Anomalies: none blocking. Memory/streaming/guts counters reproduce v8 byte-identically
except main RAM `nz_total` (7,350,605 → 7,350,612, +7 B — run-to-run noise, sub-score
unaffected). Attract-loop backdrop at matching timestamps shifted from v8 (e.g. `shot-121s`
now shows a canyon backdrop rather than beach) — expected non-determinism in emulated frame
timing, not a regression. kb §4.v's G1 blindness for this PIO-loading title remains closed
since battery v6 (see History).

## 4. Memory fit (axis: 49.8)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 7,350,612 | 16,777,216 | 0.4381 | 100.0 | v8 was 7,350,605 (+7 B, run-to-run noise, u unchanged at displayed precision) · address peak 29,130,560 (u 1.736, informational; nz_above_cap 3,289,898 — byte-identical to v8) · `dma_high_water` 0 — PIO-loaded, measured via snapshot+diff |
| VRAM (FB-masked content + 2×FB: 8,800,955 + 2×614,400) | 10,029,755 | 8,388,608 | 1.196 | 49.8 | **binding region**, byte-identical to v8 — genuinely over cap: real non-FB content plus two 640×480×2 framebuffers doesn't fit 8 MB · raw address peak 16,279,552 (u 1.941, informational, byte-identical to v8) |
| ARAM (content volume, fill-excluded, `content_total`) | 1,604,876 | 2,097,152 | 0.7653 | 100.0 | reproduces bit-identically v7→v8→v9 · address peak 8,257,552 (u 3.94 under pre-v7 keying) with only 8 B of content above the 2 MB line (raw nz above 2M 32,768 — the fill-exclusion doing real work); NOT the DMPD canary (that requires `nz_above_cap == 0x600000` exactly, kb §8/§4) |

Watermarks (informational, content-scan — stale-data prone): main 29,130,560 ·
vram 16,279,552 · aram 8,388,608.

## 5. Cart streaming (axis: 100.0)

DMA events 0 · `pio_bytes` 27,167,524 B (~27 MB streamed via PIO over the 600 s window —
a lower bound; the `CARTPIOCNT` counter is cumulative from the first PIO read, not gated
by the handoff threshold) · 1,078 `CARTPIO offset=` pokes logged. The entire cart loads
and streams by PIO — zero cart-DMA traffic the whole run (`steady_mb_per_min` 0.0,
re-read 0.0, `short_window: false`). All streaming counters reproduce v8 byte-identically.

## 6. Guts (axis: 90.0)

Code 1,048,576 B · functions 1,300 · MMIO refs: scif 0, rtc 4, g2ext 88 ·
BIOS vector refs: none · flags: `eeprom_bios`, `rtc` → −10.
Carve base `0x0c021000`, entry `0x0c021000`, header title `SEGA TETRIS`.
SDK strings: NAOMI LIBRARY Ver 0.8 AM R&D, NLOBJPUT 0.99, NLSPRITE 0.11, libintr 1.051
(Sega libraries, 1999 builds).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 2 rotate buttons (L/R) + start, 2 players.
MAME input ports: `naomi`. A stock DC pad maps 1:1 (d-pad + A/B rotate) — decisively,
the official DC port shipped exactly that.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sgtetris)
(8-way joystick + 6-button JVS standard declaration, 2P);
[tetris.wiki](https://tetris.wiki/Sega_Tetris) (rotate L/R buttons, left-turn-only
secret bonus, NAOMI DAS bug carried into the DC port).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 49.8^.40 · 100.0^.20 · 90.0^.20 · 100.0^.10 · 40.0^.10 = **67.6 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **VRAM is the real porting work**: 8,800,955 B of FB-masked content + two framebuffers
  = 1.196× the 8 MB cap — a genuine over-cap region, not an address artifact. The
  official 2000 DC port is shipped proof the trim is doable.
- **PIO loader shape**: `dma_high_water` = 0 and zero cart-DMA events — main RAM is
  measured by snapshot+diff only, and the ~27 MB PIO figure is a lower bound. A
  regression golden (`tools/assess/tests/test_metric_guards.py::test_sgtetris_pio_face_stays_measured`)
  guards this shape.
- Official DC port exists — this assessment is reference/validation data per
  GAME_FORMATS.md policy, not a port candidate ranking.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v6 | 2026-08-07 | PARKED G3-ARAM | First end-to-end measurement: the unified `dma\|pio` handoff (fork `65f9f7857`) closed the kb §4.v no-handoff G1 blind spot for this PIO-loading cart; under address-keyed ARAM (peak 8,257,552, u 3.94) it parked on a real, evidenced gate — kb §4.v |
| v7 | 2026-08-07 | 38.7 (C) | §6 checkpoint re-keyed G3-ARAM on content volume (1,604,876 B, u 0.765 — the most extreme address-vs-volume divergence on record, 8 B above cap at address-u 3.94) → un-parked; VRAM address high-water binding (12.4) — kb §6 item 5 |
| v8 | 2026-08-07 | 47.4 (B) | VRAM re-keyed on FB-masked content + 2×FB (sub 12.4 → 49.8); main write-truth address peak became binding (20.5); main and ARAM reproduce bit-identically to v7 — spec `2026-08-07-vram-fb-masking-design.md` |
| v9 | 2026-08-08 | 67.6 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` 7,350,605 (u 0.438) instead of address peak (u 1.736); binding region moved back to VRAM — spec `2026-08-08-main-content-rekey-design.md` |
| v9 | 2026-08-09 | 67.6 (A) | ranking-groom chunk 4: fresh v9 capture, provenance v8→v9 (scoring keys unchanged) — memory/streaming/guts reproduce v8 byte-identically except main `nz_total` +7 B (run-to-run noise) |
