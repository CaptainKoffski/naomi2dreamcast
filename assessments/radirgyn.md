# Radirgy Noa (Japan) (841-0062C) (`radirgyn`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 79.0 (A), was 52.1 (B)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 10,831,427 B (content-u 0.646) replaces peak 24,850,767 B (u 1.481).
> Memory axis 87.0, binding region now **aram** (was memory 30.8). Verdict section below is the capture-time (v≤8) record.

> **Battery v8 vram-fb-masking re-run (2026-08-08): 52.1 (B)** — spec
> `2026-08-07-vram-fb-masking-design.md`. Sidecar: flycast `f014a410c`, battery 8. No
> park, boot ok, PIO handoff at 20.0 s. Streaming reproduces essentially identically
> (304 DMA events, re-read 0.6887, steady 4.164 MB/min — bit-identical to v4). Main peak
> matches this doc's old "informational" watermark exactly (24,850,767 B). ARAM
> `content_total` 2,041,920 B (u=0.974) → sub 87.0, first content-volume measurement
> (v7-class keying). **VRAM flips from address high-water (11,195,744 B, u=1.33, sub
> 36.6) to FB-masked content: `content_total` 5,123,604 B + `2×fb_bytes` 1,228,800 B
> (`fb_bytes` 614,400 B, exactly 640×480×2) = fit 6,352,404 B, u=0.757 → sub 100.0** — a
> rise, as required. Main RAM's write-truth sub (30.8, u=1.481) is now the binding
> region — lower than the design doc's speculative "main 55.2" bound, the same
> measurement-decides pattern seen on gunsur2/illvelo/mamonoro this wave (write-truth
> found real above-cap content the old DMA figure missed). Memory axis **36.6 → 30.8**,
> final **55.9 → 52.1**, tier unchanged **B**. Sanity clean: `content_total +
> fb_masked_nz` matches `nz_total` exactly in the raw log (5,123,604 + 471,657 =
> 5,595,261). Coverage re-annotated `demo` (unchanged).

> **Battery v4 re-assessment (2026-08-04): **55.9 (B)**.**
> v2 parked it G3-aram via the DMPD fill artifact. v4: scored, demo coverage.
> Below the v8 section is the battery v4-era assessment, itself superseding the v2-era
> assessment below that; each section's *measured* figures (boot evidence, memory,
> streaming, score) are **superseded** by the section above it — the identity,
> controls-research and similarity sections remain valid throughout. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v8 verdict & measurements

| | |
|---|---|
| **Final** | **52.1 (B)** |
| Coverage | demo |
| Assessed | 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/radirgyn.zip` |

| Region | Peak / fit | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 24,850,767 | 16,777,216 | 1.481 | matches the doc's old "informational" watermark exactly (real writes, not stale data); sub 30.8, now binding |
| VRAM (FB-masked content + 2×FB) | 6,352,404 (content_total 5,123,604 + 2×fb_bytes 1,228,800) | 8,388,608 | 0.757 | battery v8 re-keying — sub 100.0, was 36.6 under address high-water (11,195,744, u=1.33) |
| ARAM (content, volume-keyed) | 2,041,920 | 2,097,152 | 0.974 | sub 87.0, first content-volume measurement (v7-class keying); was 1.07× / content above cap 122,039 under the old address peak |

Streaming: 304 DMA events · total 45.3 MB · unique 14.1 MB · re-read 0.6887 · steady 4.164 MB/min (bit-identical to v4)
Axes: memory 30.8 · streaming 75.5 · guts 85.0 · controls 100.0 · similarity 40.0 → **final 52.1 (B)**
Screenshots: `evidence/radirgyn/shot-060s.png` · `shot-365s.png` · `shot-609s.png` (same 3-shot curation as v4 — story-panel "INSERT COIN(S)" ×2, attract gameplay)

---

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **55.9 (B)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/radirgyn.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 19,552,576 | 16,777,216 | 1.17 |  |
| VRAM (write-truth diff) | 11,195,744 | 8,388,608 | 1.33 | nz_total 5,585,861 |
| ARAM (content, fill-excluded) | 2,252,880 | 2,097,152 | 1.07 | content above cap 122,039 |

Streaming: 304 DMA events · total 43.2 MB · unique 13.5 MB · re-read 0.6887 · steady 4.164 MB/min
Axes: memory 36.6 · streaming 75.5 · guts 85.0 · controls 100.0 · similarity 40.0 → **final 55.9 (B)**
Screenshots: `evidence/radirgyn/shot-060s.png` · `evidence/radirgyn/shot-365s.png` · `evidence/radirgyn/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the **sixth** boot-time full-bank G3-aram park in the campaign, the second on a cartridge. Everything else nearly fits: main RAM 1.17× and VRAM 1.33× are the **mildest overruns measured in the campaign so far**, streaming is light, the attract demo renders fully, controls are a stock DC pad, and ROT0 "vertizontal" means zero TATE work. The sibling precedent is the most direct of the series: the original Radirgy — same developer, same franchise — shipped an official DC port in 2006, so this exact series' sound design demonstrably compresses into 2 MiB. If the kb §6 checkpoint softens the ARAM rule, `radirgyn` is the first unpark candidate. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `radirgyn` (no clones — `parent: null` in controls.json; single GAME line, MAME src/mame/sega/naomi.cpp @59e7c0b line 11121). The 2005 GD-ROM sets `radirgy`/`radirgyo` (GDL-0032A/0032, `naomigd`, ROT270) are a **separate family** |
| Maker / year | Milestone / Lucky, 2009 (JP arcade June 2009 per [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=radirgyn)); Lucky Co. Ltd published, MileStone Inc. developed |
| Genre / format | Shmup ★ — **ROT0 "vertizontal"**: vertical-scrolling playfield on a horizontal 640×480 monitor, side bands used for P1/P2 status panels ([shmups forum "Vertically Scrolling Yoko Games"](https://shmups.system11.org/viewtopic.php?t=53533)); first Milestone game with 2-player simultaneous play (arcadeitalia). **M4 cartridge** 841-0062C — 2× 512 Mb S29GL512N flash with data (ic8/ic9; "IC10 and IC11 Populated, Empty") + PIC `317-5138-JPN`, XC3S50 "VER.2", XCF01S "8A", rom_board id 5504, machine `naomim4` (MAME naomi.cpp @59e7c0b cart table ~line 688 + `ROM_START(radirgyn)` line 6793). 107.4 MB zip. **841-0062 is the highest 841-xxxx cart number in MAME's Naomi list — the final third-party Naomi cartridge game** (June 2009, ~11 years after the 1998 launch; only Sega's Star Horse Progress Returns units 840-0183…0187 are contemporaneous). Note: arcadeitalia's "BAD DUMP" remark is unsupported by the MAME source — no `BAD_DUMP` macro anywhere in `ROM_START(radirgyn)` (clean CRCs on ic8/ic9 and the PIC); primary source wins |
| Official DC port | No — Noa's ports are Japan-only and post-DC: *Radirgy Noa Wii* (2010-02-25), *Milestone Shooting Collection 2* (Wii, 2010, with Chaos Field/Karous/Illvelo/Radirgy — [shmups.wiki](https://shmups.wiki/library/MileStone_Shooting_Collection_2), [MobyGames](https://www.mobygames.com/game/56616/milestone-shooting-collection-2/)), *Radirgy Noa Massive* (X360, 2010-10-28, adds Classic/Death/Massive modes — [shmups.wiki](https://shmups.wiki/library/Radirgy_Noa)), Windows (2011-02-25, [HandWiki](https://handwiki.org/wiki/Software:Radirgy_Noa)). Only the original Radirgy got a DC release (2006-02-16, [Wikipedia](https://en.wikipedia.org/wiki/Radirgy)) — the in-family precedent the Gate section leans on |
| Community ports | None found (searched 2026-08-03) — the [sega-naomi.eu mega list](https://www.sega-naomi.eu/forum/viewtopic.php?t=2185) lists Noa as Wii/X360 only; the conversion scene targets GD-ROM sets and an M4 cart needs a decrypted dump ([DC Junkyard Naomi article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/radirgyn.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. All 10 battery
shots have unique content; the full attract cycle was observed: story cards (MAYUMI
character art with dialogue boxes) → live gameplay demo across two stages (forest,
city) with the vertizontal side-panel layout and the ABSnet visibly deployed →
ranking table → title screen → loop wrap (shot-602s crossfades the shot-060s story
card over the school building).

Screenshots kept (5 of 10):
- `assessments/evidence/radirgyn/shot-060s.png` — attract story card: character with dialogue box, INSERT COIN(S)
- `assessments/evidence/radirgyn/shot-121s.png` — attract gameplay, forest stage: mecha with the yellow ABSnet ring deployed; left panel portrait/battery/ABS gauge (網 button), right panel ラジルギノア logo — the vertizontal layout
- `assessments/evidence/radirgyn/shot-246s.png` — ランキング hi-score table (SHT/LBS/BBL)
- `assessments/evidence/radirgyn/shot-308s.png` — title screen: Radirgy Noa logo, RANK: NORMAL / EXTEND table, MILESTONE INC. logo
- `assessments/evidence/radirgyn/shot-424s.png` — attract gameplay, city stage: 圏外 indicator and "abs OK!" charged gauge

Deleted surplus (5): two more story cards, a second forest-stage gameplay shot, a
black transition frame, the loop-wrap crossfade.
Anomalies: none — renders fully under the fork (second campaign title after `illvelo`).

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,269,011 B` nonzero
above the cap at scan. Boot-time full-bank load — **sixth** in the kb §6 tally
(`ikaruga`, `azumanga`, `ss2005`, `takoron`, `illvelo`), second cartridge title.

**Strongest unpark case of the series.** The gate is the *only* blocking axis:

- Main-RAM DMA high-water `19,552,576 B` = **1.17×** the DC's 16 MB — the lightest
  main-RAM figure in the campaign (prior GD titles cluster at 1.63–1.82×).
- VRAM peak `11,195,744 B` = 1.33× the 8 MB cap — also the campaign's mildest, and an
  address-extent figure: nonzero content is `5,557,130 B` total with `2,335,723 B`
  parked above the 8 MB line (the `kurucham` relocation pattern).
- Streaming is light: 290 DMA events, `40,585,216 B` total / `14,110,720 B` unique,
  re-read ratio 0.6523, steady-state 3.724 MB/min (`short_window: false`).
- Controls map 1:1 to a stock pad and the ROT0 vertizontal screen needs **no TATE
  work at all** — the arcade picture is already a native horizontal 640×480 (§2).

The sibling precedent is even more direct than `illvelo`'s Radirgy/Karous argument:
here it is the **same franchise** — the original Radirgy shipped an official DC port
in 2006 ([Wikipedia](https://en.wikipedia.org/wiki/Radirgy)), so this exact series'
sound design demonstrably compresses into the DC's 2 MiB AICA RAM. The 4× bank is
Naomi-side luxury, not intrinsic unportability. **If the kb §6 checkpoint softens the
ARAM rule, `radirgyn` is the first unpark candidate.**

Guts was **unavailable at v2 time**: the M4 static scan failed with
`static scan: load entry out of file: rom=0x40000000 len=0x200000` — third instance
of the kb §4.q M4-cart carve failure (after `zunou`, `illvelo`), so `guts.flags` was
BIOS-only (`[eeprom_bios]`) and `sdk_strings` was empty. Similarity inputs from the
sidecar at that time: `developer_match: false`, `sdk_overlap: "none"`,
`cart_loader_match: false` — the developer false is the same reference-list artifact
flagged in the `illvelo` doc, despite Milestone's in-franchise DC porting pedigree.
**Re-scanned 2026-08-06** after the `carve_boot.py` bit-30 fix: the M4 load-entry rom
offset carries bit 30 as an encrypted-read flag, not a file offset (MAME
`src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast `m4cartridge.cpp:115,132`
@ebae3b513); masking it (`& 0x1ffffffe`) lets the scan carve and Ghidra-analyze the
2 MiB boot blob → `guts.dat_available = true`, guts axis **85.0**,
`similarity.sdk_overlap = "partial"`, similarity axis **40.0** (`developer_match` and
`cart_loader_match` remain false — v4 axes above; capture itself was not re-run).

What would unblock it: a per-title audio trim (downsample the PCM banks / ADPCM) —
standard porting work with **same-franchise** released-port precedent — plus modest
main-RAM (1.17×) and VRAM (1.33×, mostly relocatable) reduction.

## Risks & notes

- **Controls are the easy axis**: `controls.device_class = stick` — 8-way stick +
  3 buttons (A shot with color-cycled weapons, B sword/slash — chargeable, fills the
  ABSnet gauge, C ABSnet bullet-absorbing net; contact damage new in Noa), 2P
  simultaneous. 1:1 on a stock DC pad. Sources: MAME src/mame/sega/naomi.cpp @59e7c0b
  INPUT_PORTS `naomi` (GAME line ROT0);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=radirgyn)
  (8-way joystick, "Shoot, Sword, Special", 2P concurrent, horizontal);
  [Radirgy DB fan wiki](https://radirgy.neocities.org/tips/noa/);
  [HandWiki](https://handwiki.org/wiki/Software:Radirgy_Noa). The Wii/X360/PC ports
  shipped on standard pads, confirming pad-friendliness.
- **M4 guts gap: closed 2026-08-06.** `carve_boot.py` now masks bit 30 (the M4
  encrypted-read flag) on cart load-entry offsets, so the static scan carves and
  Ghidra-analyzes the boot blob. Re-scored via `tools/assess/rescore_static.py`
  (guts 85.0, similarity 40.0, final 55.9 B above); capture was not re-run.
- MAME emulation status: blanket naomi.cpp `GAME_FLAGS`
  (`MACHINE_IMPERFECT_GRAPHICS|MACHINE_IMPERFECT_SOUND|MACHINE_NOT_WORKING`, line
  10914), mirrored by arcadeitalia as "preliminary" — yet the title runs and renders
  fully under our fork.
- Main watermark `24,850,767 B` (informational, stale-data-prone) is 1.27× the DMA
  high-water — and notably **not** the 32,505,920 B ceiling value the GD titles
  cluster at, consistent with a real (and small) cart-title working set.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset.
