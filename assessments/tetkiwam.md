# Tetris Kiwamemichi (Japan) (GDL-0020) (`tetkiwam`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **87.5 (S)** |
| Bottom line | The GD-ROM ships a DC-bootable build of this exact game (`TETRIS.BIN` in the disc root — TCRF, §2), and this is the first capture to measure it: with the v7 ARAM-content and v8 VRAM FB-mask fields actually populated (the prior v6 sidecar predated both and scored those regions through conservative peak-keyed fallbacks), all three regions land well under their DC caps — main content 0.52×, VRAM FB-masked fit 0.38×, ARAM content 0.55× — none binding, matching the shipped-build proof even more directly than the v6 fallback numbers did. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `tetkiwam` (covers: no clones — `parent: null` in controls.json, no set lists it as parent). `sgtetris` (Sega Tetris, 1999, `naomim2` cart) is a separate family, not a clone. |
| Maker / year | **Success** (Sega-published arcade; Arika only "heavily influenced" it via the TGM series — [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=tetkiwam)), 2004 |
| Genre / format | Puzzle ★ (Tetris variant, Guideline ruleset — [tetris.wiki](https://tetris.wiki/Tetris_Kiwamemichi)), GD-ROM (GDL-0020, 62.3 MB) |
| Official DC port | No official DC release. PS2 port by Success exists ([Hard Drop](https://harddrop.com/wiki/Tetris_Kiwamemichi); arcadeitalia notes say PS2 2003 and GBA *Tetris Advance* 2003 — year unverified). **But the arcade disc itself contains a DC build** (below). |
| Community ports | **The GD-ROM's root filesystem contains a Dreamcast-bootable `TETRIS.BIN`** — "identical to the Arcade build" except coin-op is live (press Y to insert a coin; not free-play). Documented with a full reproducible recipe at TCRF: [Tetris Kiwamemichi (Arcade)](https://tcrf.net/Tetris_Kiwamemichi_(Arcade)) + [Notes page](https://tcrf.net/Notes:Tetris_Kiwamemichi_(Arcade)): `chdman extractcd -i gdl-0020.chd -o gdl-0020.gdi` → GD-ROM Explorer → "Decrypt and Extract" `TETRIS.BIN` with DES key `62790B91859854C7` → trim the first 0x500 bytes (Naomi DIMM header) → playable DC GDI. The disc even carries `0GDTEX.PVR` (DC audio-CD-player disc art), reused from Success's *Pocke-Kano* — the GD was mastered as a DC-style disc. Scene discussion: [dreamcast-talk t=15366 "NAOMI Rom in GDI"](https://www.dreamcast-talk.com/forum/viewtopic.php?t=15366). Circumstantial circulation evidence: khinsider hosts a rip labeled "[(Naomi) (Dreamcast) (gamerip)](https://downloads.khinsider.com/game-soundtracks/album/tetris-kiwamemichi-naomi-2002-dreamcast-gamerip)". (TCRF content cited via search snippets — direct fetch is bot-trapped, kb §4.o.) |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`, GD DIMM ~1 MB bootstrap) · run 600 s · rom: `naomi/tetkiwam.zip`
Attract/demo reached: **demo** — two-board Tetris attract gameplay confirmed across the capture: `shot-121s.png` ("TARGET" mode round start), `shot-365s.png` ("LINE BREAK" mode, active boards), `shot-548s.png` ("START GAME" round transition); sidecar `capture.coverage = "demo"` (battery writes `null` — set explicitly in this pass after reviewing the shots)
Screenshots: `evidence/tetkiwam/shot-060s.png` · `evidence/tetkiwam/shot-121s.png` · `evidence/tetkiwam/shot-365s.png` · `evidence/tetkiwam/shot-548s.png` · `evidence/tetkiwam/shot-609s.png`
Anomalies: none — single clean leg (`tetkiwam-battery.log`: "leg 1: tetkiwam.zip attempt 1 -> ran full window").

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,643,391 | 16,777,216 | 0.5152 | 100.0 | unchanged byte-for-byte from v6 (main was already volume-keyed) · address peak 32,508,220 (u 1.938, informational) · `nz_above_cap` 7,268,643 of content above the 16 MB line by address is placement, not volume · `dma_high_water` 30,495,872 unchanged |
| VRAM (v8 FB-masked content: `content_total` + 2×`fb_bytes`) | 1,986,720 + 2×614,400 = 3,215,520 | 8,388,608 | 0.3833 | 100.0 | **first real v8 measurement** — v6 had no `content_total`/`fb_bytes` and fell back to raw peak (7,763,712, u 0.9255, sub-score 90.6); nz_total 2,408,482 · `nz_above_cap` 0 |
| ARAM (v7 content volume, `content_total`) | 1,160,242 | 2,097,152 | 0.5533 | 100.0 | **first real v7 measurement** — v6 had no `content_total` and fell back to raw peak (2,031,344, u 0.9686, sub-score 87.4, then the axis-binding region); `nz_above_cap` 0 |

Memory axis = min(100.0, 100.0, 100.0) = **100.0** — no region binds anymore; v6's binding region
(ARAM) moved from a peak-keyed 0.97× near-cap fallback to a content-keyed 0.55× measurement,
same for VRAM's fallback→measured move. Main was unaffected (already volume-keyed pre-v9 for
this title) — its identical numbers are a control on the re-capture itself.

Watermarks (informational, content-scan — stale-data prone): main 32,508,220 ·
vram 9,711,616 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 72.0)

DMA events 1,431 · total 106,876,928 B (101.9 MB) · unique 35,442,688 B (33.8 MB) · re-read ratio
0.6684 · steady-state 8.986 MB/min (`short_window: false`) · PIO 1,115,456 B
(v6: 1,410 events, 105,492,480 B total, reread 0.664, 8.824 MB/min — a fresh capture's normal
run-to-run noise, not a fallback effect; axis moves 72.3→72.0, immaterial)

## 6. Guts (axis: 85.0)

Code 1,114,112 B · functions 3,636 · MMIO refs: scif 25, rtc 3, g2ext 201 ·
BIOS vector refs: none (`extra_bios_classes: 0`) · flags: `eeprom_bios`, `serial`, `rtc`.
Carve base `0x8c020000`, entry `0x8c021000`, header title `TETRIS KIWAMEMITI JAPAN`.
`guts.sdk_strings` shows a fully Katana-adjacent stack — including strings that name the
Dreamcast outright: `Nindows2 for DREAMCAST version %s`, `sd2 for DC Ver 2.50.18`,
`RMC … SEGAKATANA`, Kunoichi2 Library for NAOMI 2.07, Ninja2 2.01, NEC KAMUI2, CRI
ADX/Sofdec.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + buttons, 2 players (solo or concurrent). MAME
input ports: `naomi`. A Tetris variant needs 4-way movement + rotate buttons (inverted
rotation layout is a noted quirk) + start. Proposed DC mapping: d-pad + A/B rotate
(+X/Y), Start — 1:1 on a stock pad. Decisively: the disc's own embedded DC build is
played on a stock DC pad, with coin insert mapped to the Y button (TCRF) — the pad
mapping is not proposed, it shipped.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=tetkiwam)
(8-way joystick + 6-button JVS standard declaration, 2P);
[tetris.wiki](https://tetris.wiki/Tetris_Kiwamemichi) (Guideline ruleset, inverted
rotation buttons, 750 ms post-entry delay);
[TCRF](https://tcrf.net/Tetris_Kiwamemichi_(Arcade)) (embedded DC build, Y = coin).
No in-binary INPUT TEST name strings surfaced in `guts.sdk_strings`.

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 72.0^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **87.5 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes.
Prose note: the shipped Katana build implies the SDK overlap is **full** in reality —
the sidecar's `partial` remains a checkpoint-worthy calibration observation.

## 9. Risks & notes

- **Port-planning takeaway: the shipped DC build and the content numbers now agree.**
  Main content volume is 8.6 MB (u 0.515); the 7,268,643 B of content sitting above the
  16 MB address line is placement, not volume — exactly what the disc's own `TETRIS.BIN`
  (§2) proves a real DC build relocates. ARAM is the binding region at 0.9686×
  (peak-keyed on a pre-v7 sidecar without `content_total`; a volume re-capture can only
  score the same or higher per the scorer's fallback contract).
- **Real-hardware verification flag:** upstream Flycast has an open, undiagnosed,
  hardware-independent freeze in the Naomi version's 2P versus mode after ~1–2 min
  ([flyinghead/flycast#1500](https://github.com/flyinghead/flycast/issues/1500), reported
  2024-05-02; prior report libretro/flycast#965). Attract-mode capture is unaffected, but
  any port claim must exercise 2P versus on real hardware per the working-style rule.
- The main address peak (32,508,220) is close to but not identical with the 64-byte
  `0x1F00000` structure shared by `kurucham`/`ss2005`/`ikaruga` — tetkiwam's own writes
  reach 2,300 B past it (kb §6 item 3). Informational under content keying.
- The embedded DC build is not free-play (coin on Y, per TCRF) — a trivial delta for any
  release-shaped conversion work.
- TCRF is currently bot-trapped for automated fetchers (kb §4.o) — citations here come
  from indexed search snippets; a human-browser archival copy is worth taking.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | 43.5 (B) | First assessment; display-blind capture (stale TA frame), coverage `title` lower bound; main DMA high-water 30.5 MB flagged as suspect vs the disc's DC-bootable `TETRIS.BIN` — kb §4.m, §6 item 3 |
| v4 | 2026-08-04 | 43.3 (B) | Re-capture with demo coverage (the v2 title-⚠ was the headless-era artifact); VRAM peak still carried the BIOS boot-frame block — kb §7 |
| v5 | 2026-08-06 | 43.3 (B) | Pre-`VRAMHANDOFF` sample drop removed the BIOS boot-frame: VRAM 7,763,712 B fits under 8 MB; main high-water unchanged, still binding — kb §9 |
| v6 | 2026-08-07 | 38.1 (C) | Cluster re-run: main re-keyed on write-truth address peak 32,508,220 B (u 1.94); `dma_high_water` byte-identical v5→v6, confirming the GD-title clustering is real per-title — kb §6 item 3 |
| v9 | 2026-08-08 | 82.9 (S) | Scoring-only re-key (no re-capture): main keyed on content volume `nz_total`; binding region moved to ARAM — spec `2026-08-08-main-content-rekey-design.md` |
| v9 | 2026-08-09 | 87.5 S | ranking-groom chunk 2: fresh v9 capture (was v6) — first real measurement of v7 ARAM-content + v8 VRAM FB-mask fields replaces conservative fallbacks; 82.9→87.5 |
