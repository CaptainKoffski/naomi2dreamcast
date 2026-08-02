# Assessment battery — tooling & reproducibility record

Campaign version: **battery v2** (`BATTERY_VERSION = "2"` in `tools/assess/run_battery.py`).
This doc is the reproducibility record required before the campaign runs the 84-family
queue in `assessments/QUEUE.md` — exact tool versions, invocation, env knobs, what each run
produces/discards, the two calibration results that establish the battery is trustworthy,
and every troubleshooting lesson from Tasks 1–10 that cost real time. Method/formulas:
`docs/superpowers/specs/2026-08-02-portability-assessment-design.md`. Day-to-day steps:
`assessments/RUNBOOK.md`.

## 1. Toolchain pins

| Tool | Version / commit | Source |
|---|---|---|
| Instrumented Flycast fork | `9e882cbd2` at `../cleopatra/tools/flycast-src` | Cleopatra project's build, reused **as-is** — zero C++ changes made for this battery (see §2 GD-path finding below for why no `gdcartridge.cpp` patch was needed) |
| Ghidra | `12.1.2_PUBLIC` (build `20260605`) | Installed per `../cleopatra/docs/kb/tooling.md` — no Homebrew cask exists; direct download: `curl -L https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.2_build/ghidra_12.1.2_PUBLIC_20260605.zip`, extracted to `../cleopatra/tools/ghidra_12.1.2_PUBLIC/` (gitignored) |
| Java | OpenJDK, Ghidra requires 21+ | `brew install openjdk` (formula, no sudo); actual installed version this session: **26.0.1** (`java -version` → `openjdk version "26.0.1"`). `tools/assess/ghidra/run_guts.sh` prepends `/opt/homebrew/opt/openjdk/bin` to `PATH` before invoking `analyzeHeadless` |
| MAME source (naomi.cpp reference) | `59e7c0b` at `../cleopatra/tools/mame` | Pinned checkout; `controls_extract.py` and every sidecar's `controls.sources` cite this exact commit — never a live/floating MAME checkout |
| Battery | **v2** | `tools/assess/run_battery.py` — 600 s default capture, `BATTERY_VERSION = "2"` in every sidecar's `versions.battery` |
| macOS | `sw_vers -productVersion` → `26.5.2` (this session) | Record per-session; capture timing (`no-handoff-120s` abort, retry logic) is wall-clock-based and OS-version-sensitive in principle |
| Python | `python3 --version` → `Python 3.14.3` (this session) | No third-party packages — every `tools/assess/*.py` is stdlib-only (`json`, `re`, `glob`, `subprocess`, `time`) |

## 2. Battery invocation, env knobs, per-run artifacts

### Once per session (`assessments/RUNBOOK.md` §"Once per session")

```bash
python3 tools/assess/tests/test_score.py   # must print ALL OK — toolchain sanity gate
mkdir -p tools/assess/out && python3 tools/assess/controls_extract.py > tools/assess/out/controls.json
cp ../cleopatra/bios/naomi.zip ~/Library/Application\ Support/Flycast/data/   # if missing
```

### Per family

```bash
python3 tools/assess/run_battery.py <set>              # ~10 min unattended, default 600 s
python3 tools/assess/score.py assessments/<set>.metrics.json
python3 tools/assess/gen_tables.py ranking && python3 tools/assess/gen_tables.py patch
```

### Env knobs (all optional; defaults point at the sibling `../cleopatra` checkout)

| Var | Consumed by | Default |
|---|---|---|
| `FLYCAST_BIN` | `run_battery.py` | `../cleopatra/tools/flycast-src/build/Flycast.app/Contents/MacOS/Flycast` |
| `NAOMI_DIR` | `run_battery.py` | `<repo>/naomi` |
| `MAME_NAOMI` | `controls_extract.py` | `../cleopatra/tools/mame/src/mame/sega/naomi.cpp` |
| `GHIDRA_HOME` | `tools/assess/ghidra/run_guts.sh` | `../cleopatra/tools/ghidra_12.1.2_PUBLIC` |
| `ASSESS_GHIDRA_PROJ` | `tools/assess/ghidra/run_guts.sh` | `<repo>/tools/assess/out/ghidra-proj` |

### Per-run artifacts

Each `run_battery.py <set>` call writes:
- `assessments/<set>.metrics.json` — the committed sidecar (scores, memory/streaming/guts/
  controls/similarity, `versions`, `params`).
- `assessments/evidence/<set>/shot-*.png` — one screenshot per 60 s tick, **committed** after
  hand-curation (RUNBOOK: delete near-duplicate attract-loop repeats, keep the distinct/
  representative frames — typically 3-5 kept of ~10 captured).
- `assessments/evidence/<set>/raw/` — `cartlog.txt` (full DMA/handoff trace, can be 100s of MB),
  `stdout.log`, `timeline.json`, full-res `shot.png` scratch file. **Gitignored**
  (`assessments/evidence/*/raw/` in `.gitignore`) — regenerable from a re-run, and `cartlog.txt`
  can embed byte content read off the cart/disc. Never staged.
- `tools/assess/out/` (controls.json, `<set>.boot.bin`, `<set>.guts.json`, `ghidra-proj/`) —
  entirely gitignored scratch. `<set>.boot.bin` is a **decrypted first-1MB carve of the cart's
  own code** — a copyrighted dump — and `static_scan()`'s `finally` block deletes both the
  `.dat` and `.boot.bin` after each run unless `--keep-dat` is passed (never pass it outside a
  one-off debugging session; nothing under `tools/dat-extract/out/` or `tools/assess/out/` is
  ever committed, per the project's copyrighted-bytes rule).

## 3. Calibration results (the battery's control-test anchor)

Two calibration sidecars exist, both re-run under battery v2 for uniformity, both docs marked
with a "calibration reference" banner and excluded from the queue proper.

**Calibration A — `cleoftp`** (`assessments/cleoftp.md`, `assessments/cleoftp.metrics.json`):
scores **84.2 S** under v2 (was 84.7 S under v1 — only the streaming axis moved, 70.8→69.0,
pure dilution from the longer 600 s window, not an error). Reproduces the completed
`../cleopatra` port's own Phase 2/5 instrumented measurements **bit-identically**: main RAM
DMA high-water 11,761,888 B, VRAM write-truth peak 8,181,717 B (7.8 MiB, `nz_above_cap = 0`),
ARAM write-truth peak exactly 2,097,152 B (2 MiB, `nz_above_cap = 0`) — all three held across
every clean run this title has had (v1 run 1, run 2, retry, v2 re-run). This is the project's
CLAUDE.md rule-2 control test: a known-good, real-hardware-verified reference run through the
same measurement path, proving the battery's own instrumentation before trusting it on anything
else. `serial_pokes`/`guts.functions=1645`/`guts.flags=[eeprom_bios,serial,rtc]` also reproduce
exactly.

**Calibration B — `ikaruga`** (`assessments/ikaruga.md`, `assessments/ikaruga.metrics.json`):
**PARKED `G3 memory: aram peak > 2x DC capacity`** — not a numeric score, by design. Its actual
purpose (does the logged `CARTDMA` path see GD-ROM/DIMM streaming, not just cart-image
streaming) **PASSED**: `streaming.dma_events = 396`, reproduced identically at both a 360 s (v1)
and a 600 s (v2) capture — proof the DMA events all land during boot, well before either window
closes. Because this came back nonzero on the very first run, the brief's contingency (patching
`../cleopatra/tools/flycast-src/core/hw/naomi/gdcartridge.cpp` to add a `cartlog` call and
rebuilding Flycast) was **never needed** — the existing `Naomi_DmaStart` instrumentation already
covers GD-ROM traffic. The G3 park is separate, real data: `memory.aram.peak = 8,388,608 B`
(exactly 8 MiB, Naomi's full ARAM bank) against the DC's 2 MiB AICA RAM cap — 4.00× utilization,
over `score.py`'s gate threshold (`u > 2.0`).

## 4. Lessons learned (Tasks 1–10)

**a. Launch flake (~1-in-3 to 1-in-4 Flycast launches hang at the DC BIOS home menu).**
Signature: `boot.failure_class = "no-handoff-120s"`, `cartlog.txt` holds zero
`ARAMHANDOFF`/`CARTDMA` tags, and the curated screenshots show the stock Dreamcast BIOS home
menu (swirl logo, Play/File/Music/Settings) instead of the cart — the game never loaded at all,
it isn't a game-code hang. `cleoftp` alone flaked on 2 of 6 total launches across both
calibration sessions. Battery v2 auto-retries once per candidate rom (`run_battery.py`'s
`no-handoff-120s` branch, tries the same file again before falling through to the next
candidate). Observed once (`cleoftp`'s v2 re-run) that even the automatic retry wasn't enough —
it exhausted both the `.zip` and `.chd` fallback candidates (each auto-retried) and still
parked; a fully manual re-run of the identical command then cleared it. Remedy: on a `PARKED
G1`/`no-handoff-120s` result for a set with a prior clean sidecar, retry manually once more
before treating it as a real failure or escalating to an explicit `--rom` override.

**b. Static pre-game screens can eat most of the capture window.** Ikaruga counts down
roughly 330 s of a brightness/contrast calibration screen (Naomi cabinet setup UI, standard,
not a fault) before the title screen even appears — user-observed and confirmed by an exact
1-count/sec countdown (270 at t=60s → 24 at t=306s → auto-start ≈t=330s). Under v1's 360 s
default capture this left only ~30 s past the calibration screen, measuring essentially
nothing representative. This is why battery v2 defaults to **600 s** and RUNBOOK now mandates
a screenshot representativeness check before trusting any sidecar's streaming/attract-derived
figures.

**c. Free-play title-idle: some games never enter a demo loop at all.** Ikaruga's cabinet
capture is configured FREE PLAY, which appears to suppress the attract/demo loop entirely —
the capture sits on a blinking "PRESS START BUTTON" title screen for the full 600 s with zero
attract content, confirmed by two post-title screenshots 238 s apart being byte-identical
(same MD5). This means "boots fine" alone doesn't distinguish a real attract-demo capture from
a title-idle-only one. Every run must record which of **three states** it reached — calibration
screen / title-only / attract-demo — and title-only metrics must be flagged as lower bounds for
VRAM and streaming (real gameplay would very likely push both higher). ARAM is the exception:
in both calibration games the full ARAM bank loads at boot (before the title screen even
appears, bit-identical across different capture lengths), so ARAM peaks are usually **not**
understated by a title-idle capture.

**d. The G3 ARAM gate may be too aggressive as currently tuned.** Ikaruga's official Dreamcast
port (2002) shipped and ran inside the DC's real 2 MiB ARAM — a real, released 4× sound-data
trim, proving the reduction the gate implies is needed is actually achievable. That makes a
flat "Naomi asset size > 2× DC capacity ⇒ hard gate" reading questionable specifically for the
ARAM axis (as opposed to main RAM/VRAM, where no such counter-evidence exists yet). Flagged as
a candidate for a future `score.py` revision (e.g. a softer ARAM curve, or weighting against
known DC-port precedent) — **deliberately not changed mid-campaign**; the gate stands as
measured for both calibration docs.

**e. Deferred v3 idea: scripted START-press injection.** A future Flycast fork change could
inject a deterministic START button-press sequence (still no human input, fully scripted) to
push free-play title-idlers like Ikaruga into real gameplay coverage, closing lesson (c)'s
lower-bound gap. Not built this campaign — noted for a later battery version.

**f. Carve validation: the cleoftp carve is byte-identical to the known-good reference.**
`carve_boot.py`'s output for `cleoftp` (`tools/assess/out/cleoftp.boot.bin`, 1,048,576 bytes)
matches `../cleopatra/tools/boot.bin` **byte-for-byte**: same size, same SHA-1
(`3fb069a4966668a3bd95206ce166a0a9f632f083`) — the strongest possible proof the carve pipeline
(`chd2dat.sh` → `carve_boot.py`) is correct, not just plausible. However, `cleoftp`'s `.dat` has
`hdr_at = 0` (header at absolute file offset 0), so this run never exercised the header-relative
branch of `carve_boot.py`'s offset heuristic (`if hdr > 0 and rom < 0x100000: rom = hdr + rom` —
i.e. "small ROM offset ⇒ interpret as relative to a header that sits at `0x800000`"). That
branch is covered only by `test_carve_boot.py`'s synthetic `test_carve_fallback` test — watch
it closely on the first real GD-ROM set in the queue whose header actually sits at `0x800000`.

**g. MAME input-ports hints can hide the real cabinet hardware.** 19 sets share the plain
`input_ports = "naomi"` fragment (an ordinary 2p-joystick-plus-buttons panel) with genuine
stick games, but are actually card/medal/hopper hardware: the 12 World Club Champion Football
sets (trading-card scanner is the core mechanic), 3 Club Kart Prize sets (ticket/prize
dispenser), 3 Shootout Pool Prize/Medal sets (redemption cabinet — `shootplm`'s machine config
is literally `naomim1_hop`, a hopper board), and the standalone `hopper` (SWP Hopper Board)
diagnostic ROM. `controls_extract.py`'s `HINT_OVERRIDES` forces all 19 to `device_class_hint =
"review"` (never an auto-set final class) — never trust the shared input-port name alone as
proof of cabinet type; the researching agent must confirm real hardware per RUNBOOK step 2.

## 5. Campaign start checklist

The battery is calibrated (§3) and the queue is generated. From here the campaign is pure
RUNBOOK execution:

1. Read `assessments/RUNBOOK.md` in full (once-per-session prereqs, per-family steps, parked
   short-form doc shape, re-assessment rule).
2. Open `assessments/QUEUE.md` — 84 families, ★ genres (puzzle/shmup) sorted first. Work top
   to bottom, or hand-curate the order if a different priority makes sense.
3. Per family: run the battery → research controls → score → write the doc from
   `assessments/TEMPLATE.md` → regenerate `RANKING.md`/patch `GAME_FORMATS.md` → flip the
   family's `QUEUE.md` status cell → commit (RUNBOOK's exact file list) → append any new
   >10-minute lesson to this doc's §4.
