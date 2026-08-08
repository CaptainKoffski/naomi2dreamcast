# Kasei Channel Mars TV (Japan) (840-0025C) (`marstv`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 74.6 (A), was 47.6 (B)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 9,091,782 B (content-u 0.542) replaces peak 25,984,736 B (u 1.549).
> Memory axis 86.6, binding region now **aram** (was memory 28.0). Verdict section below is the capture-time (v≤8) record.

> **Battery v8 vram-fb-masking re-run (2026-08-07): 47.6 (B)** — spec
> `2026-08-07-vram-fb-masking-design.md`. Sidecar: flycast `f014a410c`, battery 8. No
> park, boot ok, PIO handoff at 20.0 s — earlier than v4's 30.0 s (handoff-detection
> timing moved, not the game; the main/aram raw figures below are unaffected). Main RAM
> reproduces bit-identically to v4 (25,984,736 B). ARAM `content_total` 2,053,563 B
> (u=0.979, sub 86.6) is measured by
> volume for the first time (v7-class keying — this doc never ran v6/v7 individually).
> **VRAM flips from address high-water (14,350,336 B, u=1.71, sub 21.6) to FB-masked
> content: `content_total` 5,047,259 B + `2×fb_bytes` 1,228,800 B (`fb_bytes` 614,400 B,
> exactly 640×480×2) = fit 6,276,059 B, u=0.748 → sub 100.0** — a rise, as required.
> Main RAM's write-truth sub-score (28.0, u=1.548) is now the binding region, exactly the
> design doc's predicted "main 28.0 becomes binding". Memory axis **21.6 → 28.0**, final
> **42.8 → 47.6**, tier unchanged **B**. Sanity clean: `fb_bytes` == 614,400,
> `content_total + fb_masked_nz` matches `nz_total` exactly in the raw log
> (5,047,259 + 594,393 = 5,641,652). Coverage re-annotated `demo` (unchanged — display
> blindness from the v2 era stays fixed, as it was under v4).

> **Battery v4 re-assessment (2026-08-04): **42.8 (B)**.**
> v2 parked it G3-aram; the park note already flagged "content above cap only 80 KB: gate-metric divergence". v4's content metric vindicates that: 42.8 B.
> Below the v8 section is the battery v4-era assessment, itself superseding the v2-era
> assessment below that; each section's *measured* figures (boot evidence, memory,
> streaming, score) are **superseded** by the section above it — the identity,
> controls-research and similarity sections remain valid throughout. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v8 verdict & measurements

| | |
|---|---|
| **Final** | **47.6 (B)** |
| Coverage | demo |
| Assessed | 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/marstv.zip` |

| Region | Peak / fit | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 25,984,736 | 16,777,216 | 1.548 | bit-identical to v4's DMA-high-water figure — write-truth found nothing beyond it here; sub 28.0, now binding |
| VRAM (FB-masked content + 2×FB) | 6,276,059 (content_total 5,047,259 + 2×fb_bytes 1,228,800) | 8,388,608 | 0.748 | battery v8 re-keying — sub 100.0, was 21.6 under address high-water (14,350,336, u=1.71) |
| ARAM (content, volume-keyed) | 2,053,563 | 2,097,152 | 0.979 | sub 86.6, first content-volume measurement (v7-class keying); was 1.02× / content above cap 47,694 under the old address peak |

Streaming: 164 DMA events · total 199.8 MB · unique 52.4 MB · re-read 0.7376 · steady 20.991 MB/min (matches v4's 21.076 within run-to-run noise)
Axes: memory 28.0 · streaming 54.3 · guts 90.0 · controls 100.0 · similarity 40.0 → **final 47.6 (B)**
Screenshots: `evidence/marstv/shot-060s.png` · `shot-365s.png` · `shot-609s.png` (same 3-shot curation as v4 — title/eerie-face screen ×2, attract camera-minigame instructions)

---

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **42.8 (B)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 30.0 s · run 600 s · rom `naomi/marstv.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 25,984,736 | 16,777,216 | 1.55 |  |
| VRAM (write-truth diff) | 14,350,336 | 8,388,608 | 1.71 | nz_total 5,788,726 |
| ARAM (content, fill-excluded) | 2,147,400 | 2,097,152 | 1.02 | content above cap 47,694 |

Streaming: 164 DMA events · total 199.8 MB · unique 52.4 MB · re-read 0.7376 · steady 21.076 MB/min
Axes: memory 21.6 · streaming 54.2 · guts 90.0 · controls 100.0 · similarity 40.0 → **final 42.8 (B)**
Screenshots: `evidence/marstv/shot-060s.png` · `evidence/marstv/shot-365s.png` · `evidence/marstv/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB) and `score.py` gates on the peak — the **twelfth** boot-time full-bank G3-aram park and, at 1999, the **earliest**: full-bank behavior now spans the platform's whole life. But this park is the campaign's strongest evidence that the gate is measuring the wrong thing: nonzero content above the DC cap is only **81,598 B** (~80 KB, trivially trimmable) — every earlier full-bank title had MBs up there. A content-based gate (`nz_above_cap`) would let marstv through with essentially DC-fitting sound; see the Gate section and kb §6 item 5. The real memory loads are VRAM 1.70× and main 1.55×, and the title is display-blind under our fork (frozen splash while it demonstrably runs underneath, kb §4.m class). |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `marstv` (covers: no clones — `parent: null` in controls.json; single GAME line, naomi.cpp @59e7c0b line 10969). M2-type cart 840-0025C, boot ROM `epr-22993.ic22` (2 MB, reloaded) + 15×64 Mb mask ROMs, M2 crypt key `280b8ef5` (317-0274-JPN) — ROM_START lines 5449–5474, comment table line 384 (no special-I/O note). arcadeitalia's "NAOMI GD-ROM" platform label and "BAD DUMP" flag are both wrong: it is a cart, and **0** `BAD_DUMP` flags appear in the ROM_START block (verified @59e7c0b) — same spurious-label class as `inunoos` |
| Maker / year | Sega (MAME GAME line), developed by Sega AM3 ([Play:Right](https://www.playright.dk/arcade/titel/kasei-channel-mars-tv)), 1999 |
| Genre / format | Party — 3-player variety/minigame collection, 16 minigames (button-mashing, timing, reflex, quiz; described in Japan as "セガ版ビシバシ", Sega's Bishi Bashi), **cart** — M2 840-0025C, 57.8 MB |
| Official DC port | No — Japan-only arcade, no home version on any platform ([lifeshipsailing red-data-book entry](https://www.lifeshipsailing.net/entry/2019/05/16/220000): 移植なし / no ports, conservation status "extinct"; no home SKU on [Giant Bomb](https://www.giantbomb.com/kaizen-channel-mars-tv/3030-69400/) or [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37524-kaizen-channel-mars-tv)) |
| Community ports | None found (searched 2026-08-03) — noted as never ported in the [Dreamcast Junkyard Naomi-conversion article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html); no dreamcast-talk/Reddit conversion threads. **Name-variant trap for future searches:** databases misspell it "Kaisen" (arcade-history) and "Kaizen" (LaunchBox, Giant Bomb); correct romanization is Kasei (火星 = Mars), Japanese sources also use just 火星チャンネル |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 40.0 s · run 600 s · rom: `naomi/marstv.zip` (single clean zip leg)
Attract/demo reached: **title (conservative)** — sidecar `capture.coverage = "title"`;
visual classification is impossible (see Display blindness), so the lower-bound label is
used even though activity metrics show the game running for the full window.

### Display blindness

All 10 battery screenshots are one identical image (single MD5
`2a3564fc6aea6b69aab2a6de1e03fe81` across all 10) — the frozen NAOMI cart-boot splash
(orange-ring "NAOMI™" logo on white). That is a stale TA frame in the GL display path
(kb §4.m class, same as `kurucham`/`ss2005`/`inunoos`), not a hang: underneath it the
game demonstrably runs — BIOS handoff at 40.0 s, 141 cart DMA events / 177,912,960 B
streamed across the window (**the campaign's highest streaming volume to date**), the
full 8 MiB ARAM bank written, and 5,048,671 B of nonzero VRAM content
(`memory.vram.nz_total`).

Screenshots kept (first + last, identical splash, proving the freeze):
- `assessments/evidence/marstv/shot-060s.png` — frozen NAOMI splash at t=60 s
- `assessments/evidence/marstv/shot-603s.png` — same splash at t=603 s, unchanged
Anomalies: display blindness as above; nothing else.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate. **Twelfth** boot-time full-bank load in
the kb §6 tally — and the **earliest**: at 1999 it pushes full-bank behavior back to the
platform's first year; the practice now spans Naomi's whole life (1999–2009).

**But this park exposes a measurement divergence — the strongest single argument yet
that the G3-aram gate metric should be `nz_above_cap`, not peak.**
`memory.aram.nz_above_cap = 81,598 B`: the nonzero content above the DC's 2 MiB is
~80 KB, trivially trimmable. Every earlier full-bank title in the tally had MBs of real
content up there (azumanga 6.2 MB, ss2005 6.29 MB, illvelo 6.29 MB, inunoos 4.53 MB…);
marstv's watermark was pushed to the top of the bank by something near-empty (zero-fill
or test-pass class), not by sound data. The gate fires on peak; a content-based rule
would let marstv through with essentially DC-fitting sound. Recorded as kb §6 item 5 —
and re-scoring all parked sidecars under a content rule requires no re-runs, since
`nz_above_cap` is already in every sidecar.

What would unblock it: under a content-based ARAM rule, nothing audio-side — the ~80 KB
trim is noise. The real memory work is elsewhere: VRAM peak `14,235,648 B` (1.70× the
8 MB cap, and unlike the kurucham pattern with real content above it —
`nz_above_cap = 2,664,632 B` of `nz_total = 5,048,671 B`) and main-RAM DMA high-water
`25,984,736 B` (1.55× the DC's 16 MB; watermark identical at 25,984,736 B — no gap).

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at
the gate): streaming 141 DMA events, 177,912,960 B total / 54,971,872 B unique, re-read
ratio 0.691, steady-state 18.165 MB/min (`short_window: false`); guts **works** (M2
cart, `dat_available: true`): 2,097,152 B code, 1,473 functions, MMIO refs scif 0 /
rtc 4 / g2ext 248, flags `eeprom_bios`/`rtc`; similarity inputs
`developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

## Controls (researched — recorded for the record)

Sidecar `controls.device_class` set to **`stick`** (the G3 gate fires before controls in
`score.py`, so the class is recorded, not scored).

**Buttons only — no stick, no special hardware.** First title in the campaign with a
*dedicated* per-title MAME INPUT_PORTS (naomi.cpp @59e7c0b lines 1567–1584, `marstv`):
per player Start + three differently-sized buttons — "Red Large Button 大", "Yellow
Medium Button 中", "Blue Small Button 小" — everything else `IPT_UNUSED`. The size-graded
buttons are the Bishi Bashi-style cabinet gimmick; electrically they are three plain
digital buttons. The comment `// TODO: Player 3` marks the cabinet's third player as
not yet wired in MAME; the in-binary INPUT TEST screen (`guts.sdk_strings`:
`"PLAYER      1P      2P      3P"`) confirms 3-player, as do operator photos of the
dedicated cabinet. No special I/O: no comment in the naomi.cpp table (unlike
Samba/Marine Fishing rows), no extra firmware in the ROM set, and no marstv
special-casing in Flycast's `maple_jvs.cpp`/`naomi_roms_input.h` — stock JVS digital.

Ladder reading: the spec §4.4 top rung is "standard stick/buttons (incl. up to 4
players — DC has 4 ports)". This is *less* than standard — 3 buttons + Start map 1:1
onto A/B/X + Start on a stock pad, and 3 players fit the DC's 4 ports. Genre precedent:
Konami's Bishi Bashi Special shipped on PS1 standard pads. Note for a port: P3 input is
unmapped in current MAME and Flycast (emulation gap, not a hardware one).

Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `marstv` (1567–1584);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=marstv)
(declared "Buttons only", 3 buttons);
[games.sakura-marche.com](https://games.sakura-marche.com/ac-mars-channel/) (3人同時プレー,
16 minigames); [lifeshipsailing](https://www.lifeshipsailing.net/entry/2019/05/16/220000)
("Sega's Bishi Bashi"); [Play:Right](https://www.playright.dk/arcade/titel/kasei-channel-mars-tv)
("Big button" controls, 3 players);
[Game Center Technopolis on X](https://x.com/GC_Tecnopolis/status/2002210874782851094)
(dedicated cabinet, 3-player simultaneous); in-binary INPUT TEST strings
(`assessments/marstv.metrics.json` → `guts.sdk_strings`). Sega's official history page
exists at https://www.sega.jp/history/arcade/product/9901/ (Cloudflare-blocked to
fetches; cited for existence).

## Risks & notes

- **Even with a content-based ARAM rule, two regions still need real reduction:** VRAM
  1.70× with 2.66 MB of genuine content above the cap, and main RAM 1.55×. The park
  gate is arguably wrong for this title; the memory work is not.
- **Heaviest streaming in the campaign:** 177.9 MB total over 600 s, 18.165 MB/min
  steady-state, re-read 0.691 — from a cart. A GD-ROM-based port needs seek/throughput
  attention more than any title measured so far.
- **Display-path gap blocks emulator validation** (kb §4.m): the fork shows a stale TA
  frame while the game draws 5 MB of content elsewhere. Per the working-style rule,
  rendering must be verified on real DC hardware; emulator-side diagnostic is the
  raw-VRAM decode recipe (`FLYCAST_VRAMDUMP` + `vramdump2png.py`).
- MAME status is the blanket `GAME_FLAGS` macro (kb §4.r) — no per-title signal;
  arcadeitalia's "preliminary / imperfect gfx+sound" mirrors the driver-wide boilerplate,
  and its "GD-ROM" + "BAD DUMP" labels are refuted in §2.
- Early-Naomi SDK snapshot in `guts.sdk_strings`: `nlam Ver 1.00 Build:Oct 28 1999` +
  `libintr Ver 1.051` — a 1999 library stack, useful as the campaign's earliest SDK data
  point.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (here watermark = high-water exactly, so no observed gap).
