# Zero Gunner 2 (`zerogu2`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 34.3 (C), unchanged** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v7 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> adopted to main 2026-08-09): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 7,071,568 B (content-u 0.421) replaces peak 15,859,776 B (u 0.945).
> Memory axis 11.5, binding region now **aram** (was memory 11.5). Verdict section below is the capture-time (v≤8) record.

## 1. Verdict

| | |
|---|---|
| **Final score** | **34.3 (C)** — un-parked 2026-08-07 (battery v7), right at the borderline; was `PARKED — G3 memory: aram peak > 2x DC capacity` under the old address-keyed rule |
| Bottom line | Clean full-window run. The §6 checkpoint re-keys G3-ARAM on content volume: `content_total` = 4,115,639 B (u = 1.962), landing just under the u>2.0 gate — a genuine borderline result, not a comfortable clearance. That leaves ARAM's sub-score floor-adjacent (11.5) and still binding the memory axis. Main RAM is write-truth-measured for the first time here too (this title skipped v6): peak 15,859,776 B (u = 0.9453, sub-score 89.1, not binding), vs. the old DMA high-water of 12,582,912 B (u = 0.75). VRAM (10,217,733 B, u = 1.22) reproduces bit-identically to v5. Final **34.3 (C)** — un-parked, but only just, and only just above the floor. The official 2001 DC port is shipped proof the audio *can* be re-authored to fit further; it remains the ready-made reference for what the rework looks like. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |

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

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/zerogu2.zip` (single clean zip leg)
Attract/demo reached: **demo** — `shot-060s.png` / `shot-609s.png` show the attract
gameplay demo (helicopter vs. stealth-bomber boss, PRESS START overlay), `shot-304s.png`
the title screen. Sidecar `capture.coverage = "demo"`.
Screenshots: `assessments/evidence/zerogu2/shot-060s.png`, `shot-304s.png`, `shot-609s.png` (curated from 10).
Anomalies: none — no flake, no display blindness.

## Gate

**No gate — un-parked 2026-08-07 (battery v7), right at the borderline: ARAM content volume u=1.962, just under the u>2.0 gate — memory axis floor-adjacent (11.5), final 34.3 (C).**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 15,859,776 | 16,777,216 | 0.9453 | sub-score 89.1, not binding; `dma_high_water` 12,582,912 (u=0.75, the old v5 scoring input) |
| VRAM (write-truth diff) | 10,217,733 | 8,388,608 | 1.22 | nz_total 3,108,110 · above cap 1,441,076; sub-score ~45.7 (bit-identical to v5) |
| ARAM (content volume, fill-excluded) | 4,115,639 | 2,097,152 | **1.962** | `content_total` (§6 volume-keyed, battery v7) — sub-score 11.5, floor-adjacent, the binding region, just under the u>2.0 gate; old content-high address peak 8,257,552 (u=3.94, pre-v7 keying, gated) unchanged, same 2,130,349 B above the 2 MB line either way |

Streaming (informational): 283 DMA events · total 111.8 MB · unique 22.1 MB ·
re-read 0.8021 · steady 10.586 MB/min (bit-identical to v5). The old doc's "Watermarks
(stale-data-prone): main 15,859,776" figure is no longer merely informational — it is
now the scored write-truth peak (main row above); vram/aram watermarks are unchanged.

Un-parked, but barely: ARAM's u=1.962 sits close enough to the u>2.0 gate that a small
run-to-run delta could tip it either way — this is the borderline case the wave's
expectations table flagged. What would still raise the score: the `azumanga` playbook —
ARAM bank-structure analysis (`tools/assess/parse_osb.py` on a `FLYCAST_ARAMDUMP`) to see
whether the above-cap content is position-independent OSB banks (rebuild + base move)
plus GD/cart-streamable BGM. Decisive shortcut available here that azumanga lacks:
**diff against the official DC port's audio** — Psikyo already solved the 2 MiB fit in
2001; matching sample banks would turn the rework from research into transcription.

## 7. Controls (axis: 100.0)

Cabinet: standard Naomi 8-way stick + 3 used buttons (shot · rotate-marker · special),
2 players. MAME input ports: `naomi`. Hold-rotate pivots the craft around a marker —
fully pad-mappable; the official DC port shipped on a stock pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=zerogu2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC guide](https://gamefaqs.gamespot.com/dreamcast/565354-zero-gunner-2/faqs/23479)
(shot / rotate / special, marker mechanic).
