# Dynamite Baseball NAOMI (`dybbnao`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,820,872 B → utilization **3.729** — 3rd-highest of the 19-strong parked ARAM cohort, hotter than its successor `dybb99` (3.531). The other two regions are over 1× but under the gate: main content u **1.209** (would score ≈47), VRAM content+2×fb u **1.193** (would score ≈50) — under a softer ARAM rule this unparks into the same low-mid band as `dybb99`. Series precedent for the softening argument (kb §6 item 1): Sega shipped pad-native licensed baseball on DC — *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* — inside 2 MiB AICA RAM by construction ([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)); a DC port of *Dynamite Baseball* itself was announced but cancelled (`GAME_FORMATS.md` near-miss list). Controls on-ladder: `stick` — this set OWNS the series input port set (`INPUT_PORTS_START( dybbnao )`) that `dybb99`/`smlg99`/`wsbbgd` reuse; every input has a native DC-pad analog counterpart. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `dybbnao` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10938, `/* 0001 */`, parent `naomi`) |
| Maker / year | Sega, 1998 (MAME `GAME()` row) — build stamp `98/12/14 6:30` in carve strings |
| Genre / format | 3D baseball (NPB-licensed — real club logos in attract TEAM RANKING, `shot-060s.png` scoreboard), **cart** (naomim2), 114.8 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — a DC port was announced but cancelled, never released (`GAME_FORMATS.md` "cancelled-but-unreleased DC ports" list); the series never reached home consoles ([Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)). Sibling-genre DC lineage: *World Series Baseball 2K1*/*2K2* ([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family; successor `dybb99` (1999) is a separate queue family (finalized parked G3-aram, same engine lineage) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/dybbnao.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Full attract cycle under a FREE PLAY / PRESS START banner, no static pre-game
screen: stadium fly-through with live scoreboard (`shot-060s.png`), demo fielding gameplay with
diamond minimap (`shot-121s.png`), PLAYER RANKING salary board (`shot-182s.png`), demo player-intro
card (`shot-243s.png`, SUN #20), demo pitching with STRIKE overlay and full defensive AI
(`shot-304s.png`), TEAM RANKING with six NPB club logos (`shot-365s.png`), dugout cutscenes
(`shot-426s.png` Carp, `shot-609s.png` Swallows), demo fly-ball fielding with OUT HUD
(`shot-487s.png`), HOMERUN RANKING (`shot-548s.png`). The park is unambiguously the game running
its attract cycle, not tooling.
Screenshots: `evidence/dybbnao/shot-060s.png` · `shot-121s.png` · `shot-243s.png` ·
`shot-304s.png` · `shot-487s.png`
Anomalies: none — leg 1 attempt 1 ran the full 600 s window. `shot-182s.png`, `shot-365s.png`,
`shot-548s.png` curated out (attract info/ranking screens), `shot-426s.png`, `shot-609s.png`
curated out (dugout cutscene dups).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,820,872 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.729** — past `region_score()`'s `u > 2.0` gate, **3rd-highest of the 19-strong
parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `asndynmt` 2.782, `alpilot` 2.958,
`takoron` 2.997, `inunoos` 3.206, `shaktamb` 3.245, `ninjaslt` 3.341, `pokasuka` 3.368,
`mazan` 3.483, `dybb99` 3.531, `mok` 3.558, `monkeyba` 3.637, `ringout` 3.684,
`sstrkfgt` 3.687, `alienfnt` 3.702, `dybbnao` **3.729**, `vonot` 3.746, `slashout` 3.756 (max) —
0.198 hotter than successor `dybb99`, same engine family. `nz_above_cap` = 5,863,155 B
(address-keyed placement figure, informational). Address peak 8,272,376 B (u 3.945,
pre-volume-keying read — the usual near-full 8 MiB bank).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — both over 1×, neither gated:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 20,278,821 | 16,777,216 | **1.209** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈47); `nz_above_cap` (address-placement) 11,567,189 B · `dma_high_water` 31,448,704 B (u 1.874) · watermark/peak 33,540,512 B (u 1.999 — full 32 MiB Naomi bank touched) |
| VRAM (content volume + 2×fb) | 10,010,390 | 8,388,608 | **1.193** | `content_total` 8,781,590 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — 19.3% over the cap (would score ≈50); raw `nz_total` 9,337,961 (u 1.113) · address peak 16,136,192 (u 1.924) |
| ARAM (content volume) | 7,820,872 | 2,097,152 | **3.729** | the gate — see above |

Streaming context: 53,336 DMA events · 101,002,240 B total · 24,820,256 B unique · re-read
ratio 0.7543 · steady-state 9.875 MB/min (`short_window: false`) · `pio_bytes` 36,364,048 B.
Guts: carve 1,032,192 B (`carve_meta.title = "DYNAMITE BASEBALL NAOMI"`) · 1,768 functions ·
MMIO refs rtc 2 / g2ext 163 / scif 0 · flags `eeprom_bios`/`rtc` · Naomi-native SDK stack
(`NAOMI LIBRARY Ver 0.8 AM R&D`, `libam/Version 1.221940`, `syChain Ver 1.01`).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `stick`):** 2-player panel, per player one **Sega
analog joystick** (`IPT_AD_STICK_X/Y`) + **2 buttons** + one **pedal-class analog axis**
(`IPT_PEDAL`) + start — `INPUT_PORTS_START( dybbnao )`, MAME src/mame/sega/naomi.cpp
@59e7c0b lines 1655–1697: this is dybbnao's **own** port set, bound by the `GAME()` row at
line 10938 and reused verbatim by `smlg99` (10951), `dybb99` (10957) and the GD-ROM
*World Series Baseball* `wsbbgd` (11161). Corroboration:
[Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dybbnao)
lists "Stick, Pedal / 2 buttons / 2 players"; the physical panel's Sega analog joystick is
documented in the [Arcade-Projects thread](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/)
"Sega Analog joystick (from Dynamite Baseball/World Series control panels)".
Proposed DC mapping: analog stick → DC pad analog stick, 2 buttons → A/B, pedal axis →
analog trigger — every cabinet input has a native DC-pad analog counterpart, the mapping
Sega's own DC baseball line already used ([WSB 2K1, Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)).
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp INPUT_PORTS + GAME()
rows · [Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dybbnao) ·
[Arcade-Projects](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/) ·
[Wikipedia WSB 2K1](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1) ·
[Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html).

**What would unblock it — kb §6 item 1 (ARAM gate softening):** the 3.729× overshoot is a
sound-bank trim, the category where the gate is provably too strict (Ikaruga's official DC
port made a 4× trim). Precedent is stronger here than genre-only: a DC port of this very
game was announced and cancelled (`GAME_FORMATS.md` near-miss list), and Sega shipped
pad-native licensed baseball on DC — *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* —
with commentary and stadium audio inside the DC's 2 MiB AICA RAM by construction
([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)). Under a softer ARAM
rule dybbnao unparks with main ≈47 / VRAM ≈50 sub-scores — same low-mid band as `dybb99`
(≈61/≈48), with main RAM the harder residual squeeze (20.9% over). Unpark priority: behind
the sole-blocker candidates (`ausfache`, `radirgyn`, `vonot`) and the narrow-miss
`asndynmt`, with the alienfnt-class multi-region cases; if the series ever unparks, prefer
`dybb99` — cooler ARAM (3.531 vs 3.729), better main fit (1.134 vs 1.209), newer rosters.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.729, 3rd-highest of 19-strong cohort, hotter than successor dybb99 (3.531); main 1.209/VRAM 1.193 over 1× (no gate); owns the series INPUT_PORTS set (stick); cancelled DC port + WSB 2K1/2K2 precedent noted for kb §6 item 1 |
