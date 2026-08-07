# Noukone Puzzle Takoron (Japan) (GDL-0042) (`takoron`) — portability assessment

> **Battery v6 cluster re-run (2026-08-07): still PARKED — `G3 memory: aram peak > 2x DC
> capacity`, reconfirmed with real ARAM volume, not a fill artifact.** v6's content
> metric puts `nz_above_cap` at 4,347,346 B (4.15 MiB, within run-to-run jitter of v4's
> 4,336,179 B) — heavy under any keying, address or content: this is not a marginal park
> that a softer G3 rule (kb §6 item 1 checkpoint) would clear. Main RAM `dma_high_water`
> is 29,360,128 B = **exactly `0x1C00000`** (a suspiciously round 28 MiB) — one more data
> point for stream-cache placement rather than a per-title working set (kb §6 item 3).
> Unlike `kurucham`/`ss2005`/`tetkiwam`, `takoron`'s write-truth main peak (30,425,060 B)
> falls short of the shared `0x1F00000` structure seen on the other GD titles — no
> signature match here. Findings: `docs/kb/assessment-tooling.md` §6 item 3
> (2026-08-07). Sidecar: flycast `65f9f7857`, battery 6, `handoff.trigger = "pio"` (GD
> DIMM ~1 MB bootstrap).

## v6 verdict & measurements

| | |
|---|---|
| **Final** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Coverage | demo |
| Assessed | 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s (trigger=pio) · run 600 s · rom `naomi/takoron.zip` |

| Region | v6 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 30,425,060 | 16,777,216 | 1.81 | nz_total 17,017,505 · nz_above_cap 8,609,276 · dma_high_water 29,360,128 (1.75×) = exactly `0x1C00000` |
| VRAM (write-truth) | 15,222,784 | 8,388,608 | 1.81 | nz_total 5,992,148 |
| ARAM (content, fill-excluded) | 8,257,552 | 2,097,152 | 3.94 | content above cap 4,347,346 |

Streaming: 75 DMA events · total 62.2 MB · unique 40.2 MB · re-read 0.3539 · steady 4.852 MB/min
Gate: `G3 memory: aram peak > 2x DC capacity` — see the note above; axes not computed (`scores: null`).
Screenshots: `evidence/takoron/shot-060s.png` · `evidence/takoron/shot-365s.png` · `evidence/takoron/shot-609s.png`

Note: this is a reconfirmation, not a new finding — v4 already established the park as
content-real (4.14 MiB above cap, not the v2 fill artifact); v6 measures the same thing
again and gets the same answer (4.15 MiB). The only new datum is `dma_high_water`'s exact
28 MiB round number, which strengthens the stream-cache-placement reading of the GD-title
main-RAM clustering (kb §6 item 3).

---

> **Battery v4 re-assessment (2026-08-04): **PARKED — `G3 memory: aram peak > 2x DC capacity`**.**
> Park **confirmed** under the v4 content metric: 4.14 MiB of genuine sound content above the DC cap — a real G3, not the fill artifact. Tutorial demo renders (shot-609s).
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
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/takoron.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 29,360,128 | 16,777,216 | 1.75 |  |
| VRAM (write-truth diff) | 15,222,784 | 8,388,608 | 1.81 | nz_total 5,965,059 |
| ARAM (content, fill-excluded) | 8,257,552 | 2,097,152 | 3.94 | content above cap 4,336,179 |

Streaming: 75 DMA events · total 59.3 MB · unique 33.3 MB · re-read 0.4382 · steady 4.852 MB/min
Gate: `G3 memory: aram peak > 2x DC capacity` — see the note above; axes not computed (`scores: null`).
Screenshots: `evidence/takoron/shot-060s.png` · `evidence/takoron/shot-365s.png` · `evidence/takoron/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** (not a numeric tier) |
| Bottom line | The full 8 MiB Naomi ARAM bank is written at boot (4.00× the DC's 2 MiB AICA RAM) and `score.py` gates before any axis is computed — the fourth boot-time full-bank G3-aram park (kb §6 tally: `ikaruga`, `azumanga`, `ss2005`, now `takoron`). The gate is not the only memory problem: main-RAM DMA high-water is 1.75× and VRAM peak 1.81× the DC caps — all three regions over. The title is also display-blind under our fork (frozen splash in every screenshot while the game verifiably runs underneath) — same class as `kurucham`/`ss2005`. |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `takoron` (covers: no clones — `parent: null` in controls.json; single ROM_START, security PIC `317-5127-jpn.pic`, standard NAOMIGD_BIOS + NAOMI_DEFAULT_EEPROM — MAME src/mame/sega/naomi.cpp @59e7c0b) |
| Maker / year | Compile Heart, 2006 — their only arcade title. GDL-0042 is the **last entry in MAME's GDL list** (naomi.cpp @59e7c0b line 11290), i.e. the final third-party Naomi GD-ROM release. The "publisher Milestone" hint is disproved: MAME, [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron) and [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37904-noukone-puzzle-takoron) all credit Compile Heart; no Milestone involvement documented ([Wikipedia](https://en.wikipedia.org/wiki/Octomania) silent on it) |
| Genre / format | Puzzle ★ (2×2-cursor octopus-rotating tile matcher), GD-ROM (GDL-0042, 52.6 MB) |
| Official DC port | No — ported to **Wii** instead, as *Octomania* / JP しゃるうぃ〜☆たころん (JP 2007-08-23, NA 2008-03-25; Wii port by Hyper-Devbox Japan, publishers Idea Factory/Conspiracy — [Wikipedia](https://en.wikipedia.org/wiki/Octomania), accessed 2026-08-03). No Dreamcast release |
| Community ports | None found (searched 2026-08-03) — not in the [Dreamcast Junkyard Naomi GD-ROM article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html) (checked: no Takoron/Octomania mention), no dreamcast-talk conversion threads surfaced |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 30.0 s · run 600 s · rom: `naomi/takoron.zip` (single clean zip leg)
Attract/demo reached: **title (conservative)** — sidecar `capture.coverage = "title"`;
visual classification is impossible (see Display blindness), so the lower-bound label is
used even though activity metrics show the game running for the full window.

### Display blindness

All 10 battery screenshots show the same frozen NAOMI GD-ROM SYSTEM splash. That is a
**stale TA frame** left in the GL display path (kb §4.m class, same as `kurucham` and
`ss2005`), not a hang: underneath it the game verifiably runs — BIOS handoff at 30.0 s,
75 GD DMA events / 62,215,616 B streamed across the window, the full 8 MiB ARAM bank
written, and 5,729,465 B of nonzero VRAM asset uploads (`memory.vram.nz_total`). MAME's
own status for the set is preliminary / imperfect graphics + sound
([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron)) —
consistent with a title whose 2D composition trips emulator display paths, not a broken
game: it shipped in arcades and was recompiled for the Wii.

Screenshots kept (first + last, identical splash, proving the freeze):
- `assessments/evidence/takoron/shot-060s.png` — frozen NAOMI GD-ROM SYSTEM splash at t=60 s
- `assessments/evidence/takoron/shot-607s.png` — same splash at t=607 s, unchanged
Anomalies: display blindness as above; otherwise a clean first-attempt boot, no
`no-handoff-120s` flake.

## Gate

**G3 memory: aram peak > 2x DC capacity.** `memory.aram.peak = 8,388,608 B` (exactly
8 MiB, the full Naomi ARAM bank) against the DC's 2,097,152 B AICA RAM → utilization
4.00×, past `region_score()`'s `u > 2.0` gate; `nz_above_cap = 4,429,878 B` nonzero
above the cap at scan. Boot-time full-bank load — fourth in the campaign tally after
`ikaruga` (calibration), `azumanga` and `ss2005` (kb §6 item 1 checkpoint data point).

Evidence: `assessments/takoron.metrics.json` → `memory.aram`; `guts.sdk_strings` shows
the Sega Naomi sound stack doing the bank load (`libsnd Ver.1.05a`, NAOMI LIBRARY /
nlam 2005 builds).

What would unblock it: a per-title audio trim (downsample the PCM banks / ADPCM) —
standard porting work with released-port precedent (the official Ikaruga DC port's 4×
sound trim, kb §4.d). But the gate is not the only memory problem: main-RAM DMA
high-water is `29,360,128 B` (1.75× the DC's 16 MB) and VRAM peak `15,222,784 B` (1.81×
the 8 MB cap) — **all three regions over cap**, like `azumanga`. VRAM is milder than the
peak implies: nonzero content is only `5,729,465 B` total, with `5,728,565 B` of it
above the 8 MB line — an address-extent artifact of an asset store parked high (the
`kurucham` pattern); a port would relocate it.

Context values quoted from the sidecar (no axis scores exist — the pipeline stops at the
gate): streaming 75 DMA events, 62,215,616 B total / 39,146,944 B unique, re-read ratio
0.3708, steady-state 4.987 MB/min (`short_window: false`); guts 4,194,304 B code, 809
functions, MMIO refs scif 2 / rtc 4 / g2ext 30, flags `eeprom_bios`/`serial`/`rtc`;
similarity inputs `developer_match: false`, `sdk_overlap: "partial"` (NAOMI LIBRARY /
NLOBJPUT / NLSPRITE, syHw/syG2 Katana-adjacent builds, KAMUI2/KAMUI-Darkness),
`cart_loader_match: true`.

## Risks & notes

- **Display-path gap blocks emulator validation.** Even a ported build could not be
  visually validated in this emulator today — the fork shows a stale TA frame while the
  game composes frames the display path never shows. Per the working-style rule,
  rendering must be verified on real DC hardware; the emulator-side diagnostic is the
  raw-VRAM decode recipe (`FLYCAST_VRAMDUMP` + `vramdump2png.py`, kb §4.m).
- **All three memory regions over cap** (ARAM 4.00×, main 1.75×, VRAM 1.81×) — a port
  is trim-everything work in every region, not just the audio gate.
- **The code demonstrably moved off Naomi once** — portability-positive: Hyper-Devbox
  Japan built libraries to *recompile the original arcade source* for the Wii port
  ([Wikipedia](https://en.wikipedia.org/wiki/Octomania)), so the game logic is not
  hardware-welded, though DC memory budgets are the harder wall.
- **Streaming is light** — 75 DMA events, re-read ratio 0.3708, 4.987 MB/min steady:
  the title is nearly self-contained after boot, a porting positive.
- **Controls are the easy axis**: `controls.device_class = stick`. The game's own INPUT
  TEST menu (in-binary, `guts.sdk_strings`) lists UP/DOWN/LEFT/RIGHT +
  ROTATE(L)/ROTATE(R)/CANCEL + START per player — one 8-way stick and three game
  buttons, 1:1 on a DC pad (d-pad + A/B rotate, X cancel, Start). Sources: MAME
  src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron)
  (8-way joystick + 6-button JVS standard declaration, 2P);
  [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37904-noukone-puzzle-takoron)
  (cursor movement + Main button rotate);
  [Wikipedia](https://en.wikipedia.org/wiki/Octomania) (Wii port: pointer + one rotate
  button).
- `guts.code_bytes = 4,194,304` — exactly 4 MiB, *at* but not over the
  `code_over_4mb` threshold, so no penalty flag fired; a boundary case worth
  remembering if the carve is ever re-run.
- Main watermark `30,425,060 B` (informational, stale-data-prone) is 1.04× the DMA
  high-water — mild; little content above the last DMA'd asset.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset.
