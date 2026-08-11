# Mushiking The King Of Beetles - Mushiking II / III / III+ (Ver. 2.001) (World) (`mushik2e`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **70.5 (A)** |
| Bottom line | Sega's kids' card-battle machine measures green on every technical axis — all three memory regions ≤0.62× cap under content keying, streaming a trivial 1.55 MB/min — and the ⚠ that queued it (barcode card reader + card dispenser) turns out to be fully software-replaceable: the fork already emulates the whole card path in pure software (barcode digits over SCIF serial, RFID management chip on maple, dispenser status spoofed in JVS), and actual play is three rock-paper-scissors buttons. Controls rule `pad_adaptable` (50), not off-ladder: a DC port needs a card-select UI, not hardware. Score is dragged below its cohort's S-range by that 50 plus a missing guts axis (EPR-mode M4 cart defeats the carve) and floor similarity. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `mushik2e` (MAME parent; covers clones `mushi2eo` "Ver. 1.001 (World)" and `mushik2k` "Ver. 1.000- (Korea)" — MAME src/mame/sega/naomi.cpp @59e7c0b GAME lines 11037–11041; the Korea clone needs an undumped rev.H Korea BIOS, comment line 6617). **Multi-version set:** one cart carries Mushiking II, III and III+, switched in a secret menu ("in game test mode highlight EXIT then press P1+P2 buttons 2 30 times", naomi.cpp line 6587; "~equivalent of Japanese 2K5 versions", GAME line 11038). Sibling families NOT covered: `mushike` (2K3, 2004, M1 board, 4 clones incl. the MUSHIUSA prototype), the five Japanese `mushi2k*` sets (2003–2006, all separate parents), and `mushik4e`/`mushik4t` (IV/V/VI, 2007) |
| Maker / year | Sega, 2005 |
| Genre / format | Card battle (barcode-card beetle collecting + rock-paper-scissors button combat), **cart, Naomi M4** 840-0164, rom_board id `5582`, PIC 317-0437-COM — ROM_START lines 6601–6614: 2× 64 MiB flash (fpr-24333/24334) + 4 MiB `epr-24357.ic7` loaded over offset 0 ("EPR mode, overwrite FPR data", line 6607) |
| Official DC port | No — home versions are GBA (2005, Japan) and Nintendo DS (2007) only ([Wikipedia](https://en.wikipedia.org/wiki/Mushiking:_The_King_of_Beetles)) |
| Community ports | None found (searched 2026-08-11) — only Naomi music rips catalogued under the DC sound format ([Zophar DSF page](https://www.zophar.net/music/sega-dreamcast-dsf/mushiking-the-king-of-beetles)), no port project |
| Representative choice | MAME parent of the II/III/III+ family, latest World revision (Ver. 2.001 over `mushi2eo`'s 1.001); assessed by explicit user order despite the ⚠ Card battle queue flag |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/mushik2e.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop cycles in-engine 3D story cutscenes (Popo-and-fairy narrative,
`shot-060s.png`, `shot-609s.png`), the title card pair "This is a free game / You'll get a card"
(`shot-182s.png`), a clean title screen (`shot-304s.png`), and a barcode-card gallery showcasing
the collectible cards themselves (`shot-487s.png`) — all under a FREE PLAY banner.
Screenshots: `evidence/mushik2e/shot-060s.png` · `shot-182s.png` · `shot-304s.png` · `shot-487s.png` · `shot-609s.png`
Anomalies: none — clean single leg; battery-printed provisional 76.9 A (pre-research `stick` placeholder).
The `raw/` log dir had already been rotated out by the next battery's startup at doc time; all
quoted numbers are sidecar fields.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 4,208,384 | 16,777,216 | 0.251 | 100.0 | address peak 33,292,352 (u 1.98, informational — placement artifact under content keying) · `nz_above_cap` 1,900,058 B of content above the 16 MB line (see Risks) · `dma_high_water` 27,542,752 (informational) |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 3,197,135 | 8,388,608 | 0.381 | 100.0 | `content_total` 1,968,335 + 2×`fb_bytes` 614,400 · `nz_above_cap` 0 · address peak 6,634,783 (u 0.791) |
| ARAM (content volume, fill-excluded, `content_total`) | 1,293,578 | 2,097,152 | 0.617 | 100.0 | address peak 2,097,136 (16 B under cap — full-bank touch is uniform fill, kb §6) · `nz_above_cap` 0 |

Watermarks (informational, content-scan — stale-data prone): main 33,292,352 ·
vram 9,692,984 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 78.0)

DMA events 1,530 · total 26.2 MB (26,208,256 B) · unique 11.0 MB (10,967,040 B) ·
re-read ratio 0.5815 · steady-state 1.553 MB/min (`short_window: false`) ·
PIO 3,148,352 B. Bandwidth is trivial (sub-score 100); the 0.58 re-read ratio
(sub-score 45.1) caps the axis at 78.0.

## 6. Guts (axis: n/a — no .dat, weights renormalized)

`guts.dat_available = false`: `cart2dat.py` fails with `no NAOMI header at 0 or
0x800000 after decrypt (offset 0 = b'\x02\xde\xddB_\xee\xf3U')` (sidecar `guts.error`,
`cart2dat.py:160`). This is NOT the solved kb §4.q bit-30 carve bug (ausfache and
other plain M4 carts scan fine post-fix) — it is a new sub-case: mushik2e is an
**EPR-mode hybrid** (4 MiB `epr-24357.ic7` overlaid on offset 0 of the M4 flash
image, naomi.cpp line 6607), and the assembled head is neither plaintext (`NAOMI`
absent raw → M4-plain path not taken) nor recoverable by the whole-ROM M4 stream
decrypt. Flycast's own M4 loader boots it regardless (§3). Guts axis dropped;
`flags: [eeprom_bios]` recorded but unused. Logged as a kb lesson.

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: Sega's kids' card machine — a **barcode card scanner** (players scan
lengthwise-barcode beetle and skill cards to load their fighter), a **card dispenser**
(one collectible card vends per play — the attract's own "You'll get a card",
`shot-182s.png`), an internal rewritable **RFID management chip**, and **three
attack buttons** playing rock-paper-scissors (Hitting / Pinching / Throwing)
([Wikipedia](https://en.wikipedia.org/wiki/Mushiking:_The_King_of_Beetles)).
JVS input side is the plain digital-button standard: MAME INPUT_PORTS `naomi`
(GAME line 11038).

**Why `pad_adaptable`, not off-ladder:** the fork proves the entire card path is
pure software, no physical hardware required to reach or play core gameplay —

- gameId `MKG TKOB*` → `card_reader::barcodeInit()` (`core/hw/naomi/naomi_cart.cpp:695-703`
  @f014a410c); the `BarcodeReader` pipes typed card digits + `'*'` terminator straight
  into the game over SCIF serial (`core/hw/naomi/card_reader.cpp:681-737`);
- the RFID management chip is auto-generated (`MUSHIKING_CHIP_DATA`, with a
  mushik2e-specific mask keyed on gameId `"MKG TKOB 2 JPN VER2.001-"`,
  `core/hw/maple/maple_jvs.cpp:2740-2782`) and auto-inserted on two maple RFID
  reader/writer devices (`core/hw/maple/maple_cfg.cpp:248-258`);
- dispenser health is spoofed in the JVS board (`jvs_837_13551_mushiking` forces
  "dispenser OK", cancels empty/jammed signals, `core/hw/maple/maple_jvs.cpp:1249-1278`);
- the UI exposes a Barcode Card text field (`core/ui/gui.cpp:647-655`) and a
  pad-mappable "Insert Card" button (`DC_BTN_INSERT_CARD`,
  `core/ui/settings_controls.cpp:279`).

Proposed DC mapping: A/B/X = the three attack buttons, Start; card scanning becomes
an in-game card-select UI (Flycast's barcode-string-over-SCIF is the exact software
seam to hook), RFID chip persistence → VMU. Not `stick` (100): the card flow is the
game's core loop and needs that re-implemented UI, not a 1:1 mapping. Not off-ladder
`card_reader` → G2: unlike `dragntr`'s medal hopper, nothing here is physically
unmappable — every card interaction is already demonstrated in software.
Sources: all of the above + MAME GAME line citation are in sidecar `controls.sources` (8 entries).

## 8. Score computation

final = memory^.50 · streaming^.25 · controls^.125 · similarity^.125 (guts dropped, spec §4.3)
      = 100.0^.50 · 78.0^.25 · 50.0^.125 · 20.0^.125 = **70.5 (A)**
Similarity inputs: developer no, SDK overlap none (no sdk_strings — carve failed, §6), loader match no.

## 9. Risks & notes

- **1.9 MB of main-RAM content sits above the 16 MB line** (`nz_above_cap`
  1,900,058; address peak 1.98× cap). Content volume (4.2 MB) fits four times
  over, but a port must relocate whatever lives up there — first thing to map.
- **Scored M4 title with no guts axis** (kb §4.q's checkpoint warning applies):
  missing guts + floor similarity make 70.5 a lower-bound-flavored score; EPR-mode
  support in `cart2dat.py` would firm it up.
- **Card-flow UI is the real porting work.** The three-button game itself is
  trivially pad-mappable; budget the effort for a card-select/collection UI
  (and VMU persistence for the management-chip counters). The fork's
  barcode-over-SCIF + maple-RFID emulation (§7) is a complete blueprint.
- **Rendering must be verified on real DC hardware** (working-style rule); our
  evidence is fork-rendered attract only — no battle gameplay was reachable
  unattended (attract never demos a fight; it cycles story/title/card gallery).
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r);
  the game runs under our fork regardless.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 70.5 (A) | Initial assessment (⚠ Card battle family, by explicit user order). Battery-printed 76.9 A was the `stick` placeholder; controls research ruled `pad_adaptable` (card path fully software-emulable per fork source) → 70.5. Guts absent: EPR-mode M4 defeats cart2dat (new kb sub-case) |
