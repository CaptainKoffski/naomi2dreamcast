# World Series 99 / Super Major League 99 (`smlg99`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,725,487 B → utilization **3.684** — 7th-highest of the 20-strong parked ARAM cohort, a hair (1,214 B) under `ringout` 3.684 and sitting between its Dynamite Baseball engine siblings `dybb99` (3.531) and `dybbnao` (3.729). The other two regions are over 1× but under the gate: main content u **1.177** (would score ≈53), VRAM content+2×fb u **1.122** (would score ≈63 — best of the baseball trio). Franchise precedent for the softening argument (kb §6 item 1) is the strongest of the trio: this game's own western brand shipped pad-native on DC — *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* (DC 2001-08-14) — inside 2 MiB AICA RAM by construction ([Wikipedia, WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series))), and the arcade line's own GD-ROM successor `wsbbgd` (*World Series Baseball / Super Major League*, GDS-0010, 2001) reuses the identical input port set. Controls on-ladder: `stick` — reuses `INPUT_PORTS_START( dybbnao )` (analog X/Y + 2 buttons + pedal), every input with a native DC-pad analog counterpart. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `smlg99` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10951, `/* 0012 -01*/`, parent `naomi`) |
| Maker / year | Sega, 1999 (MAME `GAME()` row) — build stamp `99/07/11 0:00` in carve strings |
| Genre / format | 3D baseball (MLB/MLBPA-licensed — "Major League Baseball trademarks … used with permission" + "© 1999 MLBPA" title footer, `shot-121s.png`; real 1999 MLB rosters in carve strings), **cart** (naomim2), 109.7 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — smlg99 itself never reached DC. Same-franchise DC line: *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* (DC 2001-08-14) ([Wikipedia, WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series))); arcade successor `wsbbgd` (GDS-0010, 2001) stayed NAOMI GD-ROM (naomi.cpp line 11161) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family; Dynamite Baseball engine lineage — `dybbnao` (1998, parked G3-aram 3.729) and `dybb99` (1999, parked G3-aram 3.531) are separate queue families |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/smlg99.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Full attract cycle under PRESS START / FREE PLAY banners, no static pre-game
screen: MLB logo splash (`shot-060s.png`), SUPER MAJOR LEAGUE 99 title with MLB/MLBPA license
footer (`shot-121s.png`), DEMONSTRATION PLAY batter intro card ATL @ FLA, C. Jones 3B with photo
and stats (`shot-182s.png`), Sega logo (`shot-243s.png`), demo pitch-speed overlay ("999 MPH"
flaming-ball gag shot, `shot-304s.png`), HOW TO PLAY pitching tutorial showing the analog-stick
pitch-aim diagram and "PUSH A BUTTON TO PITCH" (`shot-365s.png`), second title pass
(`shot-487s.png`), second DEMONSTRATION PLAY matchup FLA @ MON, A. Gonzalez SS (`shot-548s.png`).
The park is unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/smlg99/shot-121s.png` · `shot-182s.png` · `shot-304s.png` ·
`shot-365s.png` · `shot-548s.png`
Anomalies: none — leg 1 attempt 1 ran the full 600 s window. `shot-060s.png`, `shot-426s.png`
(MLB logo dups), `shot-243s.png`, `shot-609s.png` (Sega logo dups), `shot-487s.png` (title dup)
curated out.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,725,487 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.684** — past `region_score()`'s `u > 2.0` gate, **7th-highest of the 20-strong
parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `asndynmt` 2.782, `alpilot` 2.958,
`takoron` 2.997, `inunoos` 3.206, `shaktamb` 3.245, `ninjaslt` 3.341, `pokasuka` 3.368,
`mazan` 3.483, `dybb99` 3.531, `mok` 3.558, `monkeyba` 3.637, `smlg99` **3.684**,
`ringout` 3.684 (7,726,701 B — 1,214 B hotter), `sstrkfgt` 3.687, `alienfnt` 3.702,
`dybbnao` 3.729, `vonot` 3.746, `slashout` 3.756 (max). Within the baseball trio smlg99 sits
between `dybb99` (3.531) and `dybbnao` (3.729), same engine family. `nz_above_cap` =
5,763,469 B (address-keyed placement figure, informational). Address peak 8,257,552 B
(u 3.938, pre-volume-keying read — the usual near-full 8 MiB bank).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — both over 1×, neither gated:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 19,739,224 | 16,777,216 | **1.177** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈53); `nz_above_cap` (address-placement) 11,426,407 B · `dma_high_water` 16,911,232 B (u 1.008 — most loading is PIO, `pio_bytes` 35.5 MB) · watermark/peak 33,554,432 B (u 2.000 — full 32 MiB Naomi bank touched) |
| VRAM (content volume + 2×fb) | 9,415,489 | 8,388,608 | **1.122** | `content_total` 8,186,689 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — 12.2% over the cap (would score ≈63, best of the baseball trio); raw `nz_total` 8,795,748 (u 1.049) · address peak 16,251,904 (u 1.937) |
| ARAM (content volume) | 7,725,487 | 2,097,152 | **3.684** | the gate — see above |

Streaming context: 206,721 DMA events · 50,532,032 B total · 14,422,272 B unique · re-read
ratio 0.7146 · steady-state 4.864 MB/min (`short_window: false`) · `pio_bytes` 35,523,604 B.
Guts: carve 1,376,256 B (`carve_meta.title = "SUPER MAJOR LEAGUE 99"`) · 2,085 functions ·
MMIO refs rtc 2 / g2ext 179 / scif 0 · flags `eeprom_bios`/`rtc` · Naomi-native SDK stack
(`NAOMI LIBRARY Ver 0.8 AM R&D`, `libam/Version 1.232810`, `KM1Naomi Ver 1.31`).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `stick`):** 2-player panel, per player one **Sega
analog joystick** (`IPT_AD_STICK_X/Y`) + **2 buttons** + one **pedal-class analog axis**
(`IPT_PEDAL`) + start — smlg99's `GAME()` row (MAME src/mame/sega/naomi.cpp @59e7c0b line
10951) binds `INPUT_PORTS_START( dybbnao )` (lines 1655–1697, owned by `dybbnao` row 10938),
the series port set also reused by `dybb99` (10957) and the GD-ROM *World Series Baseball*
`wsbbgd` (11161). Corroboration:
[Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=smlg99)
lists "Stick, Pedal / 2 buttons / 2 players" for smlg99; the physical panel's Sega analog
joystick is documented in the [Arcade-Projects thread](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/)
"Sega Analog joystick (from Dynamite Baseball/World Series control panels)" — the panel
name covers this very game; and the game's own attract tutorial shows the analog-stick
pitch-aim rose + "PUSH A BUTTON TO PITCH" (`evidence/smlg99/shot-365s.png`).
Proposed DC mapping: analog stick → DC pad analog stick, 2 buttons → A/B, pedal axis →
analog trigger — every cabinet input has a native DC-pad analog counterpart, the mapping
Sega's own DC baseball line already used ([WSB 2K1, Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)).
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp INPUT_PORTS + GAME()
rows · [Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=smlg99) ·
[Arcade-Projects](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/) ·
[Wikipedia WSB 2K1](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1) ·
in-game HOW TO PLAY screen (`evidence/smlg99/shot-365s.png`).

**What would unblock it — kb §6 item 1 (ARAM gate softening):** the 3.684× overshoot is a
sound-bank trim, the category where the gate is provably too strict (Ikaruga's official DC
port made a 4× trim). smlg99 carries the strongest franchise precedent of the baseball trio:
its own western brand — *World Series* — shipped pad-native MLB baseball on DC as
*World Series Baseball 2K1* (NA 2000-07-25) and *2K2* (DC 2001-08-14), commentary and
stadium audio inside the DC's 2 MiB AICA RAM by construction
([Wikipedia, WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series))),
and the arcade line itself continued on NAOMI GD-ROM as `wsbbgd` with the identical control
panel. Under a softer ARAM rule smlg99 unparks with main ≈53 / VRAM ≈63 sub-scores —
best VRAM residual of the trio (1.122 vs dybb99 ≈1.206 / dybbnao 1.193), main squeeze
(17.7% over) between dybb99 (1.134) and dybbnao (1.209). Unpark priority: behind the
sole-blocker candidates (`ausfache`, `radirgyn`, `vonot`) and the narrow-miss `asndynmt`;
within the baseball trio smlg99 is the preferred unpark for a western-market port
(MLB license + DC WSB lineage), `dybb99` for the coolest ARAM/main numbers (3.531/1.134).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.684, 7th-highest of 20-strong cohort, between engine siblings dybb99 (3.531) and dybbnao (3.729); main 1.177/VRAM 1.122 over 1× (no gate, best trio VRAM); reuses dybbnao stick port set; own-franchise DC precedent (WSB 2K1/2K2) noted for kb §6 item 1 |
