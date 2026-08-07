# VRAM FB-Masking Re-Key Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Key the VRAM region of the portability scorer on FB-masked content volume plus a flat double-framebuffer budget, promote the BIOS-logo signature clamp to a refusal canary, then re-run the 10 affected families (anchors first) and regenerate campaign tables.

**Architecture:** One emulator-fork change (`cartlog_vram_profile()` gains FB-masked `content_*` counters, mirroring the ARAM v4 pattern) plus three `tools/assess/` changes (parser captures the new fields; scorer keys VRAM on `content_total + 2×fb_bytes` with raw-peak fallback; battery version bumps to 8), followed by anchor control runs, an 8-set re-run wave, and a docs/tables pass.

**Tech Stack:** C++ (Flycast fork, read-only instrumentation), Python 3 stdlib only (repo convention: no dependencies). Plain-assert test files run directly with `python3`, no pytest.

**Spec:** `docs/superpowers/specs/2026-08-07-vram-fb-masking-design.md` — read it first; the Rulings section records the user decisions this plan implements.

## Global Constraints

- Work in the main checkout on branch `main` (repo convention: campaign commits go straight to `main`). Do NOT use a git worktree: the battery needs the gitignored `naomi/` ROM tree and the local emulator build.
- The fork checkout is `../cleopatra/tools/flycast-src` (absolute: `/Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src`). Fork commits happen THERE, not in this repo.
- Never commit ROMs, BIOS images, or disc images — `naomi/` and `assessments/evidence/*/raw/` stay untracked/gitignored.
- Instrumentation never mutates guest state — the fork change is strictly read-only over `vram[]` and PVR registers.
- `tools/assess/tests/test_metric_guards.py` invariants may only be **strengthened**, never weakened. Task 4 rewrites the BIOS-logo guard from clamp-and-score to refuse-to-score — stricter, spec-mandated. All tests green at every commit.
- `BATTERY_VERSION` becomes exactly `"8"`.
- One Flycast instance at a time (`pgrep -x Flycast` must be empty before any run); the wave is strictly serial. Signal the binary with `pgrep -x`/`pkill -x`, never `-f` (kb: the `-f` match kills the shell wrapper and orphans the emulator).
- Scorer + tests land **before** any wave run — no mid-wave re-keying. Wave results are never hand-adjusted; a result outside its spec bound stops the wave for instrumentation debugging (kb §7 posture, superpowers:systematic-debugging).
- VRAM fallback semantics: pre-v8 sidecars (no `content_total`/`fb_bytes`) key on raw `peak`. There is no volume≤address theorem for VRAM (spec records this honestly); every measured sidecar satisfies `content + 2×fb < peak` by a wide margin, so the fallback under-scores in practice. Nothing in this plan may let the fallback produce a score the volume path would beat.
- Commit messages follow repo style: short `area: summary` subject (`git log --oneline` for examples), ending with the Claude co-author trailer.

---

### Task 1: Fork — FB-masked content counters in `cartlog_vram_profile()`

**Files:**
- Modify: `/Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src/core/hw/naomi/naomi.cpp:242-266` (the whole `cartlog_vram_profile()` body)
- Reference: same file `:194-229` (`cartlog_aram_profile` — the `content_*` naming precedent), `core/hw/pvr/pvr_regs.h` (`FB_R_SIZE.fb_y_size`, `FB_W_LINESTRIDE.stride` bitfields), `core/hw/pvr/Renderer_if.cpp:622` (the read-side fb_size formula precedent)

**Interfaces:**
- Consumes: `vram[]`, `cartlog_vram_base`, `VRAM_SIZE`, `VRAM_MASK`, PVR regs `FB_W_SOF1`, `FB_W_SOF2`, `FB_R_SOF1`, `FB_R_SIZE`, `FB_W_LINESTRIDE` — all already visible in this translation unit (the existing `VRAMREGS` line uses the SOF regs).
- Produces: `VRAMPROFILE` log lines with five new fields inserted before `size=`, e.g.
  `VRAMPROFILE high=c00000 nz=400000 nz_below8m=100000 nz_above8m=300000 content_high=7f0000 content_below8m=100000 content_above8m=200000 fb_bytes=96000 fb_masked_nz=100000 size=1000000`
  Raw `high/nz/nz_below8m/nz_above8m` fields and `VRAMHIST`/`VRAMREGS` are byte-identical to v7 output. Task 2's parser consumes the new fields.

- [ ] **Step 1: Replace the function body**

Replace `cartlog_vram_profile()` (currently lines 242-266 of `core/hw/naomi/naomi.cpp`) with:

```cpp
static void cartlog_vram_profile()
{
	const u8 *base = cartlog_vram_base;
	const u32 size = VRAM_SIZE, BUCK = 0x40000;   // 256 KB buckets (64 for Naomi's 16 MB)
	u32 hist[64] = {0}, nb = size / BUCK;
	if (nb > 64) nb = 64;
	// v8 FB masking (spec 2026-08-07-vram-fb-masking-design.md, §6 ruling 2):
	// content_* counters exclude the framebuffer regions the CURRENT video regs
	// point at — FB placement is the arcade build's choice, not fit-relevant
	// content (chocomk parks its flip pair at/above the DC's 8 MB line); a DC
	// port budgets 2 FBs separately (score-side: content + 2*fb_bytes).
	// Sample-time regs only, no sticky union: a stale FB region left by a mode
	// change counts as content again later — truthful-if-rare, documented.
	// FB_W_SOF2 is usually a never-written BIOS default (31 kHz progressive
	// parks the field-2 pointer at 0xc00000); masking it costs nothing when
	// nothing was written there. fb_size: write-side stride (8-byte units)
	// x display height — read/write FBs share dimensions under page flipping
	// (read-side variant: Renderer_if.cpp fb_watch formula).
	const u32 fb_size = (FB_R_SIZE.fb_y_size + 1) * FB_W_LINESTRIDE.stride * 8;
	const u32 fb_sof[3] = { FB_W_SOF1 & VRAM_MASK, FB_W_SOF2 & VRAM_MASK, FB_R_SOF1 & VRAM_MASK };
	u32 high = 0, nz = 0, nz_below8m = 0;
	u32 chigh = 0, cnz = 0, cnz_below8m = 0, fb_masked_nz = 0;
	for (u32 i = 0; i < size; i++)
		if (vram[i] != (base != nullptr ? base[i] : 0)) {
			nz++; high = i + 1;
			if (i < 0x800000) nz_below8m++;
			u32 b = i / BUCK; if (b < 64) hist[b]++;
			// unsigned wrap makes (i - sof < fb_size) a one-compare range check
			bool in_fb = (i - fb_sof[0] < fb_size) || (i - fb_sof[1] < fb_size)
			          || (i - fb_sof[2] < fb_size);
			if (in_fb) {
				fb_masked_nz++;
			} else {
				cnz++; chigh = i + 1;
				if (i < 0x800000) cnz_below8m++;
			}
		}
	cartlog("VRAMPROFILE high=%x nz=%x nz_below8m=%x nz_above8m=%x content_high=%x content_below8m=%x content_above8m=%x fb_bytes=%x fb_masked_nz=%x size=%x\n",
			high, nz, nz_below8m, nz - nz_below8m, chigh, cnz_below8m, cnz - cnz_below8m, fb_size, fb_masked_nz);
	char line[576]; int p = 0;
	for (u32 b = 0; b < nb; b++)
		p += snprintf(line + p, sizeof(line) - p, "%x ", hist[b]);
	cartlog("VRAMHIST %s\n", line);   // nz-byte count per 256 KB bucket (bucket 32+ = past 8 MB)
	cartlog("VRAMREGS isp_base=%x isp_limit=%x ol_base=%x ol_limit=%x fb_w_sof1=%x fb_w_sof2=%x fb_r_sof1=%x\n",
			TA_ISP_BASE & VRAM_MASK, TA_ISP_LIMIT & VRAM_MASK,
			TA_OL_BASE & VRAM_MASK, TA_OL_LIMIT & VRAM_MASK,
			FB_W_SOF1 & VRAM_MASK, FB_W_SOF2 & VRAM_MASK, FB_R_SOF1 & VRAM_MASK);
}
```

Keep the leading comment block above the function (lines 231-241) as is — it documents the blind spot the new fields address; append one line to it: `// v8: content_* fields below mask the FB regions out (spec 2026-08-07).`

- [ ] **Step 2: Build with Vulkan and re-bundle MoltenVK**

```bash
cd /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src
cmake -S . -B build -DUSE_VULKAN=ON
cmake --build build -j8
cp /Applications/Flycast.app/Contents/Frameworks/libvulkan.dylib \
   build/Flycast.app/Contents/Frameworks/libvulkan.dylib
```

Expected: build succeeds; the `cp` is idempotent (repo memory: GL never presents CPU-framebuffer screens, the battery needs Vulkan).

- [ ] **Step 3: Smoke-run headlessly and verify the new log fields**

`gwing2` is a booting cart set NOT in the v8 wave (zero contamination risk), and this direct run writes no sidecar. One instance at a time — check `pgrep -x Flycast` is empty first.

```bash
cd /Users/captainkoffski/AntigravityProjects/naomi2dreamcast
SMOKE=/private/tmp/claude-501/-Users-captainkoffski-AntigravityProjects-naomi2dreamcast/3ae34f38-d8fe-49f6-9e13-0230db9743f6/scratchpad/smoke-vramfb.log
FLYCAST_CARTLOG=$SMOKE /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src/build/Flycast.app/Contents/MacOS/Flycast \
  -config config:rend.vsync=no naomi/gwing2.zip &
sleep 180 && pkill -x Flycast; sleep 2
grep -m2 -E "VRAMPROFILE .*content_high=[0-9a-f]+ content_below8m=[0-9a-f]+ content_above8m=[0-9a-f]+ fb_bytes=[0-9a-f]+ fb_masked_nz=[0-9a-f]+ size=" $SMOKE
grep -c "VRAMPROFILE" $SMOKE
```

Expected: post-`VRAMHANDOFF` lines match the full new-field pattern; `fb_bytes` reads `96000` (hex — 614,400 B, 640×480×16bpp) once video is initialized; `content_below8m + content_above8m + fb_masked_nz == nz` on any single line (spot-check one by hand). If `fb_bytes=0` on every line or the pattern never appears, the reg reads are wrong — stop and debug before committing.

- [ ] **Step 4: Commit the fork change and push**

```bash
cd /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src
git add core/hw/naomi/naomi.cpp
git commit -m "instrumentation v8: FB-masked VRAM content counters + fb_bytes (naomi2dreamcast spec 2026-08-07)"
git remote -v   # confirm origin is the CaptainKoffski flycast4naomi2dreamcast fork before pushing
git push origin HEAD
git rev-parse --short HEAD   # record this hash — Tasks 6-9 cite it
```

If the push is rejected or origin is not the fork, report it and continue — the local commit is what the battery stamps into sidecars (`flycast_commit()`); the push can be retried later.

---

### Task 2: Parser — capture `content_*`/`fb_bytes`, emit `vram.content_total` + `vram.fb_bytes`

**Files:**
- Modify: `tools/assess/parse_capture.py:14` (`_VPROF` regex), `:35` (vram init), `:99-103` (`_VPROF` branch), `:152-154` (return dict)
- Test: `tools/assess/tests/test_parse_capture.py`

**Interfaces:**
- Consumes: Task 1's `VRAMPROFILE` lines (the five new fields are optional — absent on pre-v8 logs).
- Produces: `parse(...)["vram"]["content_total"]` — `int` bytes (max over per-sample `content_below8m + content_above8m`) or `None`; `parse(...)["vram"]["fb_bytes"]` — `int` bytes (max over samples) or `None`. Task 5 copies both into the sidecar; Task 3 scores them.

- [ ] **Step 1: Write the failing test**

Append to `tools/assess/tests/test_parse_capture.py` (before the `__main__` block):

```python
def test_vram_content_total_per_sample_max_and_handoff_gate():
    # §6 ruling 2 (spec 2026-08-07-vram-fb-masking-design.md): content_total is
    # the max of PER-SAMPLE below+above totals. max(below)+max(above) across
    # different samples (0x280000+0x200000=0x480000) is a volume that never
    # existed at once and must NOT be the answer. The pre-VRAMHANDOFF sample
    # (vs-null baseline, kb §9) must be ignored — new fields included.
    log = (
        "VRAMPROFILE high=f00000 nz=e00000 nz_below8m=100000 nz_above8m=d00000"
        " content_high=f00000 content_below8m=100000 content_above8m=d00000"
        " fb_bytes=96000 fb_masked_nz=0 size=1000000\n"
        "CARTDMA src=00010000 dest=0c020000 len=100000\n"
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "VRAMPROFILE high=c00000 nz=400000 nz_below8m=100000 nz_above8m=300000"
        " content_high=7f0000 content_below8m=100000 content_above8m=200000"
        " fb_bytes=96000 fb_masked_nz=100000 size=1000000\n"
        "VRAMPROFILE high=c00000 nz=380000 nz_below8m=280000 nz_above8m=100000"
        " content_high=280000 content_below8m=280000 content_above8m=0"
        " fb_bytes=96000 fb_masked_nz=100000 size=1000000\n"
    )
    m = parse_capture.parse(log)
    assert m["vram"]["content_total"] == 0x300000, hex(m["vram"]["content_total"])
    assert m["vram"]["fb_bytes"] == 0x96000, m["vram"]["fb_bytes"]
    # raw fields keep their independent-max semantics, post-handoff only
    assert m["vram"]["peak"] == 0xc00000 and m["vram"]["nz_above_cap"] == 0x300000

def test_vram_legacy_line_leaves_content_none():
    # v7-format line (no content_* fields): keys stay None so the sidecar
    # omits them (no zero-fill) and the scorer falls back to the address.
    log = (
        "VRAMHANDOFF baselined size=1000000 trigger=dma\n"
        "VRAMPROFILE high=7b0000 nz=200000 nz_below8m=200000 nz_above8m=0 size=1000000\n"
    )
    m = parse_capture.parse(log)
    assert m["vram"]["content_total"] is None and m["vram"]["fb_bytes"] is None
    assert m["vram"]["peak"] == 0x7b0000
```

Register both in the `__main__` block alongside the existing calls:

```python
    test_vram_content_total_per_sample_max_and_handoff_gate(); print("test_vram_content_total_per_sample_max_and_handoff_gate OK")
    test_vram_legacy_line_leaves_content_none(); print("test_vram_legacy_line_leaves_content_none OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: FAIL with `KeyError: 'content_total'`

- [ ] **Step 3: Implement**

In `tools/assess/parse_capture.py`, four edits:

(a) `_VPROF` regex (line 14) — five optional fields; `content_high` and `fb_masked_nz` are matched but not captured (forensics-only, the sidecar doesn't carry them):

```python
_VPROF = re.compile(r"^VRAMPROFILE high=([0-9a-f]+) nz=([0-9a-f]+) nz_below8m=([0-9a-f]+) nz_above8m=([0-9a-f]+)"
                    r"(?: content_high=[0-9a-f]+ content_below8m=([0-9a-f]+) content_above8m=([0-9a-f]+)"
                    r" fb_bytes=([0-9a-f]+) fb_masked_nz=[0-9a-f]+)?", re.I)
```

(b) vram init (line 35):

```python
    vram = {"peak": 0, "nz_total": 0, "nz_above_cap": 0, "nz_below_max": 0, "regs_last": "",
            "content_total": None, "fb_bytes": None}
```

(c) `_VPROF` branch — after the existing four `max()` lines (inside `if m and handoff["vram_zeroed"]:`), append:

```python
                        if m.group(5) is not None:
                            # §6 ruling 2: one coherent sample's below+above —
                            # never max(below)+max(above) across samples
                            total = int(m.group(5), 16) + int(m.group(6), 16)
                            vram["content_total"] = max(vram["content_total"] or 0, total)
                            vram["fb_bytes"] = max(vram["fb_bytes"] or 0, int(m.group(7), 16))
```

(d) return dict (lines 152-154):

```python
        "vram": {"peak": vram["peak"], "nz_total": vram["nz_total"],
                 "nz_above_cap": vram["nz_above_cap"],
                 "content_total": vram["content_total"], "fb_bytes": vram["fb_bytes"],
                 "watermark_max": wm.get("vram", 0), "regs_last": vram["regs_last"]},
```

- [ ] **Step 4: Run the full parser test file**

Run: `python3 tools/assess/tests/test_parse_capture.py`
Expected: `ALL OK` (existing tests prove the optional group didn't break legacy lines; `test_pre_handoff_vram_noise` proves the handoff gate still holds for raw fields).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/parse_capture.py tools/assess/tests/test_parse_capture.py
git commit -m "assess: parser captures FB-masked vram content_* + fb_bytes (spec 2026-08-07)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Scorer — VRAM keyed on `content_total + 2×fb_bytes`, address fallback

**Files:**
- Modify: `tools/assess/score.py:161-184` (inside `score_sidecar`: the vram_peak/bios_noise block and the `peaks`/gate-message lines)
- Test: `tools/assess/tests/test_score.py`

**Interfaces:**
- Consumes: sidecar `memory.vram.content_total` + `memory.vram.fb_bytes` (int bytes, both absent on pre-v8 sidecars) and `memory.vram.peak` (raw address high-water).
- Produces: unchanged function signatures. `score_sidecar` gates VRAM with message `G3 memory: vram content > 2x DC capacity` when volume-keyed, keeps `G3 memory: vram peak > 2x DC capacity` on fallback. `region_score`, `memory_axis`, `CAPS`, thresholds, the BIOS clamp (Task 4 replaces it): untouched here.

- [ ] **Step 1: Write the failing tests**

Append to `tools/assess/tests/test_score.py` (before the `__main__` block; it auto-discovers `test_*` names). `_volume_sc` already exists (aram-volume plan, Task 2) — reuse it:

```python
def _vram_sc(vram):
    # aram comfortably fits so the memory axis == the vram sub-score path
    sc = _volume_sc({"peak": 1 * MB, "nz_above_cap": 0})
    sc["set"] = "synth-vram"
    sc["memory"]["vram"] = vram
    return sc

def test_vram_fb_masked_volume_scores():
    # chocomk shape (spec motivating case): raw peak 13.5 MB (address-u 1.61,
    # sub 25.6) but only ~2 MB of non-FB content. Volume keying: fit =
    # 2,000,000 + 2*614,400 = 3,228,800 -> u 0.38 -> sub 100.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395,
                   "content_total": 2000000, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]

def test_vram_fb_budget_is_double():
    # Pins the flat 2x multiplier (§6 ruling 2): content 5,800,000 + 2*614,400
    # = 7,028,800 -> u 0.8379 -> 97.2. A 1x budget would give u 0.7647 -> 100.
    sc = _vram_sc({"peak": 8 * MB, "nz_above_cap": 0,
                   "content_total": 5800000, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["scores"]["memory"] == 97.2, sc["scores"]

def test_vram_volume_overflow_parks_with_content_message():
    # Genuinely unfittable texture volume: 16 MiB + 1.2 MB FB budget -> u 2.07
    # -> park, and the message says "content" (the gate keyed on volume).
    sc = _vram_sc({"peak": 16 * MB, "nz_above_cap": 8 * MB,
                   "content_total": 16 * MB, "fb_bytes": 614400})
    score.score_sidecar(sc)
    assert sc["gate"] == "G3 memory: vram content > 2x DC capacity", sc["gate"]

def test_vram_no_content_falls_back_to_address():
    # Pre-v8 sidecar (chocomk's committed shape): no content keys -> raw peak
    # keys the axis exactly as today (sub 25.6). Fallback under-scores.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 25.6, sc["scores"]

def test_vram_zero_volume_is_a_measurement_not_missing():
    # content_total == 0 with fb_bytes == 0 must key the axis (u=0 -> 100),
    # NOT fall back to the 13.5 MB address — `is not None`, not truthiness.
    sc = _vram_sc({"peak": 13496860, "nz_above_cap": 3156395,
                   "content_total": 0, "fb_bytes": 0})
    score.score_sidecar(sc)
    assert sc["gate"] is None, sc["gate"]
    assert sc["scores"]["memory"] == 100.0, sc["scores"]
```

- [ ] **Step 2: Run tests to verify the new ones fail**

Run: `python3 tools/assess/tests/test_score.py`
Expected: `test_vram_fb_masked_volume_scores`, `test_vram_fb_budget_is_double`, `test_vram_volume_overflow_parks_with_content_message`, and `test_vram_zero_volume_is_a_measurement_not_missing` all raise AssertionError (the current scorer ignores the content keys and scores the raw peak). `test_vram_no_content_falls_back_to_address` passes already (documents current behavior).

- [ ] **Step 3: Implement**

In `tools/assess/score.py`, replace lines 161-164 (`vram_peak = ...` through the clamp) with:

```python
    vram = sc["memory"]["vram"]
    vram_peak = vram["peak"]
    bios_noise = BIOS_VRAM_SIGNATURES.get((vram_peak, vram.get("nz_above_cap")))
    if bios_noise is not None:
        vram_peak = min(vram_peak, CAPS["vram"])
    # §6 checkpoint ruling 2 (2026-08-07, spec 2026-08-07-vram-fb-masking-design.md):
    # VRAM keys on FB-masked content VOLUME plus a flat double-framebuffer
    # budget — texture placement is a porting artifact (the ARAM v7 argument)
    # and FB placement doubly so (chocomk parked its flip pair at/above the
    # 8 MB line). Pre-v8 sidecars fall back to the raw address high-water;
    # no volume<=address theorem exists here (unlike ARAM), but every
    # measured sidecar satisfies content+2*fb < peak by a wide margin, so
    # the fallback under-scores in practice (spec, stated honestly).
    vram_ct, vram_fb = vram.get("content_total"), vram.get("fb_bytes")
    vram_fit = vram_ct + 2 * vram_fb if (vram_ct is not None and vram_fb is not None) \
               else vram_peak
```

Then in the `peaks`/gate block (currently lines 178-184), use the fit value and extend the metric lookup:

```python
    peaks = {"vram": vram_fit, "aram": aram_fit}
    if main_peak:
        peaks["main"] = main_peak
    mem, gated = memory_axis(peaks)
    if mem is None:
        volume_keyed = {"aram": aram_ct is not None,
                        "vram": vram_ct is not None and vram_fb is not None}
        metric = "content" if volume_keyed.get(gated) else "peak"
        sc["gate"] = f"G3 memory: {gated} {metric} > 2x DC capacity"
```

(The `aram_ct`/`aram_fit` lines between these two blocks stay exactly as they are.)

- [ ] **Step 4: Run the scorer and guard suites**

Run: `python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py`
Expected: both print `ALL OK`. The guard file's synthetic sidecars carry no vram content keys, so they exercise the fallback path — including the still-present BIOS clamp tests (Task 4 changes those).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/score.py tools/assess/tests/test_score.py
git commit -m "assess: VRAM keyed on FB-masked content + 2x FB budget, address fallback (§6 ruling 2)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Scorer — BIOS-logo signature clamp becomes a refusal canary

**Files:**
- Modify: `tools/assess/score.py:20-29` (signature table comment), the clamp block from Task 3, `:209-212` (`vram_bios_noise_excluded` write)
- Test: `tools/assess/tests/test_metric_guards.py:32-50`

**Interfaces:**
- Consumes: `BIOS_VRAM_SIGNATURES` (unchanged table), sidecar `memory.vram.peak`/`nz_above_cap`.
- Produces: `score_sidecar` raises `MetricRegression` when a **booted** sidecar matches a signature exactly; `scores.vram_bios_noise_excluded` is never written again. G1-parked sidecars with signature values (dragntr3) return normally — the boot gate precedes the check.

- [ ] **Step 1: Rewrite the two clamp guard tests and add the G1 guard**

In `tools/assess/tests/test_metric_guards.py`, replace `test_gd_bios_logo_excluded` (lines 32-40) with — this STRENGTHENS the invariant (clamp-and-score → refuse-to-score), per spec ruling 4:

```python
def test_gd_bios_logo_signature_refuses_to_score():
    """v8 (spec 2026-08-07-vram-fb-masking-design.md ruling 4): post-v5
    handoff gating, the exact 9.4 MB Naomi-logo signature on a BOOTED title
    can only mean pre-VRAMHANDOFF samples leaked into the profile again —
    refuse, same posture as the DMPD canary (was: clamp to cap and score)."""
    sc = base_sc()
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57048}
    try:
        score.score_sidecar(sc)
    except score.MetricRegression:
        return
    raise AssertionError("BIOS-logo signature was scored instead of refused")


def test_gd_bios_logo_values_on_g1_park_do_not_raise():
    """dragntr3 shape: a G1-parked (never-booted) sidecar legitimately carries
    the logo values — the boot gate precedes the canary, no raise."""
    sc = base_sc()
    sc["boot"] = {"ok": False, "failure_class": "no-render-after-handoff"}
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57048}
    score.score_sidecar(sc)
    assert sc["gate"] == "G1 broken: no-render-after-handoff", sc["gate"]
```

Update `test_signature_requires_exact_match` (lines 43-50) — one byte off must still score normally, and the dead key must stay dead:

```python
def test_signature_requires_exact_match():
    """One byte off the signature = real game content -> normal (penalized)
    scoring through the address fallback, no refusal, no clamp key."""
    sc = base_sc()
    sc["memory"]["vram"] = {"peak": 0x943000, "nz_above_cap": 57049}
    score.score_sidecar(sc)
    assert sc["gate"] is None
    assert sc["scores"]["memory"] < 60.0, sc["scores"]
    assert "vram_bios_noise_excluded" not in sc["scores"]
```

- [ ] **Step 2: Run guards to verify the rewritten tests fail**

Run: `python3 tools/assess/tests/test_metric_guards.py`
Expected: `test_gd_bios_logo_signature_refuses_to_score` raises AssertionError ("scored instead of refused" — the clamp still scores it 85).

- [ ] **Step 3: Implement**

In `tools/assess/score.py`:

(a) Replace the clamp (the `bios_noise`/`vram_peak = min(...)` lines from Task 3's block) with:

```python
    vram = sc["memory"]["vram"]
    bios_noise = BIOS_VRAM_SIGNATURES.get((vram["peak"], vram.get("nz_above_cap")))
    if bios_noise is not None:
        raise MetricRegression(
            f"METRIC REGRESSION: '{sc['set']}' vram (peak, nz_above_cap) match the "
            f"BIOS-logo signature ({bios_noise}) on a booted title — post-v5 "
            f"handoff gating this can only mean pre-VRAMHANDOFF samples leaked "
            f"into the profile again (kb §8); refusing to score.")
```

and change the fallback expression's `vram_peak` to `vram["peak"]` (the local `vram_peak` variable disappears):

```python
    vram_ct, vram_fb = vram.get("content_total"), vram.get("fb_bytes")
    vram_fit = vram_ct + 2 * vram_fb if (vram_ct is not None and vram_fb is not None) \
               else vram["peak"]
```

(b) Delete the two `vram_bios_noise_excluded` lines near the end of `score_sidecar` (`if bios_noise is not None: sc["scores"]["vram_bios_noise_excluded"] = bios_noise`).

(c) Update the `BIOS_VRAM_SIGNATURES` comment block (lines 20-26) — replace the last two sentences ("When a sidecar matches ... floor 85).") with:

```python
# v8 (spec 2026-08-07-vram-fb-masking-design.md ruling 4): the v5 handoff
# gating removed the noise this table once clamped, so an exact match on a
# booted title now means the gating regressed — refuse to score (canary,
# same posture as ARAM_DMPD_ABOVE_CAP below). dragntr3's G1-parked sidecar
# legitimately carries these values; the boot gate precedes this check.
```

- [ ] **Step 4: Run the scorer and guard suites, then the committed-sidecar smoke**

```bash
python3 tools/assess/tests/test_score.py && python3 tools/assess/tests/test_metric_guards.py
python3 - <<'EOF'
import copy, json, glob, sys
sys.path.insert(0, "tools/assess")
import score
for f in sorted(glob.glob("assessments/*.metrics.json")):
    sc = copy.deepcopy(json.load(open(f)))
    score.score_sidecar(sc)   # any MetricRegression here = a committed sidecar trips the new canary
print("no committed sidecar trips the canary")
EOF
```

Expected: both test files `ALL OK`; the smoke prints its success line (dragntr3 is G1-gated before the canary; no other sidecar carries the signature values).

- [ ] **Step 5: Commit**

```bash
git add tools/assess/score.py tools/assess/tests/test_metric_guards.py
git commit -m "assess: BIOS-logo signature clamp -> MetricRegression canary (spec ruling 4)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Battery — sidecar fields + `BATTERY_VERSION = "8"`

**Files:**
- Modify: `tools/assess/run_battery.py:18` (version), `:316-318` (sidecar vram block)

**Interfaces:**
- Consumes: `cap["vram"]["content_total"]` / `cap["vram"]["fb_bytes"]` from Task 2's parser.
- Produces: sidecar `memory.vram.content_total` + `memory.vram.fb_bytes` (keys present only when measured — spec: "no zero-fill") and `versions.battery == "8"`. Tasks 6-7 rely on both.

- [ ] **Step 1: Bump the version constant**

Replace line 18 of `tools/assess/run_battery.py` with:

```python
BATTERY_VERSION = "8"  # v8: VRAM keyed on FB-masked content VOLUME + flat 2x framebuffer budget (spec docs/superpowers/specs/2026-08-07-vram-fb-masking-design.md, second §6 ruling). Fork cartlog_vram_profile masks the sample-time FB regions ({FB_W_SOF1/2, FB_R_SOF1} x fb_size) out of new content_* counters and logs fb_bytes; sidecar gains memory.vram.content_total (max of per-sample below+above) + fb_bytes; score.py keys vram on content_total + 2*fb_bytes with raw-peak address fallback for pre-v8 sidecars; BIOS_VRAM_SIGNATURES clamp promoted to MetricRegression canary. Capture format changes (fork commit recorded in versions.flycast).
```

- [ ] **Step 2: Write the new fields into the sidecar**

Replace the vram block of the `"memory"` dict (lines 316-318) with:

```python
                   "vram": {"peak": cap["vram"]["peak"], "nz_total": cap["vram"].get("nz_total"),
                            "nz_above_cap": cap["vram"]["nz_above_cap"],
                            "regs_last": cap["vram"]["regs_last"],
                            **({"content_total": cap["vram"]["content_total"],
                                "fb_bytes": cap["vram"]["fb_bytes"]}
                               if cap["vram"]["content_total"] is not None else {})},
```

- [ ] **Step 3: Run the whole assess test suite**

Run: `for t in tools/assess/tests/test_*.py; do python3 "$t" || break; done`
Expected: every file prints `ALL OK`. (No unit test covers `run_battery.main()` — Task 6's first anchor run verifies the pipeline end to end.)

- [ ] **Step 4: Commit**

```bash
git add tools/assess/run_battery.py
git commit -m "assess: battery v8 — sidecar carries vram.content_total + fb_bytes

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Anchor control runs — cleoftp, then ikaruga

**Files:**
- Modify: `assessments/cleoftp.metrics.json`, `assessments/cleoftp.md`, `assessments/ikaruga.metrics.json`, `assessments/ikaruga.md`, `assessments/evidence/<set>/shot-*.png`
- Reference: `assessments/RUNBOOK.md` (per-family flow)

**Interfaces:**
- Consumes: Tasks 1-5 landed. The battery preflight (`selftest()`) runs `test_score.py`, `test_metric_guards.py`, and the calibration guard, refusing to start if red — the spec's "calibration guard green first" is automatic.
- Produces: two v8 sidecars proving the new fork build measures correctly (a park on either raises `MetricRegression` by design). Task 7 proceeds only if both reproduce.

These are CONTROL runs for the fork change (kb discipline: a fork change needs known-good titles first). cleoftp is the project's calibration anchor; ikaruga is the official-DC-port anchor whose final cannot move (main 12.5 binds) — it is here purely to validate the build.

Per anchor (cleoftp first), run this cycle — strictly one at a time, `pgrep -x Flycast` empty first:

- [ ] **Step 1: Record the prior committed figures**

```bash
git show HEAD:assessments/<set>.metrics.json | python3 -c "
import json, sys
sc = json.load(sys.stdin)
m, v = sc['memory'], sc['memory']['vram']
print('coverage:', sc['capture'].get('coverage'), '| battery:', sc['versions']['battery'])
print('main peak:', m['main'].get('peak'), '| dma_hw:', m['main']['dma_high_water'])
print('aram content_total:', m['aram'].get('content_total'), '| aram peak:', m['aram']['peak'])
print('vram peak:', v['peak'], '| nz_total:', v.get('nz_total'), '| nz_above_cap:', v['nz_above_cap'])
print('scores:', sc.get('scores'), '| gate:', sc.get('gate'))"
```

- [ ] **Step 2: Run the battery and verify the v8 sidecar**

```bash
python3 tools/assess/run_battery.py <set>
python3 - <<'EOF'
import json
sc = json.load(open("assessments/<set>.metrics.json"))
v = sc["memory"]["vram"]
assert sc["versions"]["battery"] == "8", sc["versions"]
assert "content_total" in v and "fb_bytes" in v, "pipeline lost the v8 vram fields"
assert sc.get("gate") is None, sc["gate"]   # an anchor park would have crashed already
fit = v["content_total"] + 2 * v["fb_bytes"]
print(sc["set"], "| flycast:", sc["versions"]["flycast"],
      "| content_total:", v["content_total"], "| fb_bytes:", v["fb_bytes"],
      "| fit:", fit, "| fit-u:", round(fit / (8 << 20), 3),
      "| raw peak:", v["peak"], "| final:", sc["scores"]["final"])
EOF
```

**Reproduction check against Step 1** (this is the control): boot ok, same `handoff.trigger`, and raw figures (`main peak`, `aram content_total`, `vram peak`) within ~10% of the prior run's. Spec bounds: cleoftp fit-u ≤ ~0.75 (content 4.8 MB raw nz minus FB writes + 1.2 MB budget — likely vram sub 100, final rises above 84.8); ikaruga fit-u ≈ ≤ 0.9, final unchanged at 38.6 (main 12.5 still binds). A park, a missing field, raw-figure drift >10%, or `fb_bytes` not 614,400 (both anchors are 640×480) — STOP the wave, debug the fork change with superpowers:systematic-debugging, never hand-adjust.

- [ ] **Step 3: Re-annotate `capture.coverage`** — a re-run resets it to null. Inspect the run's `assessments/evidence/<set>/shot-*.png` per RUNBOOK's representativeness check ("demo" if any frame shows in-game/demo footage, "title" if only title/attract cards); set the field in the sidecar JSON, using Step 1's prior value as the reference — if the new run's screenshots reach less than the prior run did, keep the conservative lower of the two.

- [ ] **Step 4: Update the assessment doc** (`assessments/<set>.md`):
  - §1 header status row: append `; vram-fb-masking re-run 2026-08-07 · battery v8 · flycast <hash from the sidecar>`.
  - §4 Memory fit table: change the VRAM row to `VRAM (FB-masked content + 2×FB)` with the fit bytes, new u, new sub-score, evidence `grep VRAMPROFILE (content_* fields)`; add one prose line under the table with the raw peak, `fb_bytes`, and `fb_masked_nz` figures for continuity.
  - §8 score computation + §1 verdict: the new memory axis / final / tier.

- [ ] **Step 5: Commit the set**

```bash
git add assessments/<set>.metrics.json assessments/<set>.md assessments/evidence/<set>/
git commit -m "assess: <set> vram-fb-masking anchor control (battery v8) — <one-line outcome>

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Repeat for ikaruga. Both anchors green → Task 7.

---

### Task 7: Re-run wave — 8 sets, serial

**Files:**
- Modify (per set): `assessments/<set>.metrics.json`, `assessments/<set>.md`, `assessments/evidence/<set>/shot-*.png`
- Reference: `assessments/RUNBOOK.md`, `assessments/chocomk.md` §4/§9 (the flags this wave resolves)

**Interfaces:**
- Consumes: Task 6 both anchors reproduced.
- Produces: 8 more v8 sidecars with measured `vram.content_total`/`fb_bytes`; updated per-set docs. Task 8 regenerates tables from these.

Wave order and expectations (spec § Expected outcomes — bounds, the measurement decides). "Next binding" = the sub-score that caps the memory axis once VRAM rises:

| # | Set | Today (vram sub) | Expected | Next binding |
|---|---|---|---|---|
| 1 | chocomk | 25.6 | fit ≈ 3.2 MB, u ≈ 0.38 → vram 100, memory 85, rank climbs (the motivating case) | main/aram 85.0 |
| 2 | sgtetris | 12.4 | vram rises by the FB share of its 5.6 MB above-cap content | main 20.5 |
| 3 | gunsur2 | 13.0 | rises | main 14.6 |
| 4 | marstv | 21.6 | rises | main 28.0 |
| 5 | illvelo | 22.4 | rises | main 24.9 |
| 6 | mamonoro | 24.6 | rises | main 37.3 |
| 7 | radirgyn | 36.6 | rises | main 55.2 |
| 8 | moeru | 87.9 | u 0.96 → likely vram 100, memory 100 | none (main/aram 100) |

Per set, repeat the Task 6 cycle with these deltas:

- [ ] **Step 1: Prior figures** — same command as Task 6 Step 1.

- [ ] **Step 2: Run + verify** — same commands as Task 6 Step 2, except: `gate` may legitimately be non-None only if it already was (none of the 8 is currently parked — any NEW park is a stop-the-wave signal, not a result), and the reproduction tolerance applies to `main`/`aram` figures only (`vram` numbers are expected to change shape). Sanity-check per set: `content_total + fb_masked_nz ≈ nz_total` (within the run-to-run delta), `fb_bytes == 614400` unless the title runs a non-640×480 mode — a wildly different `fb_bytes` means reg garbage, stop and debug. Compare the new vram sub against the table: a title that moves the OPPOSITE way (vram sub drops below today's) breaks the design's rises-only expectation — stop the wave and debug before continuing.

- [ ] **Step 3: Re-annotate coverage** — same as Task 6 Step 3.

- [ ] **Step 4: Update the doc** — same as Task 6 Step 4, plus for **chocomk only**: mark the §4 "deliberately not hand-adjusted" paragraph and the §9 first bullet **RESOLVED 2026-08-07** (battery v8, spec pointer, measured fit figures) — mirror how gwing2's Gate tensions were struck through and resolved.

- [ ] **Step 5: Commit the set** — same as Task 6 Step 5, message `assess: <set> vram-fb-masking re-run (battery v8) — <one-line outcome>`.

Then move to the next set in the table.

---

### Task 8: Blanket re-score + regenerate tables

**Files:**
- Modify: `assessments/RANKING.md`, `GAME_FORMATS.md`; `assessments/QUEUE.md` only if a status actually changes (none expected)

**Interfaces:**
- Consumes: all 10 v8 sidecars committed; scorer from Tasks 3-4.
- Produces: campaign tables consistent under one scorer version. Task 9 cites them.

- [ ] **Step 1: Re-score every sidecar under the new scorer**

```bash
for f in assessments/*.metrics.json; do
  python3 tools/assess/score.py "$f" || echo "NOT RESCORED: $f"
done
```

`score.py` refuses sidecars whose controls research is pending — every committed sidecar has researched controls, so expect zero `NOT RESCORED` lines; if one appears, report it, don't force it.

- [ ] **Step 2: Verify the no-change proof**

Run: `git diff --stat assessments/`
Expected: **zero modified files.** Non-wave sidecars lack the vram content keys, take the address fallback, and reproduce their committed scores byte-for-byte (no committed sidecar carries `vram_bios_noise_excluded`, verified at plan time); wave sidecars were already scored by the v8 battery. Any diff means the fallback changed a score it must not touch — stop and debug before proceeding.

- [ ] **Step 3: Regenerate tables**

```bash
python3 tools/assess/gen_tables.py ranking
python3 tools/assess/gen_tables.py patch
```

`QUEUE.md` is hand-curated — no v8 set changes park/scored status (no VRAM parks exist either way), so expect no edits; if a wave result did flip a status, update only that cell.

- [ ] **Step 4: Sanity-check RANKING.md**

Read the regenerated `assessments/RANKING.md`: the 10 wave sets show battery `8` provenance; chocomk's rank climbed (memory 85 vs 25.6); no non-wave row's final moved.

- [ ] **Step 5: Commit**

```bash
git add assessments/RANKING.md GAME_FORMATS.md
git commit -m "tables: regenerate under vram-fb-masking scorer (battery v8 wave)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

(Add `assessments/QUEUE.md` to the `git add` only if Step 3 actually edited it.)

---

### Task 9: Knowledge base entry, close the brief, final verification

**Files:**
- Modify: `docs/kb/assessment-tooling.md` (§1 tooling table, §6), `docs/superpowers/specs/backlog-vram-fb-masking.md`

**Interfaces:**
- Consumes: wave results (Tasks 6-7 sidecars), regenerated tables (Task 8), the fork hash from Task 1.
- Produces: the §6 checkpoint record for ruling 2; the updated tooling inventory; the closed motivating brief.

- [ ] **Step 1: Write the kb entries**

In `docs/kb/assessment-tooling.md`:

(a) §1 tooling table: update the "Instrumented Flycast fork" row to the Task 1 commit hash with a note — `v8 FB-masked VRAM content counters (spec 2026-08-07-vram-fb-masking-design.md); v6 base 65f9f7857`.

(b) Campaign version line (top of file): battery **v8**, with the §-reference for the new entry.

(c) §6 intro: mark `backlog-vram-fb-masking.md` **landed 2026-08-07 as battery v8** — mirror the phrasing used for the aram-gate-volume brief.

(d) Append a new numbered §6 item recording, with actual measured numbers pulled from the wave sidecars:

- The ruling (user, 2026-08-07 brainstorm): VRAM gate + axis re-keyed on `content_total + 2×fb_bytes`; flat 2× budget; raw-peak fallback for pre-v8 sidecars; `BIOS_VRAM_SIGNATURES` clamp → refusal canary. Second §6 semantics change under the opened checkpoint.
- The evidence: chocomk's flip pair at/above the 8 MB line (3,156,395 of 3,169,579 nz bytes above cap); the phantom-`fb_w_sof2=0xc00000` finding (universal BIOS default, never written in ausfache/cleoftp/moeru); nine scored titles binding on VRAM, not the brief's four.
- The measured fit-u distribution across all 10 wave sets, extracted with:

```bash
python3 - <<'EOF'
import json
for s in ("cleoftp","ikaruga","chocomk","sgtetris","gunsur2","marstv","illvelo","mamonoro","radirgyn","moeru"):
    sc = json.load(open(f"assessments/{s}.metrics.json"))
    v = sc["memory"]["vram"]
    fit = v["content_total"] + 2 * v["fb_bytes"]
    print(f"{s}: content={v['content_total']:,} fb={v['fb_bytes']:,} fit-u={fit/(8<<20):.3f} "
          f"(raw peak-u {v['peak']/(8<<20):.3f}) final={(sc.get('scores') or {}).get('final')}")
EOF
```

- The deferrals: the TA/ISP-OL structure budget stays out of the metric (host-side blind spot, documented in the fork comment — unchanged from v1); the remaining §6 items (ARAM 2× multiple, streaming re-read, main high-water, controls band) still open.

- [ ] **Step 2: Close the motivating brief**

Edit `docs/superpowers/specs/backlog-vram-fb-masking.md`'s Status line to:

```markdown
**Status:** LANDED 2026-08-07 as battery v8 — design
`2026-08-07-vram-fb-masking-design.md`, kb §6 checkpoint entry records the
ruling and wave results. Kept as the motivating brief.
```

- [ ] **Step 3: Final verification**

```bash
for t in tools/assess/tests/test_*.py; do python3 "$t" || break; done
git status --short
cd /Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src && git status --short && git log --oneline -1
```

Expected: every test file `ALL OK`; no unexpected untracked/modified files in either repo (evidence `raw/` dirs are gitignored); the fork's HEAD is the Task 1 commit.

- [ ] **Step 4: Commit**

```bash
git add docs/kb/assessment-tooling.md docs/superpowers/specs/backlog-vram-fb-masking.md
git commit -m "kb: §6 vram-fb-masking checkpoint entry (ruling 2); close motivating brief

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```
