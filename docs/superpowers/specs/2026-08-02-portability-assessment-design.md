# Naomi → Dreamcast portability assessment — design

Date: 2026-08-02 · Source requirements: `REQUIREMENTS.md` · Status: approved by user (pipeline, scoring, template, tooling — all three design parts)

## 1. Goal & scope

Rank every Naomi game that never got an official Dreamcast release by **ease of Naomi→DC porting**, so ports can proceed easiest-first. The output is one assessment document per game family plus a scored, sorted summary — not the ports themselves and not deep per-game reverse engineering (that remains each port project's job).

**In scope:** all families in `naomi/` with no official same-game DC release (`DC port` = `No` or `Partial` in `GAME_FORMATS.md`), one representative set per parent/clone family.
**Out of scope:** the 58 `Yes` sets (official DC build exists), deep manual Ghidra work, asset-format reverse engineering, any porting.

### Decisions taken with the user

| Decision | Choice |
|---|---|
| Assessment depth | Fully automated battery per game; no manual RE. Scores are provisional; a port's own early phases re-verify its pick. |
| Clones | One assessment per parent/clone family. Representative = newest revision in the game's original region among in-scope members. Clones get table rows linking to the family doc. |
| Aggregation | Hard gates, then five axes 0–100 combined by **weighted geometric mean**. |
| Exotic (⚠) games | Same uniform battery as everyone (machine time is cheap); the controls axis / G2 gate ranks or parks them. |

A family is in scope only if **no member is the same game officially released on DC**. `Partial` (related-but-not-identical version reached DC) stays in scope. The in-scope family list with chosen representatives is generated from `GAME_FORMATS.md` + MAME parent/clone data and committed as `assessments/QUEUE.md` before assessments start.

## 2. Pipeline (per family, strictly serial)

1. **Boot pre-check.** Launch the representative set in instrumented Flycast, headless screenshots every 60 s, boot timeout 120 s. On failure: automatic same-candidate retry once on the no-handoff flake, then fall through to the next launch-file candidate (`.zip`/`.chd`); alternate-BIOS-region retry is not implemented — treated as an operator diagnostic step per `RUNBOOK.md` instead. Capture stderr, classify (missing files / crash / black screen / error screen), corroborate against MAME `MACHINE_NOT_WORKING` flags to separate tooling faults from broken games. No boot → park as `Broken` (gate G1), short-form doc, stop.
2. **Dynamic capture.** One unattended **600 s** attract-mode run. Per-set `FLYCAST_CARTLOG` file, screenshots every 60 s as progress evidence. Collected: main-RAM cart-DMA high-water + WATERMARK scan, VRAM and ARAM **write-truth** profiles (zero-at-handoff on first cart DMA — the mechanism that eliminated the 9.4 MB BIOS-logo false positive in the Cleopatra work), full cart-DMA log, video-mode registers. No human input.
3. **Static scan.** Produce `out/<set>.dat` via `tools/dat-extract`, parse header, run headless Ghidra (version pinned to the Cleopatra project's) with a metrics post-script: code size, MMIO cross-references (serial, EEPROM, RTC, network/DIMM), Naomi-BIOS call sites, SDK/library string fingerprints. **Delete the `.dat` afterwards** (SSD hygiene).
4. **Controls research.** Input device class parsed from MAME `src/mame/sega/naomi.cpp` input ports (primary source), plus web research (manuals, cabinet photos, flyers) — every claim cited, primary sources outrank wikis.
5. **Score & write-up.** All metrics land in `assessments/<set>.metrics.json`; `score.py` computes axes → final → tier; the assessing agent writes `assessments/<set>.md` from the template; `gen_tables.py` regenerates the summary tables.

Stages 1–2 run as a **single 600 s launch with a 120 s early-abort**: if no game handoff (first cart DMA) is seen by 120 s, the run is killed and classified per stage 1; otherwise it continues as stage 2. Battery parameters (recorded in every sidecar): capture 600 s · steady-state window starts at handoff + 120 s · screenshot interval 60 s · boot timeout 120 s. Some games idle on a static pre-game screen for minutes (e.g. Ikaruga's ~300 s brightness-calibration countdown, user-observed 2026-08-02); the runbook therefore mandates a post-run screenshot representativeness check, with a longer `--secs` re-run whenever attract was not reached. The cartlog carries no timestamps; the orchestrator samples the log's byte size every 10 s into a timeline file, and the parser maps log lines to time through it (±10 s, ample for MB/min rates). The steady-state window start is validated during calibration (GD-ROM DIMM boot loads can be long) and adjusted once, before any real assessment, if the control runs show boot streaming leaking into the window.

## 3. Gates

Failing any gate parks the game — no score, short-form doc (identity + gate evidence + what would unblock it), table note.

| Gate | Condition | Rationale |
|---|---|---|
| **G1 Broken** | Won't boot after the retry ladder, and the failure is attributable to the game (not tooling) | Can't port what can't run |
| **G2 Controls** | Requires physically unmappable hardware: card reader/printer (WCCF), medal/hopper payout, mandatory multi-cabinet satellite topology | No DC equivalent exists at any effort level |
| **G3 Memory** | Any region's write-truth peak exceeds **2× DC capacity** (> 32 MB main / > 16 MB VRAM / > 4 MB ARAM) | Beyond plausible trimming |

## 4. Axes & scoring

Five axes, each clamped to **[10, 100]** (the floor prevents one axis from annihilating the geometric mean; true blockers are the gates' job).

### 4.1 Memory fit (weight .40)

Per region, utilization `u = write-truth peak / DC capacity` (capacities: main 16 MB, VRAM 8 MB, ARAM 2 MB) maps piecewise-linearly:

| u | Score | Reading |
|---|---|---|
| ≤ 0.80 | 100 | Fits with ≥ 20 % headroom |
| 0.80 – 1.00 | 100 → 85 | Fits, tight (u = 1.00 exactly ⇒ 85) |
| 1.00 – 1.25 | 85 → 40 | Overshoot ≤ 25 %: plausible trim |
| 1.25 – 2.00 | 40 → 10 | Heavy overshoot |
| > 2.00 | — | Gate G3 |

Axis = **min of the three region scores** — regions are not tradeable against each other. Main RAM scores on the **DMA high-water** (write-truth via DMA: actual asset placement); the content-scan WATERMARK is recorded as informational only and flagged in Risks when it far exceeds the high-water — content scans cannot distinguish stale bytes from real use (Cleopatra's main scan read ~32 MB of residue vs the real 11.2 MB; scoring on it would have parked the proven-ideal candidate at gate G3). Known v1 limitation, stated in each doc's Risks: CPU-written data above the DMA'd assets (heaps, tables) is not captured for main RAM. VRAM/ARAM use post-handoff write-truth peaks only.

### 4.2 Cart streaming (weight .20)

The port re-issues cart reads as GD-ROM reads; sustained scattered streaming is the enemy (seek latency), total size is not (both media are ~1 GB class).

- **Bandwidth score** (0.6): steady-state cart-DMA bandwidth B (MB/min) inside the steady-state window: B ≤ 6 → 100 · 6–24 → 100→60 · 24–60 → 60→20 · > 60 → 10 (linear within bands).
- **Re-read score** (0.4): re-read ratio R = re-read bytes / total streamed bytes: R ≤ 0.1 → 100 · 0.1–0.5 → 100→50 · 0.5–1.0 → 50→20 (linear).
- Axis = 0.6·bandwidth + 0.4·re-read. Burstiness (p95 inter-DMA gap, max burst) and working-set size are recorded in the sidecar as informational, unscored in v1.

### 4.3 Guts (weight .20)

Start at 100, subtract tabled penalties (floor 10). Penalty sizes are calibrated from what each item actually cost in the Cleopatra port (serial stub and EEPROM shim were small tasks; live network features were never attempted):

| Finding | Penalty |
|---|---|
| Serial-port writes present | −5 |
| EEPROM access via BIOS routines | −5 |
| EEPROM direct/custom access | −10 |
| RTC usage | −5 |
| Network/DIMM-board communication beyond boot (netpic/online features) | −25 |
| Naomi-BIOS call sites beyond the standard set (the classes Cleopatra used: boot handoff, EEPROM read/write) | −2 per distinct site class, max −10 |
| Code size > 4 MB | −5 |

**No `.dat` available** (`hotd2`, `mushik2e`): not parked — the guts axis is dropped and remaining weights renormalize ×1.25 (memory .50, streaming .25, controls .125, similarity .125), flagged prominently in the doc.

### 4.4 Controls (weight .10)

Device-class ladder, from MAME input ports + cited web research:

| Class | Score |
|---|---|
| Standard stick/buttons (incl. up to 4 players — DC has 4 ports) | 100 |
| A DC peripheral exists: light gun, wheel, fishing rod, keyboard, maracas, twin stick | 75 |
| Pad-adaptable with real design work (e.g. Inu no Osanpo) | 50 |
| Awkward but conceivable | 25 |
| Physically unmappable | Gate G2 |

Optional link play is ignored; a *mandatory* linked-cabinet topology is G2.

### 4.5 Similarity (weight .10)

Distance to the nearest already-ported title (v1: only Cleopatra Fortune Plus; the axis generalizes as ports accumulate). Score = min(100, 20 + parts):

| Signal | Points |
|---|---|
| Baseline (unknown ≠ impossible) | 20 |
| Same developer as a ported title | +30 |
| SDK/library string-fingerprint overlap — full (+40) = every library banner string found in the ported title also present; partial (+20) = at least one shared banner | +40 |
| Same cart type and header/loader structure | +30 |

v1 uses strings + metadata only; function-hash overlap is deferred until it would change a ranking decision.

### 4.6 Final score & tiers

`final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10` (weighted geometric mean — bottleneck-sensitive: one weak axis drags the product down, as porting reality demands).

Tiers: **S ≥ 80 · A 60–79 · B 40–59 · C 20–39 · D < 20 · Parked (G1/G2/G3)**.

Calibration anchor: Cleopatra Fortune Plus with its known numbers (main 11.2 MB → 100, VRAM 7.8/8 → ≈86, ARAM 2.0/2 → 85 ⇒ memory 85; streaming ≈100; guts ≈90; controls 100; similarity 100) lands ≈ 92 = **S**, as the one proven-ideal candidate should. If a scoring-table revision ever stops Cleopatra scoring S, the tables are wrong.

Weights, breakpoints, and penalties live **only** in `score.py`. Revising them means re-running `score.py` + `gen_tables.py` over all sidecars (cheap — no re-capture) and bumping the battery version.

## 5. Per-family deliverables

```
assessments/
  RUNBOOK.md              ← the uniform procedure every assessing agent follows verbatim
  QUEUE.md                ← generated: in-scope families + chosen representative + status
  RANKING.md              ← generated: all assessed families sorted by score
  <set>.md                ← human-readable assessment (template §5.1)
  <set>.metrics.json      ← battery-generated sidecar: every raw metric + tool versions
  evidence/<set>/         ← committed: ≤5 representative screenshots (boot, title, attract);
                            gitignored: raw capture logs + the full screenshot series
```

The **sidecar is the single source of truth for numbers**: the battery writes it, `score.py` extends it with scores, tables regenerate from it, and the MD quotes it — no hand-maintained figures. Raw capture logs stay local (large, regenerable by re-running the battery); metrics and screenshots are committed.

### 5.1 Assessment template (`<set>.md`)

1. **Verdict** — score, tier, one-line bottom line, assessment date, toolchain versions (flycast-fork commit, battery version, Ghidra version, MAME source version).
2. **Identity** — set, family members covered, maker, year, genre, cart type, size, DC-port status, existing community/fan ports (researched, linked — no point re-porting the scene's work), representative-selection note.
3. **Boot & run evidence** — boots Y/N, run duration, screenshot references, anomalies.
4. **Memory fit** — one row per region: write-truth peak, average, DC capacity, headroom %, sub-score; the cartlog grep tag that verifies each number.
5. **Cart streaming** — DMA count, steady-state bandwidth, working set, re-read ratio, burstiness, sub-score, log references.
6. **Guts** — header load-chain summary, code size, peripheral touchpoints with addresses/counts, applied penalties, sub-score.
7. **Controls** — cabinet inputs (MAME source cited), proposed DC mapping, sub-score, web sources.
8. **Score computation** — §4.6 formula instantiated with this game's numbers: reproducible arithmetic in plain sight.
9. **Risks & notes** — anomalies, and what a future port project should verify first.

Parked short-form: sections 1–3 + gate evidence + "what would unblock".

### 5.2 Sidecar schema (`<set>.metrics.json`, key fields)

`set`, `assessed` (date) · `versions{flycast, battery, ghidra, mame_src}` · `params{capture_s, steady_after_s, ...}` · `boot{ok, failure_class, notes}` · `capture{duration_s, handoff_s, screenshots[], coverage: "demo"|"title"|"calibration" (agent-set from the representativeness check; battery writes null; surfaced as a ⚠ flag in RANKING.md)}` · `memory{main{dma_high_water, watermark}, vram{peak, nz_above_cap}, aram{peak, nz_above_cap}}` · `streaming{dma_count, total_bytes, steady_mb_per_min, working_set_bytes, reread_ratio}` · `guts{dat_available, code_size, mmio{serial, eeprom, rtc, network}, bios_call_sites, sdk_strings[]}` · `controls{device_class, mame_ports[], sources[]}` · `similarity{developer_match, sdk_overlap, cart_loader_match}` · `scores{memory, streaming, guts, controls, similarity, final, tier}` · `gate` (null or G1/G2/G3 + evidence). (p95 gap / max burst dropped: unmeasurable without per-line timestamps; family membership lives in QUEUE.md.)

### 5.3 Summary tables

`GAME_FORMATS.md`'s per-set table already ends in an assessment-status column (currently `not assessed`); the generator patches **that one cell** keyed on set name — `**<score>** <tier> · [assessment](assessments/<set>.md)` for representatives, `see <family doc>` for clones, `parked <gate>` for gated games. The sorted ranking lives in generated `assessments/RANKING.md`, linked from `GAME_FORMATS.md` — the hand-curated inventory never gets re-sorted or rewritten by script beyond that column.

## 6. Tooling

New code in `tools/assess/`; Flycast changes in the `flycast4naomi2dreamcast` fork.

| Tool | Job |
|---|---|
| `run_battery` | Orchestrates one family end-to-end: boot check → timed capture → parsers → static scan → sidecar. Strictly serial; unique per-set log paths |
| Flycast fork | **No C++ change needed for v1**: timed exit = wrapper background-launch + kill (the proven `capture.sh` pattern, incl. the macOS persistence-dialog suppression); screenshots = existing `FLYCAST_SHOT` + `FLYCAST_SHOT_EVERY` + `SIGUSR1`; video-mode record = existing `VRAMREGS`. Binary = the already-built instrumented app at `../cleopatra/tools/flycast-src/build/Flycast.app` (fork commit recorded in every sidecar). Still to **verify in calibration**: (a) write-truth VRAM/ARAM profiles are game-agnostic (they hook generic Naomi paths — verify, don't assume); (b) GD-ROM/DIMM reads route through the logged `CARTDMA` path — 77/152 sets are GD-ROM; if they bypass it, add a cartlog call to `core/hw/naomi/gdcartridge.cpp` and rebuild (the one contingency that would touch C++) |
| `parse_capture.py` | Capture log → metric fragments (peaks, rates, working set, histograms, noise exclusion) |
| `ghidra_metrics` | Headless Ghidra import (SH4 loader config from the Cleopatra kb) + post-script exporting code size, MMIO xrefs, BIOS call sites, SDK strings |
| `controls_extract.py` | Parse MAME `naomi.cpp` input ports per set → device-class JSON (MAME version pinned & recorded) |
| `score.py` | The only implementation of §4: breakpoints, penalties, ladder, similarity, geometric mean, tiers |
| `gen_tables.py` | Emits `QUEUE.md`, `RANKING.md`; patches the two `GAME_FORMATS.md` columns |

Every tool install/version gets recorded (reproducibility rule): exact versions and flags in `docs/kb/tooling.md` of this repo.

## 7. Calibration — control tests before any real assessment

1. **Cleopatra Fortune Plus through the full battery.** Must reproduce the known-good numbers — main 11.2 MB, VRAM 7.8 MB with 0 bytes ≥ 8 MB, ARAM exactly 2.0 MB — and score S. Any mismatch means fix the battery, never the numbers.
2. **One GD-ROM set with an official DC port** (default: `ikaruga`). Validates the GD/DIMM logging path end-to-end; a game that demonstrably fit a DC should show comfortable memory fits.

Both runs are calibration only — not queue entries, but their sidecars and docs are kept as reference points. If instrumentation or scoring changes materially mid-campaign, previously assessed families are re-run/re-scored so all results stay comparable (battery version in every sidecar makes staleness detectable).

## 8. Policies & caveat handling

- **BIOS-logo noise** → zero-at-handoff, generic for every game (proven in the Cleopatra work).
- **Parallel interference** → serial execution only, unique log paths. Slower is acceptable by requirement.
- **SSD hygiene** → `run_battery` deletes `out/<set>.dat` after the static scan.
- **Copyrighted bytes** → `naomi/`, raw logs containing dumped data, and any `.dat` stay uncommitted/gitignored. Screenshots (evidence) and extracted metrics are fine to commit.
- **Knowledge base** → lessons from tooling prep and assessments land in this repo's `docs/kb/`, Cleopatra-style.
- **Citations** → every hardware/behavioral claim in a doc carries its source: a log grep tag, a screenshot path, or a URL (primary sources outrank wikis).
- **Uniform execution** → every assessing agent follows `assessments/RUNBOOK.md` verbatim; captures may run as unattended serial batches with research/write-up per family afterwards.

## 9. Cost estimate

~78 in-scope families × (~10 min capture + ~10 min static scan + ~10 min research/write-up) ≈ a few days of mostly-unattended wall-clock, serialized.

## 10. Explicitly deferred

- Function-hash similarity (v1 is strings + metadata).
- Scoring burstiness / working-set size (recorded, unscored).
- Per-asset extraction & format analysis — aggregate memory + streaming metrics cover the assessment need; single-asset pathologies (e.g. one texture > 8 MB) surface as VRAM/streaming outliers anyway, and true asset work belongs to the individual port project.
- Hands-on gameplay capture — Cleopatra's play pass barely moved any number vs attract mode; attract-only is the uniform, unattended choice. A port project re-verifies with gameplay for its one game.
