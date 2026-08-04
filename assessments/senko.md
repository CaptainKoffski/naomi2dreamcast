# Senko no Ronde (Japan, Rev A) (GDL-0030A) (`senko`) — portability assessment

> **Battery v4 re-assessment (2026-08-04): **36.1 (C)**.**
> v2 parked it G3-aram via the DMPD fill artifact. v4: scored. Coverage title-⚠: attract rotation cycles ADX logo → story text → hiscore (shots 182/365/487/609) but no gameplay frame was sampled.
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **36.1 (C)** |
| Coverage | title |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/senko.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 33,453,344 | 16,777,216 | 1.99 |  |
| VRAM (write-truth diff) | 12,931,936 | 8,388,608 | 1.54 | nz_total 5,110,148 |
| ARAM (content, fill-excluded) | 2,097,136 | 2,097,152 | 1.00 | content above cap 0 |

Streaming: 348 DMA events · total 58.9 MB · unique 32.5 MB · re-read 0.4479 · steady 5.555 MB/min
Axes: memory 10.2 · streaming 82.6 · guts 85.0 · controls 100.0 · similarity 70.0 → **final 36.1 (C)**
Screenshots: `evidence/senko/shot-060s.png` · `evidence/senko/shot-182s.png` · `evidence/senko/shot-365s.png` · `evidence/senko/shot-487s.png` · `evidence/senko/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the **seventh** boot-time full-bank G3-aram park in the campaign. The sibling precedent here is the most direct yet: G.Rev itself shipped its own Naomi title *Under Defeat* on Dreamcast (developed **and** published by G.Rev, 2006), so the studio demonstrably compressed its Naomi sound designs into 2 MiB AICA. But unlike `radirgyn`, senko is **not** a light unpark candidate: main-RAM DMA high-water is 1.99× the DC's 16 MB — the campaign's heaviest main figure, sitting just under its own 2× gate — and VRAM is 1.54× over. This 241 MB versus title is genuinely asset-heavy. The title renders fully under the fork — attract demo confirmed, with the Rev A "NEW VER." tag visible on screen. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `senko` (Rev A, representative) covers `senkoo` (original GDL-0030). Same PIC `317-5107-jpn` for both; they differ in GD image (`gdl-0030a` vs `gdl-0030`) and default MIE EEPROM (MAME src/mame/sega/naomi.cpp @59e7c0b, ROM_START blocks lines 8737–8767; GAME lines 11272–11273, both ROT0). Rev A displays "Senko no Ronde New Ver." on screen — visually confirmed in `shot-308s.png`/`shot-485s.png`; the original "Old ver." was "quickly updated" and is poorly documented, no public changelog ([SuperCombo wiki](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X), [archive.org](https://archive.org/details/arcade_senko)) |
| Maker / year | G.Rev, 2005 (arcade debut 2005-04-26, [Wikipedia](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)). Founded by ex-Taito staff; music by Yasuhisa Watanabe (ex-Taito), in-binary credits confirm ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senko), `guts.sdk_strings`) |
| Genre / format | Shmup ★ per queue — actually a 1v1 arena "versus shooting"/fighting hybrid (Virtual On-adjacent, Psychic Force lineage per SuperCombo). **GD-ROM** GDL-0030A, 241 MB, machine `naomigd`, horizontal ROT0 |
| Official DC port | No — the official port is Xbox 360: *Senko no Ronde Rev.X* (JP 2006-07-27, G.rev), released overseas as *WarTech: Senko no Ronde* (NA 2007-05-29 / EU 2007-06-08, Ubisoft) ([Wikipedia](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)). Arcade debut was 2005, years after DC production ended; no DC release planned or cancelled |
| Community ports | None found (searched 2026-08-03) — only the generic Naomi-conversion threads on dreamcast-talk ([NAOMI Rom in GDI](https://www.dreamcast-talk.com/forum/viewtopic.php?t=15366), [Naomi and Naomi 2 conversion](https://dreamcast-talk.com/forum/viewtopic.php?t=14103)), which conclude a Naomi image can't run as-is (DIMM loads the whole image vs DC disc streaming) |
| Representative choice | Rev A is the revision the entire later lineage (X360 Rev.X, arcade SP) descends from; `senkoo` is the short-lived first pressing |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/senko.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. All 10 battery shots
are unique; the full attract cycle was observed: story text cards → 3D Rounder model
showcase → HISCORE/CHARACTER RANKING over a 3D cityscape → character profiles → two live
attract fights with a "DEMONSTRATION" overlay. Both gameplay shots show "NEW VER."
bottom-left — on-screen proof this is the Rev A build.

Screenshots kept (5 of 10):
- `assessments/evidence/senko/shot-060s.png` — early attract: story intro text card, FREE PLAY
- `assessments/evidence/senko/shot-121s.png` — 3D Rounder (mech) model showcase
- `assessments/evidence/senko/shot-183s.png` — HISCORE RANKING over 3D cityscape
- `assessments/evidence/senko/shot-308s.png` — attract fight: HUD health bars + 99 timer, "DEMONSTRATION" overlay, "NEW VER." tag
- `assessments/evidence/senko/shot-485s.png` — second attract fight (Cuilan vs Sakurako): dense bullet patterns, RELOAD indicators, "NEW VER." tag

Deleted surplus (5): second/third story text cards, CHARACTER RANKING table, character
profile card, character art frame.
Anomalies: none — full rendering under the fork.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,291,456 B` nonzero above
the cap at scan. Boot-time full-bank load — **seventh** in the kb §6 tally after
`ikaruga`, `azumanga`, `ss2005`, `takoron`, `illvelo`, `radirgyn`.

**Sibling precedent — the studio's own:** G.Rev developed and published the Dreamcast
port of its own Naomi shmup *Under Defeat* (Naomi 2005 → DC 2006-03-23,
[Wikipedia](https://en.wikipedia.org/wiki/Under_Defeat)) and self-published *Border Down*
on DC (2003). The same team provably fit its Naomi-era sound work into the DC's 2 MiB
AICA RAM — the 8 MiB bank measures Naomi-side luxury, not intrinsic unportability.

**But senko is not a light unpark candidate** (contrast `radirgyn`, main 1.17×/VRAM
1.33×): main-RAM DMA high-water is `33,453,344 B` — **1.99× the DC's 16 MB, the
campaign's heaviest main figure, just under its own 2× gate** — and VRAM peak
`12,931,936 B` (1.54×). VRAM is milder than the peak implies: nonzero content totals
`5,070,220 B` with `4,021,088 B` above the 8 MB line (the address-extent pattern seen on
`kurucham`), so relocation helps there — but the main-RAM load looks real: a 241 MB
versus title with 8 playable characters × 2 variants, stage sets and per-character voice
work is genuinely asset-heavy. Even with a softer ARAM rule this stays a hard port.

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at the
gate): streaming 337 DMA events, `56,293,376 B` total / `29,962,240 B` unique, re-read
ratio 0.4677, steady-state 5.559 MB/min (`short_window: false`). Guts is **available**
(GD chd2dat path works, unlike the M4 carts): code `1,503,756 B`, 4,007 functions, MMIO
refs scif 2 / rtc 3 / g2ext 398, flags `[eeprom_bios, serial, rtc]`, carve title
`SENKO NO RONDE`. `guts.sdk_strings` shows the familiar DC-adjacent stack: "Kunoichi2
Library for NAOMI Version 2.07", "syStartCwKn Ver 2.08", Ninja2 2.01.011, "sd2 for DC
Ver 2.50.17", "SEGAKATANA" RMC, NEC KAMUI2, CRI ADX. Similarity inputs:
`developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true` — the
developer false is the known reference-list artifact (the reference's `makers` list
contains only `Altron / Taito`); G.Rev was founded by ex-Taito staff and has direct
first-party Naomi→DC porting pedigree, the same checkpoint note as `illvelo`.

What would unblock it: a per-title audio trim (downsample PCM/ADPCM — in-house precedent
in Under Defeat DC), plus a real main-RAM reduction at 1.99× and VRAM
relocation/trimming — a heavier lift than the other full-bank parks with DC-port
precedent.

## Risks & notes

- **Main RAM 1.99× is the headline risk beyond the gate.** The campaign's heaviest main
  DMA high-water; unlike `radirgyn` (near-fit outside ARAM) this versus title carries a
  genuinely large resident working set. Main watermark `33,554,341 B` is only 1.003× the
  high-water — unusually consistent, so the figure is unlikely to be a content-scan
  artifact.
- **Controls are the easy axis**: `controls.device_class = stick` — 8-way stick +
  **3 buttons**: M (Main Weapon), S (Sub Weapon), A (Action: dash with a direction,
  barrier neutral); B.O.S.S. mode = A+M+S together. The Barrage (C) macro and OverDrive
  (OD) button are Rev.X/SP-era additions — the 5-button cabinet is the later *SP*
  release, not this family. 1:1 on a stock DC pad. Sources: MAME
  src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT0);
  [SuperCombo Rev.X](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X);
  [SuperCombo Controls](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X/Controls);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senko);
  [Highway Games (SP cabinet)](https://www.highwaygames.com/arcade-machines/senko-ronde-9157/).
- **2P/versus play is a proven-good path in Flycast** (contrast `tetkiwam`'s 2P freeze
  #1500): no senko issues in flyinghead/flycast; marked OK in the
  [libretro compatibility list](https://github.com/libretro/flycast/issues/136), an
  active Flycast GGPO/Fightcade competitive scene runs the Naomi version routinely
  ([SuperCombo infobox](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X),
  [savestate contribution](https://github.com/blueminder/flycast-netplay-savestates/issues/27)).
- MAME emulation status: blanket naomi.cpp `GAME_FLAGS`
  (IMPERFECT_GRAPHICS|IMPERFECT_SOUND|NOT_WORKING, line 10914) — and per kb §4.r the
  sidecar's `boot.mame_not_working` carries no per-title signal for Naomi sets; the
  title runs and renders fully under our fork regardless.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (the near-identical watermark suggests little such data
  here).
