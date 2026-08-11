# Lupin The Third - The Typing (Rev A) (GDS-0021A) (`luptype`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **60.6 (A)** |
| Bottom line | The same maple-keyboard controls story as tonight's sibling `keyboard` (84.2 S) — the cabinet's keyboards **are Dreamcast keyboards** (MAME wires literal `DC_KEYBOARD` maple devices, the fork wires `MDT_Keyboard`, the ROM links Katana `pdKbd`) → `dc_peripheral` (75) — but memory drags it a tier below: ARAM audio **content** is 2.45 MB against the DC's 2 MB (u 1.226 → 44.4, the axis min), a genuine ~470 KB overage a port must trim or stream, not a placement artifact. Main and VRAM fit by content volume with big headroom (0.57 u / 0.51 u) even though both are placement-scattered (main address peak 33.4 MB sits a hair under the G3 2× line at u 1.991 — the v9 content rekey is the only reason this axis scores at all). The ⚠ is audience: kana/kanji typing prompts. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `luptype` (no clones — sole dumped set; MAME src/mame/sega/naomi.cpp @59e7c0b line 11180: `/* 0021A */ GAME( 2002, luptype, naomigd, naomigd_kb, naomi_kb, naomi_state, init_naomigd, ROT0, "Sega", "Lupin The Third - The Typing (Rev A) (GDS-0021A)", GAME_FLAGS )`; line 11179's comment records the GDS-0021 original as undumped) |
| Maker / year | Sega, 2002 (MAME `GAME()` row; title screen `shot-243s.png` reads "©WOW ENTERTAINMENT INC /SEGA CORPORATION, 2002" under the "©モンキー・パンチ／TMS・NTV" Monkey Punch license) |
| Genre / format | Typing ⚠ (kana/kanji typing action — prompts like プロモデル and 灰になった with romaji guidance, §3), **GD-ROM** GDS-0021A, 153.9 MB (GAME_FORMATS.md) |
| Official DC port | No — none found (searched 2026-08-12) |
| Community ports | None found (searched 2026-08-12) — search hits are DC keyboards/controllers adapted *into* the Naomi cabinet (MAPLE2NAOMI, JVS converters), the reverse direction |
| Representative choice | Only dumped set in the family (Rev A parent, original undumped); the second of the queue's two Typing-⚠ families (`keyboard` is the other, assessed tonight) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/luptype.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop runs Sofdec anime footage and live 3D typing-demo rounds:
the cel-animation intro montage (`shot-060s.png`, Lupin/Jigen split panels), the title screen
with full copyright block (`shot-243s.png`), a lounge demo round with the katakana prompt
プロモデル over both players' cash/LIFE HUD (`shot-304s.png`), a Jigen Daisuke character-intro
card with Japanese descriptive text (`shot-426s.png`), and a boulder-chase demo round with the
kana prompt 灰になった, its romaji reading "HAININATTA" partially typed ("ATTA" highlighted),
TIME 09 and both players' scores live (`shot-548s.png`) — all under FREE PLAY.
Screenshots: `evidence/luptype/shot-060s.png` · `shot-243s.png` · `shot-304s.png` ·
`shot-426s.png` · `shot-548s.png`
Anomalies: none — clean full-window first-attempt leg; the battery-printed provisional 60.6 A
stands unchanged after controls research (§7). `shot-121s.png`/`shot-182s.png` (title fade
frames), `shot-365s.png` (score-ranking table), `shot-487s.png` (RANKING splash) and
`shot-609s.png` (near-black transition) were curated out as redundant frames of the same loop.

## 4. Memory fit (axis: 44.4)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,542,072 | 16,777,216 | 0.569 | 100.0 | Address peak 33,399,328 (u **1.991** — a hair under the G3 2× line; address-keyed scoring would have scored this ~10) · `dma_high_water` 12,840,480 · `nz_above_cap` 712,870 — ~0.7 MB of content currently placed above the 16 MB line needs relocation |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 4,254,628 | 8,388,608 | 0.507 | 100.0 | `content_total` 3,025,828 + 2×`fb_bytes` 614,400 · raw `nz_total` 3,556,436 · address peak 13,423,280 (u 1.600) · `nz_above_cap` 3,529,996 — nearly all content sits above the 8 MB line because `regs_last` parks the write-FB flip pair at 0x800000/0xc00000 (the chocomk-precedent FB placement the v8 masking rekey exists for) |
| ARAM (content volume, fill-excluded, `content_total`) | 2,570,363 | 2,097,152 | 1.226 | 44.4 | **Genuinely over cap by content**, not placement: ~473 KB of audio beyond the DC's 2 MB · address peak 8,372,192 · `nz_above_cap` 605,860 |

Watermarks (informational, content-scan — stale-data prone): main 33,399,328 ·
vram 13,423,280 · aram 8,388,608 (the boot-time "DMPD" fill, not content).
Axis = min(regions) = 44.4 — ARAM is the sole drag; main and VRAM fit by content
volume with ~45% headroom each (both need a relocation pass, §9).

## 5. Cart streaming (axis: 67.1)

DMA events 1,306 · total 131.2 MB (137,570,304 B) · unique 47.0 MB (49,289,216 B) ·
re-read ratio 0.6417 · steady-state 13.131 MB/min (`short_window: false`) ·
PIO 1,049,920 B. Bandwidth is comfortable (sub-score 84.2); the 0.64 re-read ratio
(sub-score 41.5) drags the axis to 67.1 — the attract loop re-streams its Sofdec
movies and per-round banks (CRI ADX/Sofdec + `OPKFILE.TBL`/`CPKFILE.TBL`/`HPKFILE.TBL`
pack loads, `guts.sdk_strings`) rather than caching them.

## 6. Guts (axis: 85.0)

Code 1,048,576 B (1.0 MiB) · functions 2,742 · MMIO refs: scif 2, rtc 3, g2ext 38 ·
BIOS vector refs: none · penalties: `eeprom_bios` −5, `serial` −5, `rtc` −5 → 85.0.
Carve clean (`hdr_at` 0, title `" LUPIN THE THIRD  -THE TYPING-"`, base 0x8c020000).
SDK strings show the stock Sega Katana/Naomi library stack (Kunoichi 0.99, Ninja
012000114, Nindows, KM1Naomi 1.33, the CRI ADX/Sofdec stack, gdCi/cvFs GD filesystem,
"RMC Version 0.92 ... SEGA SEGAKATANA") → `sdk_overlap: partial` — and, decisively for
§7, **`pdKbd Ver 1.51`**, the Katana SDK's maple keyboard peripheral driver (alongside
`pd Ver 1.51`, the maple peripheral core).

## 7. Controls (axis: 75.0 — `dc_peripheral`)

Cabinet: two-player typing cabinet with physical keyboards — the same wiring as tonight's
decisive `keyboard` precedent (d60b169). MAME input ports: `naomi_kb` (GAME line 11180;
`INPUT_PORTS_START(naomi_kb)` lines 2105–2270 with `naomi_kb_r<0>/<1>` custom key readers).
The decisive fact is *which device* MAME wires those ports into: luptype's machine config is
the same `naomigd_kb` (naomi.cpp lines 2592–2599) that instantiates
`DC_KEYBOARD(config, "dcctrl0"/"dcctrl1", m_maple, 1/2)` — `dc_keyboard_device`, MAME's
**Dreamcast keyboard**, on the Naomi's maple ports. The arcade input device *is* the DC
peripheral; there is nothing to adapt. Not JVS: the JVS I/O-board strings in the ROM are the
stock Naomi I/O check, and the fork's `maple_jvs.cpp` contains no keyboard handling.

Three further independent confirmations:
1. **Flycast fork** (@`f014a410c`, `core/hw/maple/maple_cfg.cpp:239–246`,
   `createNaomiDevices()`): gameId `" LUPIN THE THIRD  -THE TYPING-"` — byte-identical to
   this sidecar's `carve_meta.title` — creates `MDT_Keyboard` maple devices on ports 1 and 2
   and sets `settings.input.keyboardGame = true` (the same clause lists all three Naomi
   typing titles: ToTD, luptype, keyboard).
2. **The ROM itself** links `pdKbd Ver 1.51`, the Katana SDK's keyboard peripheral library
   (`guts.sdk_strings`, §6) — the game reads its keyboards through the DC SDK's own maple
   keyboard driver.
3. **Real hardware**: the MAPLE2NAOMI adapter's compatibility list names this exact title —
   "Keyboard Only: La Keyboard, Lupin The Typing, Typing of the Dead"
   ([misteraddons.com](https://misteraddons.com/products/naomi-dreamcast-controller-adapter)) —
   real DC keyboards drive real cabinets over the Maple protocol.

**Why `dc_peripheral` (75), not `stick` (100):** unplayable on a plain stick/pad — it
requires the official DC keyboard (HKT-4000/HKT-7600), a stock but non-default peripheral.
The precedent is first-party and same-genre: Sega shipped *The Typing of the Dead* on DC
keyboard-playable (Naomi original; DC Japan 2000-03-30 —
[Wikipedia](https://en.wikipedia.org/wiki/The_Typing_of_the_Dead)), selling HKT-4000/HKT-7600
keyboard bundles for it. Proposed DC mapping: none needed — native maple keyboard input,
1:1 by construction; a port keeps the `pdKbd` path as-is (2P needs a second keyboard, or
ships single-player).
Sources: all five citations are in sidecar `controls.sources` (MAME GAME row + `naomigd_kb`
DC_KEYBOARD config, Flycast fork maple path, MiSTer Addons MAPLE2NAOMI, Wikipedia ToTD).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 44.4^.40 · 67.1^.20 · 85.0^.20 · 75.0^.10 · 70.0^.10 = **60.6 (A)**
Similarity inputs: developer no, SDK overlap partial (stock Katana/Naomi + CRI libs, §6), loader match yes.

## 9. Risks & notes

- **ARAM is the port's real work**: 2,570,363 B of fill-excluded audio content vs 2,097,152 B
  of DC ARAM — ~473 KB must go (re-encode/downsample the per-round voice banks and jingle
  `*.wav` sets named in `guts.sdk_strings`, or stream more from disc). This is content volume,
  already position-independent-compacted — unlike main/VRAM it cannot be fixed by relocation.
- **Both other regions need relocation passes, not cuts**: main has 712,870 B of content above
  the 16 MB line (address peak 33.4 MB, u 1.991 — just under G3; the v9 content rekey is what
  keeps this scoreable) and VRAM parks its FB flip pair at 0x800000/0xc00000 with ~3.5 MB of
  content above 8 MB — content+2×FB is only 4.25 MB (§4).
- **The ⚠ is audience, not hardware**: prompts are kana/kanji (プロモデル `shot-304s.png`,
  灰になった `shot-548s.png`) — romaji guidance is displayed, but reading Japanese is the game.
- **Keyboard required, pad impossible**: audience bounded by DC keyboard ownership
  (HKT-4000/HKT-7600); two-player needs two keyboards.
- Re-read ratio 0.64 at 13.1 MB/min steady — Sofdec attract movies + per-round pack reloads;
  a DC port over GD-ROM reproduces this pattern trivially.
- Rendering must be verified on real DC hardware (working-style rule); evidence here is
  fork-rendered attract only.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 60.6 (A) | Initial assessment — last family in the campaign queue. Clean full-window first-attempt leg; controls research confirmed the battery's `dc_peripheral` hint via the `keyboard` precedent set the same night (same `naomigd_kb` DC_KEYBOARD maple config, same fork `MDT_Keyboard` gameId clause, ROM links `pdKbd`), so the provisional 60.6 stood. ARAM content over-cap (u 1.226) is the bottleneck; main address peak grazed the G3 line at u 1.991 but the v9 main content rekey keyed on 9.5 MB of actual content |
