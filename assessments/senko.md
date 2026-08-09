# Senko no Ronde (Japan, Rev A) (GDL-0030A) (`senko`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **36.1 (C)** |
| Bottom line | Genuinely asset-heavy 241 MB versus shooter: main RAM binds at u 1.994 (scored on the v4 DMA high-water fallback — this sidecar has no write-truth `nz_total`, re-run queued) and VRAM's address extent is 1.54×; G.Rev's own Under Defeat DC port proves the audio side compresses, but this stays a hard port. |
| Assessed | capture 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `senko` (Rev A, representative) covers `senkoo` (original GDL-0030). Same PIC `317-5107-jpn` for both; they differ in GD image (`gdl-0030a` vs `gdl-0030`) and default MIE EEPROM (MAME src/mame/sega/naomi.cpp @59e7c0b, ROM_START blocks lines 8737–8767; GAME lines 11272–11273, both ROT0). Rev A displays "Senko no Ronde New Ver." on screen — visually confirmed in the battery v2 attract capture; the original "Old ver." was "quickly updated" and is poorly documented, no public changelog ([SuperCombo wiki](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X), [archive.org](https://archive.org/details/arcade_senko)) |
| Maker / year | G.Rev, 2005 (arcade debut 2005-04-26, [Wikipedia](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)). Founded by ex-Taito staff; music by Yasuhisa Watanabe (ex-Taito), in-binary credits confirm ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senko), `guts.sdk_strings`) |
| Genre / format | Shmup ★ per queue — actually a 1v1 arena "versus shooting"/fighting hybrid (Virtual On-adjacent, Psychic Force lineage per SuperCombo). **GD-ROM** GDL-0030A, 241 MB, machine `naomigd`, horizontal ROT0 |
| Official DC port | No — the official port is Xbox 360: *Senko no Ronde Rev.X* (JP 2006-07-27, G.rev), released overseas as *WarTech: Senko no Ronde* (NA 2007-05-29 / EU 2007-06-08, Ubisoft) ([Wikipedia](https://en.wikipedia.org/wiki/WarTech:_Senko_no_Ronde)). Arcade debut was 2005, years after DC production ended; no DC release planned or cancelled |
| Community ports | None found (searched 2026-08-03) — only the generic Naomi-conversion threads on dreamcast-talk ([NAOMI Rom in GDI](https://www.dreamcast-talk.com/forum/viewtopic.php?t=15366), [Naomi and Naomi 2 conversion](https://dreamcast-talk.com/forum/viewtopic.php?t=14103)), which conclude a Naomi image can't run as-is (DIMM loads the whole image vs DC disc streaming) |
| Representative choice | Rev A is the revision the entire later lineage (X360 Rev.X, arcade SP) descends from; `senkoo` is the short-lived first pressing |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/senko.zip` (single clean zip leg)
Attract/demo reached: **title (conservative)** — sidecar `capture.coverage = "title"`:
the v4 attract rotation cycled ADX logo → story text → hiscore across the sampled
shots but no gameplay frame was sampled. (The v2 run had observed the full cycle,
including two live attract fights with a "DEMONSTRATION" overlay and the Rev A
"NEW VER." tag on screen — full rendering under the fork.)
Screenshots: `evidence/senko/shot-060s.png` · `evidence/senko/shot-182s.png` ·
`evidence/senko/shot-365s.png` · `evidence/senko/shot-487s.png` ·
`evidence/senko/shot-609s.png`
Anomalies: none — full rendering under the fork.

## 4. Memory fit (axis: 10.2)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (DMA high-water fallback — this v4 sidecar has no `nz_total`/`peak`) | 33,453,344 | 16,777,216 | 1.994 | 10.2 | **binding region** — provably conservative under v9 keying (`nz_total <= peak+1`); write-truth re-run queued as adopt work · watermark 33,554,341 is only 1.003× the high-water (unusually consistent — unlikely a content-scan artifact) |
| VRAM (write-truth peak — no `content_total`/`fb_bytes` in this v4 sidecar) | 12,931,936 | 8,388,608 | 1.542 | 28.3 | nz_total 5,110,148 with nz_above_cap 4,072,382 — address-extent pattern (kurucham class), relocation helps |
| ARAM (address peak — no `content_total` in this v4 sidecar) | 2,097,136 | 2,097,152 | 1.000 | 85.0 | 16 B under cap · nz_above_cap 0 |

Watermarks (informational, content-scan — stale-data prone): main 33,554,341 ·
vram 12,931,936 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 82.6)

DMA events 348 · total 58.9 MB · unique 32.5 MB · re-read ratio 0.4479 ·
steady-state 5.555 MB/min (`short_window: false`)

## 6. Guts (axis: 85.0)

Code 1,503,756 B · functions 4,007 · MMIO refs: scif 2, rtc 3, g2ext 398 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc` → −15.
GD chd2dat static-scan path (no M4 carve needed); carve base `0x8c020000`, entry
`0x8c021000`, header title "SENKO NO RONDE".
SDK strings show the familiar DC-adjacent stack: "Kunoichi2 Library for NAOMI
Version 2.07", "syStartCwKn Ver 2.08", Ninja2 2.01.011, "sd2 for DC Ver 2.50.17",
"SEGAKATANA" RMC, NEC KAMUI2, CRI ADX.

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + **3 buttons**: M (Main Weapon), S (Sub Weapon), A (Action:
dash with a direction, barrier neutral); B.O.S.S. mode = A+M+S together. The Barrage
(C) macro and OverDrive (OD) button are Rev.X/SP-era additions — the 5-button cabinet
is the later *SP* release, not this family. 2P. `controls.device_class = stick`.
Proposed DC mapping: 1:1 on a stock DC pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT0);
[SuperCombo Rev.X](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X);
[SuperCombo Controls](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X/Controls);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senko);
[Highway Games (SP cabinet)](https://www.highwaygames.com/arcade-machines/senko-ronde-9157/).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 10.2^.40 · 82.6^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **36.1 (C)**
Similarity inputs: developer no, SDK overlap partial, loader match yes — the
developer false is the known reference-list artifact (the reference's `makers` list
contains only Altron / Taito); G.Rev was founded by ex-Taito staff and has direct
first-party Naomi→DC porting pedigree (same checkpoint note as `illvelo`).

## 9. Risks & notes

- **Main RAM 1.99× is the headline risk** — the campaign's heaviest main figure, and
  its watermark agrees to within 0.3%, so it is unlikely to be a measurement artifact:
  a 241 MB versus title with 8 playable characters × 2 variants, stage sets and
  per-character voice work carries a genuinely large resident working set. The score
  is nonetheless a conservative fallback (no write-truth `nz_total` in this v4
  sidecar; `nz_total <= peak+1`, so the queued re-run can only raise it).
- **VRAM is milder than the peak implies**: nonzero content 5,110,148 B with
  4,072,382 B above the 8 MB line (the kurucham address-extent pattern) — relocation
  helps, but real trimming likely remains.
- **Audio has in-house precedent**: G.Rev developed and published the DC port of its
  own Naomi shmup *Under Defeat* (Naomi 2005 → DC 2006-03-23,
  [Wikipedia](https://en.wikipedia.org/wiki/Under_Defeat)) and self-published *Border
  Down* on DC (2003) — the same team provably fit its Naomi-era sound work into the
  DC's 2 MiB AICA RAM. ARAM here sub-scores 85.0 (16 B under cap).
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

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot (4.00×, the DMPD fill artifact) — seventh full-bank park; full attract incl. two live fights rendered under the fork (kb §6, §7) |
| v4 | 2026-08-04 | 36.1 (C) | Unparked by the v4 ARAM content metric; main DMA high-water 1.99× binding (memory 10.2); coverage title — no gameplay frame sampled this run (kb §7) |
| v9 | 2026-08-08 | 36.1 (C) | Scoring-only re-key, result unchanged: this v4 sidecar has no `nz_total`, so main falls back to the DMA high-water — provably conservative; write-truth re-run queued as adopt work (spec `2026-08-08-main-content-rekey-design.md`) |
