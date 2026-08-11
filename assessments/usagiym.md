# Usagi - Yamashiro Mahjong Hen (`usagiym`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **50.7 (B)** |
| Bottom line | Third and last mahjong-⚠ family, and the ⚠ dissolves the same way it did for shangril and suchie3: identical `naomi_mp` key-matrix cabinet, ruled `pad_adaptable` (50) with title-specific console precedent — Taito shipped a pad-played PS2 port of this exact game in 2004 (*Usagi -Yasei no Tōhai- THE ARCADE Yamashiro Mahjong Hen*). What holds it mid-B is ARAM: 2.97 MB of fill-excluded audio content vs the 2 MB cap (u 1.416 → sub-score 33.4), which the ^.40 memory weight makes decisive — main RAM (0.54× cap) and VRAM (0.88× incl. both framebuffers) are green. Streaming adds drag (0.71 re-read ratio at 14.7 MB/min) and guts takes the full −20 (EEPROM/serial/RTC/16 MB code blob). A port lives or dies on cutting ~1 MB of audio out of ARAM. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `usagiym` (no clones — sole `usagi*` set in naomi.cpp: ROM_START line 8631, GAME line 11260) |
| Maker / year | Warashi / Mahjong Kobo / Taito, 2003 (`/* 0022 */ GAME( 2003, usagiym, naomigd, naomigd, naomi_mp, naomi_state, init_naomigd_mp, ROT0, "Warashi / Mahjong Kobo / Taito", "Usagi - Yamashiro Mahjong Hen (Japan) (GDL-0022)", GAME_FLAGS )` — naomi.cpp @59e7c0b line 11260; title screen concurs, `shot-304s.png` "© Warashi 2003 © MAHJONG KOBO 2003") |
| Genre / format | Mahjong ⚠ (2v2 tag-team versus mahjong from the manga 兎 -野性の闘牌- by 伊藤誠, Takeshobo *Kindai Mahjong* — license line on the title card), **GD-ROM** `gdl-0022`, PIC16C622A 317-5096-JPN (naomi.cpp lines 8631–8645), 110.4 MB |
| Official DC port | **No** — but this exact game shipped on a pad console: *Usagi -Yasei no Tōhai- THE ARCADE Yamashiro Mahjong Hen*, PS2, Taito, 2004-09-16, "complete reproduction of the same arcade game" ([Game Watch 2004-08-14](https://game.watch.impress.co.jp/docs/20040814/usa.htm); [GameFAQs](https://gamefaqs.gamespot.com/ps2/924382-usagi-yasei-no-topai-the-arcade-yamashiro-mahjong-hen)). The series' first arcade game also got a PS2 port ([Game Watch 2003-04-02 review](https://game.watch.impress.co.jp/docs/20030402/usagi.htm)). GAME_FORMATS.md's `No` DC-port cell verified correct. |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent, sole member of the family; third of the three mahjong-⚠ families in the queue |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/usagiym.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Attract cycles character/story art (`shot-060s.png`), a full in-engine
demo hand — hand tiles with the mahjong panel's A–N key strip rendered under them
(`shot-121s.png`), title card (`shot-304s.png`), a versus cut-in (`shot-426s.png`), and a
demo game-over cutscene overlay (`shot-548s.png`) — all under FREE PLAY.
Screenshots: `evidence/usagiym/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-426s.png` · `shot-548s.png`
Anomalies: none — clean first-attempt full-window leg; battery-printed provisional 50.7 B stands
unchanged (the battery's `pad_adaptable` hint survived research).

## 4. Memory fit (axis: 33.4)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,050,692 | 16,777,216 | 0.539 | 100.0 | Address peak 32,520,896 (u 1.94, placement artifact) · `nz_above_cap` 1,680,442 B of content above the 16 MB line (see Risks) · `dma_high_water` 27,992,288 (informational) |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 7,352,485 | 8,388,608 | 0.876 | 94.3 | `content_total` 4,905,125 + 2×`fb_bytes` 1,223,680 · address peak 12,446,720 and `nz_above_cap` 3,039,189 are FB-placement artifacts — `regs_last` parks the second write FB at 0xc00000 (`fb_w_sof2`), the chocomk precedent the v8 FB-masking rekey exists for |
| ARAM (content volume, fill-excluded, `content_total`) | 2,969,444 | 2,097,152 | 1.416 | 33.4 | **The binding region.** 0.87 MB of real audio content over the cap — fill-excluded, so this is not the boot-time "DMPD" artifact · address peak 5,926,944 · `nz_above_cap` 2,033,296 |

Watermarks (informational, content-scan — stale-data prone): main 32,520,896 ·
vram 12,446,720 · aram 8,388,608 (the boot-time "DMPD" fill, not content).
Axis = min(regions) = ARAM's 33.4.

## 5. Cart streaming (axis: 63.3)

DMA events 7,553 · total 141.2 MB (148,064,256 B) · unique 40.6 MB (42,577,920 B) ·
re-read ratio 0.7124 · steady-state 14.674 MB/min (`short_window: false`) ·
PIO 17,061,184 B. Bandwidth sub-score 80.7; the 0.71 re-read ratio (sub-score 37.3)
drags the axis to 63.3. Note the source medium is already a GD-ROM — a DC port
streams from the same physical format, so the observed rate is natively achievable.

## 6. Guts (axis: 80.0)

Code 16,973,824 B · functions 2,270 · MMIO refs: scif 2, rtc 4, g2ext 146 ·
BIOS vector refs: none · penalties: `eeprom_bios` −5, `serial` −5, `rtc` −5,
`code_over_4mb` −5 → 80.0. Carve clean (`hdr_at` 0, title "USAGI YAMASHIROMAHJONGHEN",
base 0x8c020000, entry 0x8c021000 — single 16.2 MB code+data segment, hence the
`code_over_4mb` flag). SDK strings show the NEC/Sega GD-ROM-era stack — KAMUI2/
KAMUI-Darkness (NEC), Ninja2 2.01, Kunoichi2 2.07, sd2-for-DC 2.50.17 + manatee.drv
2.50.04 (AICA sound), gdCi/cvFs GD filesystem, syStartCwKn kernel — plus Warashi's own
`LIBTHINK.A` mahjong AI ("COPY RIGHT Warashi Inc. … Taito USAGI Version 03/04/15")
→ `sdk_overlap: partial`, `cart_loader_match: true` (gdCi/cvFs, the cleoftp GD loader).

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: the Sega Naomi **mahjong keyboard-matrix panel** — the exact hardware ruled
`pad_adaptable` for `shangril` and `suchie3` this same session. MAME gives `usagiym` the
stock `naomi_mp` INPUT_PORTS (GAME line 11260, with the GD-ROM variant init
`init_naomigd_mp`): a muxed key matrix — five strobed columns, keys **A–N** plus
**Kan/Pon/Chi/Reach/Ron/Bet/Flip-Flop/Last-Chance/Start** (naomi.cpp @59e7c0b lines
1994–2049), wiring "mahjong panel uses ext. I/O 4-8" with rows on JAMMA 17–22 (lines
1172–1190). The game's own demo UI maps those keys to the hand on screen — the A–N
letter strip under the tiles in `shot-121s.png`. Our fork emulates no such matrix —
`usagiym`'s ROM entry carries no per-game input struct
(`core/hw/naomi/naomi_roms.cpp:6036` @f014a410c) and `maple_jvs.cpp` has no mahjong
handling — yet the game attracts fine on the standard JVS digital path.

**Why `pad_adaptable`, not `awkward`:** the shangril/suchie3 precedent (same panel, same
matrix vocabulary, ruled tonight) plus a title-specific console precedent — **this exact
game shipped button-played**: Taito's PS2 port *Usagi -Yasei no Tōhai- THE ARCADE
Yamashiro Mahjong Hen* (2004-09-16), which contemporary press describes as a complete
reproduction of the arcade game ([Game Watch](https://game.watch.impress.co.jp/docs/20040814/usa.htm)) —
a DualShock has no mahjong panel by construction. The series' first arcade game got the
same treatment in 2003. Mahjong is turn-based with no timing pressure, so cursor-over-
tiles plus call buttons loses nothing mechanical. Not `stick` (100): the panel's ~20
discrete keys cannot map 1:1 onto a pad; the tile-cursor UI layer is real (if
already-solved) work.

Proposed DC mapping: D-pad/stick = tile cursor, A = discard/confirm, B = cancel,
X/Y/triggers = Pon/Chi/Kan/Reach/Ron prompts (context-sensitive call prompts, the DC
mahjong idiom), Start = start — or crib the PS2 port's scheme.
Sources: all seven citations are in sidecar `controls.sources` (MAME GAME row + matrix +
wiring, Flycast fork input path, Game Watch 2004 + GameFAQs PS2 port, Game Watch 2003
series precedent, in-demo A–N strip evidence).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 33.4^.40 · 63.3^.20 · 80.0^.20 · 50.0^.10 · 70.0^.10 = **50.7 (B)**
Similarity inputs: developer no, SDK overlap partial (NEC/Sega GD stack + Warashi AI lib, §6), loader match yes (gdCi/cvFs GD loader).

## 9. Risks & notes

- **ARAM is the whole story**: 2,969,444 B of fill-excluded audio content vs the 2 MB
  cap (u 1.416) — about 0.9 MB of sound must be cut, downsampled, or re-streamed
  before anything else matters. The sound stack is stock sd2/manatee (AICA-native),
  so ADPCM recompression and on-demand bank loads are the standard levers. First
  thing to map.
- **Main RAM is comfortable** (9.05 MB content, u 0.54) but 1,680,442 B of it sits
  above the 16 MB line (`nz_above_cap`; DMA high-water 27,992,288) — relocation work,
  not capacity work.
- **VRAM fits with both framebuffers counted** (7.35 MB, u 0.876) — the scary raw peak
  is the second write FB parked at 0xc00000 (`regs_last` `fb_w_sof2`), the usual
  placement artifact. Re-base the FB, done.
- **High streaming re-read ratio (0.71)** — 141 MB moved over 10 minutes against a
  40.6 MB unique working set; flags asset-reload-per-scene attract design. Mitigating:
  the source is already a GD-ROM, so a DC port streams the identical medium at an
  observed 14.7 MB/min — native territory, no format translation risk.
- **Versus/network code is present but optional**: NLCB + "NO COMMUNICATION BOARD" +
  `mjs*` client/server state strings in the carve; the standard single cabinet has no
  comm board — a port drops versus-link.
- `serial` guts flag is 2 SCIF refs — debug-console residue, not gameplay I/O.
- The 2004 PS2 port is a ready-made reference for control scheme and any content cuts.
- Rendering must be verified on real DC hardware (working-style rule); evidence here is
  fork-rendered attract only.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 50.7 (B) | Initial assessment — third mahjong-⚠ family. Clean full-window first-attempt leg, demo reached; controls research confirmed the battery's `pad_adaptable` hint (same naomi_mp matrix as shangril/suchie3; title-specific precedent: Taito's 2004 PS2 port of this exact game), so the provisional 50.7 stood. ARAM content over cap (u 1.416) is the binding axis |
