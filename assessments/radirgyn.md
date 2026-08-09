# Radirgy Noa (Japan) (841-0062C) (`radirgyn`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **79.0 (A)** |
| Bottom line | The final third-party Naomi cart (2009) fits main RAM and VRAM outright under content keying; ARAM content at 0.974× cap is the binding region — with the most direct precedent possible, the original Radirgy's official 2006 DC port proving this exact franchise's sound fits in 2 MiB. |
| Assessed | capture 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `radirgyn` (no clones — `parent: null` in controls.json; single GAME line, MAME src/mame/sega/naomi.cpp @59e7c0b line 11121). The 2005 GD-ROM sets `radirgy`/`radirgyo` (GDL-0032A/0032, `naomigd`, ROT270) are a **separate family** |
| Maker / year | Milestone / Lucky, 2009 (JP arcade June 2009 per [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=radirgyn)); Lucky Co. Ltd published, MileStone Inc. developed |
| Genre / format | Shmup ★ — **ROT0 "vertizontal"**: vertical-scrolling playfield on a horizontal 640×480 monitor, side bands used for P1/P2 status panels ([shmups forum "Vertically Scrolling Yoko Games"](https://shmups.system11.org/viewtopic.php?t=53533)); first Milestone game with 2-player simultaneous play (arcadeitalia). **M4 cartridge** 841-0062C — 2× 512 Mb S29GL512N flash with data (ic8/ic9; "IC10 and IC11 Populated, Empty") + PIC `317-5138-JPN`, XC3S50 "VER.2", XCF01S "8A", rom_board id 5504, machine `naomim4` (MAME naomi.cpp @59e7c0b cart table ~line 688 + `ROM_START(radirgyn)` line 6793). 107.4 MB zip. **841-0062 is the highest 841-xxxx cart number in MAME's Naomi list — the final third-party Naomi cartridge game** (June 2009, ~11 years after the 1998 launch; only Sega's Star Horse Progress Returns units 840-0183…0187 are contemporaneous). Note: arcadeitalia's "BAD DUMP" remark is unsupported by the MAME source — no `BAD_DUMP` macro anywhere in `ROM_START(radirgyn)` (clean CRCs on ic8/ic9 and the PIC); primary source wins |
| Official DC port | No — Noa's ports are Japan-only and post-DC: *Radirgy Noa Wii* (2010-02-25), *Milestone Shooting Collection 2* (Wii, 2010, with Chaos Field/Karous/Illvelo/Radirgy — [shmups.wiki](https://shmups.wiki/library/MileStone_Shooting_Collection_2), [MobyGames](https://www.mobygames.com/game/56616/milestone-shooting-collection-2/)), *Radirgy Noa Massive* (X360, 2010-10-28, adds Classic/Death/Massive modes — [shmups.wiki](https://shmups.wiki/library/Radirgy_Noa)), Windows (2011-02-25, [HandWiki](https://handwiki.org/wiki/Software:Radirgy_Noa)). Only the original Radirgy got a DC release (2006-02-16, [Wikipedia](https://en.wikipedia.org/wiki/Radirgy)) — the in-family precedent §9 leans on |
| Community ports | None found (searched 2026-08-03) — the [sega-naomi.eu mega list](https://www.sega-naomi.eu/forum/viewtopic.php?t=2185) lists Noa as Wii/X360 only; the conversion scene targets GD-ROM sets and an M4 cart needs a decrypted dump ([DC Junkyard Naomi article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/radirgyn.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the full attract
cycle was observed across the battery shots: story cards (MAYUMI character art with
dialogue boxes) → live gameplay demo across two stages (forest, city) with the
vertizontal side-panel layout and the ABSnet visibly deployed → ranking table → title
screen → loop wrap.
Screenshots: `evidence/radirgyn/shot-060s.png` · `evidence/radirgyn/shot-365s.png` ·
`evidence/radirgyn/shot-609s.png` (story-panel "INSERT COIN(S)" ×2, attract gameplay)
Anomalies: none — renders fully under the fork.

## 4. Memory fit (axis: 87.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 10,831,427 | 16,777,216 | 0.646 | 100.0 | address peak 24,850,767 (u 1.481, informational — matched the old "informational" watermark exactly: real writes, not stale data) · nz_above_cap 4,250,690 (content above the 16 MB line by address — relocation work) · `dma_high_water` 19,552,576 |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 6,352,404 (content 5,123,604 + 2×614,400) | 8,388,608 | 0.757 | 100.0 | address peak 11,195,744 (u 1.335, informational) · nz_total 5,595,261 · nz_above_cap 2,525,451 (address extent, the kurucham relocation pattern) · `fb_bytes` = exactly 640×480×2 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,041,920 | 2,097,152 | 0.974 | 87.0 | **binding region** — address peak 2,252,880 (u 1.074) · nz_above_cap 122,039 |

Watermarks (informational, content-scan — stale-data prone): main 24,850,767 ·
vram 11,195,744 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 75.5)

DMA events 304 · total 43.2 MB · unique 13.5 MB · re-read ratio 0.6887 ·
steady-state 4.164 MB/min (`short_window: false`, bit-identical to v4) · PIO 2,099,776 B

## 6. Guts (axis: 85.0)

Code 2,097,152 B · functions 2,361 · MMIO refs: scif 2, rtc 3, g2ext 127 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → −15.
M4 boot blob carved at base `0x8c020000`, entry `0x8c021000`, header title
"RADIRGY NOA" — needs the `carve_boot.py` bit-30 mask (the M4 load-entry rom offset
carries bit 30 as an encrypted-read flag, not a file offset: MAME
`src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast `m4cartridge.cpp:115,132`
@ebae3b513; kb §4.q — the v2 scan failed until the 2026-08-06 fix).

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + 3 buttons (A shot with color-cycled weapons, B sword/slash —
chargeable, fills the ABSnet gauge, C ABSnet bullet-absorbing net; contact damage new
in Noa), 2P simultaneous. `controls.device_class = stick`.
Proposed DC mapping: 1:1 on a stock DC pad; the ROT0 vertizontal screen needs **no
TATE work at all** — the arcade picture is already a native horizontal 640×480 (§2).
The Wii/X360/PC ports shipped on standard pads, confirming pad-friendliness.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT0);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=radirgyn)
(8-way joystick, "Shoot, Sword, Special", 2P concurrent, horizontal);
[Radirgy DB fan wiki](https://radirgy.neocities.org/tips/noa/);
[HandWiki](https://handwiki.org/wiki/Software:Radirgy_Noa).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 87.0^.40 · 75.5^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **79.0 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no — the
developer false is the known reference-list artifact (the reference's `makers` list
contains only Altron / Taito) despite Milestone's in-franchise DC porting pedigree.

## 9. Risks & notes

- **ARAM is the binding region at 0.974× content** — a modest audio trim territory,
  with same-franchise released-port precedent: the original Radirgy shipped an
  official DC port in 2006 ([Wikipedia](https://en.wikipedia.org/wiki/Radirgy)), so
  this exact series' sound design demonstrably compresses into the DC's 2 MiB AICA RAM.
- **Main RAM fits by volume, not by address:** content is 10.8 MB (0.646×) but the
  write extent reaches 24,850,767 B (1.481×) with 4.25 MB of content above the 16 MB
  line — real relocation/layout work for a port.
- **VRAM address extent 1.335×** with 2.5 MB above the 8 MB line is the kurucham
  relocation pattern; FB-masked content fits at 0.757×.
- MAME emulation status is the blanket naomi.cpp `GAME_FLAGS`
  (`MACHINE_IMPERFECT_GRAPHICS|MACHINE_IMPERFECT_SOUND|MACHINE_NOT_WORKING`, line
  10914), mirrored by arcadeitalia as "preliminary" — yet the title runs and renders
  fully under our fork (second campaign title after `illvelo` to do so).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot (4.00×, the DMPD fill artifact) — sixth full-bank park; M4 guts scan failed (kb §4.q); flagged first unpark candidate on the Radirgy-DC-2006 precedent (kb §6) |
| v4 | 2026-08-04 | 55.9 (B) | Unparked by the v4 ARAM content metric; M4 guts gap closed 2026-08-06 via the `carve_boot.py` bit-30 fix + `rescore_static.py` (guts 85.0, similarity 40.0; kb §4.q) |
| v8 | 2026-08-08 | 52.1 (B) | Re-capture. VRAM re-keyed on FB-masked content (sub 100.0) and ARAM measured by content volume for the first time; write-truth main 1.481× became binding (spec `2026-08-07-vram-fb-masking-design.md`) |
| v9 | 2026-08-08 | 79.0 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); binding region moved to ARAM |
