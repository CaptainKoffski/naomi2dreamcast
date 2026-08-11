# Quiz Aa! Megami-sama ~Tatakau Tsubasa to Tomoni~ (`qmegamis`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,314,361 B → utilization **3.488** — 12th-highest of the now 31-strong parked ARAM cohort (between `dybb99` 3.531 and `mazan` 3.483, which it edges by 10,850 B), the **23rd G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1). **Sole-blocker:** main content u **0.454** and VRAM fit u **0.575** both clear cap comfortably — only the sound bank is over, and this title carries the cohort's strongest unpark evidence: a **same-game official DC port** (WOW Entertainment/Sega, JP 2000-11-30) shipped inside the DC's 2 MiB AICA RAM. Joins the ARAM-sole-blocker unpark shortlist alongside `ausfache`/`monkeyba`/`wsbbgd` et al. — pending the kb §6 item 1 threshold ruling. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `qmegamis` (no clones — sole GAME row, MAME src/mame/sega/naomi.cpp @59e7c0b line 10975, `/* 0030 */`, machine `naomim1`) — carve title `"AH! MY GODDESS QUIZ GAME--"` |
| Maker / year | Sega, 2000 (MAME `GAME()` row; title screen © Fujishima Kosuke/Kodansha · © SEGA/Kodansha 2000 — `shot-243s.png`) |
| Genre / format | Quiz ⚠ (`GAME_FORMATS.md`) — licensed *Ah! My Goddess* trivia quiz, ~6000 Japanese questions — **cart** 60.0 MB, Naomi M1 |
| Official DC port | **Yes** — Quiz Aa! Megami-sama ~Tatakau Tsubasa to Tomoni~, Sega Dreamcast, WOW Entertainment/Sega, JP 2000-11-30 ([LaunchBox GamesDB 107860](https://gamesdb.launchbox-app.com/games/details/107860-quiz-aa-megami-sama-tatakau-tsubasa-to-tomoni)); `GAME_FORMATS.md` DC column "Yes (2000)" |
| Community ports | Moot — the official DC port exists; none additionally found (searched 2026-08-11) |
| Representative choice | Only set in the family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/qmegamis.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop cycles the full game vocabulary: press-start pentagram splash
(`shot-060s.png`), title (`shot-243s.png`), 3D goddess dialog scenes (`shot-304s.png`), story text
pages (`shot-365s.png`), and live quiz rounds — a question with four numbered answers and the 1P
cursor picking one (`shot-487s.png`), plus norma-clear/ranking interstitials in the uncurated frames.
Screenshots: `evidence/qmegamis/shot-060s.png` · `shot-243s.png` · `shot-304s.png` · `shot-365s.png`
· `shot-487s.png` (five of ten kept; the other five were more frames of the same quiz/ranking loop).
Anomalies: none — single leg, full 600 s window on the first attempt.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,314,361 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.488** — past `region_score()`'s `u > 2.0` gate, **12th-highest of the now
31-strong parked ARAM cohort** (between `dybb99` 3.531 and `mazan` 3.483, edging mazan by
10,850 B; cohort max `slashout` 3.756). This is the **23rd G3-aram park of the 2026-08-11
sweeps** (kb §6 item 1 tallied 17 in the non-⚠ sweep; `oinori` 18th, the four Derby
generations 19th–22nd, `qmegamis` extends the ⚠ tail). `nz_above_cap` = 5,325,213 B
(address-keyed placement figure, informational). Address peak 8,257,552 B (u 3.938; watermark
the full 8,388,608 B bank) — the same address-peak figure recorded for `mazan`/`sstrkfgt`/
`toyfight`, the known address-keyed ceiling artifact (kb "ARAM write-truth vs content"), and
consistent with a boot-time full-bank voice/BGM load: the cart's `sdk_strings` carry a
per-goddess voice-bank manifest (`BE_VOICE.BIN`…`KE_VOICE.BIN` — seven goddesses), BGM bank
list (`BGM_ADV*`/`BGM_GM*.BIN`), and a several-hundred-entry `SND_SEC_*`/`SND_SEB_*` cue table.

The other two regions, quoted from the sidecar — **sole-blocker: both fit**, putting `qmegamis`
on the cohort's ARAM-sole-blocker unpark shortlist (kb §6 item 1 — joining `ausfache`,
`radirgyn`, `mamonoro`, `mok`, `ninjaslt`, `tduno2`, `monkeyba`, `shaktamb`, `wsbbgd`):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 7,618,313 | 16,777,216 | **0.454** | `nz_total` — clears cap with 8.7 MiB headroom; `dma_high_water` 3,146,016 B (u 0.188) · `nz_above_cap` 1,998,154 B (address-keyed, informational) · address peak/watermark 32,550,804 B (u 1.940 — stale-data-prone scan, contradicted by the volume figures) |
| VRAM (content volume + 2×fb) | 4,820,119 | 8,388,608 | **0.575** | `content_total` 3,591,319 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — clears cap; raw `nz_total` 4,138,749 (u 0.493) · address peak 13,385,728 (u 1.596) |
| ARAM (content volume) | 7,314,361 | 2,097,152 | **3.488** | the gate — see above |

Streaming context: 4 DMA events · 1,152 B total · 288 B unique · re-read ratio 0.75 ·
steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 80,482,132 B — a PIO-front-loaded
M1 loader; effectively zero steady-state cart traffic.
Guts: carve 3,014,656 B (`carve_meta.title = "AH! MY GODDESS QUIZ GAME--"`) · 1,281 functions ·
MMIO refs rtc 4 / g2ext 36 / scif 8 · `serial_pokes` 0 · flags `eeprom_bios`/`serial`/`rtc`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (one line — does not gate, G3 fired first):** standard 2P quiz cabinet on the generic
Naomi panel — MAME wires plain `naomi` INPUT_PORTS (8-way stick + 6 buttons per player,
naomi.cpp @59e7c0b line 1506; GAME row line 10975; [ArcadeItalia ADB](https://adb.arcadeitalia.net/dettaglio_mame.php?game_name=qmegamis)
concurs: 2 players, 8-way, 6 buttons) — and play is four numbered answer buttons (the ①–④ answer
list with 1P cursor in `shot-487s.png`; the cart's own test-mode string drives `1P PUSH_1/2/3`),
mapping 1:1 to a DC pad's face buttons → **`pad_adaptable` recorded** in the sidecar; the
official DC port on a standard pad is the shipped proof.

**Japanese-text dependence (the ⚠ lane, one line):** this is an *Ah! My Goddess* licensed trivia
quiz — the game **is** ~6000 Japanese text questions plus story pages (`shot-487s.png`,
`shot-365s.png`), so any port is JP-literate-audience only; that inherent text wall, not
hardware, is why the family sat in the ⚠ lane.

**What would unblock it:** the kb §6 item 1 G3-ARAM threshold ruling (checkpoint decides with
full data). `qmegamis` is the shortlist's cleanest case: sole-blocker with the widest margins
(main 0.454 / VRAM 0.575) *and* a same-game official DC port — the 2000 DC SKU is shipped-product
proof the voice/BGM bank trims into 2 MiB AICA RAM (the `vonot`/`alienfnt` precedent class).
Under any softened ARAM rule it would score rather than park; the residual caveat is
audience (Japanese text), not hardware.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.488, 12th of 31-strong cohort (10,850 B above `mazan`), 23rd G3-aram park of the 2026-08-11 sweeps; **sole-blocker** (main 0.454, VRAM 0.575 both fit) with same-game official DC port (JP 2000-11-30) — joins the §6 item 1 unpark shortlist; coverage demo (full attract loop incl. live quiz rounds); `pad_adaptable` recorded (4 answer buttons), G3 fired first; clean single-leg full-window run |
