# Mamoru-kun wa Norowarete Shimatta! (Japan) (841-0060C) (`mamonoro`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **76.7 (A)** |
| Bottom line | Comedic curtain-fire shmup whose memory fits under content keying — VRAM is the binding region at 0.998× cap (FB-masked content plus a verified 24bpp 640×478 double framebuffer) — and portability is proven twice over: G.Rev's own Under Defeat Naomi→DC self-port and this exact game's pad-native X360/PS3 ports. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `mamonoro` (no clones — `parent: null` in controls.json; single GAME line `/* 0060 */`, MAME src/mame/sega/naomi.cpp @59e7c0b line 11118) |
| Maker / year | G.Rev + co-developer Gulti, 2008 (arcade JP 2008-07-30, [Wikipedia](https://en.wikipedia.org/wiki/Mamorukun_Curse!)). MAME credits "G.Rev"; the G.REVOLUTION logo card appears in attract (`shot-310s.png`, deleted surplus) |
| Genre / format | Shmup ★ (comedic curtain-fire, free-scrolling, ROT270), **M4 cartridge** 841-0060C — 3× 512 Mb flash (`ic8/ic9/ic10.bin`, IC11 populated-but-empty) + PIC `317-5132-jpn`, rom_board id 5504, machine `naomim4` (naomi.cpp @59e7c0b M4 cart table line 669 + `ROM_START(mamonoro)` line 6740). 146.1 MB zip. Note: arcadeitalia's "GD-ROM" and "BAD DUMP" claims are both contradicted by the MAME source (naomim4 cart; no `BAD_DUMP` macro anywhere in `ROM_START(mamonoro)`, full CRC+SHA1 on all ROMs) — primary source wins, same arcadeitalia artifact as `illvelo` |
| Official DC port | No — the port lineage skips DC entirely: X360 JP retail 2009-06-25 (pub. G.rev) → **PS3 JP 2011-03-31 *Meikai Katsugeki Wide-ban*** (pub. CyberFront; HD widescreen, X360 DLC characters bundled, new Meikai Katsugeki mode — [Wikipedia](https://en.wikipedia.org/wiki/Mamorukun_Curse!), [VGMdb](https://vgmdb.net/release/28452), [GameTDB BLJM60323](https://www.gametdb.com/PS3/BLJM60323), [Siliconera](https://www.siliconera.com/mamoru-kun-shoots-its-way-to-playstation-3/)) → PS3 NA digital *Mamorukun Curse!* 2013-07-16 (UFO Interactive) → *Mamorukun ReCurse!* 2025 (City Connection; PC/Switch/PS5/XSX) |
| Community ports | None found (searched 2026-08-03). **Conflation trap:** the July 2026 Time Extension / Dreamcast Junkyard "Naomi port for Dreamcast" coverage ([Time Extension](https://www.timeextension.com/news/2026/07/were-finally-getting-a-naomi-port-for-dreamcast-but-the-monkeys-paw-curls), [DC Junkyard](https://www.thedreamcastjunkyard.co.uk/2026/07/naomi-fan-ports-are-finally-coming-to.html)) is **this project's own Cleopatra Fortune Plus port**, not mamonoro — a web-search summary conflated the two during research. No mamonoro DC conversion exists |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom:
`naomi/mamonoro.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle:
manga story card → title card over live gameplay footage with LIFE hearts + NOROI
(curse) gauge HUD → Beniko ranking table → night-stage gameplay with HUD →
character panel.
Screenshots: `evidence/mamonoro/shot-121s.png` · `shot-182s.png` · `shot-243s.png` ·
`shot-426s.png` · `shot-548s.png` (manga story card, title over gameplay footage,
Beniko ranking table, night-stage gameplay with HUD, character panel)
Anomalies: none numerically — every scored counter (memory/streaming/guts/controls/
similarity, `scores.final` 76.7 A) reproduced byte-identical between the v8 sidecar
and this fresh v9 capture; only `assessed` and `versions.battery` differ. Per-frame
demo content at matching timestamps drifted slightly from v8 (`shot-182s.png` now
shows the title card over a grass-stage gameplay loop rather than the shrine-island
backdrop cited in v8) — expected, since attract-mode timing isn't frame-locked
across separate runs, and it doesn't change the coverage classification.

## 4. Memory fit (axis: 85.2)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 12,939,092 | 16,777,216 | 0.771 | 100.0 | address peak 26,807,247 (u 1.598, informational) — matches the pre-v8 informational watermark exactly: real writes, not stale data (same pattern as chocomk/sgtetris/gunsur2/marstv) · nz_above_cap 6,337,712 · `dma_high_water` 22,092,160 |
| VRAM (FB-masked content + 2×FB) | 8,370,867 (content_total 6,535,347 + 2×`fb_bytes` 917,760) | 8,388,608 | 0.998 | 85.2 | **binding region** — 17,741 B under cap. `fb_bytes` 917,760 B is a genuine game-programmed mode, not register garbage: earliest samples read the BIOS-default 614,400 B then flip to a stable 1,920-byte stride × 478 lines = 640×478 at 24bpp for the rest of the window (live `FB_R_SIZE`/`FB_W_LINESTRIDE` each sample) · raw address peak 13,718,016 (u 1.64) is extent |
| ARAM (content volume, fill-excluded, `content_total`) | 1,265,219 | 2,097,152 | 0.603 | 100.0 | address peak 2,064,240 — under the 2 MiB cap even address-keyed |

Watermarks (informational, content-scan — stale-data prone): main 26,807,247 ·
vram 13,718,016 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 67.9)

DMA events 617 · total 136.5 MB · unique 53.3 MB · re-read ratio 0.6095 ·
steady-state 13.088 MB/min (`short_window: false`) · PIO 2,099,776 B

## 6. Guts (axis: 85.0)

Code 2,097,152 B · functions 3,446 · MMIO refs: scif 2, rtc 3, g2ext 364 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → −15.
M4 boot blob carved at base `0x8c020000`, entry `0x8c021000` (header title
"MAMO NORO") — needs the `carve_boot.py` bit-30 mask (M4 encrypted-read flag, MAME
`src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast `m4cartridge.cpp:115,132`;
kb §4.q).

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + **2 buttons** (A shot, B chargeable curse bomb) — the lightest
scheme in the campaign. `controls.device_class = stick`.
Proposed DC mapping: 1:1 on a stock DC pad; every console port shipped on standard
pads (PS3 even offers optional twin-stick).
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT270);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=mamonoro)
(8-way joystick, JVS 6-button declaration, "[A] Shoot, [B] Bomb");
[Wikipedia](https://en.wikipedia.org/wiki/Mamorukun_Curse!);
[PlayStation.Blog](https://blog.playstation.com/2013/06/25/how-to-shmup-mamorukun-curse-from-the-makers-of-ikaruga/)
(curse button charges up to three levels, clears standard bullets).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 85.2^.40 · 67.9^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **76.7 (A)**
Similarity inputs: developer no (reference-list artifact — reference `makers` lists
only `Altron / Taito`, despite G.Rev's first-party Naomi→DC pedigree; same checkpoint
note as `illvelo`/`senko`), SDK overlap partial, loader match no.

## 9. Risks & notes

- **VRAM is at the cap edge**: fit is 8,370,867 B against 8,388,608 — 17,741 B of
  margin — driven by the game's 24bpp 640×478 double framebuffer. The FB mode is the
  first lever a real port would examine.
- **Main RAM is address-sparse but the heaviest content in this cluster:** content
  volume 12.9 MB (0.77×) with the touched address peak at 26,807,247 B (1.60× cap,
  confirmed real writes) and 6.3 MB of nonzero bytes above the 16 MB line —
  layout/relocation work needed.
- **ROT270 vertical screen.** A DC port must handle tate/yoko presentation — solved
  in-family: Karous DC shipped 2007 with proper TATE support; mamonoro's own Wide-ban
  PS3 port solved widescreen presentation.
- MAME emulation status: blanket naomi.cpp `GAME_FLAGS`
  (IMPERFECT_GRAPHICS|IMPERFECT_SOUND|NOT_WORKING, line 10914) — per kb §4.r no
  per-title signal; the title runs and renders fully under our fork.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot read as 4.00× cap — the DIMM "DMPD" fill artifact; eleventh full-bank park, with the maximal sibling-precedent stack (Under Defeat DC self-port + own X360/PS3 ports). M4 static scan also failed (kb §4.q, §7) |
| v4 | 2026-08-04 | 46.6 (B) | Unparked by the v4 fill-excluded ARAM content metric (kb §7); attract demo renders; 2026-08-06 `carve_boot.py` bit-30 fix unlocked M4 guts (85.0) + similarity (40.0) via `rescore_static.py` (kb §4.q) |
| v8 | 2026-08-08 | 47.8 (B) | Re-capture (leg 2 after an `emulator-exited` flake, kb §7). VRAM re-keyed to FB-masked content + 2×FB with `fb_bytes` 917,760 verified genuine (spec `2026-08-07-vram-fb-masking-design.md`); main write-truth 26,807,247 binding at sub 26.1 |
| v9 | 2026-08-08 | 76.7 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory 85.2, binding region moved to VRAM |
| v9 | 2026-08-09 | 76.7 A | ranking-groom chunk 3: fresh v9 capture, provenance v8→v9 (scoring keys unchanged) |
