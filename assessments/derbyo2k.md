# Derby Owners Club 2000 Ver.2 (`derbyo2k`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 6,389,673 B → utilization **3.047** — 21st-highest of the now 27-strong parked ARAM cohort (between `virnba` 3.078 and `takoron` 2.997), the **19th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1). Not a sole-blocker: **all three regions are over** — main content u 1.306, VRAM fit u 1.169. And even a softened ARAM rule only advances it to G2 `card_reader`: the satellite's magnetic horse-card and the multi-satellite link are the game — no DC-mappable persistence/core loop. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `derbyo2k` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10993, `/* 0052 */`, parent `naomi`, machine `naomim2`) — carve title `" DERBY OWNERS CLUB ------------"`. **Family context:** `derbyoc` (line 10954, `/* 0016 */`), `derbyoc2` (line 11005, `/* 0083 */`) and `derbyocw` (line 11011, `/* 0088 */`, clones `drbyocwa`–`drbyocwt` lines 11007–11010) are separate pending QUEUE.md sets — this doc covers **only** `derbyo2k` |
| Maker / year | Sega, 2000 (MAME `GAME()` row) |
| Genre / format | Horse-race sim ⚠ (`GAME_FORMATS.md`) — multi-satellite horse-owner cabinet (magnetic-card satellite seats + shared live/master display) — **cart** 60.7 MB, Naomi M2 (315-5881 not populated, key `0xffffffff` per fork `naomi_roms.cpp` derbyo2k entry) |
| Official DC port | No — Sega's home continuation was *Derby Owners Club Online* for PC (2002), not DC ([Wikipedia](https://en.wikipedia.org/wiki/Derby_Owners_Club)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (each Derby Owners Club generation is its own QUEUE.md row) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/derbyo2k.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The satellite boots straight into its standby/attract loop: a live animated 3D
paddock (horse trotting/frolicking under changing cameras — the cart's `_UMA_WALK_`/`_UMA_TROT_`
animation vocabulary in `guts.sdk_strings`, on screen), FREE PLAY, and the entry prompts
「新しい馬をつくる — スタートボタンを押して下さい」 / 「続きから始める — カードを入れて下さい」
(new horse: press START / continue: insert your card) — `shot-304s.png`. A persistent **NO LINK**
overlay shows the satellite is running standalone: no master/live unit on the emulated link, so a
race/live cycle was never exercised — memory figures are standby-loop **lower bounds** (the 8 MiB
ARAM bank and paddock assets loaded at boot regardless).
Screenshots: `evidence/derbyo2k/shot-060s.png` · `shot-304s.png` · `shot-609s.png` (first/mid/last;
the other seven frames of the same standby scene curated out).
Anomalies: battery leg 1 flaked (emulator exited early); the automatic retry ran the full 600 s
window — this sidecar is the retry's.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 6,389,673 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.047** — past `region_score()`'s `u > 2.0` gate, **21st-highest of the now
27-strong parked ARAM cohort** (between `virnba` 3.078 and `takoron` 2.997; cohort max
`slashout` 3.756). This is the **19th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1
tallied 17 in the non-⚠ sweep; `oinori` was the 18th, `derbyo2k` extends the ⚠ tail).
`nz_above_cap` = 4,418,353 B (address-keyed placement figure, informational). Address peak
8,257,552 B (u 3.938; watermark the full 8,388,608 B bank) — the usual boot-time full-bank load.

The other two regions, quoted from the sidecar — **not a sole-blocker: all three regions over**
(the `virnba` pattern), so derbyo2k sits outside the cohort's ARAM-sole-blocker unpark shortlist:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 21,904,015 | 16,777,216 | **1.306** | `nz_total` — over cap, under the 2× gate; `nz_above_cap` 13,107,723 B · `dma_high_water` 29,417,344 B (u 1.753) · address peak/watermark 33,554,432 B (u 2.000 — the full 32 MiB bank touched) |
| VRAM (content volume + 2×fb) | 9,808,661 | 8,388,608 | **1.169** | `content_total` 8,579,861 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over budget; raw `nz_total` 9,100,654 (u 1.085) · address peak 15,845,376 (u 1.889) |
| ARAM (content volume) | 6,389,673 | 2,097,152 | **3.047** | the gate — see above |

Streaming context: 1 DMA event · 57,216 B total = unique · re-read ratio 0.0 · steady-state
0.0 MB/min (`short_window: false`) · `pio_bytes` 49,272,292 B — PIO-heavy loader, everything
front-loaded at boot.
Guts: carve 3,014,656 B (`carve_meta.title = " DERBY OWNERS CLUB ------------"`) · 1,811
functions · MMIO refs rtc 4 / g2ext 426 / scif 0 · flags `eeprom_bios`/`rtc` — the g2ext count
matches the satellite-link wiring (cart strings: "Checking Multi <--> Slave", `nlcb.c` 1998 comm
library, MASTER/LIVE DISPLAY/SLAVE SITE).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (one line, off-ladder — `card_reader`, does not gate because G3 fired first):** the DOC
satellite is a magnetic horse-card reader/writer plus buttons on generic Naomi input ports — MAME
wires plain `naomim2` + generic `naomi` inputs with no card/satellite hardware (naomi.cpp @59e7c0b
GAME() line 10993), while the Flycast fork HLEs the hardware for exactly this gameId: card reader
(`maple_cfg.cpp:274-278` → `card_reader::derbyInit()`, `DerbyLRCardReader` at
`card_reader.cpp:663-670` @4b59eceff), M3 comm board (`naomi_m3comm.cpp:172-173`) and multiboard
master/slave (`multiboard.cpp:437` — DOC slaves boot the master's cart; `naomi_roms.cpp`
`multiboard=1`), and the cart's own strings confirm the card is the persistence core
("CREDIT TO CARD GAME START", `CC2_SAVE_NO_CARD`/`CC2_ERROR_CARD`). Sources (full parity in
sidecar `controls.sources`).

**What would unblock it:** nothing plausible — the blockers stack. A kb §6 item 1 ARAM-gate
softening (the sound-trim argument) still leaves main content 1.306× and VRAM fit 1.169× over
cap in a standby-loop lower bound, and clearing G3 only advances the sidecar to **G2
`card_reader`**: the owner loop (breed → save to card → return) *is* the magnetic card, and the
cabinet's draw is the shared live race across linked satellites — the run itself sat at NO LINK.
Mirror of `oinori`: excluded by hardware class beyond the memory wall, not by trimmable assets.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.047, 21st of 27-strong cohort, 19th G3-aram park of the 2026-08-11 sweeps; not sole-blocker (all three regions over: main 1.306, VRAM 1.169); coverage demo (satellite standby/attract, NO LINK standalone — lower bounds); `card_reader` recorded, G3 fired first; leg-1 emulator-exit flake, auto-retry ran full 600 s |
