# Assessment runbook (battery v2)

Follow verbatim, one family at a time, SERIAL ONLY (never two Flycast instances).
Spec: `docs/superpowers/specs/2026-08-02-portability-assessment-design.md`.

## Once per session

1. `python3 tools/assess/tests/test_score.py` → must print `ALL OK` (toolchain sanity).
2. If `tools/assess/out/controls.json` is missing:
   `mkdir -p tools/assess/out && python3 tools/assess/controls_extract.py > tools/assess/out/controls.json`
3. Naomi BIOS must be at `~/Library/Application Support/Flycast/data/naomi.zip`
   (else: `cp ../cleopatra/bios/naomi.zip ~/Library/Application\ Support/Flycast/data/`).

## Per family (representative set from QUEUE.md)

1. **Battery:** `python3 tools/assess/run_battery.py <set>`
   (~10 min unattended; writes `assessments/<set>.metrics.json` + evidence).
   - **Representativeness check (mandatory):** open the run's screenshots. If the late shots
     still show a static pre-game screen (brightness calibration, warning/disclaimer — e.g.
     Ikaruga counts down ~300 s before the game even starts), attract was never reached and
     the metrics are unrepresentative — re-run with `--secs 900` (or higher until attract
     appears in the shots) and use that sidecar. Record which of the three states the run
     reached — `{{calibration screen | title only | demo reached}} — evidence screenshot` —
     plus capture length and the static-screen duration in doc §3. Also set
     `capture.coverage` in the sidecar to `demo` / `title` / `calibration` (the battery
     writes `null`) — RANKING.md shows it as a ⚠ flag so lower-bound scores are visible
     in the table, not just in the doc.
   - `PARKED G1 …` → verify it is the game, not tooling: check `assessments/evidence/<set>/raw/stdout.log`,
     the screenshots, and `boot.mame_not_working` in the sidecar. Write the short-form doc (§ Parked below).
     Battery v2 retries the no-handoff flake once automatically; if it still parks after the auto-retry, then diagnose.
   - `UNSCORED (controls research required)` → continue; scoring happens in step 3.
2. **Controls research:** determine the real cabinet controls. Sources in priority order:
   MAME `naomi.cpp` input ports (already cited in the sidecar) > game manual/flyer scans >
   Sega Retro/System16 hardware pages > wikis. Record ≥2 sources with URLs.
   Set `controls.device_class` in the sidecar to one of: `stick`, `dc_peripheral`,
   `pad_adaptable`, `awkward` — or, for physically unmappable hardware (card reader/printer,
   medal/hopper, mandatory multi-cabinet), replace `review` with the raw hardware name (e.g.
   `card_reader`): score.py turns any off-ladder value into gate G2. Append your sources to
   `controls.sources`.
   Also research **existing community/fan DC ports** of the game; note findings for the doc.
3. **Score:** `python3 tools/assess/score.py assessments/<set>.metrics.json`
4. **Write the doc:** copy `assessments/TEMPLATE.md` → `assessments/<set>.md`; fill every
   `{{…}}` from the sidecar and your research. Never hand-edit a number the sidecar owns —
   quote it. Every claim needs its citation (log tag, screenshot path, or URL).
5. **Tables:** `python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch`
6. **Update QUEUE.md** status cell for the family (`pending` → `done` / `parked`).
7. **Curate evidence:** keep at most 5 representative screenshots (boot / title /
   attract-demo), delete the surplus `shot-*.png`; the sidecar's `capture.screenshots`
   deliberately lists every shot the battery took — the committed set is the curated subset.
8. **Commit:** `git add assessments/<set>.md assessments/<set>.metrics.json
   assessments/evidence/<set>/*.png assessments/RANKING.md assessments/QUEUE.md GAME_FORMATS.md`
   then commit `assess(<set>): <final> <tier>` (or `parked <gate>`).
   NEVER add `evidence/<set>/raw/` or anything under `tools/assess/out/` or `tools/dat-extract/out/`.
9. **Lessons:** anything surprising (tool quirk, new failure class, scoring edge) →
   append to `docs/kb/assessment-tooling.md`.

## Parked short-form doc

Use TEMPLATE sections 1–3 only, plus a `## Gate` section: which gate, the evidence
(log line / screenshot / source), and what would unblock the game.

## Campaign checkpoint

After ~30 assessed families: run the scoring-semantics checkpoint in
`docs/kb/assessment-tooling.md` §6 (G3-ARAM threshold; streaming re-read penalty) and
decide whether `score.py` needs revision before the queue burns further down.

## Re-assessment rule

If instrumentation or `score.py` changes materially, bump `BATTERY_VERSION` in
`run_battery.py`; sidecars with an older version are stale — re-run them before
comparing scores (spec §7).
