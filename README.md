# naomi2dreamcast

Umbrella repo for porting games from the **Sega Naomi** arcade system to the
**Sega Dreamcast**. The two machines share a CPU and GPU family; the hard part
is memory — Naomi has far more RAM/VRAM/ARAM than a Dreamcast. So before
porting anything, every game in the library gets a uniform **portability
assessment**, and games are ported easiest-first. Proven reference case:
the fan port of [*Cleopatra Fortune Plus*](https://github.com/CaptainKoffski/cfp2dreamcast).

This repo stores the library inventory, the assessment method and tooling, the
per-game assessment results, and the shared knowledge base. Individual ports
live in their own repos.

## Where things are

| Path | What it is |
|---|---|
| [`GAME_FORMATS.md`](GAME_FORMATS.md) | Full library inventory & triage sheet — every set's format (cart/GD-ROM), size, genre lane, official-DC-port status, assessment score |
| [`assessments/RANKING.md`](assessments/RANKING.md) | All assessed games sorted by ease-of-port score (generated, don't hand-edit) |
| [`assessments/QUEUE.md`](assessments/QUEUE.md) | Assessment work queue, one row per game family |
| [`assessments/RUNBOOK.md`](assessments/RUNBOOK.md) | Day-to-day steps to run an assessment |
| [`assessments/<set>.md`](assessments/) | Per-game assessment report + `<set>.metrics.json` sidecar (machine-readable scores) |
| [`docs/superpowers/specs/2026-08-02-portability-assessment-design.md`](docs/superpowers/specs/2026-08-02-portability-assessment-design.md) | The assessment method: criteria, formulas, scoring |
| [`docs/kb/assessment-tooling.md`](docs/kb/assessment-tooling.md) | Reproducibility record — exact tool versions, invocation, calibration, lessons learned |
| [`docs/producing-the-dat.md`](docs/producing-the-dat.md) | What a `.dat` (decrypted DIMM image) is and when you need one |
| [`tools/assess/`](tools/assess/) | Assessment battery: capture runner, parsers, scorer, table generator (stdlib-only Python) |
| [`tools/dat-extract/`](tools/dat-extract/) | Convert a romset into a Ghidra-loadable `.dat` (cart M1/M2/M4 + GD-ROM) |
| [`GENERAL_CHECKLIST.md`](GENERAL_CHECKLIST.md) | Hardware validation checklist for finished ports |
| `naomi/` | The romset library — **gitignored, never committed** |

## How a game gets assessed

1. **Boot gate** — the set must run in the instrumented
   [Flycast fork](https://github.com/CaptainKoffski/flycast4naomi2dreamcast).
2. **Dynamic capture** — `tools/assess/run_battery.py` runs the game unattended
   through its attract/demo cycle (600 s) and logs RAM/VRAM/ARAM usage and
   GD-ROM streaming.
3. **Static analysis** — Ghidra headless pass over the game's `.dat`
   (produced by `tools/dat-extract/`) for code/"guts" scoring.
4. **Controls & research** — control scheme from pinned MAME source, plus
   per-game research (official DC releases, exotic hardware).
5. **Scoring** — `tools/assess/score.py` folds it all into one 0–100
   ease-of-port number; `gen_tables.py` regenerates RANKING/QUEUE.

Method details and every scoring rule live in the
[design spec](docs/superpowers/specs/2026-08-02-portability-assessment-design.md);
version history and calibration proof in the
[tooling KB](docs/kb/assessment-tooling.md).

## Ground rules

- **No copyrighted bytes in git** — ROMs, BIOS, disc images, `.dat`s are all
  gitignored. The repo ships method, tools, and results only.
- **Claims carry citations** — hardware/behavior facts cite primary sources
  (MAME/Flycast source, RE'd docs), not wikis.
- **Reproducibility** — every tool install and version is pinned and recorded
  in the KB so any session can rerun the pipeline.
- **Emulator ≠ proof** — final ports must pass the real-hardware checklist in
  [`GENERAL_CHECKLIST.md`](GENERAL_CHECKLIST.md).
