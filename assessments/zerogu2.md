# Zero Gunner 2 (`zerogu2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **34.3 (C)** |
| Bottom line | ARAM binds: content volume 4,115,639 B (u 1.962) sits just under the u>2.0 gate — sub-score 11.5, floor-adjacent, a genuine borderline result — while main content (0.42×) fits and VRAM, now measured directly (content_total + 2×fb_bytes, u 0.472) instead of falling back to the raw address peak, fits comfortably too; the official 2001 DC port is shipped proof the audio can be re-authored to fit, and the ready-made reference for what that rework looks like. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `zerogu2` (no clones — `parent: null` in controls.json) |
| Maker / year | Psikyo, 2001 (controls.json) |
| Genre / format | Shmup ★ (multi-directional helicopter shooter), cart (`naomim2`, 46.6 MB) |
| Official DC port | **Yes — Zero Gunner 2 (Dreamcast, Japan, 2001, Psikyo)** ([Wikipedia](https://en.wikipedia.org/wiki/Zero_Gunner), [Dreamcast Junkyard](https://www.thedreamcastjunkyard.co.uk/2018/01/a-quick-look-at-zero-gunner-2-dreamcast.html)); modern re-release *Zero Gunner 2-* (Zerodiv, Switch/PS4). Assessed as reference/validation data per GAME_FORMATS.md policy. |
| Community ports | Moot — official DC port exists. |
| Representative choice | Only member of its family (MAME parent, no clones). |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/zerogu2.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-060s.png` shows the opening attract cutscene
(helicopter vs. flying-wing bomber, PRESS START overlay), `shot-182s.png` the RANKING
high-score cycle, `shot-243s.png` in-game HUD during the scripted attract playthrough
(score/weapon icons, enemies, PRESS START overlay), `shot-304s.png` the title screen
("ZERO GUNNER 2"), `shot-609s.png` a later attract cutscene near the end of the 600 s
capture. Sidecar `capture.coverage = "demo"` (set this pass — battery wrote `null`).
Screenshots: `evidence/zerogu2/shot-060s.png` · `evidence/zerogu2/shot-182s.png` ·
`evidence/zerogu2/shot-243s.png` · `evidence/zerogu2/shot-304s.png` ·
`evidence/zerogu2/shot-609s.png` (curated from 10)
Anomalies: none — no flake, no display blindness.

## 4. Memory fit (axis: 11.5)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 7,071,568 | 16,777,216 | 0.4215 | 100.0 | address peak 15,859,776 (u 0.9453 — fits even address-keyed) · `nz_above_cap` 0 · `dma_high_water` 12,582,912 (the old v5 scoring input, informational) |
| VRAM (FB-masked content fit, `content_total + 2×fb_bytes`) | 3,954,850 | 8,388,608 | 0.4715 | 100.0 | `content_total` 2,726,050 + 2×`fb_bytes` 614,400 (dual-framebuffer budget) — **now measured**, not the v7 fallback; fits comfortably · nz_total 3,137,828 · `nz_above_cap` 1,441,076 (informational, address-keyed relic — textures are TA-relative per the v8 ruling, so position doesn't matter) · raw address peak 10,217,733 (u 1.218 — the v7 fallback that under-scored this region 45.8) |
| ARAM (content volume, fill-excluded, `content_total`) | 4,115,639 | 2,097,152 | 1.962 | 11.5 | **binding region**, floor-adjacent, just under the u>2.0 gate · address peak 8,257,552 (u 3.94 — the pre-v7 keying that gated the title) · `nz_above_cap` 2,130,349 either way |

Watermarks (informational, content-scan — stale-data prone): main 15,859,776 ·
vram 10,217,733 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 66.6)

DMA events 283 · total 111.8 MB · unique 22.1 MB · re-read ratio 0.8021 ·
steady-state 10.586 MB/min (`short_window: false`, bit-identical to v5) ·
PIO 4,053,408 B

## 6. Guts (axis: 85.0)

Code 3,036,256 B (carve `base 0x0c020000`, entry `0x0c021000`, 4 entries, header title
"ZERO GUNNER 2") · functions 1,950 · MMIO refs: scif 2, rtc 4, g2ext 53 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.
SDK strings: NAOMI LIBRARY Ver 0.9 AM R&D, NLOBJPUT 0.99, NLSPRITE 0.2, libsnd 1.03b,
KAMUI2 (Jul 1999 build) — the older AM R&D Naomi library stack, not the Katana-derived
Kunoichi/gdCi loader family (loader match no).

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 3 used buttons (shot · rotate-marker · special),
2 players. `controls.device_class = stick`. MAME input ports: `naomi`. Hold-rotate
pivots the craft around a marker — fully pad-mappable; the official DC port shipped on
a stock pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=zerogu2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC guide](https://gamefaqs.gamespot.com/dreamcast/565354-zero-gunner-2/faqs/23479)
(shot / rotate / special, marker mechanic).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 11.5^.40 · 66.6^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **34.3 (C)**
Similarity inputs: developer match no, SDK overlap partial, cart loader match no → 40.0.

## 9. Risks & notes

- **ARAM is a genuine borderline**: u 1.962 sits close enough to the u>2.0 gate that a
  small run-to-run delta could tip it either way — the borderline case the wave's
  expectations table flagged.
- **What would raise the score**: the `azumanga` playbook — ARAM bank-structure analysis
  (`tools/assess/parse_osb.py` on a `FLYCAST_ARAMDUMP`) to see whether the above-cap
  content is position-independent OSB banks (rebuild + base move) plus GD/cart-streamable
  BGM. Decisive shortcut available here that azumanga lacks: **diff against the official
  DC port's audio** — Psikyo already solved the 2 MiB fit in 2001; matching sample banks
  would turn the rework from research into transcription.
- VRAM is no longer a concern: v9's fresh capture carries the `content_total`/`fb_bytes`
  fields v7 lacked, so scoring now measures the FB-masked fit (u 0.472, sub-score 100.0)
  instead of falling back to the raw address peak (u 1.218, which had under-scored this
  region 45.8 in v7). The address-keyed `nz_above_cap` (1,441,076 B) is a relic of that
  old keying, not a live risk — textures are TA-relative (v8 ruling), so placement doesn't
  matter, only content volume does, and that volume fits.
- Main-RAM write-truth includes CPU writes (v6+ metric, first measured here at v7);
  `dma_high_water` is informational-only.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v5 | 2026-08-06 | PARKED G3-ARAM | ARAM address peak 8,257,552 B (u 3.94) tripped the memory gate under address keying; capture itself clean (flycast `ebae3b513`, coverage demo) — kb §6 |
| v7 | 2026-08-07 | 34.3 (C) | Un-parked: ARAM re-keyed on content volume (u 1.962, just under the u>2.0 gate); main write-truth measured for the first time (title skipped v6) — spec `2026-08-07-aram-gate-volume-design.md`, kb §6 |
| v9 | 2026-08-08 | 34.3 (C) | Scoring-only re-key (no re-capture): main keyed on content volume `nz_total` 7,071,568 B (u 0.421) — ARAM still binding, final unchanged — spec `2026-08-08-main-content-rekey-design.md` |
| v9 | 2026-08-09 | 34.3 (C) | ranking-groom chunk 5: fresh v9 capture (was v7) — VRAM sub-score moved from the v7 address-peak fallback (u 1.218, 45.8) to the measured FB-masked fit (`content_total` + 2×`fb_bytes`, u 0.472, 100.0); every shared raw counter (main/ARAM/streaming/PIO/handoff) reproduced byte-identical to v7; ARAM still binds (u 1.962), final unchanged |
