# Design: G3-ARAM gate + axis re-keyed on content volume

**Date:** 2026-08-07. **Supersedes:** the open decisions in
`backlog-aram-gate-volume.md` (which stays as the motivating brief).
**Checkpoint status:** the §6 scoring-semantics checkpoint was ruled **open**
at 25 assessed families (user ruling, this session) — this is the first §6
semantics change decided under it.

## Goal

Key the ARAM region of `score.py`'s memory axis — the `u > 2.0` G3 park *and*
the sub-score — on **compacted content volume** (`content_below2m +
content_above2m`) instead of the content high-water *address* (`content_high`).
ARAM layout is a porting artifact: OSB banks are position-independent, verified
live on the azumanga dump (`assessments/azumanga.md` § ARAM bank-structure
verification), so a port rebuilds banks and the address a blob happens to sit
at carries no fit information. The volume does.

The divergent pair that forced this: `gwing2` parked at address-u 3.99 from
48,674 B of content above cap (volume-u ≈ 1.02, reproduced across v5/v6 runs
with a 12 B delta); `takoron` has 4,347,346 B above cap (volume-u ≥ 3.1) —
genuinely unfittable. Address keying cannot tell them apart
(`assessments/gwing2.md` § Gate, tension 1).

**Addendum found in-session:** the brief's list of seven parked sets missed
`sgtetris` — ARAM-parked with `nz_above_cap = 8 B`, a divergence even more
extreme than gwing2's. Eight sets are ARAM-parked, not seven.

## Rulings (settled 2026-08-07, brainstorm session — user decisions)

1. **Checkpoint open now.** Rule + implement at 25 families; the ~30 in the
   brief was approximate.
2. **Full volume keying** — gate *and* axis use one `u`. Gate-only re-keying
   was rejected: it would unpark gwing2 yet still crush its sub-score to the
   10 floor from an address the port would never keep.
3. **No `.p16` discount now.** Raw `.p16` BGM in inter-bank gaps (headerless,
   GD-streamable — azumanga finding) stays counted in volume. A new
   maybe-marked brief `backlog-aram-p16-discount.md` records pros/cons,
   possible ranking impact, and the evidence bar.
4. **Keying-only; §6 item 1 (the 2× multiple itself) is ruled after the
   wave**, with the measured volume distribution this design produces.
   inunoos/pokasuka/takoron (volume-u ≥ 2.2) stay parked under this design
   and are item 1's material.
5. **Approach A — volume when present, address fallback.** Math: content
   bytes live in `[0, content_high]`, so `content_total ≤ content_high + 1`
   ⇒ volume-u ≤ address-u always ⇒ the fallback can only *under*-score,
   never over-score. Legacy sidecars stay conservative-comparable; no
   25-family re-run (15 of those runs provably cannot change any final).

## Design

### Parser — `tools/assess/parse_capture.py`

- `_APROF` gains a capture group for `content_below2m` (the fork **already
  logs it** on every `ARAMPROFILE` line; the regex deliberately skips it
  today). No fork change.
- Per sample: `total = content_below2m + content_above2m`;
  `aram["content_total"]` = max of **per-sample totals** — never
  `max(below) + max(above)`, which could combine bytes from two snapshots
  into a volume that never existed at once.
- Legacy logs without `content_*` fields: the key is absent from the sidecar
  (no zero-fill).
- Sidecar schema: `memory.aram.content_total` (bytes). `peak` (= content
  high-water address) and `nz_above_cap` are unchanged — informational +
  DMPD canary respectively.

### Scorer — `tools/assess/score.py`

- ARAM fit value: `content_total` when present, else `peak` — an explicit
  `is not None` check, **not** `or`: a genuine 0-byte volume must not fall
  back to an 8 MiB address.
- `region_score` / `memory_axis` / the `u > 2.0` park threshold / the
  piecewise map are untouched; ARAM just feeds a different byte count.
- ARAM park message becomes `G3 memory: aram content > 2x DC capacity`
  (main/vram keep "peak"; one-word-per-region lookup). Only `score.py`
  generates this string — `RANKING.md` regenerates and nothing parses it.
- DMPD canary (`nz_above_cap == 0x600000`) and the cleoftp/ikaruga anchor
  guard are unchanged. Anchors are safe by construction: volume ≤ address,
  so re-keying can only move a title *away* from parking.

### Guard tests — `tools/assess/tests/`

1. Small-blob-at-high-address synthetic (volume ≈ 2.1 MiB, address 8 MiB):
   **not parked**, aram sub ≈ 81 (`test_score.py`).
2. 2 MiB+-volume synthetic (4.4 MiB): **parks**, message says "content".
3. Sidecar without `content_total`, address 8 MiB: still parks — legacy
   fallback preserved.
4. Parser: `content_total` captured from an `ARAMPROFILE` line; per-sample-max
   semantics proven with two samples where `max(below)+max(above)` gives a
   different (wrong) answer (`test_parse_capture.py`).
5. Existing anchor + DMPD guards stay green; never weakened.

## Campaign ops

### Re-run wave — 10 sets, serial, ~10 min each

Raw cartlogs are rotated by SSD hygiene (only the latest battery's survives),
so sidecars gain `content_total` only via re-runs. Wave:

- **8 ARAM-parked:** azumanga, cspike, gwing2, inunoos, pokasuka, sgtetris,
  takoron, zerogu2.
- **2 scored sets whose finals can move:** ausfache and cleoftp — the only
  scored families whose *binding* min region is ARAM (85.0 / 85.1). Volume
  keying can only raise them; measurement decides how far.

Standard battery per `assessments/RUNBOOK.md` + the headless recipe (one
Flycast instance at a time). Every other family: no re-run — ARAM is not
their binding min and the sub-score can only rise, so finals are provably
unchanged under the fallback.

### Versioning / comparability

- **`BATTERY_VERSION` bumps "6" → "7"** (user ruling at spec review,
  overriding the brief's no-bump-if-capture-unchanged clause): the sidecar
  schema gains `aram.content_total` and the scoring semantics change, so the
  provenance column in `RANKING.md` should distinguish volume-keyed runs.
  v7 note: ARAM volume keying — parser captures the fork's already-logged
  `content_below2m`; gate+axis keyed on `content_total`, address fallback.
  Wave sidecars stamp battery "7". No fork change; capture format identical.
- The semantics change is recorded as a **kb §6 checkpoint entry**: the
  ruling, the gwing2/takoron evidence pair, the sgtetris addendum, and the
  item-1 deferral.
- After the scorer lands: blanket `score.py` pass over all sidecars +
  `gen_tables.py`, so `RANKING.md` is uniformly one scorer version — no
  mixed-semantics rows.

### Docs & campaign artifacts

- kb §6: checkpoint entry as above; item 1 explicitly deferred-with-data.
- Wave sets: assessment `.md` Gate sections updated from results; `QUEUE.md`
  status flips for unparked sets; `RANKING.md`/`GAME_FORMATS.md` regenerated.
- New `docs/superpowers/specs/backlog-aram-p16-discount.md` (maybe-marked,
  pros/cons, ranking impact, evidence bar).
- `backlog-aram-gate-volume.md` marked landed with a pointer here (mirroring
  the snapshot-diff brief's closure).
- Memory note: the ARAM ruling was made at the opened checkpoint; the
  no-mid-wave rule stays for the remaining §6 items.

## Expected outcomes (bounds — wave measurements decide)

| Set | Volume-u (bound) | Expected |
|---|---|---|
| gwing2 | ≈ 1.023 | unparks; aram sub ≈ 81 → memory axis ≈ 81 (main 86, vram 88) — strongest unpark |
| sgtetris | ≤ 1.0 | unparks; aram sub ≈ 85, higher if below-cap volume is sparse |
| cspike | ≤ 1.79 | unparks into the 10–13 memory-axis band unless below-cap volume is well under 2 MiB |
| azumanga | ≤ 1.81 | same shape as cspike |
| zerogu2 | ≈ 2.02 bound | measurement decides: park vs floor-score |
| inunoos / pokasuka / takoron | ≥ 2.2 | stay parked — §6 item 1 material |
| ausfache / cleoftp | ≤ 1.0 | memory axis 85 → up to 100 if volume < 1.68 MB; anchors safe |

## Done means

- Parser captures `content_below2m`; sidecar gains `aram.content_total`
  (per-sample-max semantics).
- Gate + axis keyed on volume with the address fallback; ARAM park message
  says "content"; guard tests for both synthetic shapes + fallback + parser
  semantics green; anchor/DMPD guards untouched.
- 10-set wave completed; blanket re-score + tables regenerated; QUEUE flips.
- kb §6 checkpoint entry recording the ruling, evidence pair, sgtetris
  addendum, and item-1 deferral; `backlog-aram-p16-discount.md` created;
  motivating brief closed with a pointer.
