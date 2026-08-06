# Ikaruga (GDL-0010) (`ikaruga`) — portability assessment

> **Battery v5 re-run (2026-08-06): **49.6 (B)** — confirmed; VRAM now truly fits.**
> v5's pre-`VRAMHANDOFF` sample drop (kb §9) replaces the signature-clamped VRAM value
> with a clean measurement: peak 7,535,232 B (0.90×, `nz_above_cap = 0`) — under the DC's
> 8 MB, as the shipped DC port always implied. Main 27,935,968 B still binds the memory
> axis (23.4); final unchanged at 49.6 B. Coverage still title-only (FREE PLAY suppresses
> attract). Sidecar: flycast `ebae3b513`, battery 5.

> **Battery v4 re-assessment (2026-08-04): **49.6 (B)**.**
> v2's G3-aram was the DMPD fill artifact — the old §Gate's "full-bank load" inference was wrong, and its own risk-flag ("gate may be too aggressive") is resolved: the measurement was at fault, not the gate. A v3 interim run also false-parked no-render (cart-DMA-only sampling + 1 MiB threshold vs its 0.96 MiB static title). v4: 49.6 B; ARAM content 1.81 MiB fits DC — as the shipped DC port always implied. Coverage still title-only (FREE PLAY suppresses attract; the v2 doc's calibration-countdown finding stands).
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **49.6 (B)** |
| Coverage | title |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/ikaruga.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 27,935,968 | 16,777,216 | 1.67 |  |
| VRAM (write-truth diff) | 9,711,616 | 8,388,608 | 1.16 | nz_total 1,002,408 |
| ARAM (content, fill-excluded) | 1,897,200 | 2,097,152 | 0.90 | content above cap 0 |

Streaming: 396 DMA events · total 8.6 MB · unique 3.4 MB · re-read 0.6103 · steady 0.128 MB/min
Axes: memory 23.4 · streaming 77.4 · guts 85.0 · controls 100.0 · similarity 70.0 → **final 49.6 (B)**
Screenshots: `evidence/ikaruga/shot-060s.png` · `evidence/ikaruga/shot-365s.png` · `evidence/ikaruga/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

> **Calibration reference — official DC port exists (2002); not a queue entry.**
> This is Calibration B: the control test that decides whether GD-ROM/DIMM
> reads route through the same logged `CARTDMA` path the battery already
> trusts for cart images (proven in Calibration A / `cleoftp`). It answers
> exactly one load-bearing question — does the logged path see GD/DIMM
> traffic at all — and does **not** need a clean numeric score to answer it.

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The calibration's actual target passed: GD/DIMM reads are fully visible through the logged `CARTDMA` path (396 events, reproduced identically across a 360 s and a 600 s run) — no C++ instrumentation change needed. The game separately gates at **G3** because its ARAM write-truth peak (8 MiB) is exactly 4× the DC's 2 MiB AICA RAM; this is real, deterministic cart data, not a battery defect, and does not affect the GD-path finding. |
| Assessed | 2026-08-02 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ikaruga` (covers: no clones — `parent: null` in controls.json) |
| Maker / year | Treasure, 2001 |
| Genre / format | Shmup, GD-ROM |
| Official DC port | Yes (2002) — `GAME_FORMATS.md:55`; released exclusively in Japan, 2002-09-05, publisher Entertainment Software Publishing — en.wikipedia.org/wiki/Ikaruga (accessed 2026-08-02) |
| Community ports | None found for this exact Naomi GD-ROM set. |
| Representative choice | Not a representative pick — this is the GD-ROM calibration control: the second half of the pair (with `cleoftp`, a cart-format known-good) that establishes the battery reads GD/DIMM streaming correctly before it is trusted on any GD-ROM set in the queue. |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/ikaruga.zip`
Attract/demo reached: **no**. Three-state capture, both timed from handoff (t=30.0 s):
- **Calibration screen** (画面の明度調整 / brightness-contrast adjustment, cabinet setup UI) from handoff to t≈330 s. Countdown observed at 270 (t=60s) and 24 (t=306s) — an exact 1-count/sec decrement, hitting 0 (auto-start) at t=330 s.
- **Title screen** (斑鳩 IKARUGA, © TREASURE 2001, "PRESS START BUTTON", FREE PLAY) from t≈330 s to the end of the 600 s capture. Across the 5 post-title frames in the full 10-shot capture (368s-606s), only the "PRESS START BUTTON" line blinks on/off (2 alternating frame hashes, directly observed across the capture session's 10-shot series, 2026-08-02) — no attract/demo gameplay loop ever starts, consistent with the cabinet being set to FREE PLAY. The two frames kept as evidence here, `shot-368s.png` and `shot-606s.png`, are themselves **byte-identical** — `md5 fd6641f8bc5fa794cd4c8fcc551ddd0b` for both — despite being 238 s apart — the screen was pixel-for-pixel unchanged for that entire span, the strongest single proof available that no attract content ever plays.
- No demo/attract state exists in this capture at any length tried (360 s and 600 s both stop at the same static title screen).

Screenshots:
- `assessments/evidence/ikaruga/shot-060s.png` — calibration screen, countdown 270
- `assessments/evidence/ikaruga/shot-306s.png` — calibration screen, countdown 24 (last frame before auto-start)
- `assessments/evidence/ikaruga/shot-368s.png` — title screen, "PRESS START BUTTON" visible
- `assessments/evidence/ikaruga/shot-606s.png` — title screen, end of 600 s capture — **byte-identical to `shot-368s.png`** (same md5, 238 s earlier): proves the extra 240 s bought by the v2 default (600 s vs. v1's 360 s) added only idle title time, not new game state.

Anomalies: none relative to expected Naomi boot behavior (the brightness-calibration screen is standard Naomi cabinet setup, not a fault). Two full battery runs (360 s v1, 600 s v2) both booted cleanly on the first attempt — no `no-handoff-120s` flake this session.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly 8 MiB, `nz_above_cap = 6,291,456 B`) against the DC's 2 MiB (`2,097,152 B`) AICA RAM cap → utilization 4.00×, more than double `score.py`'s `region_score()` gate threshold (`u > 2.0` → `None`), so `memory_axis()` returns gated on `aram` before any other axis is computed; `sc["scores"]` is `null`.

Evidence: `assessments/ikaruga.metrics.json` → `memory.aram` (both the 360 s and 600 s runs, bit-identical); `guts.sdk_strings` lists dozens of `MIDI_*`/`SFX_*`/`OS_*` sound-driver asset names consistent with a large ARAM sound bank; the peak is reached during the calibration/boot window (before t≈330 s), not during any measured gameplay (see §3/§9 — the game never reaches gameplay in this capture).

What would unblock it: nothing the battery can measure further without gameplay capture — the value is a full-bank load, not a growth trend, so a longer run would not change it (confirmed: identical 8,388,608 across 360 s and 600 s). Real unblocking would require either (a) a per-title audio-asset trim (the official DC port did exactly this — see §Risks) or (b) a scoring-side reconsideration of how hard ARAM overflow should gate vs. other regions (flagged below, not changed here).

Informational axis values computed directly via `tools/assess/score.py`'s helpers for context (not part of `sc["scores"]`, since the pipeline stops at the gate): memory sub-scores main=23.4 (u=1.665, DMA high-water 27,935,968 B / 16 MB), vram=99.1 (u=0.812, write-truth peak 6,814,341 B / 8 MB, `nz_above_cap=0`), aram=gated (u=4.00); guts=85.0 (`eeprom_bios`/`serial`/`rtc` penalties, 2104 functions); controls=100.0 (`stick`); streaming=77.4 (dma_events=396, steady 0.132 MB/min, re-read ratio 0.6103); similarity=70.0 (developer match false — Treasure ≠ Altron/Taito reference — sdk_overlap partial, cart_loader_match true).

## Risks & notes

- **GD-path visibility — the actual point of this calibration — PASSED.** `streaming.dma_events = 396` (> 0) in both the 360 s and 600 s runs, with identical `total_bytes`/`unique_bytes`/`reread_ratio` — GD-ROM/DIMM reads route through the same logged `CARTDMA` path as cart images (`cleoftp`, Calibration A). The brief's contingency (patching `gdcartridge.cpp` to add a `cartlog` call and rebuilding Flycast) is **not needed**: the existing `Naomi_DmaStart` instrumentation already sees GD-ROM traffic.
- **VRAM and streaming figures in this sidecar are lower bounds, not the game's real peak.** The capture never leaves the title screen (§3) — no level, no enemy waves, no bullet-hell rendering ever ran. `vram.peak = 6,814,341 B` and `streaming.dma_events = 396` reflect boot + title-screen assets only; real gameplay would very likely push both higher. Any future re-score of this title needs an input-driven capture (start a credit, hold the game past title) to get real gameplay figures.
- **ARAM is the opposite case — likely NOT understated.** The full 8 MiB write-truth peak is reached during the calibration/boot window, before the title screen even appears (bit-identical across both run lengths) — the same pattern as Calibration A's `cleoftp`, where the ARAM peak was also a boot-time asset load, not a gameplay accumulation (`../cleopatra/docs/kb/phase2-measurements.md`). This is Naomi's sound driver loading its full bank at startup, not a growth curve a longer capture would extend further.
- **The G3 ARAM gate may be too aggressive specifically for the ARAM axis.** Ikaruga's official Dreamcast port (2002) shipped and ran within the DC's real 2 MiB ARAM — i.e., a real, released port already achieved the 4× sound-data reduction this sidecar's raw Naomi asset size implies is needed. That's evidence a raw "Naomi asset size > 2× DC capacity ⇒ hard gate" reading can flag a title as blocked when a shipped port proves the reduction is achievable. Flagged for a future `score.py` revision (e.g., a softer ARAM curve, or weighting ARAM overflow against known DC-port precedent) — **no scoring code was changed for this task**; the gate stands as measured.
- **Free-play title-idle-without-demo is likely not unique to Ikaruga.** This session's cabinet is configured FREE PLAY (visible in every screenshot), which appears to suppress the attract/demo loop entirely — the capture sits on a blinking "PRESS START BUTTON" title for the full 600 s with zero attract content. Other GD-ROM/cart sets in the library may share this configuration. `RUNBOOK.md`'s representativeness check should record which of the three states (calibration screen / title screen / attract-demo) a capture actually reached, not just a yes/no "attract reached" flag — a title-screen-only capture is a materially different measurement than a real attract-demo capture, even though both count as "boots fine."
- Main-RAM v1 limitation (carried from spec, applies here too): the DMA high-water measure only sees cart-DMA'd data; CPU-written data placed above the last DMA'd asset is not captured. Not separately re-verified for this title (no per-title dynamic-SP logging was done, unlike `cleoftp`'s Phase 3 pass).
- Determinism check (informal, not the brief's Step 4): main/vram/aram peaks, `nz_above_cap`, `guts.functions` (2104), and `guts.flags` all reproduced bit-identically between the 360 s (v1) and 600 s (v2) runs; the only figure that moved was the streaming steady-state rate (0.275 → 0.132 MB/min), which is pure dilution from the extra idle title-screen time, not new activity.
