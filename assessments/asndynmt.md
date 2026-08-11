# Asian Dynamite / Dynamite Deka EX (`asndynmt`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 5,833,924 B → utilization **2.782** — third-lowest of the 14-strong parked ARAM cohort, i.e. one of the smallest sound trims the gate has parked. Series precedent for the gate (kb §6 item 1): **the direct predecessor *Dynamite Cop* (Dynamite Deka 2) shipped on Dreamcast in 1999, pad-native, inside the DC's 2 MiB ARAM by construction** — and Asian Dynamite reuses that game's level layouts ([Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)) and was probably built on its Dreamcast version ([HG101](https://www.hardcoregaming101.net/dynamite-deka-ex-asian-dynamite/)); the carve is saturated with SEGAKATANA/Kunoichi2/KAMUI2 (DC SDK) library strings. Weaker than the same-game precedents (`alienfnt`, `vonot`) but real. Other regions barely miss: main content u **1.132** (would score ≈61), VRAM content+2×fb u **1.032** (would score ≈79) — under a softer ARAM rule this unparks into mid-band, not the floor. Controls on-ladder: `stick` — 8-way + series-standard 3 buttons (Punch/Kick/Jump), trivially pad-mappable. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `asndynmt` (covers clone `asndynmto` "older" — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` lines 11046–11047, both `/* 0175 */`) |
| Maker / year | Sega, 2007 (MAME `GAME()` row; produced cheaply by Sega Shanghai per [Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)) |
| Genre / format | 3D beat-em-up (Dynamite Deka series revival), **cart**, 148.0 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — arcade-only: "never ported, and thus exists only in arcades and on emulators" ([HG101](https://www.hardcoregaming101.net/dynamite-deka-ex-asian-dynamite/)); "No home console release whatsoever" ([gemubaka](https://gemubaka.com/2022/09/24/the-third-dynamite-deka-game-ex/)). Series lineage on DC is direct, though: *Dynamite Cop* (Dynamite Deka 2) DC JP 1999-05-27 / EU 1999-10-14 / NA 1999-11-02 ([Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Parent set (revision-stickered cart); clone `asndynmto` is the unstickered, presumably older revision of the same cart |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/asndynmt.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Full attract cycle across all ten shots, no static pre-game screen: press-start
city panorama (`shot-060s.png`, FREE PLAY), demo gameplay with live DEKA SCORE HUD (`shot-121s.png`,
`shot-304s.png`, `shot-487s.png`), story cutscenes (`shot-182s.png`, `shot-609s.png`), demo combat
(`shot-243s.png`), title logo (`shot-365s.png`, `shot-548s.png`), demo "SUCCESS" results screen
(`shot-426s.png`). The park is unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/asndynmt/shot-060s.png` · `shot-243s.png` · `shot-304s.png` ·
`shot-365s.png` · `shot-426s.png`
Anomalies: none. `shot-121s.png`, `shot-182s.png`, `shot-487s.png`, `shot-548s.png`,
`shot-609s.png` curated out (duplicate demo gameplay ×2 / cutscene ×2 / duplicate title).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 5,833,924 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.782** — past `region_score()`'s `u > 2.0` gate but **third-lowest of the
14-strong parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `asndynmt` **2.782**,
`takoron` 2.997, `inunoos` 3.206, `ninjaslt` 3.341, `pokasuka` 3.368, `mazan` 3.483, `mok`
3.558, `monkeyba` 3.637, `ringout` 3.684, `sstrkfgt` 3.687, `alienfnt` 3.702, `vonot` 3.746
(max). `nz_above_cap` = 3,869,392 B (address-keyed placement figure, informational).
Address peak 8,257,552 B (u 3.938, pre-volume-keying read — the usual near-full 8 MiB bank).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — both nominally over 1×, but **narrowly**, unlike most of the cohort:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 18,988,905 | 16,777,216 | **1.132** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈61); `nz_above_cap` (address-placement) 12,062,733 B · `dma_high_water` 32,505,696 B (u 1.937) · watermark 33,153,112 B (u 1.976) |
| VRAM (content volume + 2×fb) | 8,660,024 | 8,388,608 | **1.032** | `content_total` 7,431,224 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — 3.2% over the cap (would score ≈79); raw `nz_total` 7,789,695 (u 0.929, fits) · address peak 12,953,600 (u 1.544) |
| ARAM (content volume) | 5,833,924 | 2,097,152 | **2.782** | the gate — see above |

Streaming context: 755 DMA events · 256,786,244 B total · 43,016,924 B unique · re-read ratio
0.8325 · steady-state 25.00 MB/min (`short_window: false`) · `pio_bytes` 5,266,640 B.
Guts: carve 2,228,224 B (`carve_meta.title = "DYNAMITE DEKA EX"`) · 3,024 functions · MMIO refs
rtc 3 / g2ext 105 / scif 2 · flags `eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false` —
note `guts.sdk_strings` is wall-to-wall Dreamcast (Katana) SDK: `SEGAKATANA`, "Kunoichi2
Library for NAOMI", KAMUI2, the sy*/pd* Katana kernel libraries, CRI ADX — consistent with
HG101's judgment that EX was built on the Dreamcast version of Dynamite Deka 2.

**Controls (on-ladder, does not gate — `stick`):** standard 2-player joystick panel. MAME
assigns the generic `naomi` input port set — 2P 8-way joystick + 6 buttons
(`GAME( 2007, asndynmt, naomi, naomim4, naomi, … )`, src/mame/sega/naomi.cpp @59e7c0b line
11046; `INPUT_PORTS_START( naomi )` line 1506, "2 players with 1 joystick and 6 buttons
each"). The series actually uses three of them — Punch / Kick / Jump
([gemubaka](https://gemubaka.com/2022/09/24/the-third-dynamite-deka-game-ex/)). The pad
adaptation is series-proven: *Dynamite Cop* shipped on DC in 1999 as a standard
controller game ([Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)).
Proposed DC mapping: d-pad/stick move + three face buttons Punch/Kick/Jump — the Dynamite
Cop DC scheme. Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp
INPUT_PORTS + GAME() row · [gemubaka](https://gemubaka.com/2022/09/24/the-third-dynamite-deka-game-ex/)
· [HG101](https://www.hardcoregaming101.net/dynamite-deka-ex-asian-dynamite/) ·
[Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop).

**What would unblock it — series precedent for kb §6 item 1:** the G3-ARAM softening
argument gets a *series-level* data point: Sega shipped ***Dynamite Cop* (Dynamite Deka 2)
on Dreamcast — JP 1999-05-27 / EU 1999-10-14 / NA 1999-11-02 — pad-native and, by
construction, inside the DC's 2 MiB AICA RAM**
([Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)). Asian Dynamite is not that game,
but it is unusually close to it: it reuses Dynamite Cop's level layouts re-themed
([Wikipedia](https://en.wikipedia.org/wiki/Dynamite_Cop)), HG101 judges it "probably built
on the Dreamcast version of the second game"
([HG101](https://www.hardcoregaming101.net/dynamite-deka-ex-asian-dynamite/)), and the
carve's Katana-SDK string wall corroborates the DC-derived engine. So the 2.78× sound trim
is one the series' own engine already made once — weaker than the same-game precedents
(`alienfnt`'s *Alien Front Online*, `vonot`) but real. Under a softer ARAM rule (kb §6
item 1's candidate fixes) it unparks with main ≈61 / VRAM ≈79 sub-scores — **mid-band, the
best post-unpark memory profile of the multi-region cohort** (VRAM is only 3.2% over and
raw `nz_total` already fits). Unpark priority: behind the sole-blocker candidates
(`ausfache`, `radirgyn`, `vonot`), ahead of the alienfnt-class multi-region cases.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 2.782 third-lowest of the 14-strong cohort; main 1.132/VRAM 1.032 narrowly over 1× (no gate); series precedent *Dynamite Cop* DC 1999 + Katana-SDK-derived engine noted for kb §6 item 1; controls stick (8-way + Punch/Kick/Jump) |
