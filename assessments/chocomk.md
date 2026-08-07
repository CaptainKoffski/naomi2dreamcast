# Musapey's Choco Marker (Rev A) (GDL-0014A) (`chocomk`) — portability assessment

> **Battery v8 vram-fb-masking re-run (2026-08-07): 76.7 (A)** — first re-run since the
> v5 baseline (fb8644d), so this catches up three §6 region-keying rulings at once: main
> write-truth (v6), ARAM content-volume (v7), and VRAM FB-masked content + 2×FB (v8, this
> task's target change — spec `2026-08-07-vram-fb-masking-design.md`, chocomk is its
> motivating case). Sidecar: flycast `f014a410c`, battery 8. No park (`gate: null`), boot
> ok, PIO handoff at 20.0 s — same as v5. Streaming/guts/controls/similarity reproduce
> within run-to-run noise (steady 3.705 vs v5's 3.700 MB/min, same 1,526 DMA events;
> guts/controls/similarity bit-identical — deterministic cart scan).
>
> All three memory regions move: **VRAM** (this wave's target) flips from address
> high-water (13,496,860 B, u=1.61, sub 25.6) to FB-masked content: `content_total`
> 2,631,542 B + `2×fb_bytes` 1,228,800 B (`fb_bytes` 614,400 B, exactly 640×480×2) = fit
> 3,860,342 B, u=0.460 → sub **100.0**. **ARAM** moves from the exactly-2,097,136-B
> address peak (u≈1.00, sub 85.0) to `content_total` 1,332,513 B, u=0.635 → sub
> **100.0**. **MAIN** is write-truth measured for the first time (v6 instrumentation):
> peak 18,533,794 B — identical to this doc's old "informational, stale-data-prone"
> watermark figure below, confirming (as with `gwing2`) those were real game writes all
> along, not stack noise — u=1.105, `nz_above_cap` 1,420,913 B genuinely above the 16 MB
> DC cap → sub **66.2**, now the binding region. Memory axis min(66.2, 100.0, 100.0) =
> **66.2**, up from 25.6; final **52.5 → 76.7**, tier **B → A**. The design doc's
> speculative "memory 85" bound (main assumed to land at the cap) undershoots reality —
> the write-truth measurement shows chocomk's main-RAM working set genuinely exceeds the
> DC's 16 MB by ~1.4 MB, a real porting cost the old DMA-high-water metric couldn't see.
> Coverage re-annotated `demo` (unchanged — the fresh run's screenshots reach the same
> 「デモプレイ」 attract loop and "回転" rotate-block tutorial cards; curated set swapped
> `shot-609s.png`, which this run caught mid-blank-transition, for two tutorial frames).

## 1. Verdict

| | |
|---|---|
| **Final score** | **76.7** (A) |
| Bottom line | Best newly-scored title of the DC-ported ★ batch: ARAM lands 16 bytes under the DC's 2 MiB cap and main-RAM DMA high-water is *exactly* 16 MiB — the content was authored to DC-shaped budgets (Ecole shipped the DC port the same year). The only over-budget axis, VRAM 1.61×, is mostly an artifact of framebuffer placement above the 8 MB line (see §4), so the true porting cost is likely lower than the score says. **(battery v8 update, see banner above:** VRAM's FB-placement artifact is now excluded by construction and no longer binds; write-truth main RAM turns out to be the real over-budget axis instead, ~1.4 MB above the 16 MB cap.) |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; vram-fb-masking re-run 2026-08-07 · battery v8 · flycast `f014a410c` |

## 2. Identity

| | |
|---|---|
| Set / family | `chocomk` (no clones — `parent: null` in controls.json) |
| Maker / year | Ecole Software, 2002 (controls.json) |
| Genre / format | Puzzle ★ (3D block-matching action-puzzle), GD-ROM (GDL-0014A, 68.5 MB) |
| Official DC port | **Yes — Musapey's Choco Marker (Dreamcast, Japan, 2002, Ecole)** ([GameFAQs](https://gamefaqs.gamespot.com/dreamcast/583195-musapeys-choco-marker), [arcade-museum](https://www.arcade-museum.com/game_detail.php?game_id=17905)). Assessed as reference/validation data per GAME_FORMATS.md policy. |
| Community ports | Moot — official DC port exists. |
| Representative choice | Only member of its family (MAME parent, no clones); Rev A is the newest revision. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/chocomk.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-060s.png` and `shot-304s.png` are live attract
gameplay with the デモプレイ/Demo banner; `shot-182s.png` and `shot-548s.png` are the
"回転" (rotate) tutorial cards, also part of the demo loop. Sidecar
`capture.coverage = "demo"`.
Screenshots: `assessments/evidence/chocomk/shot-060s.png`, `shot-182s.png`, `shot-304s.png`,
`shot-548s.png` (curated from 10; v8 re-run — `shot-609s.png` caught the loop's blank
transition frame this time, dropped in favor of the two tutorial cards).
Anomalies: none — clean single-leg GD run, no flake, no display blindness. v8 re-run
reproduced the same clean single-leg boot.

## 4. Memory fit (axis: 66.2)

Table refreshed 2026-08-07 (battery v8) to the region keying this doc's v5 baseline
never had: main on write-truth peak (v6), ARAM on content volume (v7), VRAM on
FB-masked content + 2×FB budget (v8, this task). See the banner above for the
before/after reasoning; the v5-era table below the line still stands as the original
address-keyed cross-check.

| Region | Peak / fit | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth) | 18,533,794 B (`0x11abbe2`) | 16 MB | 110.5% | 66.2 | grep `MAINPROFILE`/`MAINHIST` |
| VRAM (FB-masked content + 2×FB) | 3,860,342 B (content_total 2,631,542 + 2×fb_bytes 1,228,800) | 8 MB | 46.0% | 100.0 | grep `VRAMPROFILE` (content_* fields) |
| ARAM (content, volume-keyed) | 1,332,513 B | 2 MB | 63.5% | 100.0 | grep `ARAMPROFILE` (content_* fields) |

Memory axis = min(region sub-scores) = 66.2 (regions aren't tradeable; main now binds,
not VRAM — this is chocomk's first write-truth main measurement, and it lands genuinely
above the DC cap: `nz_above_cap` 1,420,913 B).
For continuity: VRAM's raw address high-water peak is still 13,496,860 B (u=1.61, the
pre-v8 keying), `fb_bytes` maxed at 614,400 B (exactly 640×480×2, matching both anchors'
size), and `fb_masked_nz` (evidence-only, not sidecar-persisted, from the raw cartlog)
reached up to 675,147 B across the up-to-three masked FB registers — proof the masked
intervals are genuinely FB-active buffers, not phantom unwritten registers.

(v5-era address-keyed table, retained as history:)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 16,777,216 | 16 MB | 1.00× | 85.0 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 13,496,860 | 8 MB | 1.61× | 25.6 | grep `VRAMPROFILE` |
| ARAM (content, fill-excluded) | 2,097,136 | 2 MB | 1.00× | 85.0 | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 18,533,794 /
vram 13,496,860 / aram 8,388,608. Main watermark 1.10× the DMA high-water — mild.
**v8 update: the main watermark and the new write-truth peak are the same number,
18,533,794 B — this was never stale data, it was real above-cap game usage the
DMA-high-water metric couldn't see (same pattern as `gwing2`'s v6 re-run).**

The region pattern echoes `tetkiwam`: **ARAM peaks at 2,097,136 B — 16 bytes under the
DC's 2 MiB cap, `nz_above_cap = 0`** — and main-RAM DMA lands at exactly 16,777,216 B.
Sound and main memory were authored inside DC budgets, consistent with the same-year
official DC port. ~~The binding VRAM axis is largely **framebuffer placement, not
texture volume**: `regs_last` shows `fb_w_sof1=800000`, `fb_w_sof2=c00000` — both write
framebuffers sit at/above the 8 MB line, while render structures live below
(`isp_base=0`, `ol_base=3eb780`); accordingly 3,156,395 B of the 3,169,579 B total
nonzero VRAM content is "above cap". A port would simply place the FBs inside the 8 MB
budget. Score deliberately not hand-adjusted (campaign comparability); recorded as a §6
checkpoint calibration observation.~~
**RESOLVED 2026-08-07 (battery v8, flycast `f014a410c`, spec
`2026-08-07-vram-fb-masking-design.md`):** exactly the fix this paragraph called for —
VRAM now scores on FB-masked content volume (2,631,542 B) plus a flat 2×FB budget
(1,228,800 B) instead of the raw address high-water, so the above-cap FB placement no
longer counts against the title. Measured fit 3,860,342 B, u=0.460 → VRAM sub-score
**100.0** (was 25.6). This was chocomk's motivating case for the whole v8 wave (design
doc "Goal"/"Motivating case"). The axis no longer needs a hand-adjustment caveat because
the metric itself now measures what the paragraph argued it should.

## 5. Cart streaming (axis: 76.5)

DMA events 1,526 · total 46.5 MB · unique 16.5 MB · re-read ratio 0.6459 ·
steady-state 3.705 MB/min (full window, `short_window: false`; v8 re-run, was 3.700 —
run-to-run noise, axis unchanged at 76.5)

## 6. Guts (axis: 95.0)

Code 1,572,864 B · functions 588 · MMIO refs: scif 0, rtc 0, g2ext 5 ·
BIOS vector refs: none extra (`extra_bios_classes: 0`) · penalties applied:
`eeprom_bios` → 95.0

Carve header title: `CHOCO MARKER` (base 0x0c020000, entry 0x0c021000).
`guts.sdk_strings` names Ecole's own stack — including **`D e a t h  C r i m s o n  OX`
/ "Presented by ECOLE"**: engine kinship with Death Crimson OX, a shipped Dreamcast
title, plus the JAPAN-only arcade notice and "Lib Handle Start".

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 1 used button (lay block; camera on
triggers/second button), 2 players. MAME input ports: `naomi`. Proposed DC mapping:
d-pad + A lay, triggers rotate camera — the official DC port shipped exactly that on a
stock pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcade-museum](https://www.arcade-museum.com/game_detail.php?game_id=17905)
(NAOMI standard stick+button cabinet);
[GameFAQs DC page](https://gamefaqs.gamespot.com/dreamcast/583195-musapeys-choco-marker)
(one lay-block button, triggers rotate camera).

## 8. Score computation

final (current, battery v8, from `assessments/chocomk.metrics.json` — quoted, not
hand-computed):
final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 66.2^.40 · 76.5^.20 · 95.0^.20 · 100.0^.10 · 70.0^.10 = **76.7** (tier A)

(v5-era formula below is retained as history; only memory changed — 25.6 → 66.2, the §4
region-keying catch-up — every other axis reproduces within run-to-run noise.)
      = 25.6^.40 · 76.5^.20 · 95.0^.20 · 100.0^.10 · 70.0^.10 = **52.5** (tier B)
Similarity inputs (sidecar): developer no, SDK overlap partial, loader match yes.
Prose note: as with tetkiwam, the shipped same-engine DC titles argue the real SDK
overlap is closer to full — checkpoint-worthy calibration observation.

## 9. Risks & notes

- ~~**The VRAM axis likely overcounts this title** (§4): the 1.61× peak is dominated by
  framebuffers placed above the 8 MB line (`fb_w_sof1=0x800000`, `fb_w_sof2=0xc00000`),
  and nearly all above-cap nonzero content is those FBs. Actual texture+render content
  is ~3.2 MB. Not hand-adjusted; §6 checkpoint data point (FB-placement class, joins
  the main-high-water clustering note from tetkiwam).~~
  **RESOLVED 2026-08-07 (battery v8, flycast `f014a410c`, spec
  `2026-08-07-vram-fb-masking-design.md`):** the §6 checkpoint re-keyed `score.py`'s
  VRAM region on FB-masked content volume + a flat 2×FB budget, exactly as this risk
  argued. Measured `content_total` 2,631,542 B + `2×fb_bytes` 1,228,800 B = fit
  3,860,342 B (u=0.460, well under cap) → VRAM sub-score **100.0** (was 25.6). VRAM no
  longer binds the memory axis; write-truth main RAM does instead (sub 66.2, u=1.105 —
  a genuine ~1.4 MB above-cap finding, not a metric artifact). chocomk was this wave's
  motivating case (design doc "Goal").
- Main-RAM DMA high-water of exactly 16,777,216 B (1.00×) sits right on the cap —
  fits, but with zero headroom under the v1 "assets landed" semantics; the official DC
  port proves the working set fits in practice. **v8 update: this bullet's DMA-only view
  is now superseded — write-truth (§4) shows main genuinely exceeds the cap by
  1,420,913 B (u=1.105). Left unstruck as the historical v1-metric record; the working
  set does NOT fit by the current, more complete measurement.**
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (main watermark 1.10× high-water — mild here). This is
  exactly the gap the v6 write-truth instrumentation closed (§4): the "mild" 1.10× ratio
  turned out to be the real above-cap figure, not overcount.
- A port project's first verification: diff the arcade GD content against the official
  DC release (same developer, same year) — asset-level reuse could make this the
  cheapest conversion in the scored list after `cleoftp`.
