# Shakatto Tambourine Cho Powerup Chu (2K1 AUT) (`shaktamb`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 6,804,864 B → utilization **3.245**, well past `region_score()`'s `u > 2.0` gate, slotting into the parked ARAM cluster between `inunoos` (3.206) and `ninjaslt` (3.341) — the classic music-game profile: ~50 per-song preview sample banks (`SAMPLE *` strings) plus streamed vocal tracks behind a 2 MB AICA budget. Main RAM (u 0.599) and VRAM (u 0.692) both clear comfortably and streaming is light (2.04 MB/min), so ARAM is the *only* blocker. Controls are a penalty, not a gate: the motion-sensed tambourine reduces losslessly to a stock pad (`pad_adaptable`, 50) — unlike sibling-lineage `crackndj`'s turntables (`awkward`) or `mazan`'s off-ladder motion sword — see Gate §controls. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `shaktamb` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b GAME line 11171, BIOS-parented `naomigd` set; series entries "Shakatto Tambourine (Rev B)" `shaktam` GDS-0002B (line 11152) and "Motto Norinori Shinkyoku Tsuika (2K1 SPR)" `shaktmsp` GDS-0013 (line 11167) are separate MAME parents, not members of this family) |
| Maker / year | Sega, 2001 (GAME line 11171; carve header title `SHAKATTO TAMBOURINE 2K1AUT`, sidecar `guts.carve_meta`) |
| Genre / format | Rhythm (motion-tambourine — hit/shake the sensed tambourine in marked zones), **GD-ROM** GDS-0016, 180.2 MB (GAME_FORMATS.md; dump record: [Dumpcast](https://dcemulation.org/dumpcast/viewtopic.php?t=4457)) |
| Official DC port | No — the series never reached a Sega console; its only home release is MiniMoni. Shakatto Tambourine! Dapyon! (PS1, 2002) with a dedicated tambourine controller ([Game Informed](https://gameinformed.com/the-fascinating-tale-of-mini-moni-shakatto-tambourine-da-pyon/)) |
| Community ports | None found (searched 2026-08-11: [RetroRGB Atomiswave-port list](https://retrorgb.com/dreamcast-atomiswave-ports.html) — the DC conversion scene is Atomiswave-based; `shaktamb` is a Naomi GD-ROM title, outside that pipeline) |
| Representative choice | Only member of its family (2K1 AUT is itself the newest revision in the series line covered by this set) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/shaktamb.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). The full attract loop cycles: how-to-play instruction screens
with the sailor-suit mascot holding the tambourine and the six on-screen target rings
(`shot-060s.png` "がきたらタンバリンのボタンをタン タン!", `shot-609s.png` with the tracked
ball cursor mid-screen), the "シャカっとタンバリン! 超Power Up" title logo with © SEGA
CORPORATION 2000, 2001 (`shot-182s.png`), a hard-mode high-score RANKING table
(`shot-426s.png`), and **live demo gameplay** — two dancing characters, per-player score
HUD (4960 / 5600) and the six-ring field under a "DEMO PLAY / FREE PLAY" overlay
(`shot-548s.png`). Genuine attract-demo gameplay, not a frozen pre-game screen.
"FREE PLAY" overlay = default EEPROM.
Screenshots: `evidence/shaktamb/shot-060s.png` · `shot-182s.png` · `shot-426s.png` ·
`shot-548s.png` · `shot-609s.png`
Anomalies: none affecting metrics — `shot-121s.png` (curated out) is an all-black frame, an
attract transition fade between the title and the next scene; adjacent shots are clean.
Single clean leg (battery log: `leg 1: shaktamb.zip attempt 1 -> ran full window`).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 6,804,864 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.245** — past `region_score()`'s `u > 2.0` gate, slotting into the parked
ARAM cohort between `inunoos` (3.206) and `ninjaslt` (3.341). `nz_above_cap` = 4,849,838 B
of content above the cap (address-keyed placement figure, informational — and ≠ the 0x600000
DMPD-fill canary, so the content metric is healthy). Address peak is 8,306,576 B (u 3.961,
pre-volume-keying read) — the familiar near-8 MB address-keyed ceiling seen across the parked
cohort (kb "ARAM write-truth vs content"), not a shaktamb-specific anomaly.

The volume is what a music game of this design honestly needs: the sidecar's
`guts.sdk_strings` carries a ~50-entry `SAMPLE *` music-preview bank (SAMPLE LOVE MACHINE …
SAMPLE EXTRA2), per-mode BGM/SE/VOICE/MUSIC sound-test menus, `libsnd Ver.1.03b`, and
`STREAM END` markers — a large resident sample bank on top of streamed vocal tracks.

The other two regions, quoted from the sidecar for context (ARAM gates first in `score.py`'s
region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 10,044,247 | 16,777,216 | **0.599** | `nz_total` — clears; `dma_high_water` 31,976,128 (u 1.906, address placement) · `nz_above_cap` 3,365,995 B |
| VRAM (content volume + 2×fb) | 5,803,756 | 8,388,608 | **0.692** | `content_total` 4,574,956 + 2×`fb_bytes` (2×614,400) — clears; `nz_total` 5,053,892 (u 0.602) · peak 10,313,728 (u 1.230) · write FB at `fb_w_sof2=0xc00000` above the 8 MB line (`regs_last`) — layout artifact, volume fits |
| ARAM (content volume) | 6,804,864 | 2,097,152 | **3.245** | the gate — see above |

Streaming context: 1,619 DMA events · 31,682,464 B (30.2 MB) total · 19,448,224 B (18.5 MB)
unique · re-read ratio 0.3862 · steady-state 2.041 MB/min (`short_window: false`) ·
`pio_bytes` 526,784 B — light for a 180 MB GD-ROM title.
Guts: code 524,288 B · 1,032 functions · MMIO refs rtc 4 / g2ext 61 / scif 2 · flags
`eeprom_bios`/`serial`/`rtc` · standard Sega Naomi SDK stack (`NAOMI LIBRARY Ver 0.9 AM R&D`,
KAMUI2, `nlajamma`).
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (researched per RUNBOOK even though G3 fires first): `pad_adaptable` — a penalty
(50), not a second blocker.** The cabinet supplies two motion-sensed tambourine controllers;
the player hits ("knock") or shakes the tambourine and moves it onto marked zone positions
([Coinop Express](https://www.coinopexpress.com/products/machines/music-dance-machines/shakatto-tambourine-1957.html):
"two tambourines supply from the machine … hit the tambourine or to move the tambourine on to
the correct angle"). Electrically the game's entire input vocabulary is discrete switches plus
one coarse 2D position per player: MAME `INPUT_PORTS_START(shaktamb)` (naomi.cpp @59e7c0b line
1929) models per-player **Knock Switch, Shake L/R Switches, Up, Down, Screen-In** digital bits
plus **AD_STICK X/Y** analog pairs (A0/A1, A3/A4) — all through the standard NAOMI JVS I/O
(`PORT_INCLUDE(naomi_mie)`, no dedicated expansion board), and the game's own INPUT TEST menu
lists exactly `SWITCH(KNOCK)` / `SWITCH(SHAKE L)` / `SWITCH(SHAKE R)` plus a `TAMBOURINE
ADJUSTMENT` / `HEIGHT SELECT` calibration (sidecar `guts.sdk_strings`).

The maracas question, answered explicitly: the DC's closest peripheral is the official Samba
de Amigo maracas — and the lineage is real
([Giant Bomb](https://www.giantbomb.com/shakatto-tambourine/3030-88780/): Shakatto Tambourine
is a Samba de Amigo spin-off "trading its dual-maraca controller for a tambourine
controller"). But `dc_peripheral` would be dishonest: the maracas rig senses two independent
maracas' *vertical height* plus shake — it has no strike/knock input and no 2D
single-tambourine position sensing, so it cannot express this game's input vocabulary. Not
`dc_peripheral`.

Against the `crackndj` precedent (`awkward`): the deciding line is whether the input
vocabulary survives a pad mapping. Crackin' DJ's does not — continuous scratch
velocity/direction on motorized platters through a dedicated 837-13938 rotary-encoder JVS
board; the Flycast fork needs a custom `jvs_837_13938_crackindj` device plus mouse capture.
`shaktamb` needs no such device: the Flycast fork's `shaktam_inputs`
(core/hw/naomi/naomi_roms_input.h:511, shared by all three series sets,
naomi_roms.cpp:5777–5821) maps it to a **stock pad** — KNOCK/SHAKE L/SHAKE R on buttons,
`TAMBOURINE X`/`TAMBOURINE Y` on the analog stick — with no tambourine class in
maple_jvs.cpp at all, and this capture ran the full attract on exactly that mapping. A DC pad
reproduces the mechanics completely (stick = position among the six rings, one button = knock,
two = shake); what's lost is the physical performance fun, which is precisely the
`pad_adaptable` rung — the same trade Sega itself shipped when DC Samba de Amigo officially
supported the standard controller.

What would unblock it: ARAM content would need to shrink below the 2× cap (≤ 4,194,304 B) —
realistically by evicting the ~50-entry resident `SAMPLE *` preview bank and re-streaming
previews from disc, which the light 2.04 MB/min steady-state leaves ample GD bandwidth for.
No second blocker: memory (main/VRAM) and controls all clear on their own.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — music-game resident sample bank blows the 2 MB AICA cap (u 3.245); controls researched anyway: `pad_adaptable` (motion tambourine reduces to stock pad per Flycast `shaktam_inputs`; maracas rejected — no knock input, no 2D position) |
