# Karous (Japan) (GDL-0040) (`karous`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **85.0 (S)** |
| Bottom line | Milestone shipped this exact game on DC on 2007-03-08 — the last officially licensed Dreamcast release — and under content keying the measurement now agrees with that ground truth: every region fits (main content 0.40× cap, VRAM fit 0.66×, ARAM 0.74×), so the assessment's value is scorer calibration, not a port target. |
| Assessed | capture 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `karous` (no clones — single GAME line, MAME naomi.cpp @59e7c0b line 11288; ROM_START 8959, ships `karous-default-eeprom.bin` line 8964) |
| Maker / year | Milestone, 2006 (JP arcade debut 2006-11-15) |
| Genre / format | Shmup ★ (vertical, ROT270), **GD-ROM** GDL-0040, machine `naomigd` |
| Official DC port | **Yes** — JP 2007-03-08, published by MileStone Inc.: **the last officially licensed Dreamcast release**, with proper TATE and VGA ([Wikipedia](https://en.wikipedia.org/wiki/Karous), [Shmups Wiki](https://shmups.wiki/library/Karous), [1CC Log](http://1cclog.blogspot.com/2015/09/karous-dreamcast.html)). Wii: *MileStone Shooting Collection* 2008 (NA *Ultimate Shooting Collection* 2009); the DC build is being re-released on Steam/modern platforms ([Time Extension, Dec 2025](https://www.timeextension.com/news/2025/12/the-last-officially-released-sega-dreamcast-game-is-coming-to-steam-next-year)) |
| Community ports | No Naomi→DC conversion found (searched 2026-08-08) — moot: the official DC build is canonical. Scene work targets it instead: English translation ([dreamcast-talk t=11839](https://www.dreamcast-talk.com/forum/viewtopic.php?t=11839), [SEGASKY itch.io](https://segasky.itch.io/karous-eng-translation)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/karous.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle across the 10 shots: story text cards ("神の血") → per-mode RANKING pages with character art → live demo gameplay (boss fight, EXP/Level HUD) → sky cinematic → ADX logo card → title (カラス feather art).
Screenshots kept (5 of 10):
- `assessments/evidence/karous/shot-060s.png` — story text card: 神の血 ("blood of god") intro lore
- `assessments/evidence/karous/shot-121s.png` — RANKING (EASY MODE) with full-screen character art
- `assessments/evidence/karous/shot-243s.png` — attract gameplay: boss fight, EXP 12,313,180, Level 101, shield HUD
- `assessments/evidence/karous/shot-304s.png` — story cinematic: photographic sky band with narration
- `assessments/evidence/karous/shot-609s.png` — title: カラス / Karous feather art, RANK NORMAL / EXTEND table
Anomalies: none.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 6,738,574 | 16,777,216 | 0.402 | 100.0 | address peak 32,505,920 (`0x1F00040`, u 1.938, informational) — **fifth instance of the kb §6 item 3 shared-structure signature** · `nz_above_cap` 5,092,992 B of real changed content above the 16 MB line — the shipped DC port trimmed/restructured ~5 MB · `dma_high_water` 27,289,280 (byte-identical to illvelo's v4 figure — same-engine determinism) |
| VRAM (FB-masked content + 2×FB) | 5,577,788 (content_total 4,348,988 + 2×`fb_bytes` 614,400) | 8,388,608 | 0.665 | 100.0 | raw address peak 13,778,944 (u 1.643) is extent — 4,933,719 of 4,944,963 nonzero bytes above the 8 MB line (high asset store, kurucham pattern) |
| ARAM (content volume, fill-excluded, `content_total`) | 1,545,306 | 2,097,152 | 0.737 | 100.0 | address peak 2,097,136 — 16 B under the cap, **fits even address-keyed**; matches illvelo's v4 ARAM peak exactly (the Milestone engine loads a just-under-2-MiB sound budget, DC-sized by construction) |

Watermarks (informational, content-scan — stale-data prone): main 32,505,920 ·
vram 13,778,944 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 62.4)

DMA events 2,802 · total 150,843,392 B (143.9 MB) · unique 34,498,560 B (32.9 MB) ·
re-read ratio 0.7713 · steady-state 14.287 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 2,098,496 B. Near-clone of sibling illvelo's profile
(163.3 MB / 37.3 MB / 0.7715 / 16.06 MB/min) — same engine, same small-working-set
re-read loop kb §6 item 2 flags as cache-friendly rather than disqualifying.

## 6. Guts (axis: 85.0)

Code 2,097,152 B (carve `base 0x8c020000`, entry `0x8c021000`, header title
"KAROUS JAPAN VERSION") · functions 3,181 · MMIO refs: scif 2, rtc 3, g2ext 126 ·
BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0 — `stick`)

Cabinet: standard Naomi 2P panel, 8-way stick + 3 buttons — A = Shot, B = Sword,
C = D.F.S. (full-gauge bomb); shield is passive when not firing. MAME input ports:
`naomi` (INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506).
Proposed DC mapping: d-pad + 3 face buttons, 1:1 — as the official DC port shipped
(configurable shot/sword/DFS).
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[Shmups Wiki](https://shmups.wiki/library/Karous);
[1CC Log DC review](http://1cclog.blogspot.com/2015/09/karous-dreamcast.html).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 62.4^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **85.0 (S)**
Similarity inputs: developer match no (reference `makers` list artifact — Milestone's
own DC pedigree isn't in it, same note as the illvelo doc), SDK overlap **partial**,
cart loader match **yes** → 70.0.

## 9. Risks & notes

- **Porting is redundant**: the official 2007 DC GD-ROM (TATE, VGA) is canonical, has an
  English fan translation, and is being re-released commercially. Assessment value is
  calibration, not a port target.
- **Ground-truth calibration row**: the officially DC-shipped game now scores S under
  v9 content keying — the keying agrees with reality. The durable caveats are the
  5,092,992 B of real above-cap main content the actual downport had to
  trim/restructure, and the 1.94× `0x1F00040` address peak a port must relocate.
- ROT270 vertical — solved in the official port.
- Milestone engine family (Radirgy `radirgy`/`radirgyn`, Illvelo `illvelo`): metrics here
  reproduce illvelo's byte-for-byte on two axes (dma_high_water, ARAM peak) — useful
  determinism check for the instrumentation.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v8 | 2026-08-08 | 37.0 (C) | First assessment: main bound at sub 12.5 on the 32,505,920 B `0x1F00040` address peak — fifth instance of the kb §6 item 3 signature; flagged as the campaign's cleanest gate-calibration case after ikaruga (spec `2026-08-07-vram-fb-masking-design.md` keying) |
| v9 | 2026-08-08 | 85.0 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); memory 100.0 |
