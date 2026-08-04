# Azumanga Daioh Puzzle Bobble (GDL-0018) (`azumanga`) — portability assessment

> **Battery v4 re-assessment (2026-08-04): **PARKED — `G3 memory: aram peak > 2x DC capacity`**.**
> Park **confirmed** under the v4 content metric: 1.63 MiB of genuine (non-fill) sound content above the DC cap — with the below-cap driver/data this cannot fit 2 MiB. This is a real G3, unlike the fill-artifact cohort.
> Below the v4 section is the battery v2-era assessment: its *measured* figures
> (boot evidence, memory, streaming, score) are **superseded**; the identity,
> controls-research and similarity sections remain valid. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/azumanga.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 21,645,536 | 16,777,216 | 1.29 |  |
| VRAM (write-truth diff) | 15,450,112 | 8,388,608 | 1.84 | nz_total 10,105,382 |
| ARAM (content, fill-excluded) | 6,053,632 | 2,097,152 | 2.89 | content above cap 1,709,398 |

Streaming: 446 DMA events · total 55.9 MB · unique 16.3 MB · re-read 0.7088 · steady 4.976 MB/min
Gate: `G3 memory: aram peak > 2x DC capacity` — see the note above; axes not computed (`scores: null`).
Screenshots: `evidence/azumanga/shot-060s.png` · `evidence/azumanga/shot-365s.png` · `evidence/azumanga/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM is written at boot (4.00× the DC's 2 MiB AICA RAM) — the sound design carries 11 stereo PCM BGM tracks plus per-character voice banks for the full anime cast, and `score.py` gates before any axis is computed. Even without the gate, memory would be the weak axis: main-RAM DMA high-water is 1.29× and VRAM write-truth peak 1.84× the DC caps — a heavy port despite the "easy" puzzle genre. |
| Assessed | 2026-08-02 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/azumanga.zip`
Attract/demo reached: **demo reached** — full attract cycle captured: title (60 s) →
two-player VS demo gameplay (121 s) → single-board game-over (183 s) → CLEAR!/GAME OVER
card (246 s) → how-to-play screen (425 s) → back to title (605 s). Unlike a title-idle
capture, these metrics reflect real rendered gameplay. Sidecar `capture.coverage = "demo"`.
Screenshots:
- `assessments/evidence/azumanga/shot-060s.png` — title screen
- `assessments/evidence/azumanga/shot-121s.png` — VS demo gameplay, both boards full of bubbles
- `assessments/evidence/azumanga/shot-183s.png` — single-board demo, GAME OVER
- `assessments/evidence/azumanga/shot-246s.png` — CLEAR! card
- `assessments/evidence/azumanga/shot-425s.png` — how-to-play screen; **draws the cabinet controls: one ball-top joystick + one button**
Anomalies: none — clean first-attempt boot, no `no-handoff-120s` flake.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, `nz_above_cap = 6,224,467 B` nonzero above the cap at scan) against the DC's
2 MiB (`2,097,152 B`) AICA RAM → utilization 4.00×, past `region_score()`'s `u > 2.0`
gate, so `memory_axis()` gates on `aram` and `sc["scores"]` is `null`.

Evidence: `assessments/azumanga.metrics.json` → `memory.aram`; corroborated by
`guts.sdk_strings`, which name the audio payload directly — 11 BGM tracks as stereo
16-bit PCM pairs (`BGM01L.p16`/`BGM01R.p16` … `BGM11L.p16`/`BGM11R.p16`), per-character
voice banks (`sakaki.osb`, `kagura.osb`, `yukari.osb`, `cosaka.osb`, `cchiyo.osb`, …),
and `read bank download error` strings from the ARAM bank loader. The game features the
full anime voice cast, so the bank is voice-heavy by design.

What would unblock it: a per-title audio trim (downsample the PCM BGM, cut or compress
voice banks) — standard porting work, but note the gate is not the only memory problem
(see Risks): main and VRAM also exceed DC caps, so this title needs asset reduction in
all three regions.

Informational axis values computed via `tools/assess/score.py` helpers for context (not
part of `sc["scores"]`, since the pipeline stops at the gate): memory sub-scores
main=38.4 (u=1.290, DMA high-water 21,645,536 B / 16 MB), vram=16.3 (u=1.842,
write-truth peak 15,450,112 B / 8 MB, `nz_above_cap=6,688,529`), aram=gated (u=4.00);
streaming=75.9 (386 DMA events, 52.2 MB total / 17.1 MB unique, re-read ratio 0.6729,
steady 4.628 MB/min); guts=85.0 (`eeprom_bios`/`serial`/`rtc` penalties, 1243 functions,
1 MiB code); controls=100.0 (`stick`); similarity=70.0 (developer match false,
sdk_overlap partial, cart_loader_match true).

## Risks & notes

- **VRAM is nearly as blocking as ARAM.** Write-truth peak 15,450,112 B of Naomi's
  16 MB — 1.84× the DC's 8 MB, with 6.7 MB of nonzero data above the cap — measured
  during genuine demo gameplay, not idle. The lavish 2D art (full-screen anime
  backgrounds, pinup galleries, per-character portraits — see the `pinup*.bin` /
  `photo*.bin` file lists in `sdk_strings`) roughly doubles the DC texture budget.
  A port would need to halve textures *and* quarter audio.
- Coverage is `demo`, so these are representative attract-gameplay figures, not lower
  bounds — though full play (all characters/courses selected by a player) could still
  run marginally higher than the attract rotation.
- Controls are the one genuinely easy axis: one joystick + one button per the in-game
  how-to-play screen (`shot-425s.png`), one joystick + two buttons per the
  [Azumanga Daioh Wiki](https://azumanga.fandom.com/wiki/Azumanga_Daioh_Puzzle_Bobble);
  MAME `naomi.cpp` standard `naomi` INPUT_PORTS. Maps 1:1 to a DC pad.
- Second GD-ROM title in a row to park at G3-aram with a boot-time full-bank load
  (after calibration `ikaruga`) — data point for the scoring-semantics checkpoint
  (`docs/kb/assessment-tooling.md` §6).
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset.
