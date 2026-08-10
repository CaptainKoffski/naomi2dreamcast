# Sega Strike Fighter (Rev A) (`sstrkfgt`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | A heavy sound bank parks it on first assessment: `content_total` = 7,732,473 B of fill-excluded ARAM content, **3.687×** the DC's 2 MiB AICA RAM — the highest ARAM utilization measured yet in the campaign's parked cohort (above takoron 2.997, inunoos 3.206, and pokasuka 3.368). Main RAM clears its own cap under content-volume keying (`nz_total` u ≈ 0.970) but VRAM does not: `content_total` + 2×`fb_bytes` = 9,285,394 B, u ≈ 1.107 — over its 1x line (unlike takoron/inunoos/pokasuka, which all cleared VRAM). Controls are a genuine plus: the cabinet's 4 analog flight axes (control-wheel elevator/aileron, rudder pedal, throttle) map 1:1 onto a DC pad's stick + analog triggers, so `controls.device_class = pad_adaptable` — on-ladder, not a gate. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `sstrkfgt` (covers: clone `sstrkfgta` "no training mode" — MAME src/mame/sega/naomi.cpp @59e7c0b GAME lines 10977–10978; `parent: null`/self-keyed in controls.json, `sstrkfgt` is the MAME parent) |
| Maker / year | Sega, 2000 (GAME line: `/* 0035 */`; ROM_START comment `840-0035 2000 317-0281-COM Naomi`) |
| Genre / format | Flight combat (jet fighter sim — GAME_FORMATS.md's "Fighting" queue label is a genre-taxonomy artifact, not accurate; the game is a first-person flight-combat shooter, confirmed by attract-demo cockpit HUD footage, §3), **cart** — 840-0035, boot ROM + 20×64 Mb, 75.9 MB |
| Official DC port | No (GAME_FORMATS.md: "No") |
| Community ports | None found (searched 2026-08-10) |
| Representative choice | MAME parent (`sstrkfgt`); the only other family member, `sstrkfgta`, is a "no training mode" variant of the same ROM set, not a distinct release |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/sstrkfgt.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). The full attract loop cycles through narrative setup
("OPERATION DESERT FIRE" briefing text, `shot-060s.png`), a "FIGHTER AIRCRAFT" reference
roster (`shot-121s.png`), **live in-cockpit HUD flight footage** over city and mountain
terrain with a working radar/targeting overlay (locked "TG" target boxes, ammo/altitude
readouts, `shot-182s.png` and `shot-365s.png`), the title logo (`shot-243s.png` /
`shot-426s.png`), a pilot-helmet cutscene close-up (`shot-487s.png`), and a jet
fly-by/weapons showcase (`shot-548s.png`) — genuine attract-demo gameplay, not a frozen
frame or idle settings prompt.
Screenshots: `evidence/sstrkfgt/shot-060s.png` · `shot-182s.png` · `shot-365s.png` ·
`shot-426s.png` · `shot-548s.png`
Anomalies: none. `shot-304s.png` (a near-blank fade transition) was curated out for
readability, same class as the fade-transition frames trimmed from `inunoos`/`pokasuka`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,732,473 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.687** — well past `region_score()`'s `u > 2.0` gate, and the highest ARAM
figure yet recorded among this campaign's parked ARAM titles: takoron 2.997, inunoos
3.206, pokasuka 3.368, sstrkfgt **3.687**. This is *not* inside the kb §6 item-1 empty
band (scored max 1.962, parked min 2.997) — it sits well above the parked minimum,
extending the top of the already-parked cluster rather than filling the gap; still a
useful new data point for the eventual checkpoint. `nz_above_cap` = 5,738,158 B of
content above the cap (address-keyed placement figure, informational). Address peak is
8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in
`score.py`'s region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 16,270,883 | 16,777,216 | **0.970** | `nz_total` — clears the 1x cap, just under the line; `nz_above_cap` (address-placement) 2,555,672 B · `dma_high_water` 28,398,720 B (u 1.693, old address-peak read) |
| VRAM (content volume + 2×fb) | 9,285,394 | 8,388,608 | **1.107** | `content_total` 8,056,594 + 2×`fb_bytes` (2×614,400, the standard double-buffered 640×480×2 constant, per `score.py`'s `vram_ct + 2*vram_fb` formula) — **over** the 1x cap, unlike `takoron`/`inunoos`/`pokasuka`, all of which cleared VRAM under this same keying; raw `nz_total` 8,658,642 · `nz_above_cap` 7,638,880 (address-keyed) |
| ARAM (content volume) | 7,732,473 | 2,097,152 | **3.687** | the gate — see above |

Streaming context: 32,367 DMA events · 93.8 MB total · 36.0 MB unique · re-read ratio
0.6163 · steady-state 8.115 MB/min (`short_window: false`) · `pio_bytes` 2,679,572 B.
Guts: code 2,433,024 B (2.32 MiB, under the 4 MiB `code_over_4mb` threshold) · 2,128
functions · MMIO refs rtc 2 / g2ext 231 / scif 2 · flags `eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

Evidence: `assessments/sstrkfgt.metrics.json` → `memory.aram`; `guts.sdk_strings` shows
extensive 3D asset-name tables (`o_f18sh01aaf`, `o_nimitz_option_a`, hundreds of
`h_*_PX2Z` HUD/dialogue-string entries) consistent with a large streamed sound/voice
bank for the mission-briefing and radio-chatter content visible in the attract demo.

**Controls would not gate, and would only moderately penalize, if ARAM were ever
solved.** Researched (≥2 sources): the cabinet is a dedicated flight cockpit — control
wheel/yoke (pitch + roll), rudder pedals (yaw), and a throttle lever, plus Gun
Trigger/Missile/Air Break/View Change buttons (MAME src/mame/sega/naomi.cpp @59e7c0b
`INPUT_PORTS_START( sstrkfgt )`, `PORT_INCLUDE( alpilota )` — the Airline Pilots
deluxe-cabinet I/O design, lightly modified); corroborated by
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sstrkfgt)
("Stick" input device, 4 buttons, 1 player) and
[hardcoregaming101](http://www.hardcoregaming101.net/sega-strike-fighter/) (three-screen
sit-down cockpit, a dedicated strafe pedal). Unlike `alpilota`'s full deluxe rig (dual
L/R thrust levers on A4/A5), `sstrkfgt`'s `PORT_MODIFY` zeroes A4/A5 and adds a single
combined Thrust Lever on A2 — exactly **4 analog axes total** (A0 elevator, A1 aileron,
A2 throttle, A3 rudder), which is exactly the analog-channel count a stock DC pad
offers (stick X/Y + two analog triggers): stick = aileron/elevator, L-trigger =
throttle, R-trigger = rudder, face buttons = gun/missile/air-brake/view-change. The
axis count matches 1:1, no signal is dropped or degraded the way it would be for a
truly off-ladder device (card reader, medal hopper, mandatory multi-cabinet — none of
which apply here) — so `controls.device_class = pad_adaptable` (50.0 on the
`score.py:108` ladder), not `awkward` and not an off-ladder raw hardware name. If ARAM
ever cleared, controls would still cap the axis at 50.0 (the ladder's middle rung), a
real but moderate penalty, not a G2 gate.

What would unblock it: ARAM content would need to shrink below the 2× cap — realistically
a sample-rate reduction or streaming redesign for the mission-briefing/radio-chatter
sound bank (per-title audio trim has released-port precedent, e.g. the official Ikaruga
DC port's 4× sound trim, kb §4.d, though no guarantee of enough headroom at 3.687×, the
largest cut needed in the campaign's parked cohort so far). VRAM would also need to
come down from its 1.107× line for a full clear, though it does not gate on its own.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — fighter cohort (queue genre label; actually flight combat), fresh v9 capture |
