# Backlog: re-key the G3-ARAM gate on content volume, not address

**Status:** proposed 2026-08-06 (batch: DC-ported ★ assessments). Not started —
**deliberately parked for the §6 scoring-semantics checkpoint (~30 assessed
families)**; do not change the gate mid-campaign.

## Goal

Gate and score ARAM on **compacted content volume** (`content_below2m +
content_above2m`) instead of the content high-water *address* (`content_high`),
because ARAM layout is a porting artifact: OSB banks are position-independent
(verified live on the azumanga dump — bank rebuild + base move, no pointer
archaeology; `assessments/azumanga.md` § ARAM bank-structure verification).

Why it's load-bearing: `gwing2` parked G3 at u=3.99 from a single ~47.5 KB blob near
the top of ARAM — above-cap *volume* 48,662 B, i.e. compacted u≈1.02. Contrast
`zerogu2` (2,130,349 B above cap) and `cspike` (1,649,859 B): same gate, genuinely
unfittable content. The address keying cannot tell these cases apart; volume can
(`assessments/gwing2.md` § Gate, tension 1).

## Read first

- `assessments/gwing2.md` § Gate — the divergent case and both tensions
- `assessments/zerogu2.md` / `assessments/cspike.md` / `assessments/azumanga.md` —
  the genuine-G3 contrast class + the position-independence verification
- `tools/assess/parse_capture.py` `_APROF` regex — the fork **already logs**
  `content_below2m`; the regex deliberately skips capturing it. The fix is
  parser+scorer only, no fork change
- `tools/assess/score.py` `memory_axis` / `region_score` — where `aram` peak feeds in
- `docs/kb/assessment-tooling.md` §6 — the checkpoint this decision belongs to

## Design decisions to settle in-session

- Score `u = content_total / cap` for the axis too, or only re-key the *gate* and keep
  the address for the sub-score? (Compaction argument supports full volume keying;
  keep `content_high` as informational sidecar field either way)
- Whether raw `.p16` BGM in inter-bank gaps (headerless, GD-streamable — azumanga
  finding) deserves a discount before gating, or stays counted
- Guard test: synthetic "small blob at high address" profile must not park;
  synthetic "2 MiB+ volume" must

## Constraints

- The seven G3-parked sets' sidecars lack `content_total` (raw logs deleted by SSD
  hygiene) — re-run wave needed: azumanga, takoron, inunoos, pokasuka, zerogu2,
  gwing2, cspike. Serial batteries, ~10 min each
- Scoring-semantics change ⇒ decide at the §6 checkpoint, then either
  `BATTERY_VERSION` bump (if capture format changes — it doesn't) or a scorer
  revision note + `rescore_static.py`-style pass; keep campaign comparability rules
- Anchor guard tests stay green; never weakened

## Done means

- Parser captures `content_below2m`; sidecar gains `aram.content_total`
- Gate + (per decision) axis keyed on volume; gwing2 un-parks and scores; genuine
  overflows still park
- Guard tests for both synthetic shapes
- §6 checkpoint entry recording the decision and the gwing2/zerogu2 evidence pair;
  parked-set re-run wave completed and tables regenerated
