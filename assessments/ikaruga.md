# Ikaruga (GDL-0010) (`ikaruga`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **88.7 (S)** |
| Bottom line | The GD-ROM calibration control with an official 2002 DC port — under content keying every region fits with headroom (memory axis 100.0; the informational VRAM address peak at 0.898× cap is the closest approach), so the S rank chiefly confirms what the shipped DC port already proved; coverage is title-only because FREE PLAY suppresses the attract loop. |
| Assessed | capture 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`, `pio_bytes` 1,049,920 B — byte-identical
to Calibration A's cleoftp figure: the GD DIMM bootstrap PIO-loads the same ~1 MB boot
segment on every GD title before its first cart DMA) · run 600 s · rom: `naomi/ikaruga.zip`
Attract/demo reached: **title only** — brightness-calibration countdown (画面の明度調整,
standard Naomi cabinet setup; exact 1-count/sec decrement to auto-start), then a static
斑鳩 IKARUGA title screen (© TREASURE 2001) where only the "PRESS START BUTTON" line blinks;
the cabinet is configured FREE PLAY, which suppresses the attract/demo loop entirely — no
attract content plays at any run length tried (360 s and 600 s, v2 finding).
`capture.coverage = "title"`.
Screenshots: `evidence/ikaruga/shot-060s.png` · `shot-304s.png` (calibration countdown,
256 → 13) · `shot-365s.png` · `shot-609s.png` (title screen, the two blink states).
Anomalies: none — reproduction across runs is bit-exact (v8 vs v6: main/VRAM/ARAM peaks
identical to the byte, only the blink-state screenshot alternates).

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 2,959,601 | 16,777,216 | 0.1764 | 100.0 | address peak 32,505,920 (u 1.938, informational): content splits into ~1.34 MiB at 0.26–2.36 MB plus a ~1.49 MiB band at 25.7–28.6 MB (`nz_above_cap` 1,558,254) — MAINHIST, v6 · `dma_high_water` 27,935,968 (its implied ~9 MB above cap is re-writes of identical bytes, discounted by snapshot+diff) |
| VRAM (FB-masked content + 2×FB) | 1,727,325 | 8,388,608 | 0.2059 | 100.0 | `content_total` 498,525 + 2×`fb_bytes` 614,400 (exactly 640×480×2) · address peak 7,535,232 (u 0.898, informational — closest approach to any cap) · `nz_above_cap` 0 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,517,703 | 2,097,152 | 0.7237 | 100.0 | address peak 1,897,200 (u 0.905, informational) · `nz_above_cap` 0 |

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 ·
vram 9,711,616 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content — kb §7).

## 5. Cart streaming (axis: 77.4)

DMA events 396 · total 8.6 MB · unique 3.4 MB · re-read ratio 0.6103 ·
steady-state 0.128 MB/min (`short_window: false`) · PIO 1,049,920 B
GD-path visibility (Calibration B's actual target — PASSED, v2): GD-ROM/DIMM reads route
through the same logged `CARTDMA` path as cart images, reproduced identically across a
360 s and a 600 s run — no C++ instrumentation change was needed.

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 2,104 · MMIO refs: scif 2, rtc 3, g2ext 341 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc` → 85.0
Carved at base `0x8c020000`, entry `0x8c021000`, header title `-IKARUGA-`.
`guts.sdk_strings` lists dozens of `MIDI_*`/`SFX_*`/`OS_*` sound-driver asset names
consistent with a large ARAM sound bank (v2 note; the content measure puts actual ARAM
content at 1.45 MiB).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi stick + buttons, 2P (`controls.device_class = stick`). MAME input
ports: `naomi`. Proposed DC mapping: stock DC pad — the official 2002 DC port (§2)
demonstrates DC-side controls are a solved problem.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (sidecar
`controls.sources`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 77.4^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **88.7 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes.

## 9. Risks & notes

- **Not a queue entry.** This is Calibration B (GD-path control) and a scoring anchor:
  `ikaruga` is in `score.py`'s `DC_SHIPPED_ANCHORS` — a park on this title raises
  `MetricRegression` instead of writing a verdict, because the official 2002 DC port
  proves the game runs on real DC hardware.
- **VRAM and streaming figures are lower bounds, not the game's real peak.** The capture
  never leaves the title screen (§3) — no level, no enemy waves, no bullet-hell rendering
  ever ran. Any future re-score needs an input-driven capture (start a credit, hold the
  game past title) to get real gameplay figures.
- **ARAM is likely NOT understated:** the sound driver loads its bank during the
  boot/calibration window, not as a gameplay growth curve (same pattern as Calibration
  A's `cleoftp`; bit-identical across 360 s and 600 s runs).
- **Main content is address-sparse:** only 2.82 MiB of content total, but a ~1.49 MiB
  residual band sits at 25.7–28.6 MB — trivial volume, high address; a port relocates it.
  This was the main-axis instance of the address-vs-volume divergence that fed the §6
  checkpoint (kb §6), resolved by the v9 re-key.
- **FREE PLAY title-idle-without-demo is likely not unique to Ikaruga** — other sets in
  the library may share this configuration; RUNBOOK's representativeness check records
  which state (calibration / title / attract-demo) a capture actually reached.
- Main-RAM v1 limitation note (v2, superseded by v6 write-truth): the old DMA high-water
  measure only saw cart-DMA'd data; since v6 main is snapshot+diff write-truth.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-02 | PARKED `G3 memory: aram peak > 2x DC capacity` | Calibration B target passed (GD/DIMM reads visible via `CARTDMA`, 396 events ×2 runs); the "8 MiB ARAM peak" was the DIMM "DMPD" fill artifact — root-cause kb §7 |
| v4 | 2026-08-04 | 49.6 (B) | Fill-excluded ARAM content 1.81 MiB fits — un-parked; the old §Gate's "full-bank load" inference was the measurement's fault, not the gate's (a v3 interim run also false-parked no-render — cart-DMA-only sampling vs its 0.96 MiB static title; kb §7) |
| v5 | 2026-08-06 | 49.6 (B) | Pre-`VRAMHANDOFF` sample drop replaced the signature-clamped VRAM value: clean peak 7,535,232 (0.90×, 0 above cap) — under the DC's 8 MB, as the shipped port implied (kb §9); main DMA-based 23.4 still binds |
| v6 | 2026-08-07 | 38.6 (C) | Main write-truth measured for the first time: address peak 32,505,920 (u 1.938) → sub 12.5 binds; B→C is the axis entering on a real measurement, not a regression; MAINHIST address-vs-volume finding logged for the §6 checkpoint (kb §6) |
| v8 | 2026-08-07 | 38.6 (C) | Anchor control run for VRAM FB-masking: bit-identical reproduction; VRAM sub 92.6 → 100.0, ARAM 92.2 → 100.0, main 12.5 still binds — final unchanged, exactly as the design doc predicted (spec `2026-08-07-vram-fb-masking-design.md`) |
| v9 | 2026-08-08 | 88.7 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` 2,959,601 (u 0.176) — memory axis 100.0 (spec `2026-08-08-main-content-rekey-design.md`) |
