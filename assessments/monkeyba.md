# Monkey Ball (GDS-0008) (`monkeyba`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,626,335 B → utilization **3.637** — mid-pack in the parked ARAM cohort (between `mok` 3.558 and `ringout` 3.684). The other two regions FIT under the current content keying: main `nz_total` u ≈ 0.572, VRAM (content + 2×fb) u ≈ 0.906 — ARAM is the *sole* blocker (`ausfache`/`vonot`-class profile). Strong unpark evidence for kb §6 item 1: the game shipped months later as GameCube launch title *Super Monkey Ball* (pad/analog-native, controls precedent, not an ARAM precedent), and an **active 2026 community Dreamcast port** (Memorix101, built from the GC decompilation) already has beginner courses running on real DC — the game demonstrably fits the platform once assets are re-authored. Controls on-ladder: `pad_adaptable` — the cab's sole control is one analog stick (banana-shaped), 1:1 onto a DC pad's analog stick. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `monkeyba` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b, sole set `/* 0008 */`, single ROM_START) |
| Maker / year | Sega / Amusement Vision, 2001 (MAME `GAME()` row; on-screen "© AMUSEMENT VISION, LTD./SEGA,2001", `shot-060s.png`) |
| Genre / format | Action (tilt-the-floor ball-rolling), **GD-ROM** (GDS-0008, 82.5 MB) |
| Official DC port | No — after the Dreamcast's early-2001 discontinuation the enhanced version shipped as **GameCube launch title *Super Monkey Ball* (2001)** instead ([Wikipedia](https://en.wikipedia.org/wiki/Super_Monkey_Ball_(video_game))) |
| Community ports | **Yes, in progress (2026)** — Memorix101 is porting Monkey Ball to Dreamcast using assets from the decompiled GameCube *Super Monkey Ball*; beginner courses + extra levels shown running on DC, playable build circulated to press, not yet publicly released ([Dreamcast Junkyard, 2026-07](https://www.thedreamcastjunkyard.co.uk/2026/07/super-monkey-ball-is-getting-ported-to.html); [Time Extension, 2026-07](https://www.timeextension.com/news/2026/07/25-years-after-its-original-release-this-homebrew-developer-is-bringing-arcade-monkey-ball-to-the-sega-dreamcast); [dreamcast-talk thread](https://www.dreamcast-talk.com/forum/viewtopic.php?t=16352)) |
| Representative choice | Sole set of the family — no clones in MAME. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`, GD DIMM ~1 MB bootstrap) · run 600 s · rom: `naomi/monkeyba.zip` (single clean leg, `ran full window`)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after screenshot review). The attract loop cycles: balloon intro (`shot-060s.png`), the そうさせつめい/HOW TO PLAY demo with the monkey rolling under lever instructions (`shot-121s.png`), a BEGINNER MODE goal celebration with confetti (`shot-182s.png`), and live attract gameplay with full HUD — MONKEY BALL logo, TIME 058, BANANA 000/100 (`shot-365s.png`). The park is unambiguously the game running, not tooling.
Screenshots: `evidence/monkeyba/shot-060s.png` · `shot-121s.png` · `shot-182s.png` · `shot-365s.png`
Anomalies: none. (`shot-426s.png`/`shot-487s.png`/`shot-609s.png` were near-black attract-transition frames; curated out with the redundant `shot-243s.png`/`shot-304s.png`/`shot-548s.png`.)

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,626,335 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.637** — past `region_score()`'s `u > 2.0` gate, slotting mid-pack in the
parked ARAM cohort: `toyfight` 2.035, `tduno2` 2.615, `takoron` 2.997, `inunoos` 3.206,
`ninjaslt` 3.341, `pokasuka` 3.368, `mazan` 3.483, `mok` 3.558, **`monkeyba` 3.637**,
`ringout` 3.684, `sstrkfgt` 3.687, `alienfnt` 3.702, `vonot` 3.746.
`nz_above_cap` = 5,629,400 B (address-keyed placement figure, informational).
Address peak 8,323,024 B (u 3.969, pre-volume-keying read).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 9,591,300 | 16,777,216 | **0.572** | `nz_total` — clears the 1× cap comfortably; `nz_above_cap` (address-placement) 6,868,941 B · `dma_high_water` 31,458,328 B (u 1.875, ~30 MiB — the GD stream-cache-placement pattern, kb §6 item 3) · watermark 31,458,325 B — moot, content fits |
| VRAM (content volume + 2×fb) | 7,602,567 | 8,388,608 | **0.906** | `content_total` 6,373,767 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — clears the 1× cap; raw `nz_total` 6,811,695 · address peak 16,764,928 (u 1.999) — placement artifact, content fits |
| ARAM (content volume) | 7,626,335 | 2,097,152 | **3.637** | the gate — see above |

Streaming context: 13,615 DMA events · 46,748,048 B total · 22,955,064 B unique · re-read
ratio 0.509 · steady-state 3.409 MB/min (`short_window: false`) · `pio_bytes` 4,459,976 B.
Guts: code 3,145,728 B (`carve_meta.title = "MONKEY BALL JAPAN VERSION"`) · 1,469 functions ·
MMIO refs rtc 4 / g2ext 99 / scif 2 · flags `eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `pad_adaptable`):** the cabinet's only game control is a
single **banana-shaped analog joystick** — no buttons besides Start. MAME's dedicated
`monkeyba` input ports declare exactly START1 + `IPT_AD_STICK_X`/`IPT_AD_STICK_Y` (one 2-axis
analog stick), src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `monkeyba`;
[arcadeitalia](https://adb.arcadeitalia.net/dettaglio_mame.php?game_name=monkeyba) concurs
(analog joystick, 0 buttons, 1P with 2–4 alternating);
[Wikipedia](https://en.wikipedia.org/wiki/Super_Monkey_Ball_(video_game)) documents the
"distinctive banana-shaped analog stick"; the binary itself corroborates
(`guts.sdk_strings`: "Please rotate the joystick a few times and then release." calibration,
INPUT TEST ANALOG1–8 + START, "Move towards direction joystick is pressed").
Proposed DC mapping: DC pad analog stick 1:1 + Start — the adaptation is *shipped precedent*:
GameCube *Super Monkey Ball* (2001 launch title) is this game on a controller analog stick.
`controls.device_class = pad_adaptable` — on-ladder, would not gate G2 if ARAM cleared.
Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp INPUT_PORTS ·
arcadeitalia · Wikipedia (Super Monkey Ball) · in-binary INPUT TEST/calibration strings.

**What would unblock it:** ARAM gate softening (kb §6 item 1). The profile is the strong-unpark
shape: ARAM is the *sole* over-budget region (main 0.572, VRAM 0.906 both fit), controls are
on-ladder with shipped pad precedent. The kb §6 item-1 argument applies at two levels here —
*controls/gameplay* precedent from GC *Super Monkey Ball* (same gameplay, pad-native, months
after the arcade release; an adaptation precedent, **not** an ARAM precedent — the GC has its
own audio RAM budget), and *platform-fit* evidence from the 2026 Memorix101 community DC port,
which sidesteps the Naomi image's 8 MiB sound bank entirely by rebuilding from the GC
decompilation with re-authored assets and already runs beginner courses on real DC hardware.
Neither proves the Naomi image's 7.6 MB ARAM content trims into 2 MiB (the Ikaruga 4× trim,
kb §4.d, remains the released-port precedent for that kind of work) — but under any softer
ARAM rule (item 1's candidate fixes) `monkeyba` unparks with the `ausfache`/`radirgyn` group.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.637 sole over-budget region (main 0.572/VRAM 0.906 fit); GC *Super Monkey Ball* (2001) is the pad-adaptation precedent and an active 2026 community DC port (GC-decomp rebuild) is platform-fit evidence for kb §6 item 1; controls pad_adaptable (single banana analog stick) |
