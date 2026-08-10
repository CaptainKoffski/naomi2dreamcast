# Cyber Troopers Virtual-On: Oratorio Tangram M.S.B.S. ver 5.66 2000 Edition (`vonot`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,855,262 B → utilization **3.746** — the **new maximum of the parked ARAM cohort** (previous max `sstrkfgt` 3.687). Both other regions FIT: main `nz_total` u ≈ 0.809, VRAM (content + 2×fb) u ≈ 0.740 — ARAM is the *sole* blocker (`ausfache`-class profile). But this title is the campaign's strongest gate counter-evidence, stronger even than the `ikaruga` precedent (kb §6 item 1): **the same game received an official Dreamcast port (ver 5.45, Sega, JP 1999-12-09) that shipped inside the DC's 2 MiB ARAM** — and the NAOMI cart *itself* carries the DC-port codebase (Katana SDK strings, `M.S.B.S.VER.5.45`, VMU save `VOORATAN.SYS`, literal "Twin Stick" / "?Dreamcast Controller" strings in `guts.sdk_strings`). Controls on-ladder: `dc_peripheral` — the official DC Twin Stick (HKT-7500) was released *for this game*. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `vonot` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10973, sole set `/* 0028 */`) |
| Maker / year | Sega, 2000 (MAME `GAME()` row; title screen `shot-487s.png`: "©SEGA 1998, 2000", "M.S.B.S.Ver.5.66 — 2000 EDITION") |
| Genre / format | Twin-stick 3D mecha (Virtuaroid) one-on-one fighter, **cart**, 91.6 MB (`GAME_FORMATS.md`) |
| Official DC port | **Yes — earlier revision.** Ver 5.4/5.45 ported to Dreamcast: Japan 1999-12-09 (Sega), NA 2000-06-07 (Activision) ([Wikipedia](https://en.wikipedia.org/wiki/Cyber_Troopers_Virtual-On_Oratorio_Tangram)). The NAOMI *ver 5.66* assessed here is a **later revision** than the DC port's 5.45; this exact 5.66 build was ported to Xbox 360 (XBLA) 2009-04-29, not DC (same source; `GAME_FORMATS.md` note already records this nuance). |
| Community ports | Not needed — an official DC port exists (of ver 5.45); no community DC port of 5.66 found (searched 2026-08-11). |
| Representative choice | Sole set of the family — no clones in MAME. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/vonot.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). Live attract-demo combat is already on screen at the *first* shot: `shot-060s.png`
(two Virtuaroids fighting in a 3D arena, FREE PLAY overlay), `shot-548s.png` and `shot-609s.png` show
further demo combat/segments, `shot-121s.png` a "TODAY'S BEST PILOTS" ranking screen, `shot-304s.png`
the "PRESENTED BY SEGA" splash (loop restart), `shot-365s.png`/`shot-426s.png` an attract tutorial
that **renders the twin-stick controller pair on-screen** with per-stick move labels (右ターボ＋右トリガー /
前進), and `shot-487s.png` the title screen confirming the exact revision: "M.S.B.S.Ver.5.66 — 2000
EDITION". The park is unambiguously the game running, not tooling.
Screenshots: `evidence/vonot/shot-060s.png` · `shot-182s.png` · `shot-365s.png` · `shot-487s.png` ·
`shot-548s.png`
Anomalies: none operationally. Two curiosities worth recording: (1) the attract demo at `shot-182s.png`
shows a Virtuaroid with a **Dreamcast console and swirl logo rendered on its body** — the 2000 Edition's
DC tie-in content, in the arcade attract itself; (2) `guts.sdk_strings` contains Dreamcast (Katana) SDK
library strings (`RMC ... SEGA SEGAKATANA`, `bu Ver 1.47 ... VMS File System`, `?Dreamcast Controller`,
`Twin Stick`, `VOORATAN.SYS` VMU-save filenames, and the literal `M.S.B.S.VER.5.45` string) — the NAOMI
5.66 build visibly shares the DC-port codebase. `shot-121s.png`, `shot-243s.png`, `shot-304s.png`,
`shot-426s.png`, `shot-609s.png` curated out as redundant (ranking/close-up/splash/duplicate-tutorial/
duplicate-demo).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,855,262 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.746** — past `region_score()`'s `u > 2.0` gate and the **new maximum of the
parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `takoron` 2.997, `inunoos` 3.206,
`ninjaslt` 3.341, `pokasuka` 3.368, `mazan` 3.483, `mok` 3.558, `ringout` 3.684, `sstrkfgt`
3.687, `vonot` **3.746**. `nz_above_cap` = 5,884,724 B (address-keyed placement figure,
informational). Address peak 8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 13,565,606 | 16,777,216 | **0.809** | `nz_total` — clears the 1× cap; `nz_above_cap` (address-placement) 3,097,384 B · `dma_high_water` 20,828,416 B (u 1.241) · watermark 28,704,768 B (u 1.711) — both moot, content fits |
| VRAM (content volume + 2×fb) | 6,207,304 | 8,388,608 | **0.740** | `content_total` 4,978,504 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — clears the 1× cap; raw `nz_total` 5,487,138 (u 0.654) · address peak 14,024,704 (u 1.672) |
| ARAM (content volume) | 7,855,262 | 2,097,152 | **3.746** | the gate — see above |

Streaming context: 21 DMA events · 6,492,160 B total · 6,338,560 B unique · re-read ratio 0.0237 ·
steady-state 0.019 MB/min (`short_window: false`) · `pio_bytes` 79,357,952 B (PIO-loading cart).
Guts: carve 28,573,696 B (`carve_meta.title = "VIRTUAL-ON ORATORIO TANGRAM"`) · 1,140 functions ·
MMIO refs rtc 3 / g2ext 26 / scif 2 · flags `eeprom_bios`/`serial`/`rtc`/`code_over_4mb`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `dc_peripheral`):** twin-stick cabinet, but an *all-digital*
one: each stick is a 4-way digital lever with trigger + turbo. MAME assigns the **generic** `naomi`
input port set (`GAME( 2000, vonot, naomi, naomim2, naomi, ... )`, src/mame/sega/naomi.cpp @59e7c0b
line 10973) — consistent, since the twin-stick layout fits standard JVS digital bits. Flycast's own
source carries a **dedicated descriptor** `vonot_inputs` (core/hw/naomi/naomi_roms_input.h:274):
L UP/DOWN/LEFT/RIGHT + L TRIGGER/L TURBO + QM, with the right stick mapped onto P2 digital inputs
(R TRIGGER/R TURBO/R UP/DOWN/LEFT/RIGHT) — primary-source confirmation of the twin-stick scheme,
corroborated in-game by the attract tutorial rendering the stick pair (`shot-365s.png`,
`shot-426s.png`). The DC-peripheral lineage is *proven, not proposed*: Sega released the official
**DC Twin Stick (HKT-7500) on 1999-12-09 specifically for the DC Oratorio Tangram release**
([Giant Bomb](https://www.giantbomb.com/dreamcast-twin-stick/3000-100/)), and the DC port supported
both the standard controller and Twin Sticks — the cart's own `sdk_strings` list both device names
(`?Dreamcast Controller`, `Twin Stick`). `controls.device_class = dc_peripheral` — on-ladder, so
controls do not gate and would not gate G2 if ARAM cleared. Proposed DC mapping: exactly the shipped
1999 one — Twin Stick pair 1:1, or the DC pad scheme the official port shipped.
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp GAME() row · Flycast
`vonot_inputs` · [Wikipedia](https://en.wikipedia.org/wiki/Cyber_Troopers_Virtual-On_Oratorio_Tangram) ·
[Giant Bomb HKT-7500](https://www.giantbomb.com/dreamcast-twin-stick/3000-100/) · attract-tutorial
screenshots · cart `sdk_strings`.

**What would unblock it — and why this is the strongest counter-evidence yet for kb §6 item 1:**
the G3-ARAM softening argument has until now rested on *analogous* precedent (Ikaruga's official
2002 DC port shipped inside 2 MiB despite the Naomi image's 4× full-bank load). `vonot` upgrades
that to **same-title precedent**: Sega's official Dreamcast port of Oratorio Tangram (ver 5.45,
JP 1999-12-09 / NA 2000-06-07) shipped and ran inside the DC's real 2 MiB AICA RAM — a released
product proving the sound trim for *this very game* is achievable, with the NAOMI build itself
carrying the DC-port code (Katana SDK/VMU strings above). The honest nuance: the DC port is ver
5.45, an **earlier revision** than this NAOMI-exclusive 5.66 (5.66 adds balance/content later
ported to Xbox 360 XBLA in 2009, not DC) — so the precedent proves the sound budget, not a
byte-for-byte 5.66 port. With main 0.809× and VRAM 0.740× both fitting and controls on-ladder
with shipped DC-peripheral lineage, ARAM is the *only* blocker; under any softer ARAM rule
(kb §6 item 1's candidate fixes) `vonot` unparks immediately, ahead of `ausfache` (no port
exists anywhere) and `radirgyn` (franchise-only precedent) as the queue's #1 unpark candidate.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.746 new cohort max, main/VRAM both fit; same-title official DC port (ver 5.45, 1999) makes this the strongest kb §6 item-1 unpark candidate; controls dc_peripheral (DC Twin Stick HKT-7500 lineage) |
