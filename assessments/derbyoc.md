# Derby Owners Club (Japan, Rev B) (`derbyoc`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 6,390,387 B → utilization **3.047** — 21st-highest of the now 28-strong parked ARAM cohort (between `virnba` 3.078 and its own sequel `derbyo2k` 3.047, which it edges by 714 B), the **20th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1). Not a sole-blocker: **all three regions are over** — main content u 1.321, VRAM fit u 1.154. And even a softened ARAM rule only advances it to G2 `card_reader`: the satellite's magnetic horse-card and the multi-satellite link are the game — same hardware class as `derbyo2k`, whose HLE hooks in the fork key on this cart's exact gameId. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `derbyoc` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 10954, `/* 0016 */`, parent `naomi`, machine `naomim2`) — carve title `" DERBY OWNERS CLUB ------------"`, the **same gameId string as `derbyo2k`** (the fork's Derby HLE keys on it). **Family context:** `derbyo2k` (line 10993, `/* 0052 */`) parked 2026-08-11; `derbyoc2` (line 11005, `/* 0083 */`) and `derbyocw` (line 11011, `/* 0088 */`, clones `drbyocwa`–`drbyocwt` lines 11007–11010) are separate pending QUEUE.md sets — this doc covers **only** `derbyoc` |
| Maker / year | Sega, 1999 (MAME `GAME()` row) — the original Derby Owners Club |
| Genre / format | Horse-race sim ⚠ (`GAME_FORMATS.md`) — multi-satellite horse-owner cabinet (magnetic-card satellite seats + shared live/master display) — **cart** 52.5 MB, Naomi M2 (315-5881 key `0x280fee35` per fork `naomi_roms.cpp` derbyoc entry) |
| Official DC port | No — Sega's home continuation was *Derby Owners Club Online* for PC (2002), not DC ([Wikipedia](https://en.wikipedia.org/wiki/Derby_Owners_Club)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (each Derby Owners Club generation is its own QUEUE.md row) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/derbyoc.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The satellite boots straight into its standby/attract loop: a live animated 3D
paddock (horse trotting under changing cameras — the cart's `_UMA_WALK_`/`_UMA_TROT_` animation
vocabulary in `guts.sdk_strings`, on screen), FREE PLAY, and the entry prompts
「新しい馬をつくる — スタートボタンを押して下さい」 / 「続きから始める — カードを入れて下さい」
(new horse: press START / continue: insert your card) — `shot-609s.png`. A persistent **NO LINK**
overlay shows the satellite is running standalone: no master/live unit on the emulated link, so a
race/live cycle was never exercised — memory figures are standby-loop **lower bounds** (the ARAM
bank and paddock assets loaded at boot regardless). Same standalone pattern as `derbyo2k`.
Screenshots: `evidence/derbyoc/shot-060s.png` · `shot-304s.png` · `shot-609s.png` (first/mid/last;
the other seven frames of the same standby scene curated out).
Anomalies: none — single leg, full 600 s window on the first attempt.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 6,390,387 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.047** — past `region_score()`'s `u > 2.0` gate, **21st-highest of the now
28-strong parked ARAM cohort** (between `virnba` 3.078 and `derbyo2k` 3.047 — it edges its own
sequel by 714 B of content; cohort max `slashout` 3.756). This is the **20th G3-aram park of the
2026-08-11 sweeps** (kb §6 item 1 tallied 17 in the non-⚠ sweep; `oinori` 18th, `derbyo2k` 19th,
`derbyoc` extends the ⚠ tail). `nz_above_cap` = 4,419,484 B (address-keyed placement figure,
informational). Address peak 8,257,552 B (u 3.938; watermark the full 8,388,608 B bank) — the
usual boot-time full-bank load.

The other two regions, quoted from the sidecar — **not a sole-blocker: all three regions over**
(the `virnba`/`derbyo2k` pattern), so derbyoc sits outside the cohort's ARAM-sole-blocker unpark
shortlist:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 22,164,938 | 16,777,216 | **1.321** | `nz_total` — over cap, under the 2× gate; `nz_above_cap` 13,147,718 B · `dma_high_water` 29,417,344 B (u 1.753) · address peak/watermark 33,554,432 B (u 2.000 — the full 32 MiB bank touched) |
| VRAM (content volume + 2×fb) | 9,679,627 | 8,388,608 | **1.154** | `content_total` 8,450,827 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — over budget; raw `nz_total` 8,968,163 (u 1.069) · address peak 15,720,448 (u 1.874) |
| ARAM (content volume) | 6,390,387 | 2,097,152 | **3.047** | the gate — see above |

Streaming context: 1 DMA event · 57,216 B total = unique · re-read ratio 0.0 · steady-state
0.0 MB/min (`short_window: false`) · `pio_bytes` 49,274,228 B — PIO-heavy loader, everything
front-loaded at boot.
Guts: carve 3,014,656 B (`carve_meta.title = " DERBY OWNERS CLUB ------------"`) · 1,757
functions · MMIO refs rtc 2 / g2ext 405 / scif 0 · flags `eeprom_bios`/`rtc` — the g2ext count
matches the satellite-link wiring (cart strings: "CChecking Multi <--> Slave", `nlcb.c` 1998 comm
library, MASTER/LIVE DISPLAY/SLAVE SITE).
Similarity: `developer_match: false`, `sdk_overlap: "none"`, `cart_loader_match: false`.

**Controls (one line, off-ladder — `card_reader`, does not gate because G3 fired first):** the DOC
satellite is a magnetic horse-card reader/writer plus buttons on generic Naomi input ports — MAME
wires plain `naomim2` + generic `naomi` inputs with no card/satellite hardware (naomi.cpp @59e7c0b
GAME() line 10954), while the Flycast fork HLEs the hardware for exactly this cart's gameId
`" DERBY OWNERS CLUB ------------"`: card reader (`maple_cfg.cpp:274-278` →
`card_reader::derbyInit()`, whose exact-match branch at `card_reader.cpp:666` selects
`DerbyLRCardReader`, `card_reader.cpp:663-670` @4b59eceff), M3 comm board
(`naomi_m3comm.cpp:172-173`) and multiboard master/slave (`multiboard.cpp:437` — DOC slaves boot
the master's cart; `naomi_roms.cpp` derbyoc entry `multiboard=1` + `derbyoc_eeprom_dump`), and the
cart's own strings confirm the card is the persistence core ("CREDIT TO CARD GAME START",
`CC2_SAVE_NO_CARD`/`CC2_ERROR_CARD`). Sources (full parity in sidecar `controls.sources`).

**What would unblock it:** nothing plausible — the blockers stack, exactly as for `derbyo2k`. A
kb §6 item 1 ARAM-gate softening (the sound-trim argument) still leaves main content 1.321× and
VRAM fit 1.154× over cap in a standby-loop lower bound, and clearing G3 only advances the sidecar
to **G2 `card_reader`**: the owner loop (breed → save to card → return) *is* the magnetic card,
and the cabinet's draw is the shared live race across linked satellites — the run itself sat at
NO LINK. Excluded by hardware class beyond the memory wall, not by trimmable assets.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.047, 21st of 28-strong cohort (714 B above sequel `derbyo2k`), 20th G3-aram park of the 2026-08-11 sweeps; not sole-blocker (all three regions over: main 1.321, VRAM 1.154); coverage demo (satellite standby/attract, NO LINK standalone — lower bounds); `card_reader` recorded, G3 fired first; clean single-leg full-window run |
