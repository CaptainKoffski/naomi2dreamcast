# Rhythm Tengoku (Japan) (`rhytngk`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **26.7 (C)** |
| Bottom line | The only Nintendo game ever released on Naomi is technically green almost everywhere — main RAM and VRAM fit with >2× headroom under content keying, streaming is a trivial 3.0 MB/min, and the cabinet is literally the GBA game's two-button play (controls 100) — but the audio kills it: 4.1 MB of ARAM content volume is 1.96× the DC's 2 MB ARAM even after position-independent compaction credit, landing 0.04 u under the G3 park line and keying the whole memory axis at 11.7. A rhythm game lives and dies by its audio, so that overage is the entire porting problem: halve audio residency (ADPCM re-encode / downsample / stream from disc) or don't bother. Score is lower-bound-flavored: guts axis absent (Ghidra never finishes the 4.2 MB boot.bin) and similarity floored. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `rhytngk` (no clones — sole set; MAME src/mame/sega/naomi.cpp @59e7c0b, game `/* 0177 */`, GAME line 11048) |
| Maker / year | Sega / Nintendo - J.P ROOM, 2007 (GAME line 11048; arcade release 2007-09-20 per [Wikipedia](https://en.wikipedia.org/wiki/Rhythm_Tengoku)) |
| Genre / format | Rhythm, **cart, Naomi M4** — 4× 64 MiB flash `fpr-24423..24426`, PIC 317-0503-JPN, rom_board id `5504` (ROM_START lines 6863–6877) |
| Official DC port | No — the game is a GBA original (2006) that Sega reprogrammed *for* the arcade; the only Nintendo title on any Dreamcast-family hardware, never released on DC itself ([Wikipedia](https://en.wikipedia.org/wiki/Rhythm_Tengoku)) |
| Community ports | None found (searched 2026-08-11; [Rhythm Heaven Wiki arcade page](https://rhythmheaven.fandom.com/wiki/Rhythm_Tengoku/Arcade) lists no DC project) |
| Representative choice | Sole set of the family — nothing to choose between |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/rhytngk.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop cycles the title card (`shot-060s.png`), high-score ranking
boards (`shot-121s.png`), and in-engine minigame demos: Karate Man (`shot-182s.png`),
Neko Machine (`shot-365s.png`) and the Love telegram game (`shot-548s.png`) — the last two
render on-screen **A/B button prompts**, direct in-run confirmation of two-button play.
Screenshots: `evidence/rhytngk/shot-060s.png` · `shot-121s.png` · `shot-182s.png` · `shot-365s.png` · `shot-548s.png`
Anomalies: battery attempts 1–3 were killed externally mid-run — the Ghidra guts step, not the
game: headless auto-analysis of the 4.2 MB boot.bin ran >2 h CPU without finishing (a
`GUTS_TIMEOUT` cap was added in commit `be4339b`); attempt 4 completed clean end-to-end.
The `raw/` log dir was rotated out by the next battery's startup; all quoted numbers are sidecar fields.

## 4. Memory fit (axis: 11.7)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 6,906,466 | 16,777,216 | 0.412 | 100.0 | `nz_above_cap` 19,930 B above the 16 MB line (trivial) · `dma_high_water` 10,542,720 · address peak 32,528,992 (informational) |
| VRAM (FB-masked content volume + 2×framebuffer) | 3,995,091 | 8,388,608 | 0.476 | 100.0 | `content_total` 2,766,291 + 2×`fb_bytes` 614,400 · `nz_above_cap` 338,474 · address peak 9,052,160 (u 1.08, placement artifact) |
| ARAM (content volume, fill-excluded, `content_total`) | 4,103,604 | 2,097,152 | **1.957** | **11.7** | `nz_above_cap` 2,116,214 B of content above the 2 MB line · address peak 8,257,552 (u 3.94, position-independent — kb §6) · 0.04 u under the G3 park threshold (u > 2) |

Watermarks (informational, content-scan — stale-data prone): main 32,528,992 ·
vram 9,692,984 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).
Risk flag: main watermark (32.5 MB) ≫ DMA high-water (10.5 MB) — stale-data artifact class, informational.

## 5. Cart streaming (axis: 83.0)

DMA events 1,018 · total 28.8 MB (30,196,896 B) · unique 16.1 MB (16,896,992 B) ·
re-read ratio 0.4404 · steady-state 3.036 MB/min (`short_window: false`) ·
PIO 4,343,004 B. Bandwidth is trivial (sub-score 100); the 0.44 re-read ratio
(sub-score 57.5) caps the axis at 83.0.

## 6. Guts (axis: n/a — no .dat, weights renormalized)

`guts.dat_available = false`: Ghidra headless auto-analysis of the carved 4.2 MB
boot.bin is pathological — it ran **>2 h CPU without finishing** and was killed
(sidecar `guts.error` ends in `Killed: 9`); every earlier rhytngk battery "hang"
was this same step. A `GUTS_TIMEOUT` cap (default 600 s) was added in commit
`be4339b` so the battery now degrades cleanly to the guts-unavailable path
instead of hanging. Same documented degradation class as mushik2e (kb §4.w): a
*scored* title with no guts axis and floored similarity, so 26.7 is
lower-bound-flavored. Do not re-run Ghidra on this set without a fundamentally
different analysis budget. `flags: [eeprom_bios]` recorded but unused.

## 7. Controls (axis: 100.0 — `stick`)

Cabinet: simple two-button rhythm play — the GBA original's A-button gameplay
reprogrammed for arcade; no wheel, gun, touch, card, or any special I/O.
MAME input ports: `naomi` (the standard JVS 2P stick + digital-buttons block,
`INPUT_PORTS_START( naomi )` line 1506; wired to rhytngk by GAME line 11048).
The fork's per-game descriptor is two digital buttons + dpad + start:
`rhytngk_inputs = INPUT_2_BUTTONS("SHOT A", "SHOT B")`
(`core/hw/naomi/naomi_roms_input.h:548` @f014a410c), and the game's entry
(`core/hw/naomi/naomi_roms.cpp:4901-4917`) carries no special-device wiring —
no rhytngk gameId hooks anywhere in `naomi_cart.cpp`, `maple_jvs.cpp`, or
`card_reader.cpp` (grepped @f014a410c). The game itself renders A/B button
prompts in attract (`shot-365s.png`, `shot-548s.png`).
Proposed DC mapping: pad A/B = SHOT A/B, Start = Start — a 1:1 mapping with
buttons to spare.
Sources: the two fork citations + MAME GAME/INPUT_PORTS lines +
[Rhythm Heaven Wiki (arcade)](https://rhythmheaven.fandom.com/wiki/Rhythm_Tengoku/Arcade) +
[Wikipedia](https://en.wikipedia.org/wiki/Rhythm_Tengoku) — all five in sidecar `controls.sources`.

## 8. Score computation

final = memory^.50 · streaming^.25 · controls^.125 · similarity^.125 (guts dropped, spec §4.3)
      = 11.7^.50 · 83.0^.25 · 100.0^.125 · 20.0^.125 = **26.7 (C)**
Similarity inputs: developer no, SDK overlap none (no sdk_strings — no carve, §6), loader match no.

## 9. Risks & notes

- **ARAM is the whole porting problem.** 4.1 MB of audio content vs the DC's
  2 MB ARAM, even with full compaction credit (address peak u 3.94 is ignored
  as position-independent; the *volume* is what doesn't fit). A rhythm game
  cannot shed its audio, so the port plan must halve residency: ADPCM
  re-encode, downsampling, and/or per-minigame streaming from disc. At u 1.957
  this sits 0.04 under the G3 park line — treat it as a near-park, not a pass.
- **Score is a lower bound:** guts axis missing (§6) + similarity at the 20
  floor — the same skew documented for mushik2e (kb §4.w).
- Main watermark 32.5 MB vs 10.5 MB DMA high-water: content-scan stale-data
  flag, informational only; write-truth content is 6.9 MB and fits easily.
- **Rendering and audio must be verified on real DC hardware** (working-style
  rule); evidence is fork-rendered attract only — no operator play captured.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal,
  kb §4.r); the game runs under our fork regardless.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 26.7 (C) | Initial assessment. Attempts 1–3 killed externally on the Ghidra guts hang (4.2 MB boot.bin, >2 h CPU; `GUTS_TIMEOUT` added in `be4339b`); attempt 4 clean. Controls research confirmed `stick` (two-button play), so the battery-printed 26.7 stands. ARAM content 1.96× cap keys the score; guts absent — kb §4.w degradation class |
