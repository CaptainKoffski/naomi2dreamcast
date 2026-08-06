# Zero Gunner 2 (`zerogu2`) — portability assessment (parked)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Bottom line | Clean full-window run, but ARAM write-truth peaks at 7.87 MB with 2,130,349 B of genuine (non-fill) sound content above the DC's 2 MiB cap — 3.94× capacity, a real G3 like `azumanga`, not a fill artifact. The official 2001 DC port is shipped proof the audio *can* be re-authored to fit; the park ranks the arcade build as measured, and the DC port is the ready-made reference for what the rework looks like. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

**G3 `aram peak > 2x DC capacity` — genuine sound-content overflow.**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 12,582,912 | 16,777,216 | 0.75 | fits |
| VRAM (write-truth diff) | 10,217,733 | 8,388,608 | 1.22 | nz_total 3,108,110 · above cap 1,441,076 |
| ARAM (content, fill-excluded) | 8,257,552 | 2,097,152 | **3.94** | content above cap 2,130,349 |

Streaming (informational): 283 DMA events · total 111.8 MB · unique 22.1 MB ·
re-read 0.8021 · steady 10.586 MB/min. Watermarks (stale-data-prone): main
15,859,776 / vram 10,217,733 / aram 8,388,608 (ARAM watermark pinned at the full
8 MiB — the content counter, which excludes uniform fill runs, still finds 2.08 MiB
of real data above the cap, so this is not the DMPD-fill artifact class).

What would unblock: the `azumanga` playbook — ARAM bank-structure analysis
(`tools/assess/parse_osb.py` on a `FLYCAST_ARAMDUMP`) to see whether the above-cap
content is position-independent OSB banks (rebuild + base move) plus GD/cart-streamable
BGM. Decisive shortcut available here that azumanga lacks: **diff against the official
DC port's audio** — Psikyo already solved the 2 MiB fit in 2001; matching sample banks
would turn the rework from research into transcription.

## 7. Controls (research done, informational)

Cabinet: standard Naomi 8-way stick + 3 used buttons (shot · rotate-marker · special),
2 players. MAME input ports: `naomi`. Hold-rotate pivots the craft around a marker —
fully pad-mappable; the official DC port shipped on a stock pad.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=zerogu2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC guide](https://gamefaqs.gamespot.com/dreamcast/565354-zero-gunner-2/faqs/23479)
(shot / rotate / special, marker mechanic).
