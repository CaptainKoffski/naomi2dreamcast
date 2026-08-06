# Musapey's Choco Marker (Rev A) (GDL-0014A) (`chocomk`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **52.5** (B) |
| Bottom line | Best newly-scored title of the DC-ported ★ batch: ARAM lands 16 bytes under the DC's 2 MiB cap and main-RAM DMA high-water is *exactly* 16 MiB — the content was authored to DC-shaped budgets (Ecole shipped the DC port the same year). The only over-budget axis, VRAM 1.61×, is mostly an artifact of framebuffer placement above the 8 MB line (see §4), so the true porting cost is likely lower than the score says. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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
gameplay with the デモプレイ/Demo banner; `shot-609s.png` title. Sidecar
`capture.coverage = "demo"`.
Screenshots: `assessments/evidence/chocomk/shot-060s.png`, `shot-304s.png`, `shot-609s.png` (curated from 10).
Anomalies: none — clean single-leg GD run, no flake, no display blindness.

## 4. Memory fit (axis: 25.6)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 16,777,216 | 16 MB | 1.00× | 85.0 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 13,496,860 | 8 MB | 1.61× | 25.6 | grep `VRAMPROFILE` |
| ARAM (content, fill-excluded) | 2,097,136 | 2 MB | 1.00× | 85.0 | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 18,533,794 /
vram 13,496,860 / aram 8,388,608. Main watermark 1.10× the DMA high-water — mild.

The region pattern echoes `tetkiwam`: **ARAM peaks at 2,097,136 B — 16 bytes under the
DC's 2 MiB cap, `nz_above_cap = 0`** — and main-RAM DMA lands at exactly 16,777,216 B.
Sound and main memory were authored inside DC budgets, consistent with the same-year
official DC port. The binding VRAM axis is largely **framebuffer placement, not texture
volume**: `regs_last` shows `fb_w_sof1=800000`, `fb_w_sof2=c00000` — both write
framebuffers sit at/above the 8 MB line, while render structures live below
(`isp_base=0`, `ol_base=3eb780`); accordingly 3,156,395 B of the 3,169,579 B total
nonzero VRAM content is "above cap". A port would simply place the FBs inside the 8 MB
budget. Score deliberately not hand-adjusted (campaign comparability); recorded as a §6
checkpoint calibration observation.

## 5. Cart streaming (axis: 76.5)

DMA events 1,526 · total 46.5 MB · unique 16.5 MB · re-read ratio 0.6459 ·
steady-state 3.700 MB/min (full window, `short_window: false`)

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

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 25.6^.40 · 76.5^.20 · 95.0^.20 · 100.0^.10 · 70.0^.10 = **52.5** (tier B)
Similarity inputs (sidecar): developer no, SDK overlap partial, loader match yes.
Prose note: as with tetkiwam, the shipped same-engine DC titles argue the real SDK
overlap is closer to full — checkpoint-worthy calibration observation.

## 9. Risks & notes

- **The VRAM axis likely overcounts this title** (§4): the 1.61× peak is dominated by
  framebuffers placed above the 8 MB line (`fb_w_sof1=0x800000`, `fb_w_sof2=0xc00000`),
  and nearly all above-cap nonzero content is those FBs. Actual texture+render content
  is ~3.2 MB. Not hand-adjusted; §6 checkpoint data point (FB-placement class, joins
  the main-high-water clustering note from tetkiwam).
- Main-RAM DMA high-water of exactly 16,777,216 B (1.00×) sits right on the cap —
  fits, but with zero headroom under the v1 "assets landed" semantics; the official DC
  port proves the working set fits in practice.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data
  above the last DMA'd asset (main watermark 1.10× high-water — mild here).
- A port project's first verification: diff the arcade GD content against the official
  DC release (same developer, same year) — asset-level reuse could make this the
  cheapest conversion in the scored list after `cleoftp`.
