# Giga Wing 2 (`gwing2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **78.6 (A)** — un-parked 2026-08-07 (battery v7); was `PARKED — G3 memory: aram peak > 2x DC capacity` under the old address-keyed rule |
| Bottom line | Clean full-window run. Under the old address-keyed G3 rule, ARAM *content high-water address* reached 7.98 MB (3.99× the DC's 2 MiB) — but the above-cap content **volume** was only 48,662–48,674 B, the smallest observed by far (zerogu2: 2.1 MB, azumanga: 1.7 MB). The §6 checkpoint re-keyed the gate on volume (2026-08-07): measured `content_total` = 2,021,207 B (u = 0.964, under the 2 MiB cap) — the title un-parks and scores **78.6 (A)**, memory axis 86.5 (main is the binding region at u=0.980, not aram). Official 2001 DC port exists regardless. |
| Assessed | 2026-08-06 · battery v5 · flycast `ebae3b513` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; gate re-run 2026-08-07 · battery v6 · flycast `65f9f7857` (main axis measured, tension 2 resolved — see § Gate); aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |

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

Boots: yes · handoff at 20.0 s (battery v6 unified `dma|pio` trigger; v5 measured 40.0 s
under the older ARAM/VRAM-DMA-only detector) · run 600 s · rom: `naomi/gwing2.zip`
(single clean zip leg)
Attract/demo reached: **title (conservative lower bound)** — the attract loop verifiably
cycles (title `shot-060s` → red title card → Capcom logo → ... → character-intro art
`shot-487s` → TAG SCORE RANKING `shot-609s`), but no sampled frame caught in-game demo
footage, so `capture.coverage = "title"` (restored 2026-08-07 from the v5 sidecar's
annotated value — the v6 sidecar's `capture.coverage` came back `null`).
Screenshots: `assessments/evidence/gwing2/shot-060s.png`, `shot-487s.png`, `shot-609s.png` (curated from 10).
Anomalies: `memory.main.dma_high_water = 0` despite 1,366 cart-DMA events — the
cart→main-RAM load path is PIO, invisible to the DMA high-water metric (kb §4.v family;
here the ARAM handoff still fired, so the run was measurable otherwise).
**Resolved 2026-08-07 (battery v6, flycast `65f9f7857`):** the unified `dma|pio` handoff
now baselines main RAM directly, so main-RAM fit is no longer blind — write-truth peak
measured at 16,433,920 B (u = 0.980), matching this doc's old "informational" watermark
byte-for-byte (real game writes all along; see § Gate). `pio_bytes` 57,520,864 B is the
first measured lower bound for the PIO-streamed traffic the streaming figures below
still don't count (non-main DMA only).

## Gate

**No gate — un-parked 2026-08-07 (battery v7): the §6 checkpoint re-keyed G3-ARAM on content volume, exactly as tension 1 below argued.**

| Region | Peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth diff) | 16,433,920 | 16,777,216 | 0.980 | nz_total 8,050,490 · above cap 0 |
| VRAM (write-truth diff) | 8,066,048 | 8,388,608 | 0.96 | nz_total 3,444,253 · above cap 0 |
| ARAM (content volume, fill-excluded) | 2,021,207 | 2,097,152 | **0.964** | `content_total` (§6 volume-keyed, battery v7) — under cap; old content-high **address** was 8,372,160 (u=3.99, pre-v7 keying), same 48,674 B sitting above the 2 MB line either way |

Streaming (informational, partial — non-main DMA only): 1,366 events · total 11.2 MB ·
unique 3.1 MB · re-read 0.7247 · steady 1.157 MB/min. PIO-streamed (main-RAM loader,
measured for the first time in battery v6): **57,520,864 B (57.5 MB)** over the window —
a lower bound for the traffic this doc's old "streaming figures cover only non-main DMA"
caveat left uncounted.

Two recorded tensions, no hand-adjustment (campaign comparability):
1. ~~**§6 checkpoint data point (G3-ARAM semantics), standing:** the gate keys on the
   content high-water *address* (`content_high`), which a single 47.5 KB blob near the
   top of ARAM maxes out. gwing2 is the divergent case the checkpoint needs: address
   says 3.99×, volume says 1.02× (2,097,152 + 48,662). If the checkpoint re-keys the
   gate on volume, gwing2 un-parks and scores with a near-perfect ARAM sub-score.
   Battery v6 re-run (2026-08-07, flycast `65f9f7857`) reproduces this same tiny-volume
   class: `nz_above_cap` = 48,674 B vs v5's 48,662 B — a 12 B run-to-run delta, same
   conclusion. Still open, still §6 scope.~~
   **RESOLVED 2026-08-07 (battery v7, flycast `65f9f7857`):** the §6 checkpoint re-keyed
   `score.py`'s G3-ARAM gate on content **volume** (`memory.aram.content_total`) instead
   of the content high-water address, exactly as this tension argued. Measured
   `content_total` = 2,021,207 B (u = 0.964, under the 2 MiB cap) — gwing2 un-parks and
   scores **78.6 (A)**; memory axis 86.5 is bound by main RAM (u=0.980), not aram
   (u=0.964, sub-score ≈87.7). This was the sole remaining park driver.
2. ~~**Main-RAM axis blind** on PIO-loading carts (this set, sgtetris): had the ARAM
   gate not fired, memory_axis would have scored main at u=0 → 100.0 from a metric that
   saw nothing. Flagged in kb §4.v.~~
   **RESOLVED 2026-08-07 (battery v6, flycast `65f9f7857`):** the unified `dma|pio`
   handoff now baselines main RAM directly. Main axis is measured for the first time —
   write-truth peak **16,433,920 B (u = 0.980)**, `nz_above_cap` **0**, `nz_total`
   8,050,490. That peak equals the v5 doc's old "informational" watermark byte-for-byte:
   those were real game writes all along, and gwing2's main RAM **fits the DC cap**. Had
   the ARAM gate not fired, main would now score ~86 as a real measurement instead of
   the old 100-from-nothing hazard — which the v6 scorer guard also closes by
   construction (`score.py`: an unmeasured main axis is dropped/renormalized and
   flagged `main_unmeasured`, never scored as u=0 → 100). See kb §4.v RESOLVED note
   (sgtetris is the sibling case, resolved the same way).

Both tensions are now closed: PIO instrumentation landed in battery v6 and closed
tension 2 (main-RAM axis blindness); the §6 checkpoint's volume-keying landed in battery
v7 and closed tension 1 (G3-ARAM address-vs-volume semantics). gwing2 is fully scored,
no gate remains.

## 7. Controls (research done, informational)

Cabinet: standard Naomi 8-way stick + 2 used buttons (shot · bomb), 2 players. MAME
input ports: `naomi`. Stock-pad trivial; the official DC port shipped A=shot / B=bomb
and added a dedicated autofire on R.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=gwing2)
(8-way joystick + 6-button JVS standard declaration, 2P);
[GameFAQs DC systems FAQ](https://gamefaqs.gamespot.com/dreamcast/479801-giga-wing-2/faqs/12525)
(A shot / B bomb / R autofire).
