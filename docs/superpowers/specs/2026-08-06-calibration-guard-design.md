# Design: carve-pipeline calibration guard

**Date:** 2026-08-06. **Supersedes:** the open decisions in
`backlog-calibration-guard.md` (which stays as the motivating brief).

## Goal

A regression check that catches silent carve-pipeline drift: carve known-good
sets end-to-end (cart2dat/chd2dat → carve_boot) and compare against committed
sha256 hashes. Hashes and metadata only — ROM-derived bytes are copyrighted
and never committed.

Why: the bit-30 mask plus the two cheap guards in `carve_boot.py` (illegal
flag bits, entrypoint-in-range) leave one undetectable window — garbage
within the legal bits that lands in-file carves plausible-but-wrong bytes.
Per-title that is unfixable at carve time; pipeline-level goldens are the
backstop.

## Decisions (settled 2026-08-06, brainstorm session)

- **Golden sets — one per pipeline flavor:** `inunoos` (M2 cart), `ausfache`
  (M4 cart), `ikaruga` (GD-ROM). All three verified to carve cleanly on
  2026-08-06. `ikaruga` is already a `DC_SHIPPED_ANCHOR`, so blessing it
  reinforces an existing control. Rejected: blessing all assessed sets
  (broader edge coverage, but slower checks and full re-bless churn on every
  legitimate pipeline change).
- **Siting — unconditional in `run_battery.selftest()`:** measured runtimes
  are cart2dat ≈ 1.1 s per cart set and chd2dat ≈ 13 s for ikaruga, so the
  full three-flavor pass costs ~15 s against a 10+-minute battery. Running it
  every battery start also catches *environment* drift (chdman upgrade,
  recompiled `extract_dat`, 7zz change) that no repo-side trigger can see.
  Rejected: source-hash gating (blind to environment drift, adds stamp-file
  state) and standalone-only (silent drift stays silent).
- **On mismatch — refuse loudly:** the battery must never write a verdict
  through a drifted pipeline. Same posture as `score.py MetricRegression`
  (kb §8) and the existing `selftest()` red-test refusal.

## Components

### `tools/assess/calibration.py` (new)

Two modes:

- **Check (default):** for each golden set, run its producer
  (`cart2dat.py <set>` / `chd2dat.sh <set>`) into a temp dir, sha256 the
  `.dat`, carve with `carve_boot.carve()`, sha256 the boot blob, and compare
  `.dat` hash, boot hash, and carve meta (`base`, `entry`, `size`) against
  the golden table. The meta compare catches a shifted-base drift that leaves
  blob bytes identical. Delete the `.dat` immediately after hashing —
  decrypted dumps never persist. On mismatch, name the set, the stage
  (`.dat` mismatch = producer drift, boot/meta mismatch = carve drift), and
  expected vs got; exit nonzero.
- **`--bless`:** same pipeline run, then write the golden table with
  provenance. Used once at implementation time and whenever a pipeline change
  is intentional; the diff is reviewed and committed like any other change.

The comparison core is a pure function `compare(goldens, results) →
failures` so tests can drive it without ROMs.

### `tools/assess/calibration-goldens.json` (new, committed)

Per set: flavor, producer command, `.dat` sha256, boot sha256, carve
`base`/`entry`/`size`. Plus provenance: bless date, chdman version, repo
commit. Hashes and metadata only — never bytes.

Cross-check values observed 2026-08-06 (the bless run must reproduce these):

| set | .dat sha256 (prefix) | boot.bin sha256 (prefix) | base/entry |
|---|---|---|---|
| inunoos | `1ccddea101f9e38e` | `cc89bbbaab47fd7e` | 0x0c020000 / 0x0c021000 |
| ausfache | `42bc1292b2e19e42` | `cfd8460ec1ba24c7` | 0x8c020000 / 0x8c021000 |
| ikaruga | `d435938becdeb794` | `bcab6911ab9f8318` | 0x8c020000 / 0x8c021000 |

### `run_battery.py` (edit)

`selftest()` gains a third step: run `calibration.py` (check mode) after the
two test scripts; nonzero exit → the existing `sys.exit` refusal, with a
message that includes the re-bless instruction for intentional changes.

## Data flow

One direction: `calibration-goldens.json` (git) → check run (local ROMs
under `naomi/`, `../cleopatra` checkout for naomi_roms.cpp) → pass or
refuse. Nothing else reads the golden table.

## Error handling

Every failure path refuses loudly; there is no degrade-to-warning:

- Hash/meta mismatch → named set + stage + expected vs got, exit 1; battery
  never starts.
- Golden ROM missing from `naomi/` → refuse (not skip): the guard cannot
  establish pipeline health without it, and this machine is the designated
  runner.
- Producer nonzero exit or `carve()` raise → refuse with captured output.

## Testing

`tools/assess/tests/test_calibration.py` — plain-assert `__main__` script
(repo convention) driving `compare()` with fabricated results: clean pass,
hash mismatch, meta mismatch, missing set. No ROMs, milliseconds.

Not added to `selftest()`'s test list: the guard itself already runs there
every battery; the real end-to-end path needs no second driver.

## Doc updates

- `carve_boot.py` — replace the stale "planned Task 9" comment (the
  hdr-relative-ambiguity note) with a pointer to `calibration.py` and the kb
  note.
- `docs/kb/assessment-tooling.md` — new section: the guard exists, the
  window it closes, and the regen procedure (`calibration.py --bless` →
  review diff → commit).
- `docs/superpowers/specs/backlog-calibration-guard.md` — status flipped to
  implemented, pointing here.

## Done means

- `calibration-goldens.json` committed with provenance.
- Guard wired into `selftest()`, refusing loudly on drift.
- `test_calibration.py` covers the mismatch paths.
- Stale comment updated; kb note written; brief status flipped.
