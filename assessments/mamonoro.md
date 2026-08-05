# Mamoru-kun wa Norowarete Shimatta! (Japan) (841-0060C) (`mamonoro`) — portability assessment

> **Battery v4 re-assessment (2026-08-04): **46.6 (B)**.**
> v2 parked it G3-aram via the DMPD fill artifact. v4 content metric: scored; attract demo renders (logo-overlay gameplay, shot-182s).
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **46.6 (B)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/mamonoro.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 22,092,160 | 16,777,216 | 1.32 |  |
| VRAM (write-truth diff) | 13,718,016 | 8,388,608 | 1.64 | nz_total 7,422,814 |
| ARAM (content, fill-excluded) | 2,064,240 | 2,097,152 | 0.98 | content above cap 0 |

Streaming: 617 DMA events · total 136.5 MB · unique 53.3 MB · re-read 0.6095 · steady 13.057 MB/min
Axes: memory 24.6 · streaming 68.0 · guts 85.0 · controls 100.0 · similarity 40.0 → **final 46.6 (B)**
Screenshots: `evidence/mamonoro/shot-060s.png` · `evidence/mamonoro/shot-182s.png` · `evidence/mamonoro/shot-365s.png` · `evidence/mamonoro/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the **eleventh** boot-time full-bank G3-aram park in the campaign. The sibling-precedent stack is maximal for this title: G.Rev's own Under Defeat Naomi→DC self-port (the `senko` precedent) **plus** mamonoro's own pad-native X360/PS3 console ports prove both the studio's and this exact game's portability. Outside the gate it is light: main RAM 1.32× (second-lightest after `radirgyn`'s 1.17×) and VRAM 1.60× extent with 7.17 MB actual content — a strong unpark candidate behind `ausfache` and `radirgyn`. The title renders fully under the fork — attract demo confirmed. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 40.0 s · run 600 s · rom: `naomi/mamonoro.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. Full rendering
(vertical 480×640); the attract cycle observed across the 10 battery shots: NAOMI splash →
manga story card → title over a 3D shrine island → live attract gameplay with LIFE hearts +
NOROI (curse) gauge HUD → G.REVOLUTION logo → story panels → character profile → second
attract gameplay (night stage) → Mayuno RANKING table.

Screenshots kept (5 of 10):
- `assessments/evidence/mamonoro/shot-121s.png` — early attract: manga story card (Mamoru startled by the red curse imp), PRESS START / FREE PLAY
- `assessments/evidence/mamonoro/shot-183s.png` — title screen: logo over 3D floating shrine island with torii, ©2008 G.REV LTD.
- `assessments/evidence/mamonoro/shot-246s.png` — attract gameplay: player firing blue shots up a grass/cliff stage, LIFE hearts + NOROI curse gauge HUD, treasure chest and bullets on screen
- `assessments/evidence/mamonoro/shot-490s.png` — attract gameplay, night stone-path stage: player character, rabbit enemies, enemy bullets, full HUD
- `assessments/evidence/mamonoro/shot-544s.png` — "Mayuno RANKING" high-score table over the 3D island

Deleted surplus (5): NAOMI boot splash, G.REVOLUTION logo card, second manga story panel, Beniko Higatera character profile, white transition flash.
Anomalies: none — full rendering under the fork.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,291,456 B` nonzero above
the cap at scan. Boot-time full-bank load — **eleventh** in the kb §6 tally after
`ikaruga`, `azumanga`, `ss2005`, `takoron`, `illvelo`, `radirgyn`, `senko`, `senkosp`,
`ausfache`, `inunoos`.

**Sibling-precedent stack — maximal for this title:** (a) G.Rev itself shipped its own
Naomi shmup *Under Defeat* on Dreamcast (2006, developed and published by G.Rev — the
`senko` precedent line), so the studio provably fit its Naomi-era sound into 2 MiB AICA;
(b) **this exact game** shipped pad-native console ports (X360 2009, PS3 2011/2013, see
§2), so the title itself is proven portable off Naomi. The 8 MiB bank measures Naomi-side
luxury, not intrinsic unportability.

Outside the gate mamonoro is light: main-RAM DMA high-water `22,092,160 B` (1.32× the
DC's 16 MB — second-lightest among the full-bank parks after `radirgyn`'s 1.17×) and VRAM
peak `13,449,728 B` (1.60×), with nonzero content `7,166,193 B` total and `3,958,684 B`
above the 8 MB line — partly the high-parked-asset address-extent pattern (`kurucham`),
so relocation helps. **Third-strongest unpark candidate** behind `ausfache` (everything
but sound fits) and `radirgyn` (main 1.17×/VRAM 1.33×).

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at the
gate): streaming 442 DMA events, `102,471,680 B` total / `55,398,400 B` unique, re-read
ratio 0.4594, steady-state 8.909 MB/min (`short_window: false`). Guts was
**unavailable at v2 time**: `static scan: load entry out of file:
rom=0x40000000 len=0x200000` — fifth instance of the kb §4.q M4-cart carve failure
(zunou, illvelo, radirgyn, ausfache) — so `guts.flags` was BIOS-only (`[eeprom_bios]`)
and `sdk_strings` was empty. Similarity inputs from the sidecar at that time:
`developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false` — the
developer false is the known reference-list artifact (reference `makers` lists only
`Altron / Taito`), despite G.Rev's first-party Naomi→DC pedigree; same checkpoint note
as `illvelo`/`senko`. **Re-scanned 2026-08-06** after the `carve_boot.py` bit-30 fix:
the M4 load-entry rom offset carries bit 30 as an encrypted-read flag, not a file
offset (MAME `src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast
`m4cartridge.cpp:115,132` @ebae3b513); masking it (`& 0x1ffffffe`) lets the scan carve
and Ghidra-analyze the 2 MiB boot blob → `guts.dat_available = true`, guts axis
**85.0**, `similarity.sdk_overlap = "partial"`, similarity axis **40.0**
(`developer_match` and `cart_loader_match` remain false — v4 axes above; capture
itself was not re-run).

What would unblock it: a per-title audio trim (downsample PCM/ADPCM — in-house precedent
in Under Defeat DC, and the game's own console ports), plus modest main-RAM reduction at
1.32× and VRAM relocation/trimming.

## Risks & notes

- **Controls are the lightest scheme in the campaign**: `controls.device_class = stick` —
  8-way stick + **2 buttons** (A shot, B chargeable curse bomb). 1:1 on a stock DC pad;
  every console port shipped on standard pads (PS3 even offers optional twin-stick).
  Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT270);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=mamonoro)
  (8-way joystick, JVS 6-button declaration, "[A] Shoot, [B] Bomb");
  [Wikipedia](https://en.wikipedia.org/wiki/Mamorukun_Curse!);
  [PlayStation.Blog](https://blog.playstation.com/2013/06/25/how-to-shmup-mamorukun-curse-from-the-makers-of-ikaruga/)
  (curse button charges up to three levels, clears standard bullets).
- **ROT270 vertical screen.** A DC port must handle tate/yoko presentation — solved
  in-family precedent: Karous DC shipped 2007 with proper TATE support (line established
  in `illvelo.md`); mamonoro's own Wide-ban PS3 port solved widescreen presentation.
- **M4 guts gap: closed 2026-08-06.** `carve_boot.py` now masks bit 30 (the M4
  encrypted-read flag) on cart load-entry offsets, so the static scan carves and
  Ghidra-analyzes the boot blob. Re-scored via `tools/assess/rescore_static.py`
  (guts 85.0, similarity 40.0, final 46.6 B above — up from tier C); capture was not
  re-run.
- MAME emulation status: blanket naomi.cpp `GAME_FLAGS`
  (IMPERFECT_GRAPHICS|IMPERFECT_SOUND|NOT_WORKING, line 10914) — per kb §4.r no per-title
  signal; the title runs and renders fully under our fork.
- Main watermark `26,744,783 B` (informational, content-scan — stale-data prone) is 1.21×
  the DMA high-water; moderate gap, treat the high-water as the load-bearing figure.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset.
