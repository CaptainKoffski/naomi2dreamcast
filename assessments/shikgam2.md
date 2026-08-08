# Shikigami no Shiro II / The Castle of Shikigami II (GDL-0021) (`shikgam2`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 87.7 (S), was 35.4 (C)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> EXPERIMENT branch `experiment/v9-main-content`): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 7,549,942 B (content-u 0.450) replaces peak 33,538,112 B (u 1.999).
> Memory axis 97.3, binding region now **aram** (was memory 10.0). Verdict section below is the capture-time (v≤8) record.

## 1. Verdict

| | |
|---|---|
| **Final score** | **35.4** (C) |
| Bottom line | Boots and demos cleanly; ARAM fits the DC cap even address-keyed and VRAM fits under v8 masking — but the memory axis bottoms out at 10.0 on the main-RAM address peak: u=1.99903, **16,320 bytes under the G3 park line** (`0x1FFC040` vs `0x2000000`), the gunsur2 near-miss class, charged against only 213 KB of real above-cap content. Alfa System's own 2004 DC port (TATE, Extreme mode) is shipped proof the game fits 16 MB after a real downport. |
| Assessed | 2026-08-08 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `shikgam2` (no clones — single GAME line, MAME naomi.cpp @59e7c0b line 11259; ROM_START 8615, ships `shikgam2-default-eeprom.bin` line 8620) |
| Maker / year | Alfa System, 2003 (cabinet distribution by Taito) |
| Genre / format | Shmup ★ (vertical, ROT270), **GD-ROM** GDL-0021, machine `naomigd` |
| Official DC port | **Yes** — JP 2004-03-25, developed/published by Alfa System; **TATE confirmed** plus DC-exclusive Extreme mode ([Wikipedia](https://en.wikipedia.org/wiki/Castle_Shikigami_2), [1CC Log](http://1cclog.blogspot.com/2014/02/shikigami-no-shiro-ii-dreamcast.html), [GameFAQs](https://gamefaqs.gamespot.com/dreamcast/919619-shikigami-no-shiro-ii)). Also GC 2003, PS2 2004 (the only export release of the era), Xbox 2004, PC 2004/2021 Steam, Switch 2023 |
| Community ports | No Naomi→DC conversion found (searched 2026-08-08) — moot given the official port; the only DC scene activity is running the official GDI on GDEMU ([dreamcast-talk t=13300](https://www.dreamcast-talk.com/forum/viewtopic.php?t=13300)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger=pio`) · run 600 s · rom: `naomi/shikgam2.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; attract cycle across the 10 shots: live demo gameplay (city stage, rock-garden stage, temple game-over) → score-ranking pages → DEMONSTRATION overlay → title.
Screenshots kept (5 of 10):
- `assessments/evidence/shikgam2/shot-060s.png` — attract gameplay: character over 3D city, alfasystem.net URL overlay
- `assessments/evidence/shikgam2/shot-243s.png` — TOTAL RANKING page (NORMAL), character portraits
- `assessments/evidence/shikgam2/shot-426s.png` — DEMONSTRATION overlay over highway stage scenery
- `assessments/evidence/shikgam2/shot-548s.png` — title: 式神の城 II logo, ©2001,2003 AlfaSystem, settings footer (GAME RANK NORMAL · C-BUTTON RAPID-OFF)
- `assessments/evidence/shikgam2/shot-609s.png` — attract gameplay: boss fight, coin medals, bomb bubbles

Deleted surplus (5): two more ranking pages, rock-garden gameplay frame, temple game-over frame, one duplicate attract frame.
Anomalies: none.

## 4. Memory fit (axis: 10.0)

| Region | Peak / fit | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (write-truth) | 33,538,112 (`0x1FFC040`) | 16,777,216 | 1.99903 | 10.0 (binding) | `MAINPROFILE`; 16,320 B under the `u > 2.0` park line — the band value at this u, coinciding with `AXIS_FLOOR` |
| VRAM (FB-masked content + 2×FB) | 4,556,188 (content_total 2,720,668 + 2×fb_bytes 917,760) | 8,388,608 | 0.543 | 100.0 | `VRAMPROFILE`; raw address peak 12,463,830 (u 1.486) is extent — 2,709,576 of 2,720,668 nonzero bytes sit above the 8 MB line (asset store parked high, the kurucham pattern) |
| ARAM (content, volume-keyed) | 1,754,237 | 2,097,152 | 0.837 | 97.3 | `ARAMPROFILE`; address peak 2,046,288 — **fits even address-keyed** (0.976×) |

**§6 checkpoint evidence, twice over:**
1. **Main near-park (gunsur2 class):** address peak `0x1FFC040` lands u=1.99903 — the
   second title to stop within a hair of the `0x2000000` park line (gunsur2: 468 B under;
   here: 16,320 B). Real changed content is `nz_total` 7,549,942 B with only
   `nz_above_cap` 213,556 B — the floored 10.0 axis charges ~33.5 MB of address extent
   against 0.2 MB of above-cap content. Scored address-keyed per the standing 2026-08-07
   ruling; kb §6 item 3 material.
2. **Second 24bpp FB instance:** `fb_bytes = 917,760` (640×478 at 24bpp, 1,920-byte
   stride — the mamonoro value exactly), not the usual 614,400. The v8 mask handles it;
   noted so the constant isn't mistaken for register garbage.

Watermarks (informational, content-scan — stale-data prone): main 33,538,112 · vram 12,463,830 · aram 8,388,608.
`dma_high_water` 11,754,048 B (informational-only from v6 on).

## 5. Cart streaming (axis: 77.2)

DMA events 75 · total 41,635,840 B (39.7 MB) · unique 15,949,824 B (15.2 MB) ·
re-read ratio 0.6169 · steady-state 3.752 MB/min (`short_window: false`) ·
PIO bootstrap `pio_bytes` 2,098,496 B. Lightest streaming profile of the wave — the game
front-loads its working set and barely touches the disc afterward.

## 6. Guts (axis: 85.0)

Code 2,097,152 B (carve `base 0x8c020000`, entry `0x8c021000`, load entry at file offset
8,388,608, header title "SHIKIGAMI NO SHIRO 2") · functions 4,623 · MMIO refs: scif 25,
rtc 3, g2ext 144 · BIOS vector refs: {} · penalties: `eeprom_bios`+`serial`+`rtc` → −15.

## 7. Controls (axis: 100.0 — `stick`)

Cabinet: standard Naomi 2P panel, 8-way stick + 2 gameplay buttons — A = Shot (tap = wide
shot; **hold** switches to the character's shikigami attack and slows movement — the core
mechanic), B = Bomb; the title-screen settings footer also shows a C-button rapid-fire
toggle (`C-BUTTON RAPID-OFF`, `shot-548s.png`). MAME input ports: `naomi`
(INPUT_PORTS_START at naomi.cpp @59e7c0b line 1506).
Proposed DC mapping: d-pad + 2 face buttons, 1:1 — proven by the official DC port (which
adds a convenience rapid-shot on R). Hold-timing fidelity matters more than button count.
Sources: MAME naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
[arcade-history GDL-0021](https://www.arcade-history.com/?n=shikigami-no-shiro-ii-model-gdl-0021&page=detail&id=3949);
[1CC Log DC review](http://1cclog.blogspot.com/2014/02/shikigami-no-shiro-ii-dreamcast.html).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 10.0^.40 · 77.2^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **35.4** (C)
Similarity inputs: developer match no, SDK overlap **partial**, cart loader match **yes** → 70.0.

## 9. Risks & notes

- **The score is a floor artifact, not a fit verdict**: memory 10.0 comes from an address
  peak 16 KB shy of an outright park, while above-cap content is 213 KB and the official
  Alfa System DC port ships the same game in 16 MB. Under any future content keying of
  the main axis (kb §6 item 3) this title's score would move sharply upward.
- ROT270 vertical — solved in the official port (TATE + Normal modes).
- Sole Naomi entry in its series (I was Taito G-NET, III was Type X2) — no engine-sibling
  precedent on this hardware beyond its own DC port, which is precedent enough.
- Lightest disc load of the wave (3.75 MB/min steady) — streaming is a non-issue for a
  GD-ROM port.
- Main-RAM write-truth includes CPU writes (v6+); `dma_high_water` is informational-only.
