# Virtua NBA (USA) (`virnba`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | A licensed NBA title carrying a genuinely large sound bank — 6,455,043 B of fill-excluded ARAM content (u = 3.08) sits well past the u > 2.0 gate — and it is not alone: main RAM content is 1.27× its cap and VRAM FB-masked content is 1.21×, so every region is over budget; the DC already has its own native basketball lineage (Visual Concepts' NBA 2K series, 1999–2001), which makes this a low-value unpark candidate even if the ARAM rule softens. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `virnba` (parent; covers clones `virnbao` (Virtua NBA), `virnbap` (prototype, 1999), `virnbapa` (prototype 15.11, 1999) — all `parent: virnba` in controls.json, all `naomim2`) |
| Maker / year | Sega, 2000 (prototypes 1999) |
| Genre / format | Sports (5-on-5 licensed NBA basketball, all 29 teams), **cart, Naomi M2**, 100.2 MB |
| Official DC port | No — arcade-only; no home release on any platform ([MobyGames](https://www.mobygames.com/game/71386/virtua-nba/), [Museum of the Game](https://www.arcade-museum.com/Videogame/virtua-nba), searched 2026-08-11). Genre precedent on DC is strong: Sega published Visual Concepts' NBA 2K / 2K1 / 2K2 natively on Dreamcast 1999–2001, so DC owners already had licensed NBA basketball |
| Community ports | None found (searched 2026-08-11) — no conversion threads surfaced |
| Representative choice | Parent set (USA); clones are regional/prototype variants of the same game |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/virnba.zip`
(battery log: `leg 1: virnba.zip attempt 1 -> ran full window`)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; title card at
`shot-060s.png`, live attract gameplay (Lakers court) at `shot-121s.png`, in-attract
jump-shot tutorial demo at `shot-304s.png`, playoff ranking screen at `shot-609s.png`.
Screenshots: `evidence/virnba/shot-060s.png` · `evidence/virnba/shot-121s.png` ·
`evidence/virnba/shot-304s.png` · `evidence/virnba/shot-609s.png`
Anomalies: `shot-426s.png` (deleted in curation) caught a white transition frame
between attract scenes — adjacent shots on both sides render normally; not a capture
fault.

## Gate

**G3 memory: aram content > 2x DC capacity** — the volume-keyed message (`score.py`
reports `metric="content"` whenever `content_total` is present); axes not computed
(`scores: null`).

`memory.aram.content_total = 6,455,043 B` (fill-excluded content volume, battery v9)
against the DC's 2,097,152 B AICA RAM → u = 3.08, well past `region_score()`'s
`u > 2.0` gate. The fill-excluded content-high address is 8,257,552 B (u = 3.94) with
`nz_above_cap` 4,468,255 B of genuine sound content above the cap — a real, heavy sound
bank (commentary/crowd audio for a licensed NBA title), not the boot-time "DMPD" fill
artifact (kb §7; the aram watermark 8,388,608 B *is* that fill, informational only).

The gate is not the only region over budget — context values from the sidecar:

- Main RAM: write-truth peak 32,791,136 B (u 1.95) · `nz_total` 21,271,108 B — under
  the v9 content keying u = **1.27**, with `nz_above_cap` 11,905,109 B of content above
  the 16 MB line · `dma_high_water` 32,070,368 B (1.91× — the cart streams assets high
  into the 32 MB Naomi space).
- VRAM: write-truth peak 14,079,999 B (u 1.68) · v8 FB-masked fit `content_total`
  8,904,527 B + 2×`fb_bytes` 614,400 B ⇒ 10,133,327 B, u = **1.21** — over cap even
  after FB masking (`nz_total` 9,839,906 B, `nz_above_cap` 5,269,393 B).
- Streaming: 280 DMA events · 106,015,392 B total / 53,742,048 B unique · re-read
  ratio 0.4931 · steady-state 8.966 MB/min (`short_window: false`) · `pio_bytes`
  2,098,496 B — an actively streaming cart, consistent with per-team asset loads.
- Guts: code 2,097,152 B · 2,320 functions · MMIO refs scif 0 / rtc 5 / g2ext 301 ·
  flags `eeprom_bios`, `rtc` · carve clean (`title: "VIRTUA NBA"`, base `0x0c020000`).
  `guts.sdk_strings` is a large player-animation state-machine list (KAMAE/DRB/SDB
  motion transitions) — a motion-capture-heavy engine.
- Similarity inputs: `developer_match: false`, `sdk_overlap: "partial"`,
  `cart_loader_match: false`.
- Controls (easy axis, not the blocker): `controls.device_class = stick` — standard
  Naomi 2P panel, 8-way stick + 2 game buttons (PASS / SHOOT). Sources: MAME
  src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`; Flycast fork
  `core/hw/naomi/naomi_roms_input.h:543` `virnba_inputs = INPUT_2_BUTTONS("PASS",
  "SHOOT")` (strongest citation);
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=virnba)
  (8-way joystick, 2P — the "6 buttons" is the generic JVS standard declaration);
  [Museum of the Game](https://www.arcade-museum.com/Videogame/virtua-nba). Maps 1:1
  on a stock DC pad (d-pad/stick + A/B).

What would unblock it: the ARAM gate softening queued for the §6 checkpoint
(`docs/kb/assessment-tooling.md` §6 item 1 — G3-ARAM 2× threshold vs the Ikaruga
4× audio-trim precedent, kb §4.d). But unlike `ausfache` (sound-only overshoot),
virnba would remain over budget on **both** other regions (main content 1.27×, VRAM
fit 1.21×) even with a softer ARAM rule — an unpark would re-score it low, not clear
it. With NBA 2K native on DC, the porting value is also low.

## Risks & notes

- **All three regions over cap** — the ARAM gate is merely the first wall; this is a
  32 MB-class Naomi title using its full footprint.
- **DC-native alternative exists**: Sega's own NBA 2K series (Visual Concepts,
  1999–2001) — a port would compete with a better-fitting native lineage.
- **Rendering must be verified on real DC hardware** (working-style rule) if ever
  revisited; the capture renders the full attract cycle under the fork.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | First assessment: `content_total` 6,455,043 B (u 3.08), `nz_above_cap` 4,468,255 B of real sound content; main content 1.27× and VRAM fit 1.21× also over — all regions over budget |
