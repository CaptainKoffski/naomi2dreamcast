# Jingi Storm - The Arcade (Japan) (GDL-0037) (`jingystm`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **90.0 (S)** |
| Bottom line | Late (2006) 3D fighter built on the stock Sega Naomi SDK whose content volumes all fit DC caps with room to spare (main 0.56×, VRAM 0.52×, ARAM 0.65×), light GD streaming, standard stick+3-button controls — the main port work is address-layout relocation, not capacity. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `jingystm` (single member — `parent: null` in controls.json; one `ROM_START( jingystm )` in naomi.cpp @59e7c0b line 8907, no clones) |
| Maker / year | Atrativa Japan, 2006 (JP arcade release 2006-09-20, [Mizuumi wiki](https://mizuumi.wiki/w/Jingi_Storm:_The_Arcade)) |
| Genre / format | 3D fighter, **NAOMI GD-ROM** GDL-0037, ROT0 — MAME src/mame/sega/naomi.cpp @59e7c0b GAME line 11284 (`naomigd`, `init_naomigd`), PIC `317-5122-jpn` |
| Official DC port | No |
| Community ports | None of Jingi Storm itself (searched 2026-08-11). Lineage note: the game is a heavy rework of Anchor Inc.'s cancelled ~2003 Atomiswave fighter *Force Five* — Atrativa bought the code/assets and shipped it as Jingi Storm in 2006 ([Cancelled Games wiki](https://cancelled-games.fandom.com/wiki/Force_Five)). After a 2021 prototype-ROM leak, dreamcast-talk user megavolt85 released an unofficial **DC port of Force Five** — the Atomiswave ancestor, not this NAOMI build ([RetroRGB](https://retrorgb.com/new-dreamcast-atomiswave-arcade-ports-unreleased-fighters-kenju-force-five.html), [dreamcast-talk t=13989](https://www.dreamcast-talk.com/forum/viewtopic.php?t=13989)). Community consensus is that no DC conversion of the NAOMI release exists ([dreamcast-talk t=14198](https://www.dreamcast-talk.com/forum/viewtopic.php?t=14198)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/jingystm.zip`
Attract/demo reached: **demo reached** — live in-engine attract fight ("DEMONSTRATION" HUD)
in `shot-121s.png` by 121 s; loop then cycles title ↔ demo fights ↔ CRI ADX logo
(`shot-243s.png` title, `shot-304s.png`/`shot-487s.png` further demo stages;
sidecar `capture.coverage = "demo"`). No static pre-game screen — 7 unique md5s across
the 10 shots, not the byte-identical EEPROM-prompt class (kb §4.vi).
Screenshots: `evidence/jingystm/shot-060s.png` · `shot-121s.png` · `shot-243s.png` · `shot-304s.png` · `shot-487s.png`
Anomalies: none — single clean leg (battery log: `leg 1: jingystm.zip attempt 1 -> ran full window`).

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,478,613 | 16,777,216 | 0.565 | 100.0 | address peak 15,556,128 (u 0.927, informational) · `dma_high_water` 15,497,152 (informational floor) · 0 bytes above cap — grep `CARTDMA` in raw log |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 4,358,334 | 8,388,608 | 0.520 | 100.0 | `content_total` 3,129,534 + 2×`fb_bytes` 614,400 · `nz_total` 3,722,677 of which `nz_above_cap` 3,697,667 — nearly all content sits above the 8 MB boundary because the game places its framebuffers at `fb_w_sof1=0x800000` / `fb_w_sof2=0xc00000` (sidecar `regs_last`); volume fits, layout must be relocated — grep `VRAMPROFILE` |
| ARAM (content volume, fill-excluded, `content_total`) | 1,361,758 | 2,097,152 | 0.649 | 100.0 | address peak 1,476,016 (u 0.704) · 0 bytes above cap — grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 15,556,128 ·
vram 13,795,328 (address-space watermark across the FB banks above 8 MB) ·
aram 8,388,608 (the boot-time DIMM "DMPD" fill, kb §7 — not content).

## 5. Cart streaming (axis: 83.2)

DMA events 407 · total 25.4 MB (26,609,664 B) · unique 14.3 MB (15,028,224 B) ·
re-read ratio 0.4352 · steady-state 2.171 MB/min (`short_window: false`) ·
PIO 2,098,496 B

## 6. Guts (axis: 85.0)

Code 2,097,152 B · functions 2,342 · MMIO refs: scif 2, rtc 3, g2ext 106 ·
BIOS vector refs: none · penalties applied: flags `eeprom_bios`, `serial`, `rtc`.
GD boot blob carved at base `0x8c020000`, entry `0x8c021000`, header title
`JINGI STORM THE ARCADE` (sidecar `carve_meta`).
SDK strings: stock Sega Naomi stack — Ninja Ver 012000114 (`njLoadTexturePvmMemory`),
Kunoichi Library for NAOMI 0.99, nlam/nlajamma NAOMI LIBRARY FOR AM, KM1Naomi 1.33,
`sd for DC Ver 2.02.12` sound driver, CRI ADX(T) 5.94 / mwLib 2.44 middleware,
zlib inflate 1.1.4 — binary build date `Build:Aug 06 2006`.

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + 3 attack buttons (Guard / Punch / Kick; supers = motion + G+P+K), 2P.
`controls.device_class = stick`. MAME input ports: `naomi`.
Proposed DC mapping: 1:1 on a stock DC pad (A/B/X + Start); native on the DC Arcade Stick.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line 11284);
Flycast fork `core/hw/naomi/naomi_roms_input.h:555`
`INPUT_3_BUTTONS("GUARD", "PUNCH", "KICK")` (strongest per-title citation);
[Mizuumi wiki Controls/System](https://mizuumi.wiki/w/Jingi_Storm:_The_Arcade/Controls/System)
("3 button game, with a punch, kick, and guard button");
[GameFAQs guide](https://gamefaqs.gamespot.com/arcade/975571-jingi-storm-the-arcade/faqs/79284/introduction).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 83.2^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **90.0 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes.

## 9. Risks & notes

- **Port-planning takeaway: capacity is fine, layout is the work.** No region's
  content volume exceeds 0.65× its DC cap and zero bytes land above any cap in
  volume terms — but both main RAM and VRAM are address-sparse: main touches up
  to 15.56 MB of address space for 9.5 MB of content, and VRAM parks its
  framebuffers at 0x800000/0xc00000 (Naomi has 16 MB VRAM, DC has 8 MB), so
  3,697,667 of 3,722,677 non-zero VRAM bytes sit above the 8 MB boundary (§4).
  A port must relocate the FB/texture layout below 8 MB; the volume fits.
- ARAM watermark shows the full 8 MiB bank but that is the DIMM firmware "DMPD"
  fill (kb §7); real audio content is 1.36 MB — comfortable.
- Streaming is light for a GD title (2.17 MB/min steady, 14.3 MB unique over
  600 s) — attract loop only; in-game per-character/stage loads should be
  spot-checked in a longer capture before committing to a streaming design.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal,
  kb §4.r); the game runs full-window under our fork.
- Rendering must be verified on real DC hardware (working-style rule) — all
  evidence here is Flycast-fork capture.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 90.0 (S) | First assessment |
