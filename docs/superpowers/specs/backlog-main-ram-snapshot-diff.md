# Backlog: main-RAM write-truth via snapshot+diff

**Status:** proposed 2026-08-06 (batch: DC-ported ★ assessments). Not started.

## Goal

Replace the main-RAM footprint metric (currently `CARTDMA` dest high-water) with a
snapshot+diff write-truth high-water over the 16 MB main window, the same mechanism
`VRAMPROFILE`/`ARAMPROFILE` already use: snapshot at handoff, diff on a coarse cadence
(~5 s), track the high-water of *changed* addresses.

Why it's load-bearing (two birds):

1. **PIO-loading carts are blind today.** `gwing2` measured `dma_high_water = 0` with
   1,344 DMA events (cart→main loading is PIO); `sgtetris` was invisible entirely
   (parked G1 despite visibly running — kb §4.v). Worse, `score.py` maps a blind 0 to
   u=0 → main sub-score 100.0 "from nothing"; only the ARAM gate saved gwing2 from a
   fabricated memory axis (`assessments/gwing2.md` § Gate, tension 2).
2. **Retires the spec's v1 limitation for everyone:** DMA high-water measures where
   assets *land*, not the working set, and misses CPU-written data above the last DMA'd
   asset. The suspicious main high-water clustering across GD titles (kurucham 27.4 /
   ss2005 27.5 / takoron 29.4 / tetkiwam 30.5 MB — `tetkiwam.md` §9, kb §6 item 3)
   needs exactly this cleaner metric to resolve.

## Read first

- `assessments/sgtetris.md` § Gate and `assessments/gwing2.md` § Gate — the two faces
  of the blind spot, with sidecar evidence
- `docs/kb/assessment-tooling.md` §4.v — the failure class + triage rule
- Fork's VRAM/ARAM profile implementation (the `VRAMPROFILE`/`ARAMPROFILE` emitters) —
  the machinery to clone; note the pre-`VRAMHANDOFF` sample-drop lesson (kb §9): the
  main snapshot must baseline at handoff, never against a null/BIOS-era baseline
- `tools/assess/parse_capture.py` — where a `MAINPROFILE` line would be parsed
- Memory rule: instrumentation never mutates the guest — snapshot+diff only

## Design decisions to settle in-session

- Cadence: 16 MB memcmp per tick — measure cost; ~5 s is likely fine, vblank is not
- Handoff baseline for PIO titles: what event anchors the snapshot when neither
  `CARTDMA` nor `ARAMHANDOFF` fires (sgtetris)? Candidates: first `CARTPIO` read
  (needs the small PIO-counter tag, see below) or PC-leaves-BIOS on a vblank sample
- Whether the cheap interim scorer guard lands first: `dma_high_water == 0` with
  `dma_events > 0` ⇒ main axis *unmeasured* (renormalize or gate) — one evening,
  kills the 100-from-nothing hazard before any fork work
- The related `CARTPIO` byte-counter tag (handoff signal + streaming lower bounds for
  PIO titles) can ride the same fork change — decide whether to bundle

## Constraints

- Fork change ⇒ `BATTERY_VERSION` bump; prior sidecars' main figures stale per the
  re-assessment rule (spec §7) — plan a re-run wave, anchors first
- Anchors (`cleoftp`, `ikaruga`) must keep their real-DC-verified results; guard tests
  and the calibration guard must stay green — never weakened to pass
- `sgtetris` becomes the regression control for the PIO face once measurable —
  golden it like inunoos/ausfache/ikaruga (kb §10)

## Done means

- `MAINPROFILE` (or equivalent) emitted by the fork, snapshot at handoff, high-water of
  changed addresses in the sidecar; `memory.main` scored from it
- sgtetris assessable end-to-end (un-parks or parks for a *real* reason)
- gwing2 main axis measured, not blind
- Guard test: blind-main sidecar shape can never score 100
- kb lesson updated (§4.v gets a RESOLVED note), BATTERY_VERSION bumped, re-run wave
  recorded
