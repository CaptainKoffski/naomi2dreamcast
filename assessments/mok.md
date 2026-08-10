# The Maze of the Kings (GDS-0022) (`mok`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,461,993 B → utilization **3.558**, well past `region_score()`'s `u > 2.0` gate — clear of the kb §6 item-9 empty band (max scored 1.962 `zerogu2`, min parked 2.997 `takoron`) and slotting into the parked cluster between `mazan` (3.483) and `sstrkfgt` (3.687): `takoron` 2.997, `inunoos` 3.206, `pokasuka` 3.368, `mazan` 3.483, `mok` **3.558**, `sstrkfgt` 3.687. Unlike `mazan`, both other regions clear their own caps here: main `nz_total` u ≈ 0.932, VRAM (content + 2×fb) u ≈ 0.902 — ARAM is the sole blocker. Controls do not compound the block: MAME assigns `mok` the identical `hotd2` input ports as House of the Dead 2, and Flycast's own source hard-codes `gameId == "THE MAZE OF THE KINGS"` into the same lightgun-as-analog JVS group as `hotd2`/Confidential Mission/Death Crimson OX/`lupinsho` — `controls.device_class = dc_peripheral`, on-ladder (§ Gate). If ARAM ever cleared, controls would not gate G2 on their own. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `mok` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11181 is the only row for this title; `parent: null`/self-keyed in `controls.json`) |
| Maker / year | Sega, 2002 (MAME `GAME()` row line 11181; cart-PIC region comment @59e7c0b ~line 9341: `317-0333-COM` / `253-5508-0333`) |
| Genre / format | Light-gun rail shooter (Egyptian/Valley-of-the-Kings theme; confirmed by attract-demo footage — torch-lit temple corridors, an Anubis jackal-headed boss, a rod/staff-shaped weapon viewmodel at screen-bottom, §3), **GD-ROM** GDS-0022, 140.0 MB (`GAME_FORMATS.md`) |
| Official DC port | No — no console release found. A Zophar's Domain music-rip page catalogs the soundtrack under "Sega Dreamcast (DSF)" — same rip-format naming artifact already ruled non-evidence for `lupinsho` (`assessments/lupinsho.md` §2: DSF applies broadly to AICA-driven titles sharing the DC sound driver, arcade Naomi included, not a console release); web search otherwise turns up only arcade/MAME ROM listings and a "Maze of the Kings - Unported Playlist" YouTube video (searched 2026-08-10). |
| Community ports | None found (searched 2026-08-10). |
| Representative choice | Sole MAME set for this title — no clones to consider. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/mok.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). All 10 shots show live gameplay HUD (lives icon, score, and
ammo/rod-charge icon counters) across varied set-pieces: a skydiving/parachute cold-open
(`shot-060s.png`), a torch-lit hieroglyph corridor with an in-flight explosion effect
(`shot-121s.png`), a player-character rooftop cutscene introduction (`shot-182s.png`), corridor
combat against a skeletal enemy (`shot-243s.png`), a collected-loot/treasure reward tableau
(`shot-304s.png`), an Anubis jackal-headed boss encounter in a desert canyon
(`shot-365s.png`), a flock of bird enemies swarming a corridor with the rod-shaped weapon
viewmodel visible at screen-bottom (`shot-426s.png`), a treasure/score-popup staircase scene
(`shot-487s.png`), a mid-air grapple/rod-traversal frame (`shot-548s.png`), and closing corridor
combat against two reptilian enemies (`shot-609s.png`). No static idle screen or EEPROM prompt
anywhere in the capture — genuine attract-demo gameplay throughout.
Screenshots: `evidence/mok/shot-060s.png` · `shot-121s.png` · `shot-365s.png` ·
`shot-426s.png` · `shot-609s.png`
Anomalies: none. `shot-182s.png`, `shot-243s.png`, `shot-304s.png`, `shot-487s.png`, and
`shot-548s.png` were curated out as redundant with the kept intro/corridor-HUD/boss/weapon-
viewmodel/closing-combat shots, same curation class as `mazan`/`lupinsho`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,461,993 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.558** — well past `region_score()`'s `u > 2.0` gate, landing in the middle of
this campaign's parked ARAM distribution: `takoron` 2.997, `inunoos` 3.206, `pokasuka` 3.368,
`mazan` 3.483, `mok` **3.558**, `sstrkfgt` 3.687. This is clear of the kb §6 item-9 empty band
(max scored `zerogu2` 1.962, min parked `takoron` 2.997) — `mok` sits well above it, adding
another data point to the already-parked cluster, not the empty gap. `nz_above_cap` =
5,531,121 B of content above the cap (address-keyed placement figure, informational). Address
peak is 8,323,024 B (u 3.969, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in `score.py`'s
region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 15,639,228 | 16,777,216 | **0.932** | `nz_total` — clears the 1x cap; `nz_above_cap` (address-placement) 12,894,723 B · `dma_high_water` 27,615,776 B (u 1.646) · address peak 32,706,376 B (u 1.949) — both moot, ARAM gates first |
| VRAM (content volume + 2×fb) | 7,568,369 | 8,388,608 | **0.902** | `content_total` 6,339,569 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2 constant) — clears the 1x cap, unlike `mazan`/`sstrkfgt`; raw `nz_total` 7,480,446 (u 0.892) · address peak 14,382,857 (u 1.715) · `nz_above_cap` 5,276,014 B (address-keyed) |
| ARAM (content volume) | 7,461,993 | 2,097,152 | **3.558** | the gate — see above |

Streaming context: 371 DMA events · 49,501,088 B (47.2 MB) total · 26,737,536 B (25.5 MB)
unique · re-read ratio 0.4599 · steady-state 3.606 MB/min (`short_window: false`) · `pio_bytes`
31,190,656 B.
Guts: code 792,320 B (0.756 MiB) · 1,461 functions · MMIO refs rtc 2 / g2ext 130 / scif 1 ·
flags `eeprom_bios`/`serial`/`rtc`. `carve_meta.title` reads `"THE MAZE OF THE KINGS"` — the
exact string Flycast's `maple_jvs.cpp` matches against for the lightgun-as-analog group (§ below),
corroborating the carve against the same identifier the emulator itself keys on.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `dc_peripheral`):** `mok` is a positional light-gun title.
MAME assigns it `INPUT_PORTS 'hotd2'` — the identical port set used by House of the Dead 2 on
Naomi (`GAME()` row, MAME src/mame/sega/naomi.cpp @59e7c0b line 11181: `GAME( 2002, mok,
naomigd, naomigd, hotd2, naomi_state, init_naomigd, ROT0, "Sega", "The Maze of the Kings
(GDS-0022)", GAME_FLAGS )`), the same input-port assignment already established for
`lupinsho`/`lupinshoo` (`assessments/lupinsho.md` §7) and for `confmiss`/`deathcox*`. Flycast's
own source settles the classification directly: `core/hw/maple/maple_jvs.cpp:1532–1536`
(`../cleopatra/tools/flycast-src`) hard-codes `gameId == "THE MAZE OF THE KINGS"` into the *same*
branch as `hotd2*` (House of the Dead 2), `" CONFIDENTIAL MISSION ---------"`, `"DEATH CRIMSON
OX"`, and `"LUPIN THE THIRD  -THE SHOOTING-"`, setting `settings.input.lightgunGame = true` for
all five — `mok` is named by its exact game-ID string in this branch, not merely grouped by a
prefix/hash check, the most direct form of this citation in the cohort so far. Confidential
Mission, Death Crimson OX, and House of the Dead 2 all officially shipped as Sega Dreamcast Gun
(HKT-7800) games ([Wikipedia: Dreamcast light guns](https://en.wikipedia.org/wiki/Dreamcast_light_guns)).
Corroborated by [arcadeitalia MAME DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=mok):
"Input: Lightgun", up to 2 concurrent players, 2 buttons/coins. Three sources, all recorded in
sidecar `controls.sources`. `controls.device_class = dc_peripheral` — on-ladder, so controls do
**not** currently gate and would not gate G2 even if ARAM cleared; ARAM alone is the blocker.
Proposed DC mapping mirrors `lupinsho`: DC Gun (HKT-7800) screen-position aim = X/Y, trigger =
P1 Trigger, side/B button = P1 Screen-In (reload) — a direct 1:1 hardware mapping.

What would unblock it: ARAM content would need to shrink below the 2× cap — `mok`'s 3.558× sits
in the upper-middle of the parked cohort (below `sstrkfgt` 3.687×, above `mazan` 3.483×). Both
other regions already clear (main 0.932×, VRAM 0.902×), and controls are on-ladder
(`dc_peripheral`) — ARAM is the *only* blocker; a sound-asset trim sufficient to bring
`content_total` under 2,097,152 B would clear the title outright with no other work needed.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — light-gun cohort, fresh v9 capture; controls dc_peripheral (ARAM sole blocker) |
