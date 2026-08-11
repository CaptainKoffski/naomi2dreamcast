# Airline Pilots (World, Rev B) (`alpilot`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM parks it: `content_total` = 6,202,616 B of fill-excluded ARAM content, **2.958×** the DC's 2 MiB AICA RAM — the *second-lowest* parked ARAM figure in the campaign (only toyfight 2.033 is lower), sitting just under takoron's 2.997 inside what was once the empty scored/parked band (kb §6 items 1 and 9). Unlike the ARAM-sole-blocker parks, the other regions do **not** clear either: main content u ≈ 1.389 and VRAM fit u ≈ 1.196 are both over their 1× caps (not gating, but low-scoring), so an ARAM-gate softening would let it score, not score well. Controls are honestly `awkward`: the AM2 airliner cockpit has **5 analog axes** (control-wheel elevator/aileron, rudder pedal, dual thrust levers) against the DC pad's 4 analog channels, plus latching landing-gear/flap toggle switches. Reproduction requires the dedicated `airlbios` BIOS set — the first battery run parked G1 without it (§3). |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `alpilot` (no clones in current MAME — the older `alpiltdx` deluxe set was merged into it, [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=alpilot); `alpilotj` "Airline Pilots (Japan, Rev A)" is a separate MAME parent on the standard `naomi` BIOS, GAME line 10945) |
| Maker / year | Sega (AM2), 1999 (GAME line 10930: `/* 13763-01 */`; developed with input from Japan Airlines pilots/engineers — World set replaces JAL branding with fictional "Sega Airlines", `ROM_START( alpilot )` comment) |
| Genre / format | Commercial-airliner flight sim (Boeing 777 takeoff/landing trainer — GAME_FORMATS.md's "Driving" queue label is a genre-taxonomy artifact), **cart** — 13763-01, boot ROM `epr-21787b` + mpr ROMs, 41.3 MB |
| Official DC port | No (GAME_FORMATS.md: "No") |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | MAME parent (`alpilot`, World Rev B); `alpilotj` differs only in airline branding (JAL) and BIOS parentage |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/alpilot.zip`

**Reproduction requirement — dedicated `airlbios` BIOS.** `alpilot`'s MAME parent is not a
game but the BIOS set `airlbios` ("NAOMI Airline Pilots (deluxe) BIOS", `epr-21801`/
`epr-21802`, `MACHINE_IS_BIOS_ROOT` — naomi.cpp @59e7c0b GAME lines 10921/10930, and
`ROM_START( alpilot )` pulls `AIRLINE_BIOS`, not the standard NAOMI BIOS). The first
battery run parked `G1 broken: emulator-exited` because `airlbios.zip` was absent;
after installing it to `~/Library/Application Support/Flycast/data/` and `naomi/`, the
re-run booted clean and ran the full 600 s window. The standard `naomi.zip` BIOS alone
is NOT sufficient for this set.

Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote
`null`; set here after screenshot review). The attract loop cycles through a 777
takeoff/fly-by over a harbor city (`shot-060s.png`), an "INSTRUCTION — TURN" tutorial
overlay with the literal text "Turn the control wheel to make turns" and a cockpit-HUD
attitude/speed/altitude instrument cluster (`shot-121s.png`), the title logo
(`shot-243s.png`), a timed landing-approach demo with target boxes and a running clock
(`shot-426s.png`), and an "INSTRUCTION — LANDING" runway touchdown with full HUD and
POWER/FUEL gauges (`shot-609s.png`) — genuine attract-demo gameplay, not a frozen
pre-game screen.
Screenshots: `evidence/alpilot/shot-060s.png` · `shot-121s.png` · `shot-243s.png` ·
`shot-426s.png` · `shot-609s.png`
Anomalies: none in the clean run. The binary carries the deluxe multiboard link code —
`guts.sdk_strings` includes "Please Wait until Slaves synchronize...", "Slave No.%d is
OK!!", and `MultiCtrlReg` — but the single-board capture ran without a link partner and
completed normally.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 6,202,616 B`
(fill-excluded content volume, kb §6 volume keying) against the DC's 2,097,152 B AICA
RAM → utilization **2.958** — past `region_score()`'s `u > 2.0` gate. Cohort position:
this is the **second-lowest parked ARAM u** measured in the campaign, below takoron
2.997, inunoos 3.206, pokasuka 3.368, ninjaslt 3.341, mazan 3.483, mok 3.558, and
sstrkfgt 3.687, and above only toyfight 2.033 — i.e. the second title to land inside
the formerly empty (1.962, 2.997) scored/parked band tracked for the kb §6 item-1
threshold checkpoint (item 9 addendum). `nz_above_cap` = 4,172,783 B of content above
the cap (address-keyed placement figure, informational). Address peak is 6,449,000 B
(u 3.075, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in
`score.py`'s region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 23,296,994 | 16,777,216 | **1.389** | `nz_total` — over the 1× cap (would score ≈ 34 on the piecewise map, not gate); `nz_above_cap` (address-placement) 11,167,764 B · `dma_high_water` 30,469,696 B (u 1.816) · write peak 32,473,120 B (u 1.936) |
| VRAM (content volume + 2×fb) | 10,028,761 | 8,388,608 | **1.196** | `content_total` 8,799,961 + 2×`fb_bytes` (2×614,400, per `score.py`'s `vram_ct + 2*vram_fb` formula) — over the 1× cap; raw `nz_total` 9,405,577 · `nz_above_cap` 6,616,669 (address-keyed) |
| ARAM (content volume) | 6,202,616 | 2,097,152 | **2.958** | the gate — see above |

Unlike the ARAM-sole-blocker parks (toyfight, mok, ninjaslt, and the takoron/inunoos/
pokasuka trio, whose main and VRAM all clear), **alpilot is not sole-blocker**: main
1.389× and VRAM 1.196× are both over budget too. A kb §6 item-1 ARAM softening would
move it from parked to scored, but into low tiers, not high ones.

Streaming context: 10,657 DMA events · 63.6 MB total · 26.3 MB unique · re-read ratio
0.5857 · steady-state 5.359 MB/min (`short_window: false`) · `pio_bytes` 6,986,180 B.
Guts: code 1,257,472 B (1.20 MiB) · 1,446 functions · MMIO refs rtc 2 / g2ext 133 /
scif 0 · flags `eeprom_bios`/`rtc` · carve title "AIRLINE PILOTS IN JAPAN".
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

Evidence: `assessments/alpilot.metrics.json` → `memory.aram`; `guts.sdk_strings` shows
a large cabin/character animation and scenery-asset namespace (`isu_shaberi*` cabin
chatter, hundreds of `*hito_*` passenger motion entries, Tokyo-bay landmarks) consistent
with a big voice/ambience sound bank for the cabin-crew and ATC audio.

**Controls would not gate, but would take the ladder's bottom scoring rung.**
Researched (≥2 sources): the real cabinet is an AM2 airliner-cockpit rig — MAME
`INPUT_PORTS_START( alpilota )` (src/mame/sega/naomi.cpp @59e7c0b lines 1801–1853)
defines **5 analog axes**: A0 Control Wheel (Elevator, `AD_STICK_Y`), A1 Control Wheel
(Aileron, `AD_STICK_X`), A3 Rudder Pedal (`AD_STICK_Z`, neutral-centered), and A4/A5
**Thrust Lever L / Thrust Lever R** (`IPT_POSITIONAL_V`, `PORT_CENTERDELTA(0)` — 
non-centering latching levers), plus Landing Gear Switch and Flap Switch (both
`PORT_TOGGLE` — physical latching switches) and View Change. Two cabinet models were
manufactured: the standard single-monitor sit-down, and the "DX type" with three
side-by-side 29" monitors forming a surround cockpit
([LaunchBox DB](https://gamesdb.launchbox-app.com/games/details/34916)); the DX is a
multi-board linked setup on the dedicated airline BIOS (naomi.cpp GAME-line comment
"deluxe/multiboard setup uses specific BIOS 'airlbios'"; slave-sync strings in the
carve, §3), with rudder pedals, dual-thrust throttle, and landing-gear/flap controls
([Contraband Events cab page](https://www.contrabandevents.com/project/airline-pilots-arcade-game-berkshire-south-east-uk/);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=alpilot):
"Stick, Positional", 3 buttons, 1 player). A DC pad offers 4 analog channels (stick
X/Y + 2 triggers): one axis short of the cabinet's 5, so a mapping must merge the two
thrust levers or drop the rudder, and the non-centering thrust levers plus latching
gear/flap toggles degrade further on momentary pad hardware — a playable-but-degraded
mapping, so `controls.device_class = awkward` (25.0 on the `score.py:108` ladder), one
rung below sibling `sstrkfgt`'s `pad_adaptable` (whose `PORT_MODIFY` explicitly trims
the rig to exactly 4 axes). Not off-ladder — no card reader/hopper, and the single
standard cab needs no link — so no G2.

What would unblock it: an ARAM-gate softening per the kb §6 item-1 checkpoint (the
ikaruga official-port 4× sound-trim precedent comfortably covers 2.958×) — but note the
title would then score with main 1.389× and VRAM 1.196× both over their 1× caps and
`awkward` controls, i.e. a low-tier score, not a port candidate. Reproduction of any
future run requires `airlbios.zip` alongside the game zip (§3).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment; first run parked `G1 broken: emulator-exited` — dedicated `airlbios` BIOS set (epr-21801/21802) missing; installed and re-ran clean |
