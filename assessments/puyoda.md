# Puyo Puyo Da! (Japan) (841-0006C) (`puyoda`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 81.9 (S), was 77.1 (A)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> adopted to main 2026-08-09): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 4,637,168 B (content-u 0.276) replaces peak 16,515,012 B (u 0.984).
> Memory axis 100.0, binding region now **vram** (was memory 86.2). Verdict section below is the capture-time (v≤8) record.

## 1. Verdict

| | |
|---|---|
| **Final score** | **77.1** (A) |
| Bottom line | Everything fits: main RAM u=0.984 with zero content above cap, VRAM u=0.450 FB-masked, ARAM content u=0.727 — the highest-scoring cart title in the campaign so far. The ARAM *address* peak (4.67 MB, 2.23×) would have G3-parked it under pre-v7 address keying against just **4 bytes** of real above-cap content — the second sgtetris-class divergence and fresh §6 evidence that volume keying was right. A DC build already exists: the DC release (1999-12-16) *preceded* the Naomi cart by ten days. |
| Assessed | 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle across the 10 shots: ranking screens (per-difficulty 甘口/中辛 variants) → title/mode select → live demo gameplay (STAGE 3, "7 CHAINS!", running score) → 3D dance-off scenes → 2D pixel-art ELLENA intro.
Screenshots kept (5 of 10):
- `assessments/evidence/puyoda/shot-060s.png` — RANKING table (甘口 difficulty), character portraits
- `assessments/evidence/puyoda/shot-304s.png` — attract gameplay: STAGE 3, MINO VS ELLENA, 7 CHAINS!, live score
- `assessments/evidence/puyoda/shot-426s.png` — title: mode select (DANCE CHALLENGE / DANCE BATTLE), ©COMPILE 1994,1999
- `assessments/evidence/puyoda/shot-548s.png` — 3D dance-off: ELLENA VS ARLE, STAGE 1, direction-prompt columns
- `assessments/evidence/puyoda/shot-609s.png` — 2D pixel-art dance-lesson attract scene (Compile's ELLENA intro)

Deleted surplus (5): puyopuyo splash card, how-to-play blackboard, duplicate ranking (中辛), two intermediate attract frames.
Anomalies: none.

## 4. Memory fit (axis: 86.2)

| Region | Peak / fit | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth) | 16,515,012 | 16,777,216 | 0.984 (binding) | 86.2 | `MAINPROFILE`; `nz_above_cap = 0` — content fits outright |
| VRAM (FB-masked content + 2×FB) | 3,778,204 (content_total 2,549,404 + 2×fb_bytes 614,400) | 8,388,608 | 0.450 | 100.0 | `VRAMPROFILE`; raw address peak 13,140,656 (u 1.566) is extent, not content — FB pair sits at/above the 8 MB line (`fb_w_sof1=c00000 fb_r_sof1=800000`, the chocomk pattern) |
| ARAM (content, volume-keyed) | 1,524,273 | 2,097,152 | 0.727 | 100.0 | `ARAMPROFILE`; address peak 4,670,845 (2.23×) vs `nz_above_cap = 4 B` — see below |

**§6 checkpoint evidence — second sgtetris-class ARAM divergence:** the address peak
(4,670,845 B, u=2.227) is past the old `u > 2.0` address gate, so pre-v7 keying would have
G3-parked this title on **4 bytes** of real content above the 2 MiB cap (sgtetris: 8 B at
u=3.94). Volume keying (v7, kb §6 item 6) scores it correctly instead — this run is the
first *fresh* assessment (not a re-run) where the v7 re-key visibly prevented a false park.
Main RAM u=0.984 sits just under cap with zero above-cap content — consistent with a game
authored against DC budgets (the DC build shipped first).
Watermarks (informational, content-scan — stale-data prone): main 16,515,012 · vram 13,140,656 · aram 8,388,608.
`dma_high_water` 16,187,360 B (informational-only from v6 on).

## 5. Cart streaming (axis: 68.4)

DMA events 1,708 · total 127,965,184 B (122.0 MB) · unique 47,327,232 B (45.1 MB) ·
re-read ratio 0.6302 · steady-state 12.358 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 2,098,528 B. The 45.1 MB unique working set is the largest of
the wave so far — music/voice streaming for a rhythm game; a DC port streams the same
data from GD-ROM (and the DC original demonstrably did).

## 6. Guts (axis: 85.0)

Code 2,097,152 B (carve `base 0x8c020000`, entry `0x8c021000`, header title
"PUYOPUYO DA! IN JAPAN ----") · functions 2,777 · MMIO refs: scif 2, rtc 4, g2ext 132 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0 — `stick`)

Cabinet: standard Naomi 2P panel — **no dance pad**; gameplay uses 4 directional inputs +
1 action button (Simon-says prompts). MAME input ports: `naomi` (INPUT_PORTS_START at
naomi.cpp @59e7c0b line 1506 — digital stick + buttons, no analog).
Proposed DC mapping: d-pad + one face button, 1:1 — the DC original shipped with three
selectable pad layouts (Type A/B/C), so the mapping is not hypothetical but the game's
native design.
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Puyo Nexus](https://puyonexus.com/wiki/Puyo_Puyo_DA!);
[Time Extension](https://www.timeextension.com/news/2025/01/dreamcast-dance-rhythm-game-puyo-puyo-da-is-now-available-to-play-in-english).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 86.2^.40 · 68.4^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **77.1** (A)
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match no → 40.0.

## 9. Risks & notes

- **Porting is redundant**: the DC retail build is the original (shipped before the
  arcade cart) and a 2025 English fan patch modernizes it. Value of this assessment is
  as a calibration point: a genuinely DC-authored title measured through the Naomi
  battery scores 77.1 A with every region fitting — the pipeline agrees with ground truth.
- **Genre label**: our tables say Puzzle ★; the game is a rhythm/dance title. Kept as-is
  in QUEUE.md/GAME_FORMATS.md (the ★ lane logic — small 2D, pad-friendly — still applies).
- ARAM address peak 2.23× vs 4 B content above cap: strongest possible endorsement of the
  v7 volume re-key on a fresh title; belongs in the §6 item 1 discussion of whether the
  2× multiple itself still means anything under volume keying.
- Main RAM u=0.984 is close to cap — a port has ~262 KB of headroom before trimming, but
  zero above-cap content and the DC original prove it fits in practice.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.
