# Backlog: mask framebuffer regions out of the VRAM write-truth peak

**Status:** proposed 2026-08-06 (batch: DC-ported ★ assessments). Not started —
checkpoint-adjacent (§6): collect more families first; chocomk is the motivating case.

## Goal

Make the VRAM metric measure what a port actually has to fit — textures + render
structures wherever they live, **plus a framebuffer budget** — instead of the raw
address high-water, which charges the game for wherever the arcade build happened to
park its FBs.

Why it's load-bearing: `chocomk` scored memory 25.6 (final 52.5 B) almost entirely on
VRAM u=1.61 — but `regs_last` shows `fb_w_sof1=0x800000`, `fb_w_sof2=0xc00000`: both
write-FBs sit at/above the DC's 8 MB line, and 3,156,395 B of its 3,169,579 B total
nonzero VRAM content is "above cap". Actual texture/structure content is ~3.2 MB; a
port would simply place the FBs inside the budget. The title is likely under-ranked
for an artifact reason (`assessments/chocomk.md` §4, §9). This generalizes the
existing per-title `BIOS_VRAM_SIGNATURES` clamp into a principled rule.

## Read first

- `assessments/chocomk.md` §4/§9 — the evidence, with regs
- `docs/kb/assessment-tooling.md` §8 — the BIOS-logo clamp precedent (why score-side
  signature lists don't scale) and §9 (pre-handoff sampling lesson)
- Fork's `VRAMPROFILE` sampler + `VRAMREGS` emitter — FB registers are already read
  each sample; masking happens at sample time, guest untouched
- `tools/assess/score.py` `BIOS_VRAM_SIGNATURES` — the mechanism this retires or
  narrows

## Design decisions to settle in-session

- Masked-region derivation: `FB_W_SOF1/2` (+ `FB_R_SOF1`?) with size from
  `FB_R_SIZE`/video mode at sample time; double vs triple buffering
- Score formula: `non_fb_high_water + 2 × fb_size` vs `non_fb_content + 2 × fb_size`
  (address vs volume — same tension as the ARAM backlog; settle consistently)
- Sidecar shape: keep raw peak for continuity, add `vram.non_fb_peak` + `vram.fb_bytes`
- Which titles shift: re-check kurucham/ss2005/tetkiwam/ikaruga regs_last for the same
  FB-above-cap pattern before assuming chocomk is unique

## Constraints

- Fork change ⇒ `BATTERY_VERSION` bump + re-run wave (scored titles whose VRAM axis
  binds are the priority: chocomk, radirgyn, mamonoro, illvelo …); anchors first,
  calibration guard green
- Never hand-adjust existing scores meanwhile — campaign comparability; chocomk's doc
  already carries the prose flag

## Done means

- FB-masked VRAM fields in the sidecar; scorer uses textures+FB-budget formula
- chocomk re-assessed under the new metric (expected: memory axis rises, rank climbs)
- `BIOS_VRAM_SIGNATURES` retired or reduced to a comment about the era it covered
- Guard test with a synthetic FB-above-cap profile; kb note + BATTERY_VERSION bump +
  re-run wave recorded
