# Giga Wing 2 (`gwing2`) — portability assessment (parked)

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram peak > 2x DC capacity`** |
| Bottom line | Clean full-window run, gated because ARAM *content high-water address* reaches 7.98 MB (3.99× the DC's 2 MiB). But the above-cap content **volume** is only 48,662 B — the smallest observed by far (zerogu2: 2.1 MB, azumanga: 1.7 MB): relocating ~47.5 KB is trivial, so this park is a scoring-semantics artifact candidate, recorded for the §6 checkpoint (address vs. volume in the G3-ARAM rule). Official 2001 DC port exists regardless. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `gwing2` (no clones — `parent: null` in controls.json) |
| Maker / year | Takumi / Capcom, 2000 (controls.json) |
| Genre / format | Shmup ★ (vertical shooter, score/reflect system), cart (`naomim2`, 57.6 MB) |
| Official DC port | **Yes — Giga Wing 2 (Dreamcast, 2001, Capcom — JP+NA release)** ([shmups.wiki](https://shmups.wiki/library/Giga_Wing_2), [GameFAQs](https://gamefaqs.gamespot.com/dreamcast/479801-giga-wing-2)). Assessed as reference/validation data per GAME_FORMATS.md policy. |
| Community ports | Moot — official DC port exists. |
| Representative choice | Only member of its family (MAME parent, no clones). |

## 3. Boot & run evidence

Boots: yes · handoff at 40.0 s · run 600 s · rom: `naomi/gwing2.zip` (single clean zip leg)
Attract/demo reached: **title (conservative lower bound)** — the attract loop verifiably
cycles (title `shot-060s` → Capcom logo → red title card → character-intro art
`shot-487s` → TAG SCORE RANKING `shot-600s`), but no sampled frame caught in-game demo
footage, so `capture.coverage = "title"`.
Screenshots: `assessments/evidence/gwing2/shot-060s.png`, `shot-487s.png`, `shot-600s.png` (curated from 10).
Anomalies: `memory.main.dma_high_water = 0` despite 1,344 cart-DMA events — the
cart→main-RAM load path is PIO, invisible to the DMA high-water metric (kb §4.v family;
here the ARAM handoff still fired, so the run was measurable otherwise). Main-RAM fit is
therefore **unmeasured** (watermark 16,433,920 B is the only, stale-prone, indicator);
streaming figures cover only the non-main DMA traffic.

## Gate

**G3 `aram peak > 2x DC capacity` — fired on content high-water address; volume above cap is tiny.**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 0 (blind — PIO loader) | 16,777,216 | n/a | watermark 16,433,920 (informational) |
| VRAM (write-truth diff) | 8,066,048 | 8,388,608 | 0.96 | nz_total 3,580,906 · above cap 0 |
| ARAM (content, fill-excluded) | 8,372,160 | 2,097,152 | **3.99** | content above cap **48,662 B only** |

Streaming (informational, partial — non-main DMA only): 1,344 events · total 11.0 MB ·
unique 3.1 MB · re-read 0.7202 · steady 1.155 MB/min.

Two recorded tensions, no hand-adjustment (campaign comparability):
1. **§6 checkpoint data point (G3-ARAM semantics):** the gate keys on the content
   high-water *address* (`content_high`), which a single 47.5 KB blob near the top of
   ARAM maxes out. gwing2 is the divergent case the checkpoint needs: address says
   3.99×, volume says 1.02× (2,097,152 + 48,662). If the checkpoint re-keys the gate on
   volume, gwing2 un-parks and scores with a near-perfect ARAM sub-score.
2. **Main-RAM axis blind** on PIO-loading carts (this set, sgtetris): had the ARAM gate
   not fired, memory_axis would have scored main at u=0 → 100.0 from a metric that saw
   nothing. Flagged in kb §4.v.

What would unblock: the §6 checkpoint decision on address-vs-volume G3 keying (data
argues volume here); independently, PIO-read instrumentation to un-blind main RAM.

## 7. Controls (research done, informational)

Cabinet: standard Naomi 8-way stick + 2 used buttons (shot · bomb), 2 players. MAME
input ports: `naomi`. Stock-pad trivial; the official DC port shipped A=shot / B=bomb
and added a dedicated autofire on R.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=gwing2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC systems FAQ](https://gamefaqs.gamespot.com/dreamcast/479801-giga-wing-2/faqs/12525)
(A shot / B bomb / R autofire).
