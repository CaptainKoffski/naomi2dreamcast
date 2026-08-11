# Dengen Tenshi Taisen Janshi Shangri-la (`shangril`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **75.9 (A)** |
| Bottom line | First mahjong-⚠ family assessed, and the ⚠ dissolves on inspection: the cabinet's 5×6 mahjong key-matrix panel rules `pad_adaptable` (50) because this exact game shipped on Dreamcast in 1999 (T-40801M) — pad-played by construction, since the DC never had a mahjong panel peripheral. Every technical axis is green-to-good: all three memory regions fit under content keying (main is the tight one at 0.93× cap), streaming is trivial-bandwidth (5.5 MB/min) with only the 0.65 re-read ratio dragging that axis, and guts loses just 10 for EEPROM+RTC. The 75.9 lands top-tier A; the porting question is not "can it" but "why bother" — an official DC binary already exists, making this a reference/validation target, not a porting target. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `shangril` (no clones — the only `shangril*` set in naomi.cpp; GAME line 11095) |
| Maker / year | Marvelous Ent., 1999 (`/* 0004 */ GAME( 1999, shangril, naomi, naomim2, naomi_mp, naomi_state, init_naomi_mp, ROT0, "Marvelous Ent.", "Dengen Tenshi Taisen Janshi Shangri-la", GAME_FLAGS )` — naomi.cpp @59e7c0b line 11095; title screen concurs, `shot-060s.png` "©1999 Marvelous Entertainment Inc.") |
| Genre / format | Mahjong ⚠ ("Cyber Angel Mahjong Battle" — versus-mahjong with a sci-fi story attract), **cart, Naomi M2** 841-0004C, 12× 64 Mb ROM + `epr-22060`, PIC 317-5050-JPN (naomi.cpp line 367) |
| Official DC port | **Yes** — *Dengen Tenshi Taisen Maajan Shangri-La*, DC product code T-40801M, Marvelous Entertainment, Japan 1999 ([Satakore](https://www.satakore.com/sega-dreamcast-video-game-store,,38,,238,,Dengen-Tenshi-Taisen-Maajan-Shangri-La-JP.html); [Sega Retro](https://segaretro.org/Dengen_Tenshi_Taisen_Mahjong_Shangri-La): NAOMI original "ported to the Sega Dreamcast"). GAME_FORMATS.md's `No` cell corrected to `Yes (1999)` with this assessment. |
| Community ports | None needed / none found (searched 2026-08-11) — the official DC port makes one redundant (GAME_FORMATS.md DC-port policy) |
| Representative choice | MAME parent, sole member of the family; first of the three mahjong-⚠ families in the queue |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/shangril.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop is rich: title card (`shot-060s.png`), story-intro tile
fly-by (`shot-121s.png`), 3D character/story cutscenes (`shot-365s.png`, `shot-609s.png`),
and a full in-engine mahjong demo hand (`shot-487s.png`) — all under a FREE PLAY banner.
Screenshots: `evidence/shangril/shot-060s.png` · `shot-121s.png` · `shot-365s.png` · `shot-487s.png` · `shot-609s.png`
Anomalies: none — clean first-attempt full-window leg; battery-printed provisional 75.9 A stands
unchanged (the battery's `pad_adaptable` hint survived research).

## 4. Memory fit (axis: 90.5)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 15,554,605 | 16,777,216 | 0.927 | 90.5 | The binding region. Address peak 31,457,248 (u 1.87, informational placement artifact) · `nz_above_cap` 2,292,390 B of content above the 16 MB line (see Risks) · `dma_high_water` 23,205,824 (informational) |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 6,201,897 | 8,388,608 | 0.739 | 100.0 | `content_total` 4,973,097 + 2×`fb_bytes` 614,400 · address peak 15,928,868 and `nz_above_cap` 5,050,679 are FB-placement artifacts — `regs_last` parks the flip pair at 0x800000/0xc00000, exactly the chocomk precedent the v8 FB-masking rekey exists for |
| ARAM (content volume, fill-excluded, `content_total`) | 1,688,674 | 2,097,152 | 0.805 | 99.6 | Address peak 8,323,008 (near-full bank touch is the uniform fill, kb §6) · `nz_above_cap` 15,757 |

Watermarks (informational, content-scan — stale-data prone): main 31,457,248 ·
vram 15,928,868 · aram 8,388,608 (the boot-time "DMPD" fill, not content).
Axis = min(regions) = main's 90.5.

## 5. Cart streaming (axis: 76.4)

DMA events 348 · total 55.8 MB (58,460,768 B) · unique 19.6 MB (20,524,608 B) ·
re-read ratio 0.6489 · steady-state 5.476 MB/min (`short_window: false`) ·
PIO 4,197,504 B. Bandwidth is trivial (sub-score 100); the 0.65 re-read ratio
(sub-score 41.1) caps the axis at 76.4.

## 6. Guts (axis: 90.0)

Code 4,194,304 B · functions 1,317 · MMIO refs: scif 0, rtc 4, g2ext 105 ·
BIOS vector refs: none · penalties: `eeprom_bios` −5, `rtc` −5 → 90.0.
Carve clean (`hdr_at` 0, title "SHANGRI-LA", base 0x0c020000). SDK strings show the
stock Sega Naomi library stack (libintr 1.03, syG2/syHw/syTmr/syCache/sySq/syChain/syInt,
libam 1.232810) → `sdk_overlap: partial`.

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: the Sega Naomi **mahjong keyboard-matrix panel**, not a joystick. MAME input
ports `naomi_mp` (GAME line 11095): a muxed key matrix — the game strobes five columns
and reads rows back, `naomi_mp_r()` ORing `KEY1`–`KEY5` onto P1 bits 8–15 under an
`OUTPUT`-port mux (naomi.cpp lines 1994–2049). The wiring diagram (lines 1172–1190)
shows the physical panel: "mahjong panel uses ext. I/O 4-8 (regardless of I/O board
version)" as strobe columns with rows returned on JAMMA 17–22 (the 1P
start/up/down/left/right/push1 lines) — keys **A–N** (tile slots) plus
**Kan/Pon/Chi/Reach/Ron/Bet/Flip-Flop/Last-Chance/Start**. The game's own demo UI maps
the A–N keys to the 13-tile hand on screen (`shot-487s.png`, letter strip under the
tiles). Our fork emulates no such matrix — `shangril`'s ROM entry carries no per-game
input struct (`core/hw/naomi/naomi_roms.cpp:3152` @f014a410c) and `maple_jvs.cpp` has
no mahjong handling — yet the game attracts fine on the standard JVS digital path.

**Why `pad_adaptable`, not `awkward`:** the Dreamcast never had a mahjong panel
peripheral, but the decisive precedent is DC-native and first-party to this title —
**this exact game shipped on Dreamcast** (T-40801M, Marvelous, Japan 1999), pad-played
with cursor-driven tile selection like every DC mahjong release (e.g. Athena's *Pro
Mahjong Kiwame D*, DC 2000). Mahjong is turn-based with no timing pressure, so
cursor-over-tiles plus call buttons (Pon/Chi/Kan/Reach/Ron on face buttons) loses
nothing mechanical; the adaptation is not hypothetical — Marvelous shipped it the same
year as the cabinet. Not `stick` (100): the panel's ~20 discrete keys cannot map 1:1
onto a pad; the tile-selection UI layer is real (if already-solved) work.

Proposed DC mapping: D-pad/stick = tile cursor, A = discard/confirm, B = cancel,
X/Y/triggers = Pon/Chi/Kan/Reach/Ron prompts (context-sensitive call prompts, the DC
mahjong idiom), Start = start. Or simply crib the official T-40801M binary's scheme.
Sources: all six citations are in sidecar `controls.sources` (MAME matrix + wiring +
GAME row, Flycast fork input path, Satakore T-40801M, Sega Retro).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 90.5^.40 · 76.4^.20 · 90.0^.20 · 50.0^.10 · 40.0^.10 = **75.9 (A)**
Similarity inputs: developer no, SDK overlap partial (stock Sega Naomi libs, §6), loader match no.

## 9. Risks & notes

- **Main RAM is the pinch point**: 15.55 MB of write-truth content vs the 16 MB cap
  (u 0.927) — barely 1.2 MB of headroom — and 2,292,390 B of that content sits above
  the 16 MB line (`nz_above_cap`; DMA high-water 22.1 MB). A port must relocate that
  2.3 MB and then live inside ~7% slack; first thing to map.
- **VRAM looks scary raw but isn't**: 15.9 MB address peak is the framebuffer flip
  pair parked at 0x800000/0xc00000 (`regs_last`); FB-masked fit is 6.2 MB ≤ 8 MB.
  Re-base the FBs, done.
- **High streaming re-read ratio (0.65)** — the cart is re-fetching the same 19.6 MB
  working set; fine for a 98.6 MB cart that a DC port would restructure anyway,
  but it flags asset-reload-per-scene design.
- **Link-play code is present but optional**: NLCB/"NOT READY COMMUNICATION BOARD"
  strings in the carve; no `network` guts flag was assessed (no comm board in the
  standard cabinet) — a port simply drops versus-link.
- **The official DC port (T-40801M) is the elephant**: it makes a community port
  redundant for players (GAME_FORMATS.md policy) but is a ready-made reference —
  controls scheme, memory layout, and asset cuts can be compared directly against
  the real DC build before believing anything above.
- Rendering must be verified on real DC hardware (working-style rule); evidence here
  is fork-rendered attract only.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 75.9 (A) | Initial assessment — first mahjong-⚠ family. Clean full-window first-attempt leg; controls research confirmed the battery's `pad_adaptable` hint (naomi_mp key matrix; decisive DC-native precedent: the game's own official DC port T-40801M, 1999), so the provisional 75.9 stood. GAME_FORMATS DC-port cell corrected No → Yes (1999) |
