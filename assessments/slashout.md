# Slashout (`slashout`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,877,200 B → utilization **3.756** — the **new maximum of the parked ARAM cohort**, edging past `vonot`'s 3.746. Not a sole blocker: main content u ≈ 1.173 and VRAM content+2×fb u ≈ 1.414 also exceed 1× (low score band, no gate), so even a softened ARAM rule (kb §6 item 1) unparks it into the low memory band, not a comfortable fit. Controls on-ladder: `stick` — 1 lever + 4 buttons (Blade/Charge/Jump/Shift), a native fit for the DC pad's 4 face buttons. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `slashout` (no clones — MAME machine `naomigd`, parent set; `tools/assess/out/controls.json`) |
| Maker / year | Sega (developed by Amusement Vision — Spikeout lineage; credits carve lists Toshihiro Nagoshi under SPECIAL THANKS, `guts.sdk_strings`), 2000 |
| Genre / format | 3D fantasy weapons brawler (Spikeout spin-off, 1–4 players), **GD-ROM** GDS-0004, 137.4 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — Naomi exclusive, never released on any console ([The Dreamcast Junkyard Naomi-exclusives article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html), [RetroGameTalk](https://retrogametalk.com/threads/slashout-arcade-naomi.18636/)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/slashout.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). No static pre-game screen at all: the first shot post-handoff is already the
attract gameplay demo (`shot-060s.png`, 3D character in the town square with PRESS START BUTTON /
FREE PLAY overlays), and the full attract cycle loops through the title card (`shot-304s.png`,
`shot-487s.png`), HOW TO PLAY control tutorials showing the cab's lever + 4-button panel graphic
(`shot-182s.png` charge-magic page, `shot-426s.png` "レバーで移動" movement page), and more demo
combat (`shot-609s.png` with a "SLASH" hit callout). The park is unambiguously the game running its
attract cycle, not tooling.
Screenshots: `evidence/slashout/shot-060s.png` · `shot-182s.png` · `shot-304s.png` ·
`shot-426s.png` · `shot-609s.png`
Anomalies: none. `shot-121s.png`, `shot-243s.png`, `shot-365s.png`, `shot-487s.png` (duplicate
title), `shot-548s.png` curated out (additional demo-loop frames).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,877,200 B`
(fill-excluded content volume, kb §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.756** — past `region_score()`'s `u > 2.0` gate and the **new maximum of the
15-title parked ARAM cohort**: `toyfight` 2.035, `tduno2` 2.615, `asndynmt` 2.782, `takoron`
2.997, `inunoos` 3.206, `ninjaslt` 3.341, `pokasuka` 3.368, `mazan` 3.483, `mok` 3.558,
`monkeyba` 3.637, `ringout` 3.684, `sstrkfgt` 3.687, `alienfnt` 3.702, `vonot` 3.746,
`slashout` **3.756** (recomputed from all G3-aram sidecars' `content_total`, 2026-08-11).
`nz_above_cap` = 5,873,367 B (address-keyed placement figure, informational). Address peak
8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — **both also exceed 1× here**, the multi-region profile (`alienfnt`), not the
sole-blocker one (`vonot`, `ausfache`):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 19,680,341 | 16,777,216 | **1.173** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈54); `nz_above_cap` (address-placement) 13,454,436 B · `dma_high_water` 28,335,840 B (u 1.689) · watermark 32,277,280 B (u 1.924) |
| VRAM (content volume + 2×fb) | 11,858,397 | 8,388,608 | **1.414** | `content_total` 10,629,597 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over the cap, under the gate (would score ≈33); raw `nz_total` 11,795,021 (u 1.406) · address peak 16,551,936 (u 1.973) |
| ARAM (content volume) | 7,877,200 | 2,097,152 | **3.756** | the gate — see above |

Streaming context: 29 DMA events · 20,470,848 B total · 20,470,848 B unique · re-read ratio
0.0 · steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 5,535,040 B — a pure
load-once profile: the GD-ROM front-loads ~19.5 MB and never re-reads during attract.
Guts: carve 32,243,712 B (`carve_meta.title = "SLASHOUT JAPAN VERSION"`, flag `code_over_4mb`) ·
1,491 functions · MMIO refs rtc 2 / g2ext 191 / scif 2 · flags `eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `stick`):** standard 1-lever + 4-pushbutton panel.
Primary sources: Flycast carries a dedicated descriptor `slashout_inputs =
INPUT_4_BUTTONS("Blade", "Charge", "Jump", "Shift")` bound to `gds-0004`
(core/hw/naomi/naomi_roms_input.h:319, naomi_roms.cpp:5854); MAME assigns the generic `naomi`
INPUT_PORTS set (machine `naomigd`, src/mame/sega/naomi.cpp @59e7c0b via
`tools/assess/out/controls.json`). The game's own attract HOW TO PLAY pages show the panel
graphic — lever + 4 buttons — on screen: `evidence/slashout/shot-426s.png` ("レバーで移動" =
move with the lever) and `shot-182s.png` (charge-button magic tutorial). Corroboration:
[GameFAQs Slash Out guide](https://gamefaqs.gamespot.com/arcade/581529-slash-out/faqs/13766)
describes the Blade/Charge/Jump/Shift button roles. `controls.device_class = stick` — 4 buttons
map 1:1 onto the DC pad's A/B/X/Y with the analog stick/d-pad as the lever; would not gate G2
if ARAM cleared.

**What would unblock it:** ARAM gate softening — kb §6 item 1 (the 2× multiple may be too
aggressive; checkpoint ruling pending). Two honest caveats: (1) at u 3.756 `slashout` is the
single worst ARAM offender measured so far, so any threshold soft enough to admit it admits the
entire cohort; (2) main (1.173) and VRAM (1.414) also exceed capacity, so under a softer rule it
unparks into the **low memory band (≈33 VRAM-bounded)**, not a comfortable fit — a real port
would need sound *and* texture trims. Unpark priority sits behind the sole-blocker candidates
(`ausfache`, `radirgyn`, `vonot`).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.756 new cohort max (past vonot 3.746); main 1.173/VRAM 1.414 also over 1× (no gate); no DC port (Naomi exclusive); controls stick (lever + Blade/Charge/Jump/Shift, DC-pad-native) |
