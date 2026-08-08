# Design: main-RAM axis re-keyed on content volume (§6 item 3, battery v9)

**Date:** 2026-08-08. **Status:** ADOPTED — ruled at the 30-family §6
scoring-semantics checkpoint (user ruling), developed on branch
`experiment/v9-main-content`, **merged to main 2026-08-09** after user
review of the re-scored table, the control-question resolution (see
Addendum), and the RANKING work-columns/provenance additions.

## Goal

Key the main-RAM region of `score.py`'s memory axis — the `u > 2.0` G3 park
*and* the sub-score — on **write-truth content volume**
(`memory.main.nz_total`, per-sample max of the full snapshot-diff byte count,
`parse_capture.py`) instead of the write high-water *address*
(`memory.main.peak`). This completes the pattern already ruled for ARAM
(v7, `2026-08-07-aram-gate-volume-design.md`) and VRAM (v8,
`2026-08-07-vram-fb-masking-design.md`): address is a placement artifact,
volume is what a port must carry.

## Evidence (kb §6 item 3, closed at this checkpoint)

- The `0x1F00040` shared structure has **five exact instances** — ikaruga,
  kurucham, ss2005, illvelo, karous. illvelo is a **cart**, so the structure
  is not GD-firmware-specific; karous is DC-shipped ground truth scoring
  37.0 C purely from this address.
- **shikgam2** is the most extreme divergence on any axis: address-u 1.999
  (floored at 10.0) against **213,556 B** of content above the 16 MB cap.
- Main binds 23/25 scored titles, 12 saturated at sub ≤ 12.5 → an 11-title
  C-band (34.7–38.6) where the axis has zero discriminating power.
- The DC-shipped validation cohort discriminates the keyings: six shipped
  titles sit in C under address keying; all main-bound ones move to A/S
  under content keying (karous 37.0→85.0, ikaruga 38.6→88.7, shikgam2
  35.4→87.7, tetkiwam 38.1→82.9, trgheart 40.0→86.5, trizeal 37.7→72.5).
  The two that stay low (cspike, zerogu2) stay low for a real reason (ARAM
  content). No park flips in either direction; max main content-u across
  all sidecars is 1.025 (azumanga).

## Rulings (user, 2026-08-08)

1. **Re-key main on content volume, uniform mirror of the ARAM formula** —
   no surcharge for above-cap placement. Items 1 (ARAM 2×), 2 (re-read
   penalty), 4 (controls bands) and the p16 backlog stay untouched.
2. **Experiment branch first** (`experiment/v9-main-content`); the user
   judges the re-scored table before anything reaches main.
3. **Adopt-to-main prerequisites** (§8 control discipline): splash-only
   control runs quantifying firmware-written main content — dragntr3 (GD
   natural control, never boots past splash) **and a cart-side control**
   (zunou, G1 no-boot), since the illvelo instance proves the signature is
   not GD-only. Firmware content inflates `nz_total` and biases
   *conservative*, so the controls bound false precision, not false unparks.

## Honest caveats (recorded, not blockers)

- **No position-independence proof for main** (unlike ARAM's OSB banks):
  above-cap main content carries absolute pointers; karous's shipped port
  did a real ~5 MB trim. The score ranks portability — the port shipped —
  but v9 is generous where a trim is real work.
- `nz_total` has **no uniform-fill exclusion** (ARAM's content counters do):
  firmware bytes count. Conservative bias; measured by the control runs.
- tetkiwam carries 7.27 MB above-cap content despite a DC build on its own
  disc — content likely counts GD stream-cache bytes too. Same conservative
  direction.

## Design

### Scorer — `tools/assess/score.py` (only file with logic changes)

- Main fit value: `nz_total` when present, else `peak` (write-truth
  address), else `dma_high_water` — a plain `or` chain is safe here because
  `peak > 0 ⇒ nz_total ≥ 1` (some byte differed), so a 0 can only mean the
  same blind-metric case the existing falsy-drop already handles
  (region dropped + `main_unmeasured` flag; the gwing2 100-from-nothing
  guard is unchanged).
- Fallback safety: content bytes live in `[0, peak]` ⇒
  `nz_total ≤ peak + 1` ⇒ pre-v6 sidecars (senko, senkosp) can only
  *under*-score. Same theorem shape as ARAM v7.
- Main park message becomes `G3 memory: main content > 2x DC capacity` when
  volume-keyed (legacy fallback keeps "peak") — same one-word lookup as
  aram/vram.
- `region_score` / `memory_axis` / thresholds / weights: untouched.
- Canaries (DMPD, BIOS-VRAM signature, anchors-never-park): untouched.
  Anchors are safe by construction: volume ≤ address, re-keying only moves
  titles away from parking.

### Versioning — `tools/assess/run_battery.py`

`BATTERY_VERSION` "8" → "9". Scoring-semantics-only change: no fork change,
no capture-format change, sidecar schema unchanged (`nz_total` exists since
v6). Existing sidecars keep their stamped capture version; the blanket
re-score makes `RANKING.md` uniformly one scorer version.

### Guard tests — `tools/assess/tests/`

1. `test_score.py`: main content preferred over address — shikgam2 shape
   (address would park at u > 2, content 4 MB scores 100).
2. Main volume park message says "content"; legacy no-`nz_total` fallback
   still parks with "peak".
3. `test_metric_guards.py`: ikaruga anchor `min_mem` floor recalibrated
   12.5 → its v9 value (content-keyed); comment records the v9 ruling.
   The un-parked invariant is unchanged, never weakened.
4. All existing guards stay green.

## Campaign ops

- **No re-captures needed** for the re-score: `nz_total` is in every v6+
  sidecar. Blanket `score_sidecar` pass over all sidecars +
  `gen_tables.py ranking` + `patch`.
- Stale-sidecar re-runs (senko/senkosp v4 main; azumanga/kurucham/ss2005
  v8 VRAM fields; the two splash controls) are the same follow-up wave
  regardless of this ruling — listed as adopt work, not branch work.
- Per-title `assessments/*.md` prose still cites v≤8 verdicts; updating the
  25 files is merge-time work, not experiment work.
- kb §6 gains the item-8 entry (this ruling); item 3 closes with a pointer
  here.

## Addendum (2026-08-09): control-run prerequisite resolved by bound

The ruling-3 control runs proved impossible in this library — the `dragntr`
and `wccf` families were excluded by user ruling (net-medal / card-terminal
platforms, not port targets; `wccf1dup`, tried as a pure-firmware GD control,
is `emulator-exited` in Flycast), and the `zunou` v9 re-run showed the game
boots to a static attract card, so it is not firmware-only (it also
reproduced the §4.p `boot_ok` false-positive — scored 85.8 S before the
screenshot check; override re-applied, freeze md5-identical to 2026-08-04).
Replacement bound from committed sidecars (kb §6 item 8, "Prerequisite
resolution"): firmware writes **zero** persistent above-cap main content on
both media paths (six titles with `nz_above_cap = 0`: cleoftp/moeru GD,
puyoda/zerogu2/ausfache/gwing2 cart — so `0x1F00040` is title-conditional,
not universal firmware), and the sub-cap baseline is ≤ 2.70 MB (GD) /
≤ 4.64 MB (cart) by per-path minimum `nz_total` — worst-case content-u
inflation ≤ 0.16, conservative direction. Prerequisite satisfied; the adopt
decision remains the user's.

## Done means (experiment scope)

- `score.py` keys main on `nz_total` with the fallback chain; park message
  keyed; tests green including the new pins and the recalibrated anchor
  floor.
- Blanket re-score + `RANKING.md`/`GAME_FORMATS.md` regenerated on the
  branch; before/after table presented to the user.
- kb §6 item-8 entry committed on the branch.
