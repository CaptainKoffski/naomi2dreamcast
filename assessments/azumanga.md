# Azumanga Daioh Puzzle Bobble (GDL-0018) (`azumanga`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **42.7 (B)** |
| Bottom line | Lavish 2D presentation overruns all three DC regions — VRAM binds at 1.84× cap with 6.7 MB of real content above the line, ARAM voice/BGM content is 1.66×, and main content volume just tips the cap at 1.025× — a heavy port despite the "easy" puzzle genre, though the ARAM trim is verified to be a mechanical bank rebuild, not pointer archaeology. |
| Assessed | capture 2026-08-07 · battery v7 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `azumanga` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | MOSS (Taito license), 2002 |
| Genre / format | Puzzle ★, GD-ROM (GDL-0018) |
| Official DC port | No — arcade-only, Japan-exclusive ([Azumanga Daioh Wiki](https://azumanga.fandom.com/wiki/Azumanga_Daioh_Puzzle_Bobble), accessed 2026-08-02) |
| Community ports | None found — dreamcast-talk searches surface only generic Naomi→DC conversion-tool threads, no Azumanga conversion (searched 2026-08-02) |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/azumanga.zip`
Attract/demo reached: **demo** — live two-player VS attract gameplay (`shot-304s.png`); the v2-era capture documented the full attract cycle (title → VS demo → game-over → CLEAR! card → how-to-play → title). Sidecar `capture.coverage = "demo"`.
Screenshots: `evidence/azumanga/shot-060s.png` · `evidence/azumanga/shot-304s.png` · `evidence/azumanga/shot-609s.png`
Anomalies: none — clean boot, no flake.

## 4. Memory fit (axis: 16.3)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 17,201,730 | 16,777,216 | 1.025 | 80.4 | address peak 33,353,836 (u 1.988) · 9,494,189 nonzero above cap · `dma_high_water` 21,645,536 (the old v4 scoring input, informational floor) |
| VRAM (write-truth peak, post-handoff) | 15,450,112 | 8,388,608 | 1.842 | 16.3 | nz_total 10,116,736 · 6,674,248 above cap — **binding region** |
| ARAM (content volume, fill-excluded, `content_total`) | 3,475,221 | 2,097,152 | 1.657 | 23.7 | address peak 6,053,632 (u 2.887, the pre-v7 gated keying) · 1,709,398 content above cap |

Watermarks (informational, content-scan — stale-data prone): main 33,353,836 ·
vram 15,450,112 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 75.0)

DMA events 446 · total 55.9 MB · unique 16.3 MB · re-read ratio 0.7088 ·
steady-state 4.976 MB/min (`short_window: false`) · PIO 1,049,920 B

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 1,243 · MMIO refs: scif 2, rtc 3, g2ext 151 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc`.
Boot blob carved at base `0x8c020000`, entry `0x8c021000`, header title
`AZUMANGA PB VER1.000`.
SDK strings: Kunoichi2 Library for NAOMI 2.07, syStartKn 2.08, AIPKN 0.91,
Ninja2 2.01.011, KAMUI2 (NEC), manatee.drv 2.50.04 (Sega libraries, Mar 2001
builds) — plus the GD file lists that name the payload directly: `pinup*.bin` /
`photo*.bin` art galleries, `BGM01–11 L/R .p16` stereo PCM pairs, per-character
voice banks (`sakaki.osb`, `kagura.osb`, `yukari.osb`, …).

## 7. Controls (axis: 100.0)

Cabinet: one ball-top 8-way joystick + 1 button per the in-game how-to-play
screen (drawn on-screen in the v2-era capture, `shot-425s.png` — not in the
current curated set); one joystick + two buttons per the
[Azumanga Daioh Wiki](https://azumanga.fandom.com/wiki/Azumanga_Daioh_Puzzle_Bobble).
`controls.device_class = stick`. MAME input ports: `naomi`.
Proposed DC mapping: 1:1 on a stock DC pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`; wiki and
in-game screen as above.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 16.3^.40 · 75.0^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **42.7 (B)**
Similarity inputs: developer no, SDK overlap partial, loader match yes.

## 9. Risks & notes

- **All three regions are over cap under current keys.** VRAM binds (1.842×,
  6.7 MB of real content above cap — the full-screen anime backgrounds, pinup
  galleries and per-character portraits named in the `pinup*`/`photo*` GD file
  lists); ARAM content is 1.657× (11 stereo PCM BGM pairs + voice banks for the
  full anime cast, voice-heavy by design); main content volume is 1.025× — just
  over. A port needs texture halving and an audio trim; main needs only a nudge.
- **The ARAM trim is verified mechanical** (2026-08-04 live dump, fork
  `4b59eceff`, `FLYCAST_ARAMDUMP`, parser `tools/assess/parse_osb.py`; dump not
  committed — copyrighted game data): 5 `SOSB` one-shot banks resident
  (2.33 MiB, 63 tones), every tone-record offset bank-relative, banks stacked
  back-to-back 16-byte-aligned — position-independent blobs by construction;
  the ARM7 driver resolves absolute addresses, game code holds bank bases only.
  Headerless `.p16` BGM sits in the inter-bank gaps and is the natural GD-stream
  candidate. The unblock is a bank rebuild + base move. Caveat: field semantics
  beyond the offsets are an empirical read, not from a spec.
- **Main RAM is address-sparse:** 17.2 MB of content but a write-truth address
  peak of 33,353,836 B (~1.99× cap) — relocation/layout attention needed beyond
  volume trimming.
- Coverage is `demo`, so these are representative attract-gameplay figures, not
  lower bounds — full play could still run marginally higher.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-02 | PARKED G3-ARAM | Full 8 MiB ARAM bank written at boot (4.00× cap) gated before axes; main 1.29× / VRAM 1.84× already flagged as the deeper problem — §6 checkpoint data point (kb §6) |
| v4 | 2026-08-04 | PARKED G3-ARAM | Re-run; fill-excluded ARAM content peak 6,053,632 (u 2.89) still gated; same day the live ARAM dump verified OSB banks position-independent (`parse_osb.py`) |
| v7 | 2026-08-07 | 35.8 (C) | Un-parked: ARAM re-keyed on content volume (kb §6 checkpoint); main write-truth measured for the first time — address peak 33,353,836 (u 1.988) became binding, memory 10.5 |
| v9 | 2026-08-08 | 42.7 (B) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); binding region moved to VRAM, memory 16.3 |
