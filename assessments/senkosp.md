# Senko no Ronde Special (Export, Japan) (GDL-0038) (`senkosp`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **91.0 (S)** |
| Bottom line | The 2006 arcade back-port of the X360 Rev.X set on the same engine as `senko`: the fresh v9 capture replaces every v4 fallback with a measured content volume, and all three memory regions now clear the 0.80u full-score plateau — main write-truth content (0.349×), VRAM FB-masked content + double-framebuffer (0.571×), ARAM compacted content (0.643×) — pushing the memory axis from 10.2 to 100.0 and the final from 36.6 (C) to 91.0 (S), the largest single move of the ranking-groom campaign; G.Rev's own Under Defeat DC port is the in-house precedent, and SP is the version the competitive scene actually plays. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/senkosp.zip` (single clean zip leg)
Attract/demo reached: **demo** — the v9 capture observed the full attract cycle again:
story text card (`shot-060s.png`) → SP title logo (`shot-121s.png`) → in-game
"DEMONSTRATION" fight drawing the SP control-panel diagram (stick + five colored buttons
M/S/C/A/OD, sub-weapon tutorial popup — `shot-182s.png`) → credits cards → a second
DEMONSTRATION fight with the OverDrive tutorial popup (`shot-487s.png`) → HISCORE RANKING
(`shot-548s.png`) → loop restart. Sidecar `capture.coverage = "demo"`.
Screenshots: `evidence/senkosp/shot-060s.png` · `evidence/senkosp/shot-121s.png` ·
`evidence/senkosp/shot-182s.png` · `evidence/senkosp/shot-487s.png` ·
`evidence/senkosp/shot-548s.png` (curated from 10)
Anomalies: none — full rendering under the fork.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 5,850,229 | 16,777,216 | 0.3487 | 100.0 | address peak 33,554,341 (u 2.00, informational) · 4,266,292 nonzero above the 16 MB line · `dma_high_water` 33,453,344 is the pre-v6 fallback (u 1.994, sub-score 10.2 under v4) — now superseded, content <= peak+1 confirms it was provably conservative |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total` + 2×`fb_bytes`) | 4,786,768 | 8,388,608 | 0.5706 | 100.0 | content_total 3,557,968 · fb_bytes 614,400 (double-buffered → 1,228,800) — replaces the v4 address-peak fallback (peak 11,897,553, u 1.418, sub-score 33.3); raw write-truth peak still 11,897,553 (nz_total 4,067,058 · 3,017,926 above cap, informational) |
| ARAM (compacted content volume, fill-excluded, `content_total`) | 1,348,105 | 2,097,152 | 0.6428 | 100.0 | address peak 2,097,136 (u 1.000, the v4 gated keying — 16 B under the cap) · `nz_above_cap` 0 — content volume shows comfortable headroom, not a near-miss |

Watermarks (informational, content-scan — stale-data prone): main 33,554,341 ·
vram 11,897,553 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 87.9)

DMA events 177 · total 27,869,184 B (26.6 MiB) · unique 18,317,312 B (17.5 MiB) ·
re-read ratio 0.3427 · steady-state 2.344 MB/min (`short_window: false`) · PIO 1,516,856 B —
roughly half of `senko`'s attract-mode volume.

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
superseded by the v9 curation; the same panel diagram is visible again in
`shot-182s.png`/`shot-487s.png`, described in §3).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 87.9^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **91.0 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes. The developer
false is the known reference-list artifact (the reference's `makers` list is
Altron/Taito only) — same checkpoint note as `senko`/`illvelo`.

## 9. Risks & notes

- **All three memory regions now clear the 0.80u full-score plateau** — the fresh v9
  capture replaces every v4 fallback with a measured content volume: main write-truth
  `nz_total` 5,850,229 B (u 0.349) replaces the `dma_high_water` fallback (33,453,344 B,
  u 1.994, sub-score 10.2 under v4); VRAM's FB-masked fit (`content_total` 3,557,968 +
  2×`fb_bytes` 614,400 = 4,786,768 B, u 0.571) replaces the address-peak fallback
  (11,897,553 B, u 1.418, sub-score 33.3); ARAM's `content_total` 1,348,105 B (u 0.643)
  replaces the address-peak keying that had it sitting 16 B under the cap. Memory axis
  10.2 → 100.0 is entirely fallback-replacement, not a capture change — see the
  reproduction check below.
- **Reproduction check (v4 → v9, a fresh capture, not a rescore)**: every raw counter
  genuinely shared between the two sidecars reproduced either byte-identically or within
  small, non-gating noise. Byte-identical: `dma_high_water` (33,453,344), VRAM `peak`
  (11,897,553) and `nz_above_cap` (3,017,926), ARAM `peak` (2,097,136) and `nz_above_cap`
  (0), the boot/handoff fields, all `guts` fields (code_bytes, functions, mmio_refs,
  `carve_meta`, `flags`, all 500 `sdk_strings`), and `controls`/`similarity`. Moved within
  noise: VRAM `nz_total` +11,366 B (+0.28%, the above-cap portion unchanged — extra
  nonzero content landed below the 8 MB line), DMA events 178→177 (−1), streaming
  `total_bytes` −0.14%, `reread_ratio` −0.29%, `steady_mb_per_min` −0.21% — all consistent
  with attract/demo-loop phase drift between two independent 600 s captures five days
  apart, not instrumentation regression; none of it moves any region across a scoring
  breakpoint (all three sit at u ≤ 0.643, far under the 0.80 plateau edge).
- **Whatever unparks `senko` unparks SP** — same engine build (SDK stack identical down
  to build dates), and SP is the set the competitive scene plays. G.Rev developed and
  published its own Naomi→DC port (*Under Defeat*, DC 2006); the content-volume keying
  now shows the Naomi-side footprint fits the DC's memory map with headroom to spare on
  every region, reinforcing that this is a luxury/placement question, not an intrinsic
  unportability one.
- **VRAM's address extent (11.9 MB, u 1.418 raw) is milder than it looks**: only
  4,067,058 B of it is nonzero content, and the FB-masked keying (§4) already scores it
  at u 0.571 — the raw peak is the familiar high-parked asset store; a port would
  relocate it, but doesn't need to for the score.
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
| v9 | 2026-08-09 | 91.0 (S) | ranking-groom chunk 5: fresh v9 capture (was v4) — all three v4 fallbacks replaced by measured content volume (main `nz_total` u 0.349, VRAM content+2×fb u 0.571, ARAM content_total u 0.643), memory axis 10.2→100.0, final 36.6 (C)→91.0 (S), new rank 1 |
