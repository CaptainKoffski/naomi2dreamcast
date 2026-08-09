# Puyo Puyo Da! (Japan) (841-0006C) (`puyoda`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **81.8 (S)** |
| Bottom line | Everything fits with room to spare (content-u: main 0.276, VRAM 0.450, ARAM 0.727) — but porting is redundant: the DC retail build is the original, shipped ten days *before* the Naomi cart; the assessment's value is as a pipeline calibration point. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — fresh re-capture (provenance v8→v9, scoring keys unchanged; see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `puyoda` (no clones — single GAME line, MAME naomi.cpp @59e7c0b line 11097) |
| Maker / year | Compile, 1999 |
| Genre / format | Labeled Puzzle ★ in our tables, actually a **dance/rhythm game** (Simon-says call-and-response with Puyo garbage mechanics — [Puyo Nexus](https://puyonexus.com/wiki/Puyo_Puyo_DA!)). **M2-encrypted cart** 841-0006C, 315-5881 key `000acd40` (naomi.cpp lines 7513–7514), machine `naomim2`, ROT0 horizontal |
| Official DC port | **Yes — and the DC version came first**: *Puyo Puyo Da! Featuring Ellena System*, DC JP 1999-12-16; the Naomi arcade release followed 1999-12-26 ([Puyo Nexus](https://puyonexus.com/wiki/Puyo_Puyo_DA!), [Wikipedia](https://en.wikipedia.org/wiki/Puyo_Puyo_Da!)). The cart is the derivative release |
| Community ports | No Naomi→DC conversion found (searched 2026-08-08) — moot given the official DC original. English fan translation of the DC version by streeker, Jan 2025 ([dreamcast-talk t=18118](https://www.dreamcast-talk.com/forum/viewtopic.php?t=18118), [Time Extension](https://www.timeextension.com/news/2025/01/dreamcast-dance-rhythm-game-puyo-puyo-da-is-now-available-to-play-in-english)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/puyoda.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle across the 10 shots: copyright/press-start fade-in → title logo (ぷよぷよDA! featuring ELLENA System) → character vs-select cards → RANKING table (中辛 difficulty) → live demo gameplay (STAGE S, RULUE VS SATAN, running score) → 2P tutorial card → live demo gameplay (STAGE 2, TARA VS TARA, dance-off) → D's Station DS Vol.4 magazine ad (Compile promo).
Screenshots kept (5 of 10):
- `assessments/evidence/puyoda/shot-060s.png` — copyright/press-start fade-in ("1994")
- `assessments/evidence/puyoda/shot-121s.png` — title logo: ぷよぷよDA! featuring ELLENA System, press start
- `assessments/evidence/puyoda/shot-243s.png` — RANKING table (中辛 difficulty), top-5 scores/stages
- `assessments/evidence/puyoda/shot-304s.png` — attract gameplay: STAGE S, RULUE VS SATAN, live score 5,402,880
- `assessments/evidence/puyoda/shot-609s.png` — D's Station DS Vol.4 magazine ad (Compile attract promo)

Anomalies: −0.1 final (81.9→81.8) vs the prior (v8-provenance) sidecar is fresh-capture
noise, not a memory-region change. Diffing the two committed sidecars, the only axis that
moved is **streaming** (68.4→68.1): `dma_events` 1,708→1,689, `reread_ratio`
0.6302→0.6484, `steady_mb_per_min` 12.358→12.24, `unique_bytes` 47,327,232→45,092,864
(`total_bytes` roughly flat: 127,965,184→128,260,096). This is steady-state-window
dilution — wall-clock capture timing lands the 480 s steady-state sampling window
(t=120s→600s) at a slightly different phase of the game's cyclic attract/demo loop each
run, shifting the first-seen-vs-repeat DMA mix without changing what data the title
actually uses. The **memory** axis is exactly unchanged (100.0→100.0): VRAM
`nz_above_cap` (2,945,767) and `content_total` (2,549,404) are byte-for-byte identical
between the two sidecars; only the informational VRAM watermark shifted
(13,140,656→13,045,760, ~95 KB — a different frame's write extent at the handoff instant)
with no scoring effect. ARAM `content_total` moved 1,524,273→1,524,369 (+96 B, noise
floor). `guts` (85.0), `controls` (100.0), and `similarity` (40.0) are byte-identical to
the prior sidecar.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 4,636,679 | 16,777,216 | 0.276 | 100.0 | address peak 16,515,012 (u 0.984, informational) · nz_above_cap 0 — content fits outright · `dma_high_water` 16,187,360 |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 3,778,204 (content 2,549,404 + 2×614,400) | 8,388,608 | 0.450 | 100.0 | address peak 13,045,760 (u 1.555) is extent, not content — FB pair sits at/above the 8 MB line (`fb_w_sof1=800000 fb_r_sof1=c00000`, the chocomk pattern) · nz_above_cap 2,945,767 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,524,369 | 2,097,152 | 0.727 | 100.0 | address peak 4,670,845 (u 2.227) vs `nz_above_cap = 4 B` — see below |

No region binds — all three sub-scores are 100.0.
**§6 checkpoint evidence — second sgtetris-class ARAM divergence:** the address peak
(4,670,845 B, u=2.227) is past the old `u > 2.0` address gate, so pre-v7 keying would have
G3-parked this title on **4 bytes** of real content above the 2 MiB cap (sgtetris: 8 B at
u=3.94). Volume keying (v7, kb §6 item 6) scores it correctly instead — this run was the
first *fresh* assessment (not a re-run) where the v7 re-key visibly prevented a false park.
Watermarks (informational, content-scan — stale-data prone): main 16,515,012 ·
vram 13,045,760 · aram 8,388,608.

## 5. Cart streaming (axis: 68.1)

DMA events 1,689 · total 122.3 MB · unique 43.0 MB · re-read ratio 0.6484 ·
steady-state 12.24 MB/min (`short_window: false`) · PIO 2,098,528 B.
The unique working set (43.0 MB this run) is the largest of its wave — music/voice
streaming for a rhythm game; a DC port streams the same data from GD-ROM (and the DC
original demonstrably did). Run-to-run swing on this axis (68.4→68.1) is steady-state
window dilution — see §3 Anomalies.

## 6. Guts (axis: 85.0)

Code 2,097,152 B (carve `base 0x8c020000`, entry `0x8c021000`, header title
"PUYOPUYO DA! IN JAPAN ----") · functions 2,777 · MMIO refs: scif 2, rtc 4, g2ext 132 ·
BIOS vector refs: none · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 2P panel — **no dance pad**; gameplay uses 4 directional inputs +
1 action button (Simon-says prompts). `controls.device_class = stick`. MAME input ports:
`naomi` (INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506 — digital stick + buttons,
no analog).
Proposed DC mapping: d-pad + one face button, 1:1 — the DC original shipped with three
selectable pad layouts (Type A/B/C), so the mapping is not hypothetical but the game's
native design.
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Puyo Nexus](https://puyonexus.com/wiki/Puyo_Puyo_DA!);
[Time Extension](https://www.timeextension.com/news/2025/01/dreamcast-dance-rhythm-game-puyo-puyo-da-is-now-available-to-play-in-english).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 68.1^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **81.8 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Porting is redundant**: the DC retail build is the original (shipped before the
  arcade cart) and a 2025 English fan patch modernizes it. Value of this assessment is
  as a calibration point: a genuinely DC-authored title measured through the Naomi
  battery scores S-tier with every region fitting — the pipeline agrees with ground truth.
- **Genre label**: our tables say Puzzle ★; the game is a rhythm/dance title. Kept as-is
  in QUEUE.md/GAME_FORMATS.md (the ★ lane logic — small 2D, pad-friendly — still applies).
- ARAM address peak 2.23× vs 4 B content above cap: strongest possible endorsement of the
  v7 volume re-key on a fresh title; belongs in the §6 item 1 discussion of whether the
  2× multiple itself still means anything under volume keying.
- Main RAM address peak 16,515,012 (0.984×) nearly touches the cap, but content volume
  is 4.6 MB with zero above-cap content — layout, not volume; the DC original proves it
  fits in practice.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v8 | 2026-08-08 | 77.1 (A) | First assessment (fresh capture). ARAM address peak 2.23× would have G3-parked under pre-v7 address keying vs 4 B of above-cap content — first fresh title where the v7 volume re-key prevented a false park (kb §6 item 6); main write-truth address 0.984× binding |
| v9 | 2026-08-08 | 81.9 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory axis 100.0, no region binding |
| v9 | 2026-08-09 | 81.8 S | ranking-groom chunk 2: fresh v9 capture, provenance v8→v9 (scoring keys unchanged); −0.1 streaming noise |
