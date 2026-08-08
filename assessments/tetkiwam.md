# Tetris Kiwamemichi (Japan) (GDL-0020) (`tetkiwam`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 82.9 (S), was 38.1 (C)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v6 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 8,643,391 B (content-u 0.515) replaces peak 32,508,220 B (u 1.938).
> Memory axis 87.4, binding region now **aram** (was memory 12.5). Verdict section below is the capture-time (v≤8) record.

> **Battery v6 cluster re-run (2026-08-07): **38.1 (C)** — this doc's own §9 clustering
> flag is now ANSWERED.** v6 scores main RAM on the write-truth `peak` (`MAINPROFILE`
> snapshot+diff) instead of `dma_high_water`; the old `dma_high_water` figure
> (30,495,872 B) reproduces **byte-identical to v5** — the suspicious kurucham/ss2005/
> takoron/tetkiwam clustering §9 flagged is confirmed real per-title, not run noise (kb
> §6 item 3). The DC-bootable-`TETRIS.BIN` tension §9 raised is now quantified rather
> than qualitative: the write-truth main peak is 32,508,220 B, with **7,268,643 B
> (7.27 MiB) of changed content sitting above the DC's 16 MB cap** — yet the disc ships
> an actual DC build of this exact game (TCRF, §2). ARAM/VRAM are unchanged and still fit
> (ARAM `nz_above_cap` 0, VRAM `nz_above_cap` 0). Tier drop B→C is the main-axis
> definition change (same story as `kurucham`/`ss2005`), not new content or a retraction
> of the TETRIS.BIN evidence. Findings: `docs/kb/assessment-tooling.md` §6 item 3
> (2026-08-07). Sidecar: flycast `65f9f7857`, battery 6, `handoff.trigger = "pio"` (GD
> DIMM ~1 MB bootstrap).

## v6 verdict & measurements

| | |
|---|---|
| **Final** | **38.1 (C)** |
| Coverage | demo |
| Assessed | 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s (trigger=pio) · run 600 s · rom `naomi/tetkiwam.zip` |

| Region | v6 peak (scored) | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 32,508,220 | 16,777,216 | 1.94 | nz_total 8,643,391 · nz_above_cap 7,268,643 · dma_high_water 30,495,872 (1.82×, byte-identical to v5) |
| VRAM (write-truth) | 7,763,712 | 8,388,608 | 0.93 | nz_total 2,408,482 · nz_above_cap 0 |
| ARAM (content, fill-excluded) | 2,031,344 | 2,097,152 | 0.97 | content above cap 0 |

Streaming: 1410 DMA events · total 105.5 MB · unique 35.44 MB · re-read 0.664 · steady 8.824 MB/min
Axes: memory 12.5 · streaming 72.3 · guts 85.0 · controls 100.0 · similarity 70.0 → **final 38.1 (C)**
Screenshots: `evidence/tetkiwam/shot-060s.png` · `evidence/tetkiwam/shot-365s.png` · `evidence/tetkiwam/shot-609s.png`

Note: the shared `0x1F00000` 64-byte structure seen on `kurucham`/`ss2005`/`ikaruga`
does not exactly match here — tetkiwam's own writes reach 2,300 B past it
(32,508,220 vs 32,505,920), still worth flagging as the same structural family (kb §6
item 3, §8 discipline — no exclusion without a control-run proof). See §9 below for the
full DC-bootable-build discussion, now updated with the v6 numbers.

---

> **Battery v5 re-run (2026-08-06): **43.3 (B)** — confirmed; VRAM artifact gone.**
> v5's pre-`VRAMHANDOFF` sample drop (kb §9) removes the BIOS boot-frame block from the
> VRAM peak: now 7,763,712 B (0.93×, fits under 8 MB — vindicating the v2-era §4
> argument), vs the v4 table's artifact-inflated 9,711,616 B. Main 30,495,872 B still
> binds (memory 17.3); ARAM 2,031,344 B; final unchanged at 43.3 B, coverage demo.
> Sidecar: flycast `ebae3b513`, battery 5.

> **Battery v4 re-assessment (2026-08-04): **43.3 (B)**.**
> 43.3 B (was 43.5 on v2), now with demo coverage — two-board Tetris attract runs (shot-365s); the v2 title-⚠ was the headless-era artifact.
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **43.3 (B)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/tetkiwam.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 30,495,872 | 16,777,216 | 1.82 |  |
| VRAM (write-truth diff) | 9,711,616 | 8,388,608 | 1.16 | nz_total 2,388,788 |
| ARAM (content, fill-excluded) | 2,031,344 | 2,097,152 | 0.97 | content above cap 0 |

Streaming: 1446 DMA events · total 102.8 MB · unique 33.8 MB · re-read 0.6712 · steady 9.098 MB/min
Axes: memory 17.3 · streaming 71.8 · guts 85.0 · controls 100.0 · similarity 70.0 → **final 43.3 (B)**
Screenshots: `evidence/tetkiwam/shot-060s.png` · `evidence/tetkiwam/shot-365s.png` · `evidence/tetkiwam/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **43.5** (B) |
| Bottom line | The numeric score materially understates this title: the Naomi GD-ROM **ships a Dreamcast-bootable build of the game** (`TETRIS.BIN` in the disc root — TCRF, §2/§9), which is empirical, shipped-product proof the game runs on a real DC with 16 MB main RAM. Both measured DC-region budgets fit (ARAM peak exactly 2 MiB, VRAM 7.76 MB < 8 MB); the sole over-budget axis — main-RAM DMA high-water 1.82× — is therefore a v1 measurement artifact (Naomi high RAM used as GD stream cache, the spec's known limitation), not a porting cost. Score left untouched per campaign rules; recorded as a checkpoint calibration data point (kb §6 item 3). Ground-truth portability is arguably the best in the queue — the "port" already exists on the disc. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/tetkiwam.zip` (single clean zip leg)
Attract/demo reached: **title (conservative lower bound)** — sidecar
`capture.coverage = "title"`; visual classification is impossible (see Display blindness),
but activity metrics show the game running for the full window.
Screenshots: `assessments/evidence/tetkiwam/shot-060s.png`, `shot-606s.png` (curated first + last).
Anomalies: display blindness (below); otherwise a clean single-leg run.

### Display blindness

All 10 battery screenshots show the same frozen NAOMI GD-ROM SYSTEM splash (first and
last kept — identical at t=60 s and t=606 s). That is a **stale TA frame** left in the GL
display path (kb §4.m class, same as `kurucham`/`ss2005`), not a hang: underneath it the
game verifiably runs — BIOS handoff at 30.0 s, 1,356 GD DMA events / 99,764,224 B
streamed across the window, ARAM written to exactly 2 MiB, and 2,292,917 B of nonzero
VRAM uploads (`memory.vram.nz_total`). MAME flags the set preliminary / imperfect
graphics + sound ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=tetkiwam)) —
consistent with a title that trips emulator display paths. The score remains valid
because memory/streaming/guts measure real game activity, none of which depends on
rendering.

## 4. Memory fit (axis: 17.3)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 30,495,872 B | 16 MB | 1.82× | 17.3 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 7,763,712 B | 8 MB | 0.93× | 90.6 | grep `VRAMPROFILE` |
| ARAM (write-truth) | 2,097,152 B | 2 MB | 1.00× | 85.0 | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 32,508,220 /
vram 7,763,712 / aram 2,097,152. Main watermark 1.07× the DMA high-water — mild.

The region pattern is the doc's key evidence: **ARAM peaks at exactly 2,097,152 B — the
DC's AICA capacity to the byte, with `nz_above_cap = 0`** — and **VRAM fits under the DC's
8 MB** (`nz_above_cap = 0`, nonzero content 2,292,917 B). Sound and video were authored
inside DC budgets. Only main RAM reads over (1.82×), and §9 argues that number is a
measurement artifact for this title, not real footprint: the shipped DC build proves the
game runs in 16 MB.

## 5. Cart streaming (axis: 73.4)

DMA events 1,356 · total 99.76 MB · unique 35.41 MB · re-read ratio 0.645 ·
steady-state 8.353 MB/min (full window, `short_window: false`)

## 6. Guts (axis: 85.0)

Code 1,114,112 B · functions 3,636 · MMIO refs: scif 25, rtc 3, g2ext 201 ·
BIOS vector refs: none extra (`extra_bios_classes: 0`) · penalties applied:
`eeprom_bios`, `serial`, `rtc` → 85.0

`guts.sdk_strings` shows a fully Katana-adjacent stack — including strings that name the
Dreamcast outright: `Nindows2 for DREAMCAST version %s`, `sd2 for DC Ver 2.50.18`,
`RMC … SEGAKATANA`, Kunoichi2 Library for NAOMI 2.07, Ninja2 2.01, NEC KAMUI2, CRI
ADX/Sofdec. Carve header title: `TETRIS KIWAMEMITI JAPAN`.

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
      = 17.3^.40 · 73.4^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **43.5** (tier B)
Similarity inputs (sidecar): developer no, SDK overlap partial, loader match yes.
Prose note: the shipped Katana build implies the SDK overlap is **full** in reality —
the sidecar's `partial` is another checkpoint-worthy calibration observation.

## 9. Risks & notes

- **The main-RAM axis overcounts this title — shipped-product counter-evidence.** The
  GD-ROM ships a DC-bootable `TETRIS.BIN` (§2, TCRF), i.e. the game demonstrably runs on
  real DC hardware with 16 MB main RAM. The measured 30,495,872 B DMA high-water (1.82×)
  can therefore only be Naomi-side behavior — the game using high Naomi RAM as a GD
  streaming cache — which is exactly the spec's known v1 limitation (DMA high-water
  measures where assets land, not the working set). Corroboration: ARAM peaks at exactly
  the DC's 2 MiB with nothing above the cap, and VRAM fits under 8 MB — the content was
  authored to DC budgets. **The score is deliberately not hand-adjusted** (campaign
  comparability); the tension is recorded for the scoring checkpoint (kb §6 item 3),
  where the suspicious clustering of main high-waters across GD titles (kurucham 27.4 /
  ss2005 27.5 / takoron 29.4 / tetkiwam 30.5 MB) is also noted.
  **ANSWERED by the battery v6 cluster re-run (2026-08-07):** the clustering reproduces
  per-title — this title's own `dma_high_water` is byte-identical between v5 and v6
  (30,495,872 B) — so it was never run noise; see
  `docs/kb/assessment-tooling.md` §6 item 3 for the full four-title comparison. v6 also
  adds a write-truth content number the v1 metric couldn't give: **7,268,643 B
  (7.27 MiB) of changed main-RAM content sits above the DC's 16 MB cap**
  (`memory.main.nz_above_cap`, v6 sidecar) even though the disc's own `TETRIS.BIN` proves
  the game runs in 16 MB — quantifying, not resolving, the tension above. The v6 main
  peak (32,508,220 B) is close to but not identical with a 64-byte structure
  (`0x1F00000`–`0x1F0003F`, peak 32,505,920) shared by `kurucham`/`ss2005`/`ikaruga` —
  tetkiwam's own writes reach 2,300 B past it, so it is a related-but-not-identical
  signature candidate (kb §6 item 3, §8 discipline: no exclusion without a control-run
  proof).
- **Real-hardware verification flag:** upstream Flycast has an open, undiagnosed,
  hardware-independent freeze in the Naomi version's 2P versus mode after ~1–2 min
  ([flyinghead/flycast#1500](https://github.com/flyinghead/flycast/issues/1500), reported
  2024-05-02; prior report libretro/flycast#965). Attract-mode capture is unaffected, but
  any port claim must exercise 2P versus on real hardware per the working-style rule.
- **Display blindness** (§3): no visual validation is possible in our fork today — the
  same stale-TA-frame class as `kurucham`/`ss2005` (kb §4.m); coverage is the
  conservative `title` lower bound, so peaks could be understated vs. played gameplay.
- The embedded DC build is not free-play (coin on Y, per TCRF) — a trivial delta for any
  release-shaped conversion work.
- TCRF is currently bot-trapped for automated fetchers (kb §4.o) — citations here come
  from indexed search snippets; a human-browser archival copy is worth taking.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (main watermark 1.07× high-water — mild here).
