# Quiz Keitai Q mode (GDL-0017) (`quizqgd`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 4,803,898 B → utilization **2.291** — **31st of the now 32-strong parked ARAM cohort** (below `tduno2` 2.615, above only cohort-floor `toyfight` 2.035), the **24th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1). **Sole-blocker:** main content u **0.592** and VRAM fit u **0.826** both clear cap — only the sound bank is over, and by the cohort's second-smallest margin: just 609,594 B of content above the u = 2.0 line. Sibling ⚠-lane quiz title `qmegamis` parked tonight the same way (u 3.488, sole-blocker, same-game DC-port precedent — commit e679245); `quizqgd` is far closer to the gate line and, as a GD-ROM title, has a streaming path the cart sibling never had. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `quizqgd` (no clones — sole GAME row, MAME src/mame/sega/naomi.cpp @59e7c0b line 11254, `/* 0017 */`, machine `naomigd`, ROT270) — carve title `"Q-MODE VER.1.003"` |
| Maker / year | Amedio (Taito license), 2002 (MAME `GAME()` row; title screen © AMEDIO 2002 · © DORASU 2002 — `shot-304s.png`) |
| Genre / format | Quiz ⚠ (`GAME_FORMATS.md`) — mobile-phone-themed Japanese trivia/dating quiz (subtitle "〜MailもChatも恋して!〜"; the whole UI is a keitai handset frame) — **GD-ROM** 126.4 MB, GDL-0017 |
| Official DC port | No — none found (searched 2026-08-11) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Only set in the family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/quizqgd.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop cycles the game's keitai-frame vocabulary on its ROT270
vertical raster: phone-status-bar vignettes with mail-text panels (`shot-060s.png`,
`shot-182s.png`), dialog-balloon story scenes (`shot-121s.png`), per-character intro cards
(`shot-609s.png`, "スポーティ"), and the four-girl title screen with © AMEDIO 2002 / © DORASU
2002 and FREE PLAY (`shot-304s.png`).
Screenshots: `evidence/quizqgd/shot-060s.png` · `shot-121s.png` · `shot-182s.png` ·
`shot-304s.png` · `shot-609s.png` (five of ten kept; the other five were more frames of the
same title/vignette loop).
Anomalies: leg 1 hit the emulator-exited flake; the automatic retry leg ran the full 600 s
window cleanly — all metrics come from the retry.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 4,803,898 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **2.291** — past `region_score()`'s `u > 2.0` gate, but only just: **609,594 B of
content above the 2× line**, the cohort's second-smallest overage. That places it **31st of
the now 32-strong parked ARAM cohort** (680,772 B below `tduno2` 2.615; 536,069 B above
cohort-floor `toyfight` 2.035; cohort max `slashout` 3.756) and makes it the **24th G3-aram
park of the 2026-08-11 sweeps** (`qmegamis` was the 23rd). `nz_above_cap` = 2,941,699 B
(address-keyed placement figure, informational). Write-truth address peak 8,323,024 B
(u 3.969; watermark the full 8,388,608 B bank — DMPD-fill-prone content scan, kb "ARAM
write-truth vs content"). The 4.8 MB of real content is consistent with per-character voice
banks plus BGM: the cart's sound-test strings drive per-gal voice cues (`VOICE GAL` /
`VOICE TYPE` / `VOICE MONTH` / `VOICE NO`) across the four-girl cast the title screen shows
(`CHINATSU`/`AKIHA`/`MIFUYU`/`HARUKA`, `USE CHAR` menu string).

The other two regions, quoted from the sidecar — **sole-blocker: both fit**:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 9,925,936 | 16,777,216 | **0.592** | `nz_total` — clears cap with 6.5 MiB headroom; `dma_high_water` = write-truth peak = 30,248,960 B (u 1.803 — GD DIMM placement artifact, address not volume) · `nz_above_cap` 8,084,774 B (address-keyed relocation work, informational) |
| VRAM (content volume + 2×fb) | 6,925,069 | 8,388,608 | **0.826** | `content_total` 5,696,269 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — clears cap; raw `nz_total` 5,908,602 (u 0.704) · address peak 15,804,416 (u 1.884) |
| ARAM (content volume) | 4,803,898 | 2,097,152 | **2.291** | the gate — see above |

Streaming context: 353 DMA events · 56.5 MB total · 26.2 MB unique · re-read ratio 0.5355 ·
steady-state 3.931 MB/min (`short_window: false`) · `pio_bytes` 4,200,064 B — light steady
GD streaming, trivially within a DC GD-ROM drive's ability.
Guts: carve 4,194,304 B (`carve_meta.title = "Q-MODE VER.1.003"`) · 929 functions ·
MMIO refs rtc 2 / g2ext 45 / scif 2 · `serial_pokes` 0 · flags
`eeprom_bios`/`serial`/`rtc`/`network`.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: true`.

**Controls (one line — does not gate, G3 fired first):** mobile-phone-themed quiz cabinet on
the generic Naomi 2P panel — MAME wires plain `naomi` INPUT_PORTS (8-way stick + 6 buttons,
naomi.cpp @59e7c0b line 1506; GAME row line 11254, ROT270;
[ArcadeItalia ADB](https://adb.arcadeitalia.net/dettaglio_mame.php?game_name=quizqgd)
concurs: 2 players, 8-way, 6 buttons, vertical) — and the cart's own GAME ASSIGNMENTS menu
drives four `ANSWER1`–`ANSWER4` buttons plus a `USE JOY STICK` toggle (sidecar
`sdk_strings`), mapping 1:1 onto a DC pad's face buttons → **`pad_adaptable` recorded** in
the sidecar (the `qmegamis` four-answer-button precedent).

**Japanese-text dependence (the ⚠ lane, one line):** the game **is** Japanese trivia wrapped
in a keitai mail/chat frame — questions, mail panels and dialog are all Japanese text
(`shot-060s.png`, `shot-121s.png`), so any port is JP-literate-audience only; that inherent
text wall, not hardware, is why the family sat in the ⚠ lane.

**What would unblock it:** the kb §6 item 1 G3-ARAM threshold ruling (checkpoint decides
with full data). `quizqgd` is the cohort's second-nearest miss — 609,594 B of content over
the 2× line — so under any softened ARAM rule it scores rather than parks. For a literal
2 MiB AICA fit, ~2.7 MB of voice/BGM must trim or stream; sibling quiz `qmegamis` carries
the genre's shipped-product proof that quiz voice banks trim into AICA RAM (its 2000 DC SKU,
commit e679245), and `quizqgd`'s GD-ROM format adds a voice-streaming path the cart sibling
never had. The residual caveat is audience (Japanese text), not hardware.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 2.291, 31st of 32-strong cohort (only 609,594 B over the 2× line, second-nearest miss after `toyfight`), 24th G3-aram park of the 2026-08-11 sweeps; **sole-blocker** (main 0.592, VRAM 0.826 both fit) — sibling quiz `qmegamis` parked tonight u 3.488 with same-game DC-port precedent (e679245); coverage demo (keitai attract loop + title); `pad_adaptable` recorded (4 answer buttons + joystick toggle), G3 fired first; leg-1 emulator-exited flake, retry ran the full 600 s window |
