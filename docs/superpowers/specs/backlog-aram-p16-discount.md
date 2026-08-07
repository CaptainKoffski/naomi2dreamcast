# Backlog (maybe): discount GD-streamable raw .p16 BGM before the ARAM volume gate

**Status:** proposed 2026-08-07 at the §6 checkpoint, marked **maybe** — user
ruling: not implemented with the volume re-key; revisit only if the evidence
bar below is met.

## Idea

Raw `.p16` BGM sitting in inter-bank ARAM gaps (headerless, GD-streamable —
azumanga finding, `assessments/azumanga.md`) is content a real port would
stream from disc, not resident sound RAM. Subtract identified `.p16` runs
from `aram.content_total` before gating/scoring.

## Pros

- More faithful to porting reality: the DC streams BGM from GD-ROM routinely;
  resident ARAM is for SFX/voice banks.
- Could move heavy-but-streamable titles (azumanga class) from the
  10-13 memory-axis band into scoreable range, or un-park volume-parked sets
  whose overflow is mostly BGM.

## Cons

- Needs automated bank-map carving + a headerless-format classifier inside
  the deterministic scorer (`parse_osb.py`-grade analysis per title) — a big
  step up in scorer complexity and a new false-positive surface.
- Evidenced on ONE title (azumanga). No second data point yet.
- Double-counts against the §6 item-1 threshold question: if the ARAM
  multiple is softened instead, most of the same titles are reachable with
  zero new analysis code.

## Possible ranking impact (from the 2026-08-07 v7 wave)

Still-parked or low-band `content_total` this discount would apply against
(battery v7, `assessments/*.metrics.json`): `azumanga` 3,475,221 B · `cspike`
3,654,043 B · `zerogu2` 4,115,639 B · `takoron` 6,333,113 B · `inunoos`
6,597,975 B · `pokasuka` 7,064,300 B. What's still missing: how much of each
figure is `.p16` gap content (requires an ARAM dump + `parse_osb.py` pass per
title — the azumanga § ARAM bank-structure method). A set moves only if the
discounted volume crosses a scoring band edge (2.0 park line, or the
1.25/1.0/0.8 knees).

## Evidence bar (do not start before this)

- ≥ 3 titles where a `parse_osb.py`-verified `.p16` share would flip a park
  or move a memory-axis band, AND
- the §6 item-1 threshold ruling has landed (it may make this moot).
