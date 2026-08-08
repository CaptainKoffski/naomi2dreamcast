# Senko no Ronde Special (Export, Japan) (GDL-0038) (`senkosp`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 36.6 (C), unchanged** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v4 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> adopted to main 2026-08-09): main now keys on write-truth content VOLUME instead of
> the address peak — but this v4 sidecar has no `nz_total`, so main falls back to the CARTDMA high-water 33,453,344 B (u 1.994); provably conservative (`nz_total <= peak+1`), re-run queued as adopt work.
> Memory axis 10.2, binding region now **main** (was memory 10.2). Verdict section below is the capture-time (v≤8) record.

> **Battery v4 re-assessment (2026-08-04): **36.6 (C)**.**
> v2 parked it G3-aram via the DMPD fill artifact. v4: scored, demo coverage (arena gameplay in shot-609s).
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **36.6 (C)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/senkosp.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 33,453,344 | 16,777,216 | 1.99 |  |
| VRAM (write-truth diff) | 11,897,553 | 8,388,608 | 1.42 | nz_total 4,055,692 |
| ARAM (content, fill-excluded) | 2,097,136 | 2,097,152 | 1.00 | content above cap 0 |

Streaming: 178 DMA events · total 26.6 MB · unique 17.5 MB · re-read 0.3437 · steady 2.349 MB/min
Axes: memory 10.2 · streaming 87.8 · guts 85.0 · controls 100.0 · similarity 70.0 → **final 36.6 (C)**
Screenshots: `evidence/senkosp/shot-060s.png` · `evidence/senkosp/shot-304s.png` · `evidence/senkosp/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) — the **eighth** boot-time full-bank G3-aram park in the campaign. This is the 2006 arcade back-port of the X360 Rev.X enhancement set on the same engine as its sibling `senko`, and the numbers agree: main-RAM DMA high-water is **byte-identical** to senko's campaign-heaviest 1.99× figure, so everything in senko's gate analysis (G.Rev's own Under Defeat DC precedent, but a genuinely asset-heavy versus title either way) carries over unchanged. The title renders fully under the fork — attract fights confirmed, with the SP 5-button panel diagram drawn on screen. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `senkosp` — its own family (`parent: null` in controls.json; **not** a MAME clone of `senko`), single set, no clones (MAME src/mame/sega/naomi.cpp @59e7c0b GAME line 11285, ROT0; `ROM_START(senkosp)` lines 8920–8931, GD image `gdl-0038`) |
| Maker / year | G.Rev, **2006** — JP arcade 2006-08-01 ([LaunchBox GDB](https://gamesdb.launchbox-app.com/games/details/102475-senko-no-ronde-special)); MAME GAME line year 2006. A "2007" date sometimes attached to SP is the *Western X360 WarTech* release (NA 2007-05-29 / EU 2007-06-08, [Wikipedia](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)), not the arcade |
| Genre / format | 1v1 arena "versus shooting" hybrid (see `senko` §2). **GD-ROM** GDL-0038, 237.7 MB, machine `naomigd`, horizontal ROT0. Carve title `SENKO NO RONDE SP` (sidecar `guts.carve_meta.title`) |
| Official DC port | No — SP itself was never ported anywhere standalone. It is the **arcade back-port of the X360 Rev.X enhancement set**: location-tested ~2 months before Rev.X shipped and released days after it (arcade 2006-08-01 vs Rev.X JP 2006-07-27), adding the two extra physical buttons (Barrage/C, OverDrive), Novice mode, stage/music select, new HUD and initially-SP-exclusive costumes ([LaunchBox GDB](https://gamesdb.launchbox-app.com/games/details/102475-senko-no-ronde-special), [Wikipedia dates](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)). *Senko no Ronde DUO* (X360 2010) and *Senko no Ronde 2* (PS4/PC 2017) are **sequels**, not SP ports |
| Community ports | None found (searched 2026-08-03) — same generic Naomi-conversion threads as `senko`. The netplay scene runs the Naomi set directly: Flycast Dojo v0.4.13 added `senkosp` for Fightcade lobby inclusion with dipswitch defaults ([release notes](https://www.homearcadesystems.com/flycast-dojo-v0-4-13/), mirrors [github.com/blueminder/flycast-dojo](https://github.com/blueminder/flycast-dojo/releases)); live Fightcade matches exist ([YouTube, Nov 2023](https://www.youtube.com/watch?v=VQQyUW-QBZo)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/senkosp.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`. All 10 battery shots
are unique; the full attract cycle was observed: story text cards → 3D Rounder model
showcase → three attract fights with "DEMONSTRATION" overlays → HISCORE RANKING → SP title
screen → G.rev logo. The fight shots draw the SP control-panel diagram on screen (stick +
five colored buttons labeled M/S/C/A/OD) with per-button tutorial popups — on-screen proof
of the SP-specific 5-button layout and the OverDrive system in the HUD.

Screenshots kept (5 of 10):
- `assessments/evidence/senkosp/shot-121s.png` — attract: 3D Rounder model showcase with CHARACTER DESIGN credits
- `assessments/evidence/senkosp/shot-183s.png` — attract fight (Changpo vs Mika), "DEMONSTRATION" overlay, on-screen panel diagram (stick + M/S/C/A/OD) with Barrier tutorial popup (hold A)
- `assessments/evidence/senkosp/shot-246s.png` — same demo, OverDrive tutorial popup (OD button) + OD/Charge gauges in the HUD — the SP button additions on screen
- `assessments/evidence/senkosp/shot-422s.png` — title screen: 旋光の輪舞 SP logo over teal 3D cityscape
- `assessments/evidence/senkosp/shot-546s.png` — ROUND 1 / DEMONSTRATION card, second matchup (Fabian vs Lili)

Deleted surplus (5): story intro text card, HISCORE RANKING table, story/art card, third
demo fight (Sub-attack popup), G.rev logo card.
Anomalies: none — full rendering under the fork.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 6,291,456 B` nonzero above
the cap at scan. Boot-time full-bank load — **eighth** in the kb §6 tally after `ikaruga`,
`azumanga`, `ss2005`, `takoron`, `illvelo`, `radirgyn`, `senko`.

The sibling analysis is `senko`'s, unchanged — see `assessments/senko.md` Gate section:
G.Rev developed and published its own Naomi→DC port (*Under Defeat*, DC 2006), so the
8 MiB bank measures Naomi-side luxury, not intrinsic unportability — but senko is not a
light unpark candidate because the main-RAM load is real, and SP inherits that verbatim:
main-RAM DMA high-water is `33,453,344 B` (1.99× the DC's 16 MB) — **byte-identical to
senko's figure**. Same engine build (the `guts.sdk_strings` library stack matches senko's
down to the build dates: Kunoichi2 2.07, Ninja2 2.01.011, "sd2 for DC" 2.50.17, CRI ADX),
which both corroborates the measurement's determinism across the SP re-release and
confirms the asset weight is engine-resident, not attract-mode noise. VRAM peak is
`11,897,553 B` (1.42×, milder than senko's 1.54×); nonzero content totals `3,770,790 B`
with `2,721,658 B` above the 8 MB line — the familiar address-extent pattern, relocation
helps there.

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at the
gate): streaming is light — 158 DMA events, `26,849,280 B` total / `18,317,312 B` unique,
re-read ratio 0.3178, steady-state 2.61 MB/min (`short_window: false`) — roughly half of
senko's attract-mode volume. Guts is available: code `1,515,512 B`, 4,012 functions, MMIO
refs scif 2 / rtc 3 / g2ext 406, flags `[eeprom_bios, serial, rtc]`. Similarity inputs:
`developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true` — the
developer false is the known reference-list artifact (the reference's `makers` list is
Altron/Taito only), same checkpoint note as `senko`/`illvelo`.

What would unblock it: same as `senko` — per-title audio trim (in-house Under Defeat DC
precedent) plus a real main-RAM reduction at 1.99× and VRAM relocation/trimming; whatever
unparks senko unparks SP, and SP is the version the competitive scene actually plays.

## Risks & notes

- **Main RAM 1.99× is the headline risk beyond the gate** — byte-identical to `senko`
  (see its Risks section); the main watermark `33,554,341 B` is 1.003× the high-water,
  so the figure is unlikely to be a content-scan artifact.
- **Controls remain the easy axis despite the SP layout**: `controls.device_class =
  stick` — 8-way stick + **5 buttons**: the original M/S/A plus dedicated Barrage (C)
  and OverDrive (OD) buttons, which expose functions the 3-button original reached via
  chords. 5 inputs fit a stock DC pad's 6 (4 face + 2 triggers) with one to spare, and a
  chord fallback exists; X360 Rev.X shipped pad-playable. Sources: MAME
  src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line 11285, ROT0);
  [Highway Games (SP cabinet: 5 buttons)](https://www.highwaygames.com/arcade-machines/senko-ronde-9157/);
  [LaunchBox GDB (added Overdrive + Barrage buttons)](https://gamesdb.launchbox-app.com/games/details/102475-senko-no-ronde-special);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senkosp);
  our own capture `shot-246s.png` (on-screen panel diagram M/S/C/A/OD).
- **Versus play under Flycast is routine for this exact set**: Fightcade ships `senkosp`
  via Flycast Dojo (v0.4.13 release notes, links in §2) — netplay-grade emulation
  compatibility is community-proven, not inferred.
- **Date correction**: SP's arcade release is 2006-08-01, not 2007 — 2007 belongs to the
  Western X360 WarTech release (citations in §2).
- **Only English-region arcade release in the family**: security PIC `317-5123-COM`
  (export/common) vs senko's `317-5122-JPN` (naomi.cpp @59e7c0b lines 8927–8930 vs
  8915–8917), arcadeitalia lists language English — port-relevant: an English-capable
  build already exists on the Naomi side.
- MAME emulation status: blanket naomigd `GAME_FLAGS` — per kb §4.r no per-title signal;
  the title runs and renders fully under our fork regardless.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (the near-identical watermark suggests little such data
  here).
