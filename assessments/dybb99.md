# Dynamite Baseball '99 (`dybb99`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,404,736 B → utilization **3.531** — 11th of the 18-strong parked ARAM cohort, squarely mid-pack. The other two regions are over 1× but under the gate: main content u **1.134** (would score ≈61), VRAM content+2×fb u **1.207** (would score ≈48) — under a softer ARAM rule this unparks into the low-mid band. Genre precedent for the softening argument (kb §6 item 1): pad-native licensed baseball shipped on DC — *World Series Baseball 2K1* (NA 2000-07-25) and *2K2*, inside 2 MiB AICA RAM by construction ([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)) — sibling-genre only, Dynamite Baseball itself was never ported home ([Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)). Controls on-ladder: `stick` — 2P panel of Sega analog joystick + 2 buttons + one pedal-class analog axis per player; every input has a native DC-pad analog counterpart. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `dybb99` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10957, `/* 0019 */`, parent `naomi`) |
| Maker / year | Sega, 1999 (MAME `GAME()` row) |
| Genre / format | 3D baseball (NPB-licensed — 12-club license card at boot, `shot-060s.png`), **cart** (naomim2), 106.4 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — arcade-only: "never ported to a home console, though it shared many similarities with WSB 2K/2K1" ([Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html)). Sibling-genre DC lineage is direct: *World Series Baseball 2K1* (WOW/Sega, DC NA 2000-07-25) and *2K2* ([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)); in-driver, the NAOMI *World Series Baseball* (`wsbbgd`, GDS-0010) and *World Series 99 / Super Major League 99* (`smlg99`) share `dybb99`'s exact input port set (naomi.cpp @59e7c0b lines 11161, 10951) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (Rev B cart); predecessor `dybbnao` (1998) is a separate queue family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/dybb99.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Full attract cycle, no static pre-game screen: NPB 12-club license card
(`shot-060s.png`, FREE PLAY), title logo (`shot-121s.png`, dup ×2), demo player-intro card with
デモプレイ tag (`shot-182s.png`, Yomiuri Giants #11 with '99 season stats), demo pitching gameplay
(`shot-304s.png`), high-score ranking (`shot-426s.png`), starting-lineup card (`shot-548s.png`),
demo batting with live SBO/inning HUD and デモプレイ tag (`shot-609s.png`). The park is
unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/dybb99/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-304s.png` · `shot-609s.png`
Anomalies: battery leg 1 exited early (`emulator-exited` flake); the automatic retry (leg 2) ran
the full 600 s window and produced this sidecar. `shot-243s.png`, `shot-365s.png`,
`shot-487s.png` curated out (title ×2 / license-card dup), `shot-426s.png`, `shot-548s.png`
curated out (attract info screens).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,404,736 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.531** — past `region_score()`'s `u > 2.0` gate, **11th of the 18-strong parked
ARAM cohort**, squarely mid-pack: `toyfight` 2.035, `tduno2` 2.615, `asndynmt` 2.782,
`alpilot` 2.958, `takoron` 2.997, `inunoos` 3.206, `shaktamb` 3.245, `ninjaslt` 3.341,
`pokasuka` 3.368, `mazan` 3.483, `dybb99` **3.531**, `mok` 3.558, `monkeyba` 3.637,
`ringout` 3.684, `sstrkfgt` 3.687, `alienfnt` 3.702, `vonot` 3.746, `slashout` 3.756 (max).
`nz_above_cap` = 5,421,753 B (address-keyed placement figure, informational). Address peak
8,257,552 B (u 3.938, pre-volume-keying read — the usual near-full 8 MiB bank).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — both over 1×, neither gated:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 19,027,010 | 16,777,216 | **1.134** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈61); `nz_above_cap` (address-placement) 10,094,626 B · `dma_high_water` 16,912,256 B (u 1.008) · watermark/peak 33,554,432 B (u 2.000 — full 32 MiB Naomi bank touched) |
| VRAM (content volume + 2×fb) | 10,126,610 | 8,388,608 | **1.207** | `content_total` 8,897,810 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — 20.7% over the cap (would score ≈48); raw `nz_total` 9,434,107 (u 1.125) · address peak 16,777,216 (u 2.000) |
| ARAM (content volume) | 7,404,736 | 2,097,152 | **3.531** | the gate — see above |

Streaming context: 243,610 DMA events · 59,858,912 B total · 18,120,320 B unique · re-read
ratio 0.6973 · steady-state 5.99 MB/min (`short_window: false`) · `pio_bytes` 28,299,472 B.
Guts: carve 1,245,184 B (`carve_meta.title = "DYNAMITE BASEBALL '99"`) · 2,377 functions ·
MMIO refs rtc 2 / g2ext 166 / scif 0 · flags `eeprom_bios`/`rtc` · Naomi-native SDK stack
(`NAOMI LIBRARY Ver 0.8 AM R&D`, `KM1Naomi Ver 1.31`, `libam`, `AM2/AICAsoundDrv990727`).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `stick`):** 2-player panel, per player one **Sega
analog joystick** (`IPT_AD_STICK_X/Y`) + **2 buttons** + one **pedal-class analog axis**
(`IPT_PEDAL`) + start — `INPUT_PORTS_START( dybbnao )`, MAME src/mame/sega/naomi.cpp
@59e7c0b lines 1655–1697, bound to `dybb99` by the `GAME()` row at line 10957; the same set
serves `dybbnao` (1998), `smlg99` and the GD-ROM *World Series Baseball* `wsbbgd`
(lines 10938/10951/11161). Corroboration: [Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dybb99)
lists "Stick, Pedal / 2 buttons / 2 players"; the physical panel's Sega analog joystick is
documented in the [Arcade-Projects thread](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/)
"Sega Analog joystick (from Dynamite Baseball/World Series control panels)".
Proposed DC mapping: analog stick → DC pad analog stick, 2 buttons → A/B, pedal axis →
analog trigger — every cabinet input has a native DC-pad analog counterpart, the mapping
Sega's own DC baseball line already used ([WSB 2K1, Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)).
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp INPUT_PORTS + GAME()
rows · [Arcade Italia ADB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=dybb99) ·
[Arcade-Projects](https://www.arcade-projects.com/threads/sega-analog-joystick-from-dynamite-baseball-world-series-control-panels.21312/) ·
[Wikipedia WSB 2K1](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1) ·
[Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html).

**What would unblock it — kb §6 item 1 (ARAM gate softening):** the 3.531× overshoot is a
sound-bank trim, the category where the gate is provably too strict (Ikaruga's official DC
port made a 4× trim). Genre precedent: Sega shipped pad-native, fully-licensed baseball on
DC — *World Series Baseball 2K1* (NA 2000-07-25) and *2K2* — with commentary and stadium
audio inside the DC's 2 MiB AICA RAM by construction
([Wikipedia](https://en.wikipedia.org/wiki/World_Series_Baseball_2K1)); sibling-genre
precedent only, not the same game or engine. Under a softer ARAM rule dybb99 unparks with
main ≈61 / VRAM ≈48 sub-scores — low-mid band, VRAM 20.7% over budget being the harder
residual squeeze. Unpark priority: behind the sole-blocker candidates (`ausfache`,
`radirgyn`, `vonot`) and the narrow-miss `asndynmt`, with the alienfnt-class multi-region
cases.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.531 mid-pack (11th of 18-strong cohort); main 1.134/VRAM 1.207 over 1× (no gate); WSB 2K1/2K2 DC sibling-genre precedent noted for kb §6 item 1; controls stick (analog stick + 2 buttons + pedal axis, native DC-pad analog mapping) |
