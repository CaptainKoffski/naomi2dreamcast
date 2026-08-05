# Backlog: carve-pipeline calibration guard

**Status:** not started. Written 2026-08-06 as the session brief for a future
session — start that session with:
`Implement the calibration guard per docs/superpowers/specs/backlog-calibration-guard.md`

This is the thing `tools/assess/carve_boot.py`'s comment calls the "planned
Task 9" byte-compare. Note: that name collides with the *historical* Tasks
1-10 numbering in `docs/kb/assessment-tooling.md` §4 — call it the
**calibration guard** and update the stale comment as part of the work.

## Goal

A regression check that catches silent carve-pipeline drift — carve
known-good set(s) end-to-end (cart2dat/chd2dat → carve_boot) and compare the
produced `boot.bin` against committed sha256 hashes. Hashes only, NEVER the
bytes: ROM-derived content is copyrighted and stays gitignored.

Why it's load-bearing: the bit-30 mask (commit 32e99e3) plus the two cheap
guards (illegal flag bits, entrypoint-in-range, commit 22d765f) leave one
undetectable window — garbage within the legal bits that lands in-file
carves plausible-but-wrong bytes. Per-title that is unfixable at carve time;
pipeline-level goldens are the real backstop (final-review risk note,
2026-08-06).

## Read first

- `tools/assess/carve_boot.py` — the two existing cheap guards this
  complements, and the stale "Task 9" comment to fix
- `tools/assess/run_battery.py` — `static_scan()` and `selftest()`;
  `selftest()` already refuses to run on poisoned metrics
  (`MetricRegression`, kb §7) and is the natural home for a pipeline check
- `tools/dat-extract/cart2dat.py` and `chd2dat.sh` — the .dat producers
- `docs/kb/assessment-tooling.md` §4.q RESOLVED note and §7 (the
  refuse-to-score philosophy this guard should follow)
- `docs/superpowers/specs/2026-08-06-m4-carve-support-design.md` (the M4
  work this backstops; see Out of scope)

## Design decisions to settle in-session (brainstorm before coding)

- **Which golden sets:** each pipeline flavor covered — at least one M2
  cart, one M4 cart (ausfache is freshly validated), one GD-ROM via
  chd2dat. Verify the candidates carve cleanly today before blessing them.
- **Where the check runs:** battery-start `selftest()` vs. inside
  `static_scan`; consider runtime (a GD chd2dat pass is slow — measure
  before deciding).
- **On mismatch:** refuse loudly in the spirit of `MetricRegression` — a
  drifted pipeline must never write a verdict.

## Constraints

- Needs local ROMs under `naomi/` and the `../cleopatra` checkouts — run on
  this machine against real artifacts; no mocked "golden" data.
- Tests are plain-assert `__main__` scripts (repo convention).
- Batteries run serially.
- Record exact hash-generation commands so the goldens are reproducible;
  commit hashes + method, never dumps.

## Done means

- Golden-hash table committed with provenance (set, tool versions, date).
- The check wired in and failing loudly on drift.
- A test covering the mismatch path.
- `carve_boot.py`'s stale "planned Task 9" comment updated to point here /
  at the implemented guard.
- A kb note recording the guard's existence and how to regenerate goldens.
