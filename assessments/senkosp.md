# Senko no Ronde Special (Export, Japan) (GDL-0038) (`senkosp`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **36.6 (C)** |
| Bottom line | The 2006 arcade back-port of the X360 Rev.X set on the same engine as `senko`: ARAM no longer gates (fill-excluded content-high sits 16 B under the 2 MiB cap) but main RAM binds the memory axis at 10.2 through the conservative CARTDMA high-water fallback (1.99×, byte-identical to senko) — the v4 sidecar predates content-volume capture, so the fallback is provably conservative and a re-capture is queued; G.Rev's own Under Defeat DC port is the in-house precedent, and SP is the version the competitive scene actually plays. |
| Assessed | capture 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

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

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/senkosp.zip` (single clean zip leg)
Attract/demo reached: **demo** — arena gameplay in `shot-609s.png` (sidecar `capture.coverage = "demo"`).
The v2 capture observed the full attract cycle (story text cards → 3D Rounder model
showcase → three "DEMONSTRATION" fights drawing the SP control-panel diagram on screen,
stick + five colored buttons M/S/C/A/OD with per-button tutorial popups → HISCORE
RANKING → SP title screen → G.rev logo) — on-screen proof of the SP 5-button layout and
the OverDrive system, cited by the controls research.
Screenshots: `evidence/senkosp/shot-060s.png` · `evidence/senkosp/shot-304s.png` · `evidence/senkosp/shot-609s.png`
Anomalies: none — full rendering under the fork.

## 4. Memory fit (axis: 10.2)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (CARTDMA high-water fallback — v4 sidecar has no `nz_total`) | 33,453,344 | 16,777,216 | 1.994 | 10.2 | **binding region** — byte-identical to `senko`'s campaign-heaviest figure; provably conservative under v9 keying (`nz_total <= peak+1`), content-volume re-capture queued as adopt work · watermark 33,554,341 is 1.003× the high-water, so the load is real content, not a scan artifact |
| VRAM (write-truth address peak — pre-v8 sidecar, no `content_total`/`fb_bytes`) | 11,897,553 | 8,388,608 | 1.418 | 33.3 | nz_total 4,055,692 with 3,017,926 above the 8 MB line — address-extent pattern, relocation helps |
| ARAM (fill-excluded content-high address, `peak` — pre-v7 sidecar, no `content_total`) | 2,097,136 | 2,097,152 | 1.000 | 85.0 | 16 B under the cap · `nz_above_cap` 0 — no longer the gate it was under v2's full-bank fill |

Watermarks (informational, content-scan — stale-data prone): main 33,554,341 ·
vram 11,897,553 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 87.8)

DMA events 178 · total 27,908,096 B (26.6 MiB) · unique 18,317,312 B (17.5 MiB) ·
re-read ratio 0.3437 · steady-state 2.349 MB/min (`short_window: false`) — roughly half
of `senko`'s attract-mode volume.

## 6. Guts (axis: 85.0)

Code 1,515,512 B · functions 4,012 · MMIO refs: scif 2, rtc 3, g2ext 405 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → −15.
Carve base `0x8c020000`, entry `0x8c021000`, header title `SENKO NO RONDE SP`.
SDK strings match `senko`'s stack down to the build dates — Kunoichi2 Library for NAOMI
2.07, Ninja2 2.01.011, "sd2 for DC" 2.50.17, CRI ADX — corroborating that the asset
weight is engine-resident, not attract-mode noise.

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + **5 buttons** (`controls.device_class = stick`): the original
M/S/A plus dedicated Barrage (C) and OverDrive (OD) buttons, which expose functions the
3-button original reached via chords. 5 inputs fit a stock DC pad's 6 (4 face + 2
triggers) with one to spare, and a chord fallback exists; X360 Rev.X shipped
pad-playable.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line 11285, ROT0);
[Highway Games (SP cabinet: 5 buttons)](https://www.highwaygames.com/arcade-machines/senko-ronde-9157/);
[LaunchBox GDB (added Overdrive + Barrage buttons)](https://gamesdb.launchbox-app.com/games/details/102475-senko-no-ronde-special);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senkosp);
our own v2 capture `shot-246s.png` (on-screen panel diagram M/S/C/A/OD — shot since
superseded by the v4 curation, described in §3).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 10.2^.40 · 87.8^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **36.6 (C)**
Similarity inputs: developer no, SDK overlap partial, loader match yes. The developer
false is the known reference-list artifact (the reference's `makers` list is
Altron/Taito only) — same checkpoint note as `senko`/`illvelo`.

## 9. Risks & notes

- **Main RAM 1.99× is the headline risk** — byte-identical to `senko` (see its Risks
  section); the main watermark (1.003× the high-water) says the figure is real content.
  The v4 sidecar has no write-truth `nz_total`, so v9 content keying cannot apply until
  a re-capture — the current 10.2 is a conservative fallback, not a content verdict.
- **Whatever unparks `senko` unparks SP** — same engine build (SDK stack identical down
  to build dates), and SP is the set the competitive scene plays. G.Rev developed and
  published its own Naomi→DC port (*Under Defeat*, DC 2006), so the heavy Naomi-side
  footprint measures luxury, not intrinsic unportability — but the main-RAM load is real.
- **VRAM is milder than the peak implies**: 4,055,692 B of nonzero content against an
  11.9 MB address extent — the familiar high-parked asset store; a port would relocate.
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

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot read as 4.00× cap — the eighth boot-time full-bank park in the campaign tally; DIMM "DMPD" fill root-cause kb §7 |
| v4 | 2026-08-04 | 36.6 (C) | Un-parked: the v4 content metric excludes the DIMM fill (content-high 16 B under cap); scored with demo coverage — kb §7 |
| v9 | 2026-08-08 | 36.6 (C) | Scoring-only re-key (no re-capture): main keys on content volume, but this v4 sidecar has no `nz_total`, so main falls back to the CARTDMA high-water — provably conservative, re-run queued; spec `2026-08-08-main-content-rekey-design.md` |
