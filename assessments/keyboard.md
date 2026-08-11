# La Keyboard (GDS-0017) (`keyboard`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **84.2 (S)** |
| Bottom line | The strongest possible controls story in the whole ⚠ lane: the cabinet's keyboards **are Dreamcast keyboards** — MAME instantiates literal `DC_KEYBOARD` maple devices for this title, the Flycast fork wires it as `MDT_Keyboard` maple devices (not JVS), the ROM itself links the Katana SDK's `pdKbd` keyboard driver, and real DC keyboards drive real cabinets through a maple adapter → `dc_peripheral` (75) on the official HKT-4000/HKT-7600 peripheral, with Sega's own *Typing of the Dead* (DC 2000/2001) as the first-party same-genre precedent. Memory is a clean sweep — all three regions fit with headroom *even by raw address peak* (main 14.9/16 MB, VRAM 7.2/8 MB, ARAM 1.84/2 MB — one of the campaign's rare full-fits, no relocation work at all), unsurprising for a 33.6 MB GD-ROM. Only the 0.81 streaming re-read ratio (attract loop re-fetching a small 16.9 MB working set) drags an axis. The ⚠ is audience, not hardware: it is a Japanese kanji-reading typing quiz. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `keyboard` (no clones — sole `keyboard` GAME row; MAME src/mame/sega/naomi.cpp @59e7c0b line 11172: `/* 0017 */ GAME( 2001, keyboard, naomigd, naomigd_kb, naomi_kb, naomi_state, init_naomigd, ROT0, "Sega / G.Rev", "La Keyboard (GDS-0017)", GAME_FLAGS )`) |
| Maker / year | Sega / G.Rev, 2001 (MAME `GAME()` row; title screen `shot-548s.png` reads "©SEGA ROSSO/SEGA, 2001" and the credits strings carry both "CREATED BY SEGA ROSSO" and a "G.rev SIDE" staff section — MAME's row comment notes it is "spelled as 'G.rev' in ending screen") |
| Genre / format | Typing ⚠ (kanji-reading typing quiz party game — prompts are kanji with kana + romaji readings the player must type, §3), **GD-ROM** GDS-0017, 33.6 MB (GAME_FORMATS.md); ROM region string: "THIS GAME IS TO BE USED ONLY IN JAPAN." (`guts.sdk_strings`) |
| Official DC port | No — none found (searched 2026-08-11) |
| Community ports | None found (searched 2026-08-11) |
| Representative choice | Only set in the family; one of the two Typing-⚠ families in the queue (`luptype` is the other) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/keyboard.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set after
screenshot review). The attract loop runs live typing-quiz demo rounds on the game's
blackboard UI: a kanji vocabulary round with kana + romaji readings and both players'
typed-answer boxes filling in (`shot-060s.png`, 野菜/やさい "ya sai"), a ゲーム説明
(game-instructions) tutorial round showing the four-kanji idiom 五里霧中 with per-character
romaji and a completed ごりむちゅう answer (`shot-304s.png`), a ranked typing round with a
partially-typed kana answer visible (`shot-426s.png`), a math-quiz variant round ("4×5=?"
under a PRESS 1P OR 2P ENTER KEY banner, `shot-487s.png`), and the La Keyboard title logo
with ©SEGA ROSSO/SEGA, 2001 (`shot-548s.png`) — all under FREE PLAY.
Screenshots: `evidence/keyboard/shot-060s.png` · `shot-304s.png` · `shot-426s.png` ·
`shot-487s.png` · `shot-548s.png`
Anomalies: none — clean full-window first-attempt leg; the battery-printed provisional 84.2 S
stands unchanged (the battery's `dc_peripheral` hint survived research, §7). `shot-121s.png`
(transition blur), `shot-182s.png` (black inter-scene frame), `shot-243s.png` (dance-interlude
silhouette), `shot-365s.png` (empty quiz board) and `shot-609s.png` (Sega logo card) were
curated out as low-information frames of the same loop.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,906,512 | 16,777,216 | 0.531 | 100.0 | Address peak 14,928,812 (u 0.890) and `dma_high_water` 14,928,800 fit the 16 MB cap outright · `nz_above_cap` 0 |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 3,762,989 | 8,388,608 | 0.449 | 100.0 | `content_total` 2,534,189 + 2×`fb_bytes` 614,400 · raw `nz_total` 2,837,734 · address peak 7,192,576 (u 0.857) fits the cap even unmasked · `regs_last` parks the second write-FB at 0xc00000 (the chocomk-precedent FB-placement artifact the v8 masking rekey exists for) · `nz_above_cap` 0 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,593,220 | 2,097,152 | 0.760 | 100.0 | Address peak 1,842,064 (u 0.878) — **under the 2 MB cap even by address**, rare in this campaign · `nz_above_cap` 0 |

Watermarks (informational, content-scan — stale-data prone): main 14,928,812 ·
vram 9,711,616 (the BIOS-logo residue value, kb §8 — write-truth peak is 7,192,576) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).
Axis = min(regions) = 100.0 — all three regions ≤ 0.80 u. No relocation work: every
region fits by address placement as-is, not just by content volume.

## 5. Cart streaming (axis: 68.8)

DMA events 597 · total 91.2 MB (95,678,464 B) · unique 16.9 MB (17,725,440 B) ·
re-read ratio 0.8147 · steady-state 8.731 MB/min (`short_window: false`) ·
PIO 2,884,928 B. Bandwidth is easy (sub-score 93.9); the 0.81 re-read ratio
(sub-score 31.1) is the axis's drag at 68.8 — the attract loop re-fetches its small
working set per round (per-round quiz/voice `KEY_*.MLT`/`VOX_*.MSB` bank loads,
`guts.sdk_strings`), classic reload-per-scene design over a tiny 33.6 MB disc.

## 6. Guts (axis: 85.0)

Code 2,883,584 B (2.75 MiB) · functions 1,436 · MMIO refs: scif 2, rtc 3, g2ext 112 ·
BIOS vector refs: none · penalties: `eeprom_bios` −5, `serial` −5, `rtc` −5 → 85.0.
Carve clean (`hdr_at` 0, title `"------La Keyboardxyu------"`, base 0x8c020000).
SDK strings show the stock Sega Katana/Naomi library stack (Kunoichi2 2.06, Ninja2 2.01,
sd2 for DC 2.50, gdCi/cvFs GD filesystem, MANATEE.DRV, "RMC Version 0.92 ... SEGA
SEGAKATANA") → `sdk_overlap: partial` — and, decisively for §7, **`pdKbd Ver 2.00`**,
the Katana SDK's maple keyboard peripheral driver, plus the game's own
" 1P KEYBOARDNOT CONNECTED!" / " 2P KEYBOARDNOT CONNECTED!" error strings.

## 7. Controls (axis: 75.0 — `dc_peripheral`)

Cabinet: two-player typing cabinet with physical keyboards. MAME input ports: `naomi_kb`
(GAME line 11172; `INPUT_PORTS_START(naomi_kb)` lines 2105–2270 with `naomi_kb_r<0>/<1>`
custom key readers). The decisive fact is *which device* MAME wires those ports into: the
`naomigd_kb` machine config (naomi.cpp lines 2590–2598) instantiates
`DC_KEYBOARD(config, "dcctrl0"/"dcctrl1", m_maple, 1/2)` — `dc_keyboard_device`, MAME's
**Dreamcast keyboard**, on the Naomi's maple ports. The arcade input device *is* the DC
peripheral; there is nothing to adapt.

Three further independent confirmations:
1. **Flycast fork** (@`f014a410c`, `core/hw/maple/maple_cfg.cpp:239–246`,
   `createNaomiDevices()`): gameId `"------La Keyboardxyu------"` — byte-identical to this
   sidecar's `carve_meta.title` — creates `MDT_Keyboard` maple devices on ports 1 and 2 and
   sets `settings.input.keyboardGame = true`; `maple_devs.cpp:1144` `struct maple_keyboard`
   reports device function `MFID_6_Keyboard`. `maple_jvs.cpp` contains **no** keyboard
   handling at all — keyboard input for this title is pure maple, not JVS, exactly the DC
   peripheral bus.
2. **The ROM itself** links `pdKbd Ver 2.00`, the Katana SDK's keyboard peripheral library,
   and checks "1P/2P KEYBOARD NOT CONNECTED" (`guts.sdk_strings`, §6) — the game reads its
   keyboards through the DC SDK's own maple keyboard driver.
3. **Real hardware**: the MAPLE2NAOMI adapter's compatibility list names this exact title —
   "Keyboard Only: La Keyboard, Lupin The Typing, Typing of the Dead"
   ([misteraddons.com](https://misteraddons.com/products/naomi-dreamcast-controller-adapter)) —
   real DC keyboards drive real cabinets over the Maple protocol.

**Why `dc_peripheral` (75), not `stick` (100):** the game is unplayable on a plain
stick/pad — it requires the official DC keyboard (HKT-4000/HKT-7600), a stock but
non-default peripheral. The precedent is first-party and same-genre: Sega shipped *The
Typing of the Dead* on DC keyboard-playable (Naomi original; DC Japan 2000-03-30, NA
2001-01-23 — [Wikipedia](https://en.wikipedia.org/wiki/The_Typing_of_the_Dead)), selling
HKT-4000/HKT-7600 keyboard bundles for it. Proposed DC mapping: none needed — native
maple keyboard input, 1:1 by construction; a port keeps the `pdKbd` path as-is (2P needs
a second keyboard, or ships single-player).
Sources: all five citations are in sidecar `controls.sources` (MAME GAME row + `naomigd_kb`
DC_KEYBOARD config, Flycast fork maple path, MiSTer Addons MAPLE2NAOMI, Wikipedia ToTD).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 68.8^.20 · 85.0^.20 · 75.0^.10 · 70.0^.10 = **84.2 (S)**
Similarity inputs: developer no, SDK overlap partial (stock Katana/Naomi libs, §6), loader match yes.

## 9. Risks & notes

- **The ⚠ is audience, not hardware**: quiz content is kanji-reading — prompts like 野菜 and
  五里霧中 must be read and typed in Japanese (`shot-060s.png`, `shot-304s.png`), and the ROM
  declares itself Japan-only. A port is JP-literate-audience only; nothing technical blocks it.
- **Keyboard required, pad impossible**: the port's audience is bounded by DC keyboard
  ownership (HKT-4000/HKT-7600 — official, common in Japan via ToTD bundles); two-player
  needs two keyboards.
- **Re-read ratio 0.81** — per-round `KEY_*`/`VOX_*` bank reloads; a DC port over GD-ROM
  reproduces this pattern trivially (8.7 MB/min steady), or caches the 16.9 MB unique set.
- Memory is a full fit even by address placement (§4) — no relocation pass needed; first
  thing to verify on real hardware is simply the `pdKbd` maple path with a real HKT-7600.
- Rendering must be verified on real DC hardware (working-style rule); evidence here is
  fork-rendered attract only.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | 84.2 (S) | Initial assessment — first Typing-⚠ family. Clean full-window first-attempt leg; controls research confirmed the battery's `dc_peripheral` hint with four independent sources (MAME wires literal `DC_KEYBOARD` maple devices; Flycast fork wires `MDT_Keyboard` maple, not JVS; ROM links Katana `pdKbd`; MAPLE2NAOMI runs real cabinets on real DC keyboards), so the provisional 84.2 stood. Rare full memory fit — all three regions under cap even by address peak |
