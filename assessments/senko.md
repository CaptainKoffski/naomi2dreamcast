# Senko no Ronde (Japan, Rev A) (GDL-0030A) (`senko`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **89.9 (S)** |
| Bottom line | The fresh v9 capture replaces every v4 fallback with a measured content volume, and — for the first time — all three memory regions clear the 0.80u full-score plateau: main write-truth content (0.4511×), VRAM FB-masked content + double-framebuffer (0.6554×), ARAM compacted content (0.6397×), pushing the memory axis from 10.2 to 100.0 and the final from 36.1 (C) to 89.9 (S). The same capture also reached full attract/demo coverage for the first time — a live "DEMONSTRATION" fight is evidenced directly (`shot-426s.png`), clearing the v4-era ⚠ lower-bound flag. G.Rev's own Under Defeat DC port remains the in-house precedent that the audio side compresses onto DC hardware; sibling set `senkosp` moved the same way under the same v9 re-key. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/senko.zip`
(single clean zip leg)
Attract/demo reached: **demo** — the v9 capture observed the full attract cycle: story
text card (`shot-060s.png`) → title logo 旋光の輪舞 SENKO NO RONDE (`shot-121s.png`) →
ADX splash (`shot-182s.png`) → credits card over flying mechs (`shot-243s.png`) →
HISCORE RANKING (`shot-304s.png`) → story text card continuation (`shot-365s.png`) →
live "DEMONSTRATION" attract fight — Cuilan vs Sakurako, health bars, round timer, Rev A
"NEW VER." tag on screen (`shot-426s.png`) → G.Revolution developer logo (`shot-487s.png`)
→ credits card (`shot-548s.png`) → HISCORE RANKING loop restart (`shot-609s.png`).
Sidecar `capture.coverage = "demo"` — clears the v4-era ⚠ lower-bound flag (§10 History);
`shot-426s.png` is the gameplay-frame proof the RUNBOOK representativeness check requires.
Note: every sampled shot also carries a green "FREE PLAY" banner, yet the full attract
loop including a live demo fight still played — unlike `ikaruga` (§9 there), where FREE
PLAY structurally suppresses the attract loop at any run length, senko's FREE PLAY setting
does not suppress it; the v4 run's title-only result was a sampling gap, not a suppressed
demo mode.
Screenshots: `evidence/senko/shot-060s.png` · `evidence/senko/shot-121s.png` ·
`evidence/senko/shot-426s.png` · `evidence/senko/shot-548s.png` ·
`evidence/senko/shot-609s.png` (curated from 10)
Anomalies: none — full rendering under the fork.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 7,567,610 | 16,777,216 | 0.4511 | 100.0 | address peak 33,554,341 (u 2.00, informational) · 5,988,845 B nonzero above the 16 MB line · `dma_high_water` 33,453,344 is the pre-v6 fallback (u 1.994, sub-score 10.2 under v4) — now superseded, content <= peak+1 confirms it was provably conservative |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total` + 2×`fb_bytes`) | 5,497,976 | 8,388,608 | 0.6554 | 100.0 | content_total 4,269,176 · fb_bytes 614,400 (double-buffered → 1,228,800) — replaces the v4 address-peak fallback (peak 12,931,936, u 1.542, sub-score 28.3); raw write-truth `nz_total` still 5,121,514 (4,072,382 above cap, informational — the kurucham address-extent pattern) |
| ARAM (compacted content volume, fill-excluded, `content_total`) | 1,341,558 | 2,097,152 | 0.6397 | 100.0 | address peak 2,097,136 (u 1.000, the v4 near-cap keying — 16 B under the cap) · `nz_above_cap` 0 — content volume shows comfortable headroom, not a near-miss |

Watermarks (informational, content-scan — stale-data prone): main 33,554,341 ·
vram 12,931,936 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 82.6)

DMA events 348 · total 61,810,688 B (58.9 MiB) · unique 34,125,824 B (32.5 MiB) ·
re-read ratio 0.4479 · steady-state 5.556 MB/min (`short_window: false`) ·
PIO 1,505,100 B

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
dash with a direction, barrier neutral); B.O.S.S. mode = A+M+S together
(`controls.device_class = stick`). The Barrage (C) macro and OverDrive (OD) button are
Rev.X/SP-era additions — the 5-button cabinet is the later *SP* release (`senkosp`), not
this family. 2P.
Proposed DC mapping: 1:1 on a stock DC pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (GAME line ROT0);
[SuperCombo Rev.X](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X);
[SuperCombo Controls](https://wiki.supercombo.gg/w/Senko_No_Ronde_Rev._X/Controls);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=senko);
[Highway Games (SP cabinet)](https://www.highwaygames.com/arcade-machines/senko-ronde-9157/).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 82.6^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **89.9 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes — the
developer false is the known reference-list artifact (the reference's `makers` list
contains only Altron / Taito); G.Rev was founded by ex-Taito staff and has direct
first-party Naomi→DC porting pedigree (same checkpoint note as `senkosp`/`illvelo`).

## 9. Risks & notes

- **All three memory regions now clear the 0.80u full-score plateau** — the fresh v9
  capture replaces every v4 fallback with a measured content volume: main write-truth
  `nz_total` 7,567,610 B (u 0.4511) replaces the `dma_high_water` fallback (33,453,344 B,
  u 1.994, sub-score 10.2 under v4); VRAM's FB-masked fit (`content_total` 4,269,176 +
  2×`fb_bytes` 614,400 = 5,497,976 B, u 0.6554) replaces the address-peak fallback
  (12,931,936 B, u 1.542, sub-score 28.3); ARAM's `content_total` 1,341,558 B (u 0.6397)
  replaces the address-peak keying that had it sitting 16 B under the cap. Memory axis
  10.2 → 100.0 is entirely fallback-replacement, not a capture change — see the
  reproduction check below.
- **Reproduction check (v4 → v9, a fresh capture, not a rescore)**: every raw counter
  genuinely shared between the two sidecars reproduced either byte-identically or within
  small, non-gating noise. Byte-identical: `dma_high_water` (33,453,344), VRAM `peak`
  (12,931,936) and `nz_above_cap` (4,072,382), ARAM `peak` (2,097,136) and `nz_above_cap`
  (0), the boot/handoff `seen`/`t`/`aram_zeroed`/`vram_zeroed` fields, all `guts` fields
  (code_bytes, functions, mmio_refs, `carve_meta`, `flags`, all `sdk_strings`), and
  streaming `dma_events` (348), `total_bytes` (61,810,688), `unique_bytes` (34,125,824),
  `reread_ratio` (0.4479), plus `controls`/`similarity`. Moved within noise: VRAM
  `nz_total` +11,366 B (+0.22%, the above-cap portion unchanged — extra nonzero content
  landed below the 8 MB line), `steady_mb_per_min` +0.001 MB/min (+0.02%) — both
  consistent with attract-loop phase drift between two independent 600 s captures five
  days apart, not instrumentation regression; none of it moves any region across a
  scoring breakpoint (all three sit at u ≤ 0.6554, comfortably under the 0.80 plateau
  edge).
- **Coverage upgraded title → demo**: the v4 capture's ten 60 s-interval shots landed
  entirely within the story/title/hiscore rotation and never sampled a live fight; this
  v9 capture's same 10-shot cadence caught the "DEMONSTRATION" overlay fight (Cuilan vs
  Sakurako, `shot-426s.png`) — the same live-attract-fight pattern the original v2
  capture had observed (§10 History), now reproduced and evidenced directly in the v9
  curated set. senko's FREE PLAY banner does not suppress the attract loop the way it
  does for `ikaruga` — a sampling difference between runs, not a structural suppression.
- **Audio has in-house precedent**: G.Rev developed and published the DC port of its
  own Naomi shmup *Under Defeat* (Naomi 2005 → DC 2006-03-23,
  [Wikipedia](https://en.wikipedia.org/wiki/Under_Defeat)) and self-published *Border
  Down* on DC (2003) — the same team provably fit its Naomi-era sound work into the
  DC's 2 MiB AICA RAM. ARAM here now scores 100.0 under content-volume keying (u 0.6397,
  comfortable headroom, not a near-miss).
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
| v9 | 2026-08-09 | 89.9 (S) | ranking-groom chunk 5: fresh v9 capture (was v4) — all three v4 fallbacks replaced by measured content volume (main `nz_total` u 0.4511, VRAM content+2×fb u 0.6554, ARAM `content_total` u 0.6397), memory axis 10.2→100.0, final 36.1 (C)→89.9 (S); coverage upgraded title→demo, a live "DEMONSTRATION" fight now evidenced (`shot-426s.png`) |
