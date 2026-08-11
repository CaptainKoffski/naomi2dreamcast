# Spikers Battle (`spkrbtl`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,035,646 B → utilization **3.355** — mid-pack in the 23-title parked ARAM cohort (10th, between `ninjaslt` 3.341 and `pokasuka` 3.368). Not a sole blocker: main content u ≈ 1.118 and VRAM content+2×fb u ≈ 1.155 also exceed 1× (no gate, would score ≈64/≈57), so even a softened ARAM rule (kb §6 item 1) unparks it into the mid-low memory band. Controls on-ladder: `stick` — 1 lever + 4 buttons (Beat/Charge/Jump/Shift, the Spikeout panel), a native fit for the DC pad's 4 face buttons. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `spkrbtl` (no clones — MAME machine `naomigd`, parent set; `tools/assess/out/controls.json`) |
| Maker / year | Sega (developed by Amusement Vision — attract runs the AV logo, `evidence` shot at 243 s pre-curation, and move strings are Spikeout-derived `SPK_*`, `guts.sdk_strings`), 2001 |
| Genre / format | 3D street brawler / versus fighter on the Spikeout engine (1–2 players), **GD-ROM** GDS-0005, 147.3 MB (`GAME_FORMATS.md`). NOT beach volleyball — QUEUE.md's "Sports" label is a mix-up with *Beach Spikers* (a different, Naomi 2 title); see [lunatic obscurity review](http://lunaticobscurity.blogspot.com/2019/04/spikers-battle-arcade.html) ("a beat em up that thinks it's a fighting game") |
| Official DC port | **No** — Naomi exclusive, never released on any console; the Spikeout series only ever reached Xbox (Spikeout: Battle Street, 2005) ([The Dreamcast Junkyard Naomi articles](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html), [lunatic obscurity](http://lunaticobscurity.blogspot.com/2019/04/spikers-battle-arcade.html)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/spkrbtl.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). No static pre-game screen at all: the first shot post-handoff is already the
attract demo (`shot-060s.png`, title logo over 3D demo combat on the street basketball court with
PRESS START BUTTON / FREE PLAY overlays), and the cycle loops through the TOP SPIKERS ranking table
(`shot-121s.png`), and HOW TO PLAY tutorial pages that render the cab's lever-ball + 4-button panel
graphic on screen (`shot-182s.png`, `shot-304s.png` grab/throw page, `shot-609s.png` charge-attack
page). The park is unambiguously the game running its attract cycle, not tooling.
Screenshots: `evidence/spkrbtl/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-304s.png` · `shot-609s.png`
Anomalies: none in the run. One metadata note: the queue genre cell ("Sports") and the
beach-volleyball shorthand are wrong for this title — it is the Spikeout-lineage brawler (§2).
`shot-243s.png` (Amusement Vision logo card), `shot-365s.png`, `shot-426s.png`, `shot-487s.png`,
`shot-548s.png` curated out (logo card / additional demo-loop frames).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,035,646 B`
(fill-excluded content volume, kb §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.355** — past `region_score()`'s `u > 2.0` gate, 10th of the 23-title parked
ARAM cohort, between `ninjaslt` 3.341 and `pokasuka` 3.368 (cohort recomputed from all G3-aram
sidecars' `content_total`, 2026-08-11; extremes `toyfight` 2.035 … `slashout` 3.756).
`nz_above_cap` = 5,034,032 B (address-keyed placement figure, informational). Address peak
8,257,552 B (u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar (ARAM gates first in `score.py`'s region walk
regardless) — **both also exceed 1× here**, the multi-region profile (`alienfnt`, `slashout`),
not the sole-blocker one (`vonot`, `ausfache`):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 18,761,818 | 16,777,216 | **1.118** | `nz_total` — over the 1× cap, under the 2× gate (would score ≈64); `nz_above_cap` (address-placement) 10,085,670 B · `dma_high_water` 28,311,552 B (u 1.688) · watermark 32,801,248 B (u 1.955) |
| VRAM (content volume + 2×fb) | 9,684,749 | 8,388,608 | **1.155** | `content_total` 8,455,949 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over the cap, under the gate (would score ≈57); raw `nz_total` 9,055,412 (u 1.079) · address peak 15,462,400 (u 1.843) |
| ARAM (content volume) | 7,035,646 | 2,097,152 | **3.355** | the gate — see above |

Streaming context: 36 DMA events · 21,110,784 B total · 21,110,784 B unique · re-read ratio
0.0 · steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 6,714,688 B — a pure
load-once profile: the GD-ROM front-loads ~20 MB and never re-reads during attract.
Guts: carve 33,423,360 B (`carve_meta.title = "SPIKERS BATTLE JAPAN VERSION"`, flag
`code_over_4mb`) · 1,434 functions · MMIO refs rtc 2 / g2ext 158 / scif 2 · flags
`eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (on-ladder, does not gate — `stick`):** standard 1-lever + 4-pushbutton panel.
Primary sources: Flycast carries a dedicated descriptor `spkrbtl_inputs =
INPUT_4_BUTTONS("BEAT", "CHARGE", "JUMP", "SHIFT")` bound to `gds-0005`
(core/hw/naomi/naomi_roms_input.h:558, naomi_roms.cpp:5870); MAME assigns the generic `naomi`
INPUT_PORTS set (machine `naomigd`, src/mame/sega/naomi.cpp @59e7c0b via
`tools/assess/out/controls.json`). The game's own attract HOW TO PLAY pages render the panel —
lever ball + 4 colored buttons — on screen: `evidence/spkrbtl/shot-182s.png` (charge-attack
page), `shot-304s.png` (grab/throw: "push the lever toward the opponent"), `shot-609s.png`.
Corroboration: [Arcade History GDS-0005 page](https://www.arcade-history.com/?n=spikers-battle-model-gds-0005&page=detail&id=4086)
(8-way joystick) and the series scheme in the
[GameFAQs SpikeOut mini-FAQ](https://gamefaqs.gamespot.com/arcade/574616-spikeout/faqs/414)
(Beat/Charge/Jump/Shift roles). `controls.device_class = stick` — 4 buttons map 1:1 onto the
DC pad's A/B/X/Y with the analog stick/d-pad as the lever; would not gate G2 if ARAM cleared.

**What would unblock it:** ARAM gate softening — kb §6 item 1 (the 2× multiple may be too
aggressive; checkpoint ruling pending — Ikaruga's official DC port proved a 4× sound trim is
achievable). Caveat: main (1.118) and VRAM (1.155) also exceed capacity, so under a softer rule
it unparks into the **mid-low memory band (≈57 VRAM-bounded)**, not a comfortable fit — a real
port would need sound *and* modest texture/main trims. As a mid-cohort ARAM offender with both
other regions barely over 1×, it sits ahead of the deep-cohort titles (`slashout`, `vonot`) but
behind the sole-blocker candidates (`ausfache`, `radirgyn`) in unpark priority.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.355 (10th of 23 G3-aram cohort); main 1.118/VRAM 1.155 also over 1× (no gate); no DC port (Naomi exclusive); controls stick (lever + Beat/Charge/Jump/Shift, DC-pad-native); genre note: Spikeout-lineage brawler, not volleyball |
