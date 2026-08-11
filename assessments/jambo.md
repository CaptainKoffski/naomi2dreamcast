# Jambo! Safari (Rev A) (`jambo`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The safari soundscape parks it: `content_total` = 7,272,582 B of fill-excluded ARAM content, **3.468×** the DC's 2 MiB AICA RAM — mid-pack in the parked ARAM cohort, between pokasuka (3.368) and mazan (3.483). The `guts.sdk_strings` table shows why: hundreds of named sample slots (per-animal voice banks `SND_SEB_SE_ANIMAL_2_*` for lion/elephant/leopard/rhino/zebra…, per-surface tire/engine loops, rope/lasso SEs, 30+ song/jingle bank entries). Both other regions are also over their 1× lines under content keying (main u 1.398, VRAM u 1.131) though neither gates. Controls are the bright spot: a standard Sega wheel + 2-pedal + shift-lever driving cab, `device_class = dc_peripheral` — same class as Crazy Taxi/18 Wheeler, which both shipped on DC; the Flycast fork even ships a ready `jambo_inputs` DC-pad mapping. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `jambo` (no clones — single `GAME(` line in MAME src/mame/sega/naomi.cpp @59e7c0b, line 10952) |
| Maker / year | Sega, 1999 (GAME line `/* 0013 */`; cart 840-0013, `epr-22826a.ic22`) |
| Genre / format | Safari driving / animal-catching (drive a jeep, lasso animals — QUEUE's "Sports" label is a genre-taxonomy artifact), **cart**, 31.7 MB |
| Official DC port | **No — reported, never released.** [Wikipedia](https://en.wikipedia.org/wiki/Jambo!_Safari): the UK Official Dreamcast Magazine reported a 3-in-1 "Real Life Career Series" DC compilation (with Brave Firefighters and Emergency Call Ambulance) that never shipped. Added to GAME_FORMATS.md's cancelled-but-unreleased near-miss list this assessment. |
| Community ports | None found (searched 2026-08-11). Later-platform precedent instead: Sega released *Jambo! Safari: Animal Rescue* for **Wii and NDS on 2009-11-17** (Full Fat) — the game demonstrably adapts off its cab onto pad/motion controls ([Wikipedia](https://en.wikipedia.org/wiki/Jambo!_Safari), [Nintendo World Report](http://www.nintendoworldreport.com/news/18475/sega-unveils-jambo-safari-animal-rescue-for-wii-and-ds)). |
| Representative choice | Only member of the family (MAME parent, Rev A) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/jambo.zip`
(battery log: `leg 1: jambo.zip attempt 1 -> ran full window`)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set
here after screenshot review). The attract loop cycles animal-showcase vignettes (running
leopard `shot-060s.png`, zebra chase, rhino, oryx herd), HOW TO PLAY cards with live 3D
demos (lasso "BINGO!" gazelle capture `shot-121s.png`, net-capture sight), **live attract
driving footage** (jeep fording water with rope trailing `shot-304s.png`, in-cab lasso
targeting reticle on a caught animal `shot-487s.png`), the title logo (`shot-365s.png`),
and the Sega logo — genuine attract-demo gameplay, not a frozen frame or settings screen.
Screenshots: `evidence/jambo/shot-060s.png` · `shot-121s.png` · `shot-304s.png` ·
`shot-365s.png` · `shot-487s.png`
Anomalies: none affecting the verdict. Loader is the cart-PIO class (`handoff.trigger =
"pio"`, `pio_bytes` 40,636,224 B vs a single logged DMA event): `streaming.total_bytes`
8,388,607 B (0x7FFFFF) and `main.dma_high_water` 12,582,911 B (0xBFFFFF) are
end-address-minus-1 round numbers of that one block transfer — informational only,
streaming does not gate and main content was measured by write-truth (`nz_total`), not DMA.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,272,582 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.468** — well past `region_score()`'s `u > 2.0` gate. Slots mid-cohort
among the campaign's ARAM-parked titles: … pokasuka 3.368 < **jambo 3.468** < mazan
3.483 … (cohort spans toyfight 2.035 → slashout 3.756). Not inside the kb §6 item-1
empty band (scored max 1.962, parked min 2.035) — no new checkpoint signal, one more
point in the already-dense parked cluster. `nz_above_cap` = 5,342,984 B of content above
the cap (address-keyed placement figure, informational). Address peak is 8,257,552 B
(u 3.938, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in
`score.py`'s region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 23,458,599 | 16,777,216 | **1.398** | `nz_total` — over the 1× line but under 2×, would sub-score ≈34, no gate; `nz_above_cap` (address-placement) 12,345,243 B · `dma_high_water` 12,582,911 B (u 0.750) · write-truth address peak 33,292,320 B (u 1.984) |
| VRAM (content volume + 2×fb) | 9,485,703 | 8,388,608 | **1.131** | `content_total` 8,256,903 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2, per `score.py`'s `vram_ct + 2*vram_fb`) — over the 1× cap, no gate; raw `nz_total` 8,804,644 · `nz_above_cap` 4,916,655 (address-keyed) |
| ARAM (content volume) | 7,272,582 | 2,097,152 | **3.468** | the gate — see above |

Streaming context: 1 DMA event · 8.0 MB total · 8.0 MB unique · re-read ratio 0.0 ·
steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 40,636,224 B (PIO-loader
class, see §3 anomalies). Guts: code 3,670,016 B (3.5 MiB, under the 4 MiB
`code_over_4mb` threshold) · 2,718 functions · MMIO refs rtc 2 / g2ext 516 / scif 0 ·
flags `eeprom_bios`/`rtc`. Similarity: `developer_match: false`, `sdk_overlap:
"partial"`, `cart_loader_match: false`.

Evidence: `assessments/jambo.metrics.json` → `memory.aram`; `guts.sdk_strings` is
dominated by sound-bank symbol tables — per-animal voice/reaction banks
(`SND_SEB_SE_ANIMAL_2_LION_R01`…`ELEPHANT_R05`, leopard/rhino/buffalo/impala/vulture…),
per-surface tire/engine/roll loops (`SND_TIRE_SPIN_GRASS`…`WATER`), rope/lasso SEs, and
30+ `SND_SNG_SNG_BNK*_SONG/JINGLE` entries — exactly the resident-sample profile that
overflows 2 MiB of AICA RAM.

**Controls would score 75, not gate, if ARAM were ever solved.** Researched (5 sources,
full parity in sidecar `controls.sources`): the cabinet is Sega's standard sit-down
driving rig — steering wheel (A0 `IPT_PADDLE`), accelerator (A1 `IPT_PEDAL`), brake (A2
`IPT_PEDAL2`), and a push/pull shift lever read as two buttons (P2 "Shift Down"/"Shift
Up") that doubles as the lasso control in animal-catch mode (MAME
src/mame/sega/naomi.cpp @59e7c0b `INPUT_PORTS_START( jambo )`); corroborated by
[arcadeitalia](https://adb.arcadeitalia.net/?mame=jambo) (Paddle + Pedal, 2 buttons, 1
player), [Wikipedia](https://en.wikipedia.org/wiki/Jambo!_Safari) (wheel + gear shift,
lasso catching), and the [Wilcox Arcade cab review](https://www.wilcoxarcade.com/single-post/2020/03/16/jambo-safari-arcade-review)
(wheel, gas pedal, push/pull hand lever). 3 analog axes + 2 digital — under a DC pad's 4
analog channels, and the Flycast fork already ships the mapping
(`core/hw/naomi/naomi_roms_input.h` `jambo_inputs`: HANDLE → Full axis 0 = stick X,
ACCEL/BRAKE → Half axes 4/5 = triggers, LEVER UP/DOWN → buttons). `device_class =
dc_peripheral` (75.0): the spec §4.4 ladder lists "wheel" by name (DC Race Controller
class), and `controls_extract.py` keys the identical scheme for `crzytaxi`/`18wheelr` —
both of which shipped as official DC ports on this exact control reduction. The battery's
auto-hint stands (unlike `wrungp`, whose `stick` hint needed correcting).

What would unblock it: ARAM content would need to shrink below the 2× cap — kb §6 item 1
(the ARAM gate-softening question, explicitly left open for the campaign checkpoint) or a
per-title sound-bank trim (released-port precedent: the official Ikaruga DC port's 4×
sound trim, kb §4.d). At 3.468× the required cut (~71%) is deep but the bank is highly
granular (hundreds of individually named animal/tire/jingle samples — natural trim/stream
candidates), and the 2009 Wii/NDS remake proves the content survives re-budgeting.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM content u 3.468 (main 1.398 / VRAM 1.131 also over 1×, no gate); driving-cab controls researched → `dc_peripheral` confirmed; ODCM-reported DC compilation added to GAME_FORMATS.md cancelled list |
