# Design: VRAM re-keyed on FB-masked content volume + framebuffer budget

**Date:** 2026-08-07. **Supersedes:** the open decisions in
`backlog-vram-fb-masking.md` (which stays as the motivating brief).
**Checkpoint status:** second §6 scoring-semantics change ruled under the
checkpoint opened for the ARAM v7 re-keying (spec
`2026-08-07-aram-gate-volume-design.md`), at 26 assessed families.

## Goal

Make the VRAM region of `score.py`'s memory axis measure what a port actually
has to fit — texture/structure content wherever it lives, **plus a
double-framebuffer budget** — instead of the raw address high-water, which
charges the game for wherever the arcade build parked its FBs.

Motivating case: `chocomk` scored memory 25.6 (final 52.5 B) almost entirely
on VRAM u = 1.61, yet its flip pair sits at/above the DC's 8 MB line
(`fb_w_sof1=0x800000`, `fb_r_sof1=0xc00000`) and 3,156,395 B of its
3,169,579 B total nonzero VRAM content is above cap. Actual texture/structure
content is ~2 MB after FB masking; a port simply places the FBs inside the
budget (`assessments/chocomk.md` §4/§9).

## Findings that reshaped the brief (this session)

1. **The FB-above-cap pattern is near-universal, not a chocomk quirk.** All
   26 sidecars show `fb_w_sof2=0xc00000` — in most titles a **never-written
   BIOS default** (ausfache/cleoftp/moeru carry it with zero above-cap
   bytes). Naomi runs 31 kHz progressive; `FB_W_SOF2` is the interlace
   field-2 pointer and page flipping alternates `FB_W_SOF1` between two
   buffers (the pair visible as `fb_w_sof1`/`fb_r_sof1`). Consequence: any
   per-register FB budget overcharges phantom buffers — masking must exclude
   regions by extent, and the budget must be flat.
2. **Nine scored titles have VRAM as their binding memory region**, not the
   brief's four: chocomk (sub 25.6), sgtetris (12.4), gunsur2 (13.0), marstv
   (21.6), illvelo (22.4), mamonoro (24.6), radirgyn (36.6), cleoftp (86.8),
   moeru (87.9). These are the only scored finals that can move.
3. **The ARAM v7 precedent answers the address-vs-volume tension directly**:
   layout is a porting artifact; a port re-uploads textures at addresses of
   its choosing, exactly as it rebuilds ARAM banks. The fork's own sampler
   comment (`naomi.cpp`, cartlog_vram_profile) already documents that in
   Flycast ISP/OL buffers and FBs live host-side — the array content alone
   under-represents the real footprint, which is why `VRAMREGS` exists.

## Rulings (settled 2026-08-07, brainstorm session — user decisions)

1. **Volume + FB budget keying.** `fit = content_total + 2 × fb_bytes` —
   non-FB content volume plus a double-buffer budget. Consistent with the
   ARAM v7 ruling. Masked-address keying was rejected (re-introduces the
   artifact class ARAM rejected); mask-only-no-budget was rejected
   (undercharges every title — a real port must still fit two FBs).
2. **Flat 2 × fb_size budget.** Phantom-register-proof and matches how DC
   ports are built. Known ceiling: a genuinely triple-buffered title is
   undercharged one FB (~600 KB at 640×480×16bpp). Measured-region charging
   was rejected as charging arcade layout choices a port wouldn't keep.
3. **Wave = 9 binding-VRAM scored titles + ikaruga control.** Anchors
   cleoftp + ikaruga run first as controls on the new fork build (this is a
   fork change, unlike v7). Non-wave titles keep address keying via
   fallback — same accepted mixed-provenance pattern as v7.
4. **`BIOS_VRAM_SIGNATURES` promoted to refusal canary.** The clamp is
   obsolete (v5 pre-handoff gating removed the noise it corrected); an exact
   match on a booted title now raises `MetricRegression`, same posture as
   the ARAM DMPD canary.

## Design

### Fork — `cartlog_vram_profile()` (battery v8)

Inside the existing per-sample byte loop, read-only, guest untouched:

- **Masked intervals:** the distinct values of `{FB_W_SOF1, FB_W_SOF2,
  FB_R_SOF1} & VRAM_MASK` **at sample time**, each spanning
  `[sof, sof + fb_size)`. `fb_size` = one framebuffer's bytes from the
  current video regs: `(FB_R_SIZE.fb_y_size + 1) × FB_W_LINESTRIDE.stride ×
  8` — write-side stride (write extents are what land in the array) times
  display height (read/write FBs share dimensions under page flipping); the
  read-side formula precedent is `Renderer_if.cpp:622`. Sample-time regs,
  not a sticky union:
  a stale FB region left behind by a mode change counts as content again in
  later samples — truthful-if-rare, documented limitation.
- **New counters, same loop:** `content_high`, `content_below8m`,
  `content_above8m` (diff bytes outside masked intervals) + `fb_masked_nz`
  (diff bytes inside them — evidence distinguishing real FB regions from
  phantom registers). Naming mirrors `ARAMPROFILE`'s v4 `content_*` fields.
- **Emission:** `VRAMPROFILE` gains appended fields `content_high=%x
  content_below8m=%x content_above8m=%x fb_bytes=%x fb_masked_nz=%x`; the
  raw `high/nz/nz_below8m/nz_above8m` fields are unchanged (boot_ok
  threshold, canaries, old parsers keep working). `fb_bytes` = one-FB size
  at that sample.

### Parser — `tools/assess/parse_capture.py`

- `_VPROF` gains optional capture groups for `content_below8m`,
  `content_above8m`, `fb_bytes` (optional-group style like `_APROF`'s v4
  extension; legacy logs still match, absent fields ⇒ keys omitted from the
  sidecar, no zero-fill).
- Per sample: `total = content_below8m + content_above8m`;
  `vram["content_total"]` = max of **per-sample totals** — one coherent
  sample, never `max(below) + max(above)` across samples (ARAM v7 rule).
  `vram["fb_bytes"]` = max over samples (a mode change takes the larger FB).
- Existing fields (`peak`, `nz_total`, `nz_above_cap`, `nz_below_max`,
  `regs_last`, `watermark_max`) unchanged; `peak` stays the raw address
  high-water for continuity, canary keying, and the legacy fallback.
- The v5 pre-`VRAMHANDOFF` gating covers the new fields automatically
  (parsed inside the same `handoff["vram_zeroed"]` branch).
- Sidecar schema: `memory.vram.content_total` (non-FB volume, bytes) +
  `memory.vram.fb_bytes` (one-FB size, bytes). Nothing removed.

### Scorer — `tools/assess/score.py`

- VRAM fit value: `content_total + 2 * fb_bytes` when **both** present, else
  raw `peak` — explicit `is not None` checks, not `or` (a genuine 0 must not
  trigger fallback).
- **Fallback conservatism, stated honestly:** unlike ARAM there is no
  theorem that `content + 2×fb ≤ peak` (a dense single-buffered title could
  invert it), but every measured sidecar satisfies it by a wide margin;
  legacy rows under-score, matching the v7 posture.
- VRAM park message becomes `G3 memory: vram content > 2x DC capacity` when
  volume-keyed (the one-word-per-region `metric` lookup extends). No current
  title VRAM-parks either way (max address-u is sgtetris 1.94; volume only
  lowers u).
- `BIOS_VRAM_SIGNATURES`: clamp deleted; an exact `(peak, nz_above_cap)`
  match on a booted title raises `MetricRegression`.
  `scores.vram_bios_noise_excluded` is no longer written. dragntr3 is
  G1-gated before the check, so it stays parked normally, no raise.
- `region_score`, the piecewise map, the 2× park threshold, the DMPD canary,
  and the cleoftp/ikaruga anchor guard: untouched. Anchors are safe by
  construction — their fit value can only drop.

### Guard tests — `tools/assess/tests/`

1. Parser: synthetic FB-above-cap capture (FBs above 8 MB, small
   `content_*`) yields `content_total`/`fb_bytes`; per-sample-max semantics
   proven with two samples where `max(below)+max(above)` gives a different
   (wrong) answer.
2. Parser legacy: a v7-format `VRAMPROFILE` line (no `content_*`) ⇒ keys
   absent, `peak` untouched.
3. Scorer: FB-above-cap synthetic (raw-peak u ≈ 1.6, `content+2fb` u ≈ 0.4)
   scores on volume, vram sub 100; the same sidecar without the new keys
   falls back to address, sub ≈ 25 — both asserted.
4. Scorer canary: booted sidecar with the exact `(0x943000, 57048)`
   signature raises `MetricRegression`; a dragntr3-shaped G1 sidecar with
   the same values still parks normally without raising.
5. Existing anchor + DMPD guards stay green; never weakened.

## Campaign ops

### Versioning

- **`BATTERY_VERSION` bumps "7" → "8"** — a real capture-format change (fork
  emits new fields), uncontroversial under the v7 provenance precedent. v8
  note: VRAM FB masking — fork logs FB-masked `content_*` + `fb_bytes`;
  gate+axis keyed on `content_total + 2×fb_bytes`, address fallback;
  BIOS-signature clamp promoted to refusal canary.
- Fork commit lands in `../cleopatra/tools/flycast-src` (pushed to
  `flycast4naomi2dreamcast`), rebuilt with the Vulkan/MoltenVK recipe; the
  new fork hash is recorded in wave sidecars' `versions.flycast` and the kb
  tooling-inventory row.

### Re-run wave — 10 sets, serial, ~10 min each

Raw cartlogs are rotated (only the latest battery's survive), so sidecars
gain the new fields only via re-runs. Order: calibration guard green first;
then **cleoftp + ikaruga as anchor controls on the new fork build**
(boot/handoff/ARAM/main figures must reproduce within known determinism);
then chocomk, sgtetris, gunsur2, marstv, illvelo, mamonoro, radirgyn, moeru.
Standard battery per `assessments/RUNBOOK.md` + the headless recipe, one
Flycast instance at a time. Scorer + tests land **before** the wave starts —
no mid-wave re-keying.

Every other family: no re-run — VRAM is not their binding min, and under the
fallback their rows are provably unchanged.

### After the wave

- Blanket `score.py` pass over all sidecars + `gen_tables.py` — `RANKING.md`
  uniformly one scorer version, no mixed-semantics rows.
- Wave sets' assessment `.md` memory sections updated from results;
  chocomk's §4/§9 prose flags resolved at its re-assessment; `QUEUE.md`
  cells flipped on any status change; `GAME_FORMATS.md` regenerated.

### Docs & memory

- kb §6 checkpoint entry: second semantics ruling (volume + FB budget, flat
  2×), the phantom-`fb_w_sof2` finding, signatures→canary, and the evidence
  that nine titles bind on VRAM.
- `backlog-vram-fb-masking.md` closed with a pointer here (mirroring the
  ARAM brief's closure).
- Memory note: second §6 ruling made; remaining §6 items (ARAM 2× multiple,
  streaming re-read, main high-water) still open, no-mid-wave rule stands.

## Expected outcomes (bounds — wave measurements decide)

| Set | Today (vram sub / binding) | Expected under v8 |
|---|---|---|
| chocomk | 25.6 / vram | fit ≈ 2.0 M + 1.2 M ⇒ u ≈ 0.38, sub 100 → memory axis 85 — the predicted rank climb |
| sgtetris | 12.4 / vram | rises by the FB fraction of its 5.6 MB above-cap content; main 20.5 becomes binding |
| gunsur2 | 13.0 / vram | rises; main 14.6 likely becomes binding |
| marstv | 21.6 / vram | rises; main 28.0 likely becomes binding |
| illvelo | 22.4 / vram | rises; main 24.9 likely becomes binding |
| mamonoro | 24.6 / vram | rises; main 37.3 likely becomes binding |
| radirgyn | 36.6 / vram | rises; main 55.2 likely becomes binding |
| cleoftp | 86.8 / vram | u 0.98 → likely sub 100 (anchor; can only improve) |
| moeru | 87.9 / vram | u 0.96 → likely sub 100 |
| all others | — | provably unchanged (fallback; VRAM not binding min) |

## Done means

- Fork emits FB-masked `content_*` + `fb_bytes`/`fb_masked_nz` on
  `VRAMPROFILE`; parser captures them per-sample-coherently; sidecar gains
  `vram.content_total` + `vram.fb_bytes`.
- Scorer keyed on `content_total + 2×fb_bytes` with address fallback; park
  message says "content"; signature clamp replaced by `MetricRegression`
  canary; all five guard tests green; anchor/DMPD guards untouched.
- Calibration guard green, anchor controls reproduce, 10-set wave completed,
  blanket re-score + tables regenerated, chocomk re-assessed (expected:
  memory axis rises to 85, rank climbs).
- kb §6 checkpoint entry + tooling-inventory row for the new fork commit;
  `BATTERY_VERSION` = "8"; motivating brief closed with a pointer.
