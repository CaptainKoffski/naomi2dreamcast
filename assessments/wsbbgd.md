# World Series Baseball / Super Major League (GDS-0010) (`wsbbgd`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,277,014 B → utilization **3.470** — 12th-highest of the 25-strong parked ARAM cohort and the **coolest of the four Dynamite Baseball engine titles** (wsbbgd 3.470 < `dybb99` 3.531 < `smlg99` 3.684 < `dybbnao` 3.729). Unlike its three cart siblings, ARAM is the **sole blocker**: main content u **0.550** and VRAM content+2×fb u **0.914** both fit under 1× — the only member of the series with both other regions inside DC capacity. Franchise precedent is the strongest available: the game's own western brand shipped pad-native on DC (*World Series Baseball 2K1*, NA 2000-07-25; *2K2*, DC 2001-08-14), making wsbbgd the preferred unpark of the whole series under kb §6 item 1 (ARAM gate softening). Controls on-ladder: `stick` — reuses `INPUT_PORTS_START( dybbnao )` (analog X/Y + 2 buttons + pedal), every input with a native DC-pad analog counterpart. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `wsbbgd` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11161, `/* 0010  */`, parent `naomigd`) |
| Maker / year | Sega, 2001 (MAME `GAME()` row) — GDS-0010 |
| Genre / format | 3D baseball (MLB/MLBPA-licensed — "Major League Baseball trademarks and copyrights are used with permission" + MLB Players Choice license screen, `shot-487s.png`; 2000-season rosters in demo: P. O'Neill NYY, C. Guzman MIN), **GD-ROM** (naomigd), 157.8 MB (`GAME_FORMATS.md`) — carve title `SUPER MAJOR LEAGUE` |
| Official DC port | **No** — wsbbgd itself never reached DC. Its own western franchise line shipped natively on DC: *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* (DC 2001-08-14, Visual Concepts) ([Wikipedia, WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series))) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family; fourth and final Dynamite Baseball engine title in the queue — the GD-ROM successor to carts `dybbnao` (parked 3.729), `dybb99` (3.531), `smlg99` (3.684), reusing their `dybbnao` input port set (naomi.cpp line 11161) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/wsbbgd.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Full attract cycle under FREE PLAY / PRESS START banners, no static pre-game
screen: in-game demo fielding chase (`shot-060s.png`), HOW TO PLAY — THROWING with P. O'Neill at
Yankee Stadium and the cabinet panel graphic — analog stick + 2 buttons + pedal
(`shot-121s.png`), DEMO PLAY MIN @ NYY 1st inning with pitch cursor (`shot-182s.png`),
National League RANKING table under SUPER MAJOR LEAGUE branding (`shot-243s.png`), HOW TO PLAY —
PITCHING pitch-type rose (`shot-304s.png`), DEMO PLAY stadium flyover "YANKEES VS ATHLETICS —
NETWORK ASSOCIATES COLISEUM" (`shot-365s.png`), DEMO PLAY NYY @ OAK 0-2 count (`shot-426s.png`),
MLB / MLB Players Choice license screen (`shot-487s.png`), HOW TO PLAY — BATTING
(`shot-548s.png`), player close-up with crowd (`shot-609s.png`).
The park is unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/wsbbgd/shot-121s.png` · `shot-182s.png` · `shot-243s.png` ·
`shot-365s.png` · `shot-487s.png`
Anomalies: none — leg 1 attempt 1 ran the full 600 s window. `shot-060s.png` (demo dup),
`shot-304s.png`, `shot-548s.png` (HOW TO PLAY dups of 121s), `shot-426s.png` (demo dup),
`shot-609s.png` (close-up) curated out.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,277,014 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.470** — past `region_score()`'s `u > 2.0` gate, **12th-highest of the 25-strong
parked ARAM cohort**: just 4,432 B above `jambo` (3.468) and below `mazan` (3.483); cohort spans
`toyfight` 2.035 … `slashout` 3.756. Within the Dynamite Baseball engine series wsbbgd is the
coolest of the four: **3.470** < `dybb99` 3.531 < `smlg99` 3.684 < `dybbnao` 3.729.
`nz_above_cap` = 5,237,222 B (address-keyed placement figure, informational). Address peak
8,323,024 B (u 3.969, pre-volume-keying read — the usual near-full 8 MiB bank).

The other two regions, quoted from the sidecar — **both fit under 1×**, the only title of the
baseball series where that holds (its cart siblings ran main 1.13–1.21 and VRAM 1.12–1.21 over):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 9,233,121 | 16,777,216 | **0.550** | `nz_total` — fits with 45% headroom; `nz_above_cap` (address-placement) 2,681,443 B · `dma_high_water` 9,560,096 B (u 0.570) · watermark/peak 32,503,132 B (u 1.937 — near-full 32 MiB Naomi bank touched, stale-data-prone read) |
| VRAM (content volume + 2×fb) | 7,666,203 | 8,388,608 | **0.914** | `content_total` 6,437,403 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — fits with 8.6% headroom; raw `nz_total` 7,041,901 (u 0.839) · address peak 15,036,049 (u 1.792) |
| ARAM (content volume) | 7,277,014 | 2,097,152 | **3.470** | the gate — see above |

That makes wsbbgd an **ARAM sole-blocker** — one of 10 in the 25-strong cohort (with `inunoos`,
`mok`, `monkeyba`, `ninjaslt`, `pokasuka`, `shaktamb`, `tduno2`, `toyfight`, `vonot`) whose main
and VRAM content volumes both sit under 1×.

Streaming context: 10,788 DMA events · 78,096,320 B total · 24,547,296 B unique · re-read ratio
0.6857 · steady-state 5.873 MB/min (`short_window: false`) · `pio_bytes` 4,198,912 B.
Guts: carve 4,194,304 B (`carve_meta.title = "SUPER MAJOR LEAGUE"`) · 7,141 functions · MMIO refs
rtc 5 / g2ext 159 / scif 2 · flags `eeprom_bios`/`serial`/`rtc` · baseball state-machine symbol
set (`Runner_*`/`Fielder_*`/`Pitcher_*`/`Batter_*`) shared with the cart trio.
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `stick`):** 2-player panel, per player one **Sega analog
joystick** (`IPT_AD_STICK_X/Y`) + **2 buttons** + one **pedal-class analog axis** (`IPT_PEDAL`)
+ start — wsbbgd's `GAME()` row (MAME src/mame/sega/naomi.cpp @59e7c0b line 11161) binds
`INPUT_PORTS_START( dybbnao )` (lines 1655–1697, owned by `dybbnao` row 10938), the series port
set also reused by `dybb99` (10957) and `smlg99` (10951) — verified in source. Corroboration:
[Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=wsbbgd) lists
"Stick, Pedal / 2 buttons / 2 players" for wsbbgd; the physical panel's Sega analog joystick is
documented in the [Arcade-Projects thread](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/)
"Sega Analog joystick (from Dynamite Baseball/World Series control panels)"; and the game's own
HOW TO PLAY screens render the panel — ball-top analog stick, two buttons, pedal
(`evidence/wsbbgd/shot-121s.png`, plus PITCHING/BATTING variants curated out).
Proposed DC mapping: analog stick → DC pad analog stick, 2 buttons → A/B, pedal axis → analog
trigger — the mapping Sega's own DC baseball line already used
([WSB 2K1, Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)).
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp INPUT_PORTS + GAME() rows ·
[Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=wsbbgd) ·
[Arcade-Projects](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/) ·
[Wikipedia WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series)) ·
in-game HOW TO PLAY panel graphic (`evidence/wsbbgd/shot-121s.png`).

**What would unblock it — kb §6 item 1 (ARAM gate softening):** the 3.470× overshoot is a
sound-bank trim, the category where the gate is provably too strict (Ikaruga's official DC port
made a 4× trim). wsbbgd is the best-positioned unpark of the entire Dynamite Baseball series:
ARAM is its **sole blocker** (main 0.550 / VRAM 0.914 both fit — no residual squeeze to engineer
around, unlike smlg99's main 1.177 / VRAM 1.122), its ARAM multiple is the series' lowest, and
the franchise precedent is direct — the same western brand shipped pad-native MLB baseball on DC
as *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* (DC 2001-08-14), commentary and stadium
audio inside the DC's 2 MiB AICA RAM by construction
([Wikipedia, WSB series](https://en.wikipedia.org/wiki/World_Series_Baseball_(video_game_series))),
with the identical control panel on the arcade side. Under a softer ARAM rule wsbbgd unparks
with no other region over cap; it supersedes `smlg99` as the series' preferred unpark for a
western-market port (MLB license + DC WSB lineage + GD-ROM asset base).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.470, 12th-highest of 25-strong cohort, coolest of the four Dynamite Baseball engine titles; sole blocker (main 0.550 / VRAM 0.914 both fit, only series member); reuses dybbnao stick port set (naomi.cpp line 11161 verified); own-franchise DC precedent (WSB 2K1/2K2) noted for kb §6 item 1 |
