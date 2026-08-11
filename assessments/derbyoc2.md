# Derby Owners Club II Ver.2.1 (Japan, Rev B) (`derbyoc2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 5,923,032 B → utilization **2.824** — 26th-highest of the now 29-strong parked ARAM cohort (between `dygolf` 2.921 and `asndynmt` 2.782), the **21st G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1), and the lowest of the three parked Derby generations (`derbyoc`/`derbyo2k` both 3.047). Unlike its siblings it **is a sole-blocker**: main content u **0.917 fits**, VRAM fit u **0.696 fits** — the only Derby where memory alone is just the ARAM wall. But a kb §6 item 1 softening only advances it to G2 `card_reader`: the satellite's magnetic horse-card and the multi-satellite link are the game — the fork HLEs the card reader for exactly this cart's gameId. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `derbyoc2` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11005, `/* 0083 */`, parent `naomi`, machine `naomim2`) — carve title `" DERBY OWNERS CLUB II-----------"` (its own gameId; the fork's Derby card-reader hook lists it explicitly). **Family context:** `derbyoc` (line 10954, `/* 0016 */`) and `derbyo2k` (line 10993, `/* 0052 */`) parked 2026-08-11; `derbyocw` (line 11011, `/* 0088 */`, clones `drbyocwa`–`drbyocwt` lines 11007–11010) is a separate pending QUEUE.md set — this doc covers **only** `derbyoc2` |
| Maker / year | Sega, 2001 (MAME `GAME()` row) |
| Genre / format | Horse-race sim ⚠ (`GAME_FORMATS.md`) — multi-satellite horse-owner cabinet (magnetic-card satellite seats + shared live/master display) — **cart** 118.9 MB, Naomi M2 (315-5881 key `0x2a436bb7` per fork `naomi_roms.cpp` derbyoc2 entry) |
| Official DC port | No — Sega's home continuation was *Derby Owners Club Online* for PC (2002), not DC ([Wikipedia](https://en.wikipedia.org/wiki/Derby_Owners_Club)) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Sole set of the family (each Derby Owners Club generation is its own QUEUE.md row) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/derbyoc2.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The satellite boots straight into its standby/attract loop: a 3D paddock
backdrop under the 「NO LINK モード」 banner and "Hitmaker Racing Association" header, FREE PLAY,
a next-race schedule board (Tokyo/Kyoto turf, rank-gated 1R–3R entries), cycling between an empty
info-billboard panel (`shot-060s.png`) and the entry prompts 「調教／レース — カードを入れて
ください」 / 「新馬作成 — スタートボタンを押してください」 (training/race: insert your card /
new horse: press START) — `shot-304s.png`. No horse appears on screen in any captured frame
(unlike the `derbyoc`/`derbyo2k` paddock loops). The persistent **NO LINK** overlay shows the
satellite running standalone: no master/live unit on the emulated link, so a race/live cycle was
never exercised — memory figures are standby-loop **lower bounds** (the ARAM bank loaded at boot
regardless).
Screenshots: `evidence/derbyoc2/shot-060s.png` · `shot-304s.png` · `shot-609s.png` (billboard
state / prompt state / last frame; the other seven frames of the same two-state standby scene
curated out).
Anomalies: battery leg 1 flaked (emulator exited early); the automatic retry ran the full 600 s
window — this sidecar is the retry's. `evidence/derbyoc2/raw/` was subsequently pruned by the
next family's battery start (`run_battery.py` SSD-hygiene step deletes prior families' raw dirs),
so raw log tags are not quotable here — all figures below are quoted from the sidecar.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 5,923,032 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.824** — past `region_score()`'s `u > 2.0` gate, **26th-highest of the now
29-strong parked ARAM cohort** (between `dygolf` 2.921 and `asndynmt` 2.782; cohort max
`slashout` 3.756), the lowest of the three parked Derby generations (both siblings 3.047).
This is the **21st G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1 tallied 17 in the
non-⚠ sweep; `oinori` 18th, `derbyo2k` 19th, `derbyoc` 20th, `derbyoc2` extends the ⚠ tail).
Checkpoint note: u 2.824 sits inside the 1.962–3.02 volume-u band the §6 item 1 ruling recorded
as *empty* at the 30-family checkpoint — the later sweeps have since populated that band
(`dygolf` 2.921, `derbyoc2` 2.824, `asndynmt` 2.782, `tduno2` 2.615, `toyfight` 2.035), a datum
for the next checkpoint, not a re-ruling. `nz_above_cap` = 3,902,945 B (address-keyed placement
figure, informational). Address peak 8,257,552 B (u 3.938; watermark the full 8,388,608 B bank)
— the usual boot-time full-bank load.

The other two regions, quoted from the sidecar — **sole-blocker: main RAM and VRAM both fit**
(content-volume keying), unlike the all-regions-over `derbyoc`/`derbyo2k` pattern, so by memory
alone derbyoc2 joins the cohort's ARAM-sole-blocker unpark shortlist — but see below, the
hardware class disqualifies it in practice:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 15,377,320 | 16,777,216 | **0.917** | `nz_total` — **fits** under cap; `nz_above_cap` 9,402,439 B (placement above the cap line — relocation work, not volume) · `dma_high_water` 29,615,520 B (u 1.765) · address peak/watermark 31,786,368 B (u 1.895) |
| VRAM (content volume + 2×fb) | 5,835,839 | 8,388,608 | **0.696** | `content_total` 4,607,039 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — **fits**; raw `nz_total` 5,218,823 (u 0.622) · address peak 10,895,392 (u 1.299) |
| ARAM (content volume) | 5,923,032 | 2,097,152 | **2.824** | the gate — see above |

Streaming context: 451 DMA events · 27,682,816 B total · 27,588,608 B unique · re-read ratio
0.0034 · steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 3,671,360 B — DMA-loaded,
everything front-loaded at boot (unlike the PIO-heavy DOC1-engine siblings).
Guts: carve 3,670,016 B (`carve_meta.title = " DERBY OWNERS CLUB II-----------"`) · 5,209
functions · MMIO refs rtc 3 / g2ext 397 / scif 26 · `serial_pokes` 5174 · flags
`eeprom_bios`/`serial`/`rtc` — the g2ext count matches the satellite-link wiring; the SDK is the
newer Katana-derived stack (`syStartKn 2.08`, Ninja2/Nindows2/Kunoichi2, CRI ADX/Sofdec in
`guts.sdk_strings`), not the siblings' 1998 nlcb build.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (one line, off-ladder — `card_reader`, does not gate because G3 fired first):** the DOC
satellite is a magnetic horse-card reader/writer plus buttons on generic Naomi input ports — MAME
wires plain `naomim2` + generic `naomi` inputs with no card/satellite hardware (naomi.cpp @59e7c0b
GAME() line 11005), while the Flycast fork HLEs the hardware for exactly this cart's gameId
`" DERBY OWNERS CLUB II-----------"`: card reader (`maple_cfg.cpp:277-278` →
`card_reader::derbyInit()`, whose else branch at `card_reader.cpp:668-669` selects
`DerbyBRCardReader` — a `SanwaCRP1231BR` on the MIE via an 838-13661 RS232/RS422 board,
`card_reader.cpp:392` @4b59eceff), multiboard master/slave (`multiboard.cpp:437` — `" DERBY"`
prefix, DOC slaves boot the master's cart; `naomi_roms.cpp` derbyoc2 entry `multiboard=1` +
`derbyoc2_eeprom_dump`), and the capture itself shows the card prompts on screen
(「調教／レース — カードを入れてください」, `shot-304s.png`). Sources (full parity in sidecar
`controls.sources`).

**What would unblock it:** more than its siblings, but still nothing practical — derbyoc2 is the
one Derby where the memory wall is ARAM alone (main 0.917, VRAM 0.696 both fit in a standby-loop
lower bound), so a kb §6 item 1 ARAM-gate softening (the sound-trim argument) would clear G3
outright. But clearing G3 only advances the sidecar to **G2 `card_reader`**: the owner loop
(breed → save to card → return) *is* the magnetic card, and the cabinet's draw is the shared live
race across linked satellites — the run itself sat at NO LINK. Same hardware-class exclusion as
`derbyoc`/`derbyo2k`, just without their memory pile-on.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 2.824, 26th of 29-strong cohort (lowest Derby; inside the formerly-empty 1.962–3.02 band), 21st G3-aram park of the 2026-08-11 sweeps; **sole-blocker** (main 0.917 and VRAM 0.696 both fit — unlike siblings); coverage demo (satellite standby/attract, NO LINK standalone — lower bounds); `card_reader` recorded, G3 fired first; leg-1 emulator-exit flake, auto-retry ran full 600 s |
