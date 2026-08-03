# Illvelo (Illmatic Envelope) (Japan) (841-0059C) (`illvelo`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the fifth boot-time full-bank G3-aram park in the campaign and the **first on a cartridge** (all prior were GD-ROM). It is also the strongest sibling-precedent case yet that this gate over-parks: Milestone's own Radirgy and Karous — same maker, near-identical vertical-shmup engine, both ROT270 — shipped official Dreamcast ports whose sound necessarily fits the DC's 2 MiB AICA RAM, so the 4× bank is Naomi-side luxury, not intrinsic unportability (see Gate). Main RAM (1.63×) and VRAM (1.69× extent, 4.76 MB actual content) are also over cap, and the title has the heaviest streaming volume in the campaign so far. Unlike the recent GD parks, this title **renders** — the attract demo is visually confirmed. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `illvelo` (no clones — `parent: null` in controls.json; single GAME line, MAME src/mame/sega/naomi.cpp @59e7c0b line 11117) |
| Maker / year | Milestone, 2008 (JP arcade June 11, 2008 per [Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo))). "Illvelo" is a contraction of "Illmatic Envelope" ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=illvelo)) |
| Genre / format | Shmup ★ (vertical, ROT270), **M4 cartridge** 841-0059C — 3× 512 Mb flash (`fpr-24437/24438/24439`, IC11 populated-but-empty) + PIC `317-5131-JPN`, rom_board id 5504, machine `naomim4` (MAME naomi.cpp @59e7c0b cart table ~line 668 + `ROM_START(illvelo)`). 88.4 MB zip. Note: arcadeitalia's "840-0059C" and "BAD DUMP" claims are both contradicted by the MAME source (841- third-party prefix; no `BAD_DUMP` macro anywhere in `ROM_START(illvelo)`) — primary source wins |
| Official DC port | No — widely expected as the next "last Dreamcast game ever" after Radirgy/Karous, but Milestone went Wii instead ([Engadget, Sep 2008](https://www.engadget.com/2008-09-10-illvelo-wii-is-real-velo.html)): standalone *Illvelo Wii* (JP 2008-11-13, [Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo))), then *Milestone Shooting Collection 2* (Wii JP 2010-12-30, [MobyGames](https://www.mobygames.com/game/56616/milestone-shooting-collection-2/)), later *Sakura Flamingo Archives* (X360 2014, Shmups Wiki). `GAME_FORMATS.md` files it under "cancelled-but-unreleased DC ports", but no cancellation evidence was found — [Wikipedia's List of cancelled Dreamcast games](https://en.wikipedia.org/wiki/List_of_cancelled_Dreamcast_games) does not include it; "expected but never announced" is the accurate framing |
| Community ports | None found (searched 2026-08-03) — only generic Naomi-conversion threads on dreamcast-talk ([NAOMI Rom in GDI](https://www.dreamcast-talk.com/forum/viewtopic.php?t=15366), [Naomi and Naomi 2 conversion](https://dreamcast-talk.com/forum/viewtopic.php?t=14103)); the conversion scene targets GD-ROM sets, and an M4 cart needs a decrypted dump |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/illvelo.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. Unlike `kurucham`/`ss2005`, this title renders real frames under the fork (vertical 480×640). The full attract cycle was observed across the 10 battery shots: boot-loading → gameplay demo → story text card → MADOWS "98se" fake-desktop (ranking window / loading dialogs) → title — `shot-540s.png` shows a literal "DEMONSTRATION" overlay on live gameplay.

Screenshots kept (5 of 10):
- `assessments/evidence/illvelo/shot-060s.png` — boot: loading-bar dialog on black, FREE PLAY
- `assessments/evidence/illvelo/shot-121s.png` — attract gameplay: ship firing twin lasers at parachuting enemies inside the ILLMATIC ENVELOPE fake-OS window frame; HUD counters + weapon sidebar (POINT/DESTINY/MEGALO/…/DOLL/SHIELD/LIFE)
- `assessments/evidence/illvelo/shot-308s.png` — title screen: Illvelo character logo, EXTEND SCORE table, ©2008 MILESTONE Inc.
- `assessments/evidence/illvelo/shot-540s.png` — attract gameplay with "DEMONSTRATION" overlay, live score counter
- `assessments/evidence/illvelo/shot-605s.png` — MADOWS 98se fake-desktop with "起動中です…" (starting up) progress dialog

Deleted surplus (5): two ranking-window desktop shots, a black story-text card, a black transition frame, a second desktop loading dialog.
Anomalies: none — this is the first recent title in the campaign with fully working display output.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,291,456 B` nonzero above
the cap at scan. Boot-time full-bank load — **fifth** in the kb §6 tally after `ikaruga`,
`azumanga`, `ss2005`, `takoron`, and the **first cartridge title** in it (breaks the
GD-only pattern).

**Sibling-precedent argument (checkpoint centerpiece):** Milestone's Radirgy (GDL-0032/A,
ROT270, naomi.cpp @59e7c0b lines 11276–77) and Karous (GDL-0040, ROT270, line 11288) —
same maker, near-identical vertical-shmup engine — both shipped official Dreamcast ports:
Radirgy DC in 2006 ([Wikipedia](https://en.wikipedia.org/wiki/Radirgy)) and Karous DC on
2007-03-08 as the last officially licensed DC release, with proper TATE support
([Wikipedia](https://en.wikipedia.org/wiki/Karous)). Those DC builds necessarily fit
their sound inside the DC's 2 MiB AICA RAM. Illvelo's 4× bank therefore measures
Naomi-side luxury (load-the-whole-bank because it's there), not intrinsic
unportability — the strongest sibling-precedent evidence yet that the G3-aram 2× gate
over-parks (kb §6 item 1).

The gate is not the only memory pressure: main-RAM DMA high-water is `27,289,280 B`
(1.63× the DC's 16 MB) and VRAM peak `14,172,160 B` (1.69× the 8 MB cap). VRAM is milder
than the peak implies: nonzero content is only `4,760,762 B` total with `4,749,518 B` of
it above the 8 MB line — the address-extent artifact of an asset store parked high (the
`kurucham` pattern); a port would relocate it.

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at the
gate): streaming 2,775 DMA events, `150,388,736 B` total / `32,053,248 B` unique,
re-read ratio 0.7869, steady-state 15.214 MB/min (`short_window: false`) — the highest
streaming volume in the campaign so far. Guts is **unavailable**: the M4 static scan
failed with `static scan: load entry out of file: rom=0x40000000 len=0x200000` — second
instance of the kb §4.q M4-cart carve failure (first: `zunou`) — so `guts.flags` is
BIOS-only (`[eeprom_bios]`) and `sdk_strings` is empty. Similarity inputs from the
sidecar: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false` —
the developer false is a reference-list artifact (the similarity reference's `makers`
list contains only `Altron / Taito`), despite Milestone's directly relevant DC porting
pedigree; worth a checkpoint note if the similarity axis is ever revised.

What would unblock it: a per-title audio trim (downsample the PCM banks / ADPCM) —
standard porting work with **in-family** released-port precedent (Radirgy/Karous DC),
plus main-RAM/VRAM reduction as above.

## Risks & notes

- **ROT270 vertical screen.** A DC port must handle tate/yoko presentation — solved
  in-family: Karous DC shipped with proper TATE support, Radirgy DC likewise handled the
  vertical playfield on a horizontal display ([Wikipedia Karous](https://en.wikipedia.org/wiki/Karous),
  [Radirgy](https://en.wikipedia.org/wiki/Radirgy)).
- **Heaviest streaming in the campaign**: 150.4 MB total at 15.2 MB/min steady with
  re-read ratio 0.79 — cart re-reads on Naomi. A DC port streams from GD-ROM instead;
  the 32.05 MB unique working set is the number that matters for GD feasibility, and the
  re-read-heavy pattern is the small-working-set loop the kb §6 item 2 checkpoint already
  flags as cache-friendly rather than disqualifying.
- **Guts axis missing (M4 scan failure, kb §4.q second instance).** Fine for a parked
  title; if a softer ARAM rule ever un-parks M4 carts, cart2dat needs M4 support first or
  the guts/similarity axes will skew the score (no sdk_strings → `sdk_overlap: none`).
- **Controls are the easy axis**: `controls.device_class = stick` — 8-way stick + 3
  buttons (A shot, B DOLL module control, C MEGALOPHAZ bomb; auto-shield when not
  firing), 1:1 on a stock DC pad. Sources: MAME src/mame/sega/naomi.cpp @59e7c0b
  INPUT_PORTS `naomi` (GAME line ROT270);
  [Shmups Wiki](https://www.shmups.wiki/library/Illmatic_Envelope_(Illvelo));
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=illvelo)
  (8-way joystick, JVS standard 6-button declaration, 2P);
  [shmups forum ST thread](https://shmups.system11.org/viewtopic.php?f=5&t=67562).
  The Wii port shipped on standard pads, confirming pad-friendliness.
- MAME emulation status: blanket naomi.cpp `GAME_FLAGS`
  (`MACHINE_IMPERFECT_GRAPHICS|MACHINE_IMPERFECT_SOUND|MACHINE_NOT_WORKING`, line 10914),
  mirrored by arcadeitalia as "preliminary" — yet the title runs and renders fully under
  our fork.
- Main watermark `32,505,920 B` (informational, stale-data-prone) — byte-identical to the
  `kurucham`/`ss2005` main watermark, consistent with the content-scan ceiling artifact
  already flagged in the `ss2005` doc; treat with suspicion.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset.
