# Musapey's Choco Marker (Rev A) (GDL-0014A) (`chocomk`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **90.5 (S)** |
| Bottom line | Best-scoring title of the DC-ported ★ batch: under current keys every region fits with room to spare — main content 0.55× cap, FB-masked VRAM 0.46×, ARAM 0.64× — consistent with content authored to DC-shaped budgets (Ecole shipped the official DC port the same year); the residual porting cost is main's sparse layout, whose write-truth address peak still reaches 1.11× cap. |
| Assessed | capture 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

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

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/chocomk.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-060s.png` and `shot-304s.png` are live attract
gameplay with the デモプレイ/Demo banner; `shot-182s.png` and `shot-548s.png` are the
"回転" (rotate) tutorial cards, also part of the demo loop. Sidecar
`capture.coverage = "demo"`.
Screenshots: `evidence/chocomk/shot-060s.png` · `evidence/chocomk/shot-182s.png` ·
`evidence/chocomk/shot-304s.png` · `evidence/chocomk/shot-548s.png` (curated from 10;
`shot-609s.png` caught the loop's blank transition frame and was dropped).
Anomalies: none — clean single-leg GD run, no flake, no display blindness.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,254,982 | 16,777,216 | 0.5517 | 100.0 | address peak 18,533,794 (u 1.105) · 1,420,913 nonzero above cap · `dma_high_water` exactly 16,777,216 (informational floor) |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 3,860,342 | 8,388,608 | 0.4602 | 100.0 | content_total 2,631,542 + 2×fb_bytes 1,228,800 (`fb_bytes` 614,400, exactly 640×480×2) · address peak 13,496,860 (u 1.609) is FB placement above the 8 MB line (`fb_w_sof1=800000`, `fb_w_sof2=c00000`), excluded by construction since v8 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,332,513 | 2,097,152 | 0.6354 | 100.0 | address peak 2,097,136 — 16 B under the DC cap · 0 above cap |

All three sub-scores are 100.0 — nothing binds.
Watermarks (informational, content-scan — stale-data prone): main 18,533,794 ·
vram 13,496,860 · aram 8,388,608 (boot-time fill, not content). The main watermark
equals the write-truth address peak — real game writes, not stale data (same pattern
as `gwing2`'s v6 re-run).

## 5. Cart streaming (axis: 76.5)

DMA events 1,526 · total 46.5 MB · unique 16.5 MB · re-read ratio 0.6459 ·
steady-state 3.705 MB/min (`short_window: false`) · PIO 1,574,212 B

## 6. Guts (axis: 95.0)

Code 1,572,864 B · functions 588 · MMIO refs: scif 0, rtc 0, g2ext 5 ·
BIOS vector refs: none (`extra_bios_classes: 0`) · flags: `eeprom_bios` → 95.0.
Carve header title: `CHOCO MARKER` (base `0x0c020000`, entry `0x0c021000`).
`guts.sdk_strings` names Ecole's own stack — including **`D e a t h  C r i m s o n  OX`
/ "Presented by ECOLE"**: engine kinship with Death Crimson OX, a shipped Dreamcast
title — plus Ninja/Nindows, CRI ADX/Sofdec, the JAPAN-only arcade notice and
"Lib Handle Start".

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
      = 100.0^.40 · 76.5^.20 · 95.0^.20 · 100.0^.10 · 70.0^.10 = **90.5 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes.
Prose note: as with tetkiwam, the shipped same-engine DC titles argue the real SDK
overlap is closer to full — checkpoint-worthy calibration observation.

## 9. Risks & notes

- **Main layout is the residual cost:** content volume fits easily (9.25 MB) but the
  write-truth address peak is 18,533,794 B (1.105× cap) with 1,420,913 B of real
  nonzero data above the 16 MB line — a port needs relocation for those high-address
  writes, not asset cuts. (The old DMA-high-water metric — exactly 16,777,216 B —
  could not see this; the v6 write-truth instrumentation closed that gap.)
- ARAM address peak 2,097,136 B — 16 bytes under the DC's 2 MiB cap, 0 above cap —
  echoes `tetkiwam`: sound and main memory were authored inside DC budgets,
  consistent with the same-year official DC port.
- A port project's first verification: diff the arcade GD content against the official
  DC release (same developer, same year) — asset-level reuse could make this the
  cheapest conversion in the scored list after `cleoftp`.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v5 | 2026-08-06 | 52.5 (B) | Baseline capture (flycast `ebae3b513`): VRAM address high-water 13,496,860 (u 1.61 — framebuffers placed above the 8 MB line) bound memory at 25.6; FB-placement artifact filed as a §6 checkpoint calibration observation (kb §6) |
| v8 | 2026-08-07 | 76.7 (A) | Re-capture catching up three §6 rulings at once: main write-truth (v6), ARAM content volume (v7), VRAM FB-masked content + 2×FB (v8 — chocomk was the wave's motivating case, spec `2026-08-07-vram-fb-masking-design.md`); write-truth main (u 1.105) became binding at 66.2 |
| v9 | 2026-08-08 | 90.5 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory axis 100.0 |
