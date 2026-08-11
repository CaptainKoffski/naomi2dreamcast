# Derby Owners Club World Edition EX (Rev D) (`derbyocw`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 5,588,057 B → utilization **2.665** — 28th-highest of the now 30-strong parked ARAM cohort (between `asndynmt` 2.782 and `tduno2` 2.615), the **22nd G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1), and the lowest of the four parked Derby generations (`derbyoc`/`derbyo2k` 3.047, `derbyoc2` 2.824). Not a sole-blocker: **all three regions are over** — main content u 1.319, VRAM fit u 1.154 — the `derbyoc`/`derbyo2k` pattern, and on near-identical numbers: the 2005 World Edition EX runs the original 1999 DOC1 engine (same 3,014,656 B carve, same PIO loader) with English text. Even a softened ARAM rule only advances it to G2 `card_reader` — the fork HLEs the card reader for exactly this cart's gameId. **This closes the Derby family: all four generations assessed, all parked G3-aram.** |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `derbyocw` (covers clones `drbyocwa`–`drbyocwt` — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11011, `/* 0088 */`, parent `naomi`, machine `naomim2`; clones at lines 11007–11010, the 2001 World Edition Revs A/B/C/T) — carve title `" DERBY OWNERS CLUB WE ---------"` (its own gameId; the fork's Derby card-reader and M3-comm hooks list it explicitly). **Family context:** `derbyoc` (line 10954, `/* 0016 */`), `derbyo2k` (line 10993, `/* 0052 */`) and `derbyoc2` (line 11005, `/* 0083 */`) all parked 2026-08-11 — this doc covers **only** the World Edition family and is the last Derby set in QUEUE.md |
| Maker / year | Sega, 2005 (MAME `GAME()` row — EX Rev D; the underlying World Edition clones are 2001) |
| Genre / format | Horse-race sim ⚠ (`GAME_FORMATS.md`) — multi-satellite horse-owner cabinet (magnetic-card satellite seats + shared live/master display) — **cart** 46.7 MB, Naomi M2, encryption chip **not populated** (`0xffffffff` in fork `naomi_roms.cpp` derbyocw entry — unencrypted, unlike the siblings' 315-5881 keys) |
| Official DC port | No — Sega's home continuation was *Derby Owners Club Online* for PC (2002), not DC ([Wikipedia](https://en.wikipedia.org/wiki/Derby_Owners_Club)) |
| Community ports | None found (family searched 2026-08-11) |
| Representative choice | Parent set (EX Rev D) of the World Edition family; each Derby Owners Club generation is its own QUEUE.md row |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/derbyocw.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The satellite boots straight into its standby/attract loop: a live animated 3D
paddock (horse trotting under changing cameras), FREE PLAY, and the entry prompts in English —
"TO CREATE A NEW HORSE, PRESS START BUTTON. / TO CONTINUE THE GAME, INSERT YOUR CARD."
(`shot-060s.png`). Despite World Edition being the offline-friendly international revision,
coverage does **not** differ from the Japanese sets: the same persistent **NO LINK** overlay sits
on screen all run — the satellite ran standalone with no master/live unit on the emulated link, so
a race/live cycle was never exercised and the memory figures are standby-loop **lower bounds**
(the ARAM bank and paddock assets loaded at boot regardless). Same standalone pattern as
`derbyoc`/`derbyo2k`, English-localized.
Screenshots: `evidence/derbyocw/shot-060s.png` · `shot-304s.png` · `shot-609s.png` (first/mid/last;
the other seven frames of the same single standby scene curated out).
Anomalies: none — single leg, full 600 s window on the first attempt.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 5,588,057 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.665** — past `region_score()`'s `u > 2.0` gate, **28th-highest of the now
30-strong parked ARAM cohort** (between `asndynmt` 2.782 and `tduno2` 2.615; cohort max
`slashout` 3.756), the lowest of the four parked Derby generations (`derbyoc`/`derbyo2k` 3.047,
`derbyoc2` 2.824). This is the **22nd G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1
tallied 17 in the non-⚠ sweep; `oinori` 18th, `derbyo2k` 19th, `derbyoc` 20th, `derbyoc2` 21st,
`derbyocw` extends the ⚠ tail). Checkpoint note: u 2.665 is another datum inside the 1.962–3.02
volume-u band the §6 item 1 ruling recorded as *empty* at the 30-family checkpoint — the sweeps
have kept populating it (`dygolf` 2.921, `derbyoc2` 2.824, `asndynmt` 2.782, now `derbyocw`
2.665, `tduno2` 2.615). `nz_above_cap` = 3,623,724 B (address-keyed placement figure,
informational). Address peak 8,257,552 B (u 3.938; watermark the full 8,388,608 B bank) — the
usual boot-time full-bank load.

The other two regions, quoted from the sidecar — **not a sole-blocker: all three regions over**
(the `derbyoc`/`derbyo2k` pattern, on near-identical numbers — same engine, see below), so
derbyocw sits outside the cohort's ARAM-sole-blocker unpark shortlist:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 22,132,900 | 16,777,216 | **1.319** | `nz_total` — over cap, under the 2× gate; `nz_above_cap` 13,146,047 B · `dma_high_water` 29,417,344 B (u 1.753 — byte-identical to `derbyoc`'s) · address peak/watermark 33,554,432 B (u 2.000 — the full 32 MiB bank touched) |
| VRAM (content volume + 2×fb) | 9,679,351 | 8,388,608 | **1.154** | `content_total` 8,450,551 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over budget; raw `nz_total` 8,971,671 (u 1.070) · address peak 15,773,696 (u 1.880) |
| ARAM (content volume) | 5,588,057 | 2,097,152 | **2.665** | the gate — see above |

Streaming context: 1 DMA event · 57,216 B total = unique · re-read ratio 0.0 · steady-state
0.0 MB/min (`short_window: false`) · `pio_bytes` 48,510,240 B — the same PIO-heavy front-loaded
DOC1 loader as `derbyoc` (whose single DMA event is the same 57,216 B).
Guts: carve 3,014,656 B (`carve_meta.title = " DERBY OWNERS CLUB WE ---------"` — byte-identical
carve size to `derbyoc`'s 1999 build) · 1,741 functions · MMIO refs rtc 4 / g2ext 405 / scif 0 ·
`serial_pokes` 0 · flags `eeprom_bios`/`rtc` — the g2ext count matches the satellite-link wiring;
the cart's strings are the DOC1 vocabulary localized (English card/reader-writer state machine,
international race calendar: AMERICAN DERBY, HONG KONG DERBY, DOC 1000/2000 GUINEAS).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (one line, off-ladder — `card_reader`, does not gate because G3 fired first):** the DOC
satellite is a magnetic horse-card reader/writer plus buttons on generic Naomi input ports — MAME
wires plain `naomim2` + generic `naomi` inputs with no card/satellite hardware (naomi.cpp @59e7c0b
GAME() line 11011), while the Flycast fork HLEs the hardware for exactly this cart's gameId
`" DERBY OWNERS CLUB WE ---------"`: card reader (`maple_cfg.cpp:274-278` →
`card_reader::derbyInit()`, whose else branch at `card_reader.cpp:667-669` selects
`DerbyBRCardReader` — a `SanwaCRP1231BR` on the MIE via an 838-13661 RS232/RS422 board,
`card_reader.cpp:391-392` @4b59eceff), M3 comm board (`naomi_m3comm.cpp:172` — the WE gameId is
listed explicitly), multiboard master/slave (`multiboard.cpp:437` — `" DERBY"` prefix, DOC slaves
boot the master's cart; `naomi_roms.cpp` derbyocw entry `multiboard=1` + `derbyocw_eeprom_dump`),
and the cart's own strings are wall-to-wall card plumbing ("CREDIT TO CARD GAME START",
"INSERT CARD.", the `CARD_*`/`RQ_*` reader-writer state machine). Sources (full parity in sidecar
`controls.sources`).

**What would unblock it:** nothing plausible — the blockers stack, exactly as for `derbyoc`.
A kb §6 item 1 ARAM-gate softening (the sound-trim argument) still leaves main content 1.319×
and VRAM fit 1.154× over cap in a standby-loop lower bound, and clearing G3 only advances the
sidecar to **G2 `card_reader`**: the owner loop (breed → save to card → return) *is* the magnetic
card, and the cabinet's draw is the shared live race across linked satellites — offline-friendly
international revision or not, the run itself sat at NO LINK. Excluded by hardware class beyond
the memory wall, not by trimmable assets.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 2.665, 28th of 30-strong cohort (lowest of the four Derby generations; inside the formerly-empty 1.962–3.02 band), 22nd G3-aram park of the 2026-08-11 sweeps; not sole-blocker (all three regions over: main 1.319, VRAM 1.154 — the `derbyoc`/`derbyo2k` pattern on near-identical numbers, same 1999 DOC1 engine); coverage demo (NO LINK standby loop, English prompts — lower bounds); `card_reader` recorded, G3 fired first; clean single-leg full-window run — **closes the Derby family (4/4 parked)** |
