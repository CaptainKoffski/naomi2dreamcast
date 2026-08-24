# Proposal: live VRAM-residency metric for KAMUI2 titles

**Status: proposed, not scheduled.** Scoped 2026-08-24 at the operator's
request, for processing after the senkosp port. Nothing in the current
rankings has been changed.

## The gap this closes

The VRAM axis scores **content volume**: `content_total + 2×fb_bytes`
against the DC's 8,388,608 B cap. That measures how many unique texture
bytes the game ever writes — not how many it keeps **resident at once**
under its own allocator.

`senkosp` is the proven counter-example. Its v9 capture scored the VRAM
axis at u 0.571 (4,786,768 B, full marks). The port then hit a hard VRAM
wall on the DC build: the game's KAMUI2 texture arena needs a measured
**8,772,640 B live** in its worst scene — 384,032 B over the cap — and
hangs deterministically in attract, before any input. Volume fits;
co-residency doesn't. Full evidence:
`../senkosp2dreamcast/docs/kb/phase5-hardware.md` (Task 7 verdict +
§High-water measurement + §Fix scoping).

The signal existed in the v9 data and was discounted: `senkosp.md` §2
notes 3,017,926 B of nonzero content **above the 8 MB address line**
(informational, treated as address-extent noise). On a 16 MB Naomi
arena, sustained content above the 8 MB line is exactly what allocator
co-residency over the DC cap looks like.

## Proposed metric

For titles identified as KAMUI2-library (the library ID is already part
of the assessment): **live arena residency peak** — walk the game's own
KAMUI2 arena bookkeeping on every STARTRENDER and record the running
maximum of allocated bytes (split texture-class vs non-texture by node
flags bit 0x02).

The probe already exists: the `ARENAHW` walker in the instrumented
Flycast fork (`../flycast4naomi2dreamcast`, commit `10de83124`, see its
`INSTRUMENTATION.md`). It is passive, always-on-when-cartlog, and prints
only on a new running max — a 10–15 min unattended attract capture per
game yields the number.

DC translation (per the senkosp method): required DC arena =
`peak_tex + (DC non-texture reservations)`, where the non-texture term
is the game's framebuffer/region configuration (senkosp: 1,490,944 B).
Score `u = required / 8,388,608`; flag u > 0.95 as a gating risk with a
fix-cost note (senkosp precedent: in-place VQ shrink of the offending
textures, method in the port KB).

## Per-game setup cost

The walker needs the game's KAMUI2 arena config-block address (senkosp:
P1 `0x8c170eb8`). Discovery recipe (senkosp KB §Fix scoping, Ghidra
archaeology): find the arena initializer by its constant duality
`0x1000000` (16 MB Naomi seed) vs `0x800000` (8 MB fallback arm) and
take the config pointer it writes through. One-time, ~30–60 min per
game; semi-automatable by scanning for those pool constants. Node
layout (stride 0x18: +0x00 u16 flags, +0x08 next, +0x10 size) matched
senkosp's KAMUI2 build and likely holds across the library's era, but
verify per game.

## Limits

- **Attract-only is a lower bound.** senkosp's attract peak was already
  over the DC cap (sufficient to flag it), but its gameplay peak ran
  higher still (played 2P legs set the true max). Green-at-attract does
  not prove fit; red-at-attract is dispositive.
- KAMUI2 titles only. Non-library titles (or other libraries) need
  their own residency probe; the content-volume metric stays as-is for
  them, with the "content above the 8 MB line" informational now read
  as a residency warning, not noise.
- The metric measures the Naomi profile (16 MB arena, original ROM), so
  texture demand is content-determined and unaffected by any port
  patches; the DC translation term is computed per game.

## If adopted

Sweep candidates: KAMUI2-library titles in the current rankings,
highest-ranked first (they're the ones a residency surprise hurts
most). Each game: config-block discovery, one attract capture, add a
`VRAM residency` row to its assessment, adjust the VRAM axis or add a
gating-risk note where u approaches 1. Re-ranking is a separate,
explicit decision.
