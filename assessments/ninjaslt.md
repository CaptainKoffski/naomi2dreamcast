# Ninja Assault (World, NJA2 Ver.A) (`ninjaslt`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,005,665 B → utilization **3.341**, well past `region_score()`'s `u > 2.0` gate — clear of the kb §6 item-9 empty band (max scored 1.962 `zerogu2`, min parked 2.997 `takoron`) and slotting into the parked cluster between `inunoos` (3.206) and `pokasuka` (3.368): `takoron` 2.997, `inunoos` 3.206, `ninjaslt` **3.341**, `pokasuka` 3.368, `mazan` 3.483, `mok` 3.558, `sstrkfgt` 3.687. Both other regions clear their own caps: main `nz_total` u ≈ 0.745, VRAM (content + 2×fb) u ≈ 0.900 — ARAM is the sole blocker. Controls do not compound the block: Namco's own Flycast source gives `ninjaslt` a *dedicated* native lightgun branch (`jvs_namco_jyu`, `light_gun_count=2`), separate from the Sega-title lightgun-as-analog group `mok`/`lupinsho`/`hotd2` belong to, and MAME's own hardware notes independently confirm real cabinets "uses Namco JYU JVS I/O" — `controls.device_class = dc_peripheral`, on-ladder (§ Gate). If ARAM ever cleared, controls would not gate G2 on their own. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `ninjaslt` (World, NJA2 Ver.A) — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11137 is the MAME parent set (`cloneof "naomi"`, i.e. self-keyed); MAME also lists region clones `ninjasltj` (Japan, NJA1, line 11136), `ninjasltu` (US, NJA3, line 11138), `ninjaslta` (Asia, NJA4, line 11139) — all `cloneof ninjaslt`, identical `naomim2`/`naomi` machine+input config, region-only differences. None of the three clones are tracked as separate rows in this campaign's `GAME_FORMATS.md`/`QUEUE.md`. |
| Maker / year | Published by **Namco**, developed by **Now Production** ([Wikipedia: Ninja Assault](https://en.wikipedia.org/wiki/Ninja_Assault) infobox), 2000 (MAME `GAME()` row; arcade release Japan 2000-11-09 per Wikipedia; title-screen copyright in `shot-487s.png`: "©2000 NAMCO LTD., ALL RIGHTS RESERVED") |
| Genre / format | Light-gun rail shooter (ninja/medieval-Japan theme; confirmed by attract-demo footage — torch-lit wooden-fortress corridors, a princess-rescue narrative, gun-reload/gameplay HUD, §3), **cart**, 81.2 MB (`GAME_FORMATS.md`) |
| Official DC port | No — arcade (Sega NAOMI) and PlayStation 2 only ([Wikipedia: Ninja Assault](https://en.wikipedia.org/wiki/Ninja_Assault): PS2 Japan 2002-09-09, PAL 2002-10-04, NA 2002-11-18; no Dreamcast release listed). A Zophar's Domain music-rip page catalogs the soundtrack under "Sega Dreamcast (DSF)" — same rip-format naming artifact already ruled non-evidence for `mok`/`lupinsho` (DSF applies broadly to AICA-driven titles sharing the DC sound driver, arcade Naomi included, not a console release). |
| Community ports | None found (searched 2026-08-10; no Dreamcast homebrew/fan-port hits). |
| Representative choice | MAME parent set (World, NJA2 Ver.A); `ninjasltj`/`ninjasltu`/`ninjaslta` are region-only clones sharing identical hardware/inputs — no separate assessment needed. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ninjaslt.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (battery wrote `null`; set here after
screenshot review). All 10 shots show a genuine attract loop cycling through two full playthroughs within
the 600 s capture: a "medieval Japan" castle establishing shot with narration (`shot-426s.png`, repeated at
`shot-609s.png` — the loop restarting), an intro cutscene with the Demon Shogun Kigai/Princess Koto
kidnapping narration (`shot-060s.png`), a character close-up cutscene (`shot-243s.png`), two distinct live
gameplay-HUD demo segments each with a rule-instruction tutorial banner ("Reload by pulling the trigger
while pointing your gun off the screen" over a torch-lit corridor, `shot-121s.png`; "Shoot the enemy" over a
different courtyard with a visible enemy character, `shot-304s.png`) each showing live score/life/ammo-clip
HUD elements, two "GAME OVER" demo-end screens (`shot-182s.png`, `shot-365s.png`), the Ninja Assault title
logo with 2000 Namco copyright (`shot-487s.png`), and a Namco WonderPage high-score-ranking promo screen
(`shot-548s.png`). No EEPROM/settings prompt or static idle screen anywhere in the capture — two genuine
gameplay demo segments confirm attract reached real game content, not just menus/title.
Screenshots: `evidence/ninjaslt/shot-060s.png` · `shot-121s.png` · `shot-304s.png` · `shot-426s.png` ·
`shot-487s.png`
Anomalies: none. `shot-182s.png`, `shot-243s.png`, `shot-365s.png`, `shot-548s.png`, and `shot-609s.png`
were curated out as redundant with the kept intro/HUD-demo/HUD-demo/scene-setting/title-identity shots
(609s duplicates 426s exactly — same loop point on the second cycle), same curation class as `mok`/`lupinsho`.

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,005,665 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.341** — well past `region_score()`'s `u > 2.0` gate, landing in the middle of
this campaign's parked ARAM distribution: `takoron` 2.997, `inunoos` 3.206, `ninjaslt` **3.341**,
`pokasuka` 3.368, `mazan` 3.483, `mok` 3.558, `sstrkfgt` 3.687. This is clear of the kb §6 item-9
empty band (max scored `zerogu2` 1.962, min parked `takoron` 2.997) — `ninjaslt` sits well above
it, adding another data point to the already-parked cluster, not the empty gap. `nz_above_cap` =
5,132,859 B of content above the cap (address-keyed placement figure, informational). Address
peak is 8,290,128 B (u 3.953, pre-volume-keying read).

The other two regions, quoted from the sidecar for context (ARAM gates first in `score.py`'s
region walk regardless):

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 12,491,713 | 16,777,216 | **0.745** | `nz_total` — clears the 1x cap; `nz_above_cap` (address-placement) 8,460,669 B · `dma_high_water` 32,292,192 B (u 1.925) · address peak 32,292,192 B (same value — both moot, ARAM gates first |
| VRAM (content volume + 2×fb) | 7,551,391 | 8,388,608 | **0.900** | `content_total` 6,322,591 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2 constant) — clears the 1x cap; raw `nz_total` 6,927,122 (u 0.826) · address peak 13,897,728 (u 1.657) · `nz_above_cap` 4,407,281 B (address-keyed) |
| ARAM (content volume) | 7,005,665 | 2,097,152 | **3.341** | the gate — see above |

Streaming context: 1,064 DMA events · 109,355,552 B (104.3 MB) total · 61,250,816 B (58.4 MB)
unique · re-read ratio 0.4399 · steady-state 10.393 MB/min (`short_window: false`) · `pio_bytes`
6,883,088 B.
Guts: code 4,194,304 B (4.0 MiB) · 2,951 functions · MMIO refs rtc 4 / g2ext 155 / scif 8 ·
flags `eeprom_bios`/`serial`/`rtc`. `carve_meta.title` reads `"NINJA ASSAULT"` — the exact string
Flycast's `maple_jvs.cpp` matches against for its dedicated lightgun branch (§ below), corroborating
the carve against the same identifier the emulator itself keys on. `sdk_strings` include explicit
gun-calibration/service-mode text ("TO CHECK GUN ACCURACY", "AIM AT CENTER OF THE CROSS AND PULL
GUN TRIGGER", "GUN INITIALIZE (1P)/(2P)", "PULL BOTH GUN'S TRIGGERS") confirming genuine positional
gun hardware from the game's own service-mode code, independent of MAME/Flycast.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (on-ladder, does not gate — `dc_peripheral`):** `ninjaslt` is a positional light-gun
title, but its MAME/Flycast source picture differs from the `mok`/`lupinsho` precedent in one
respect worth stating exactly, as asked: MAME assigns it the **generic** `naomi` input port set
(`GAME()` row, MAME src/mame/sega/naomi.cpp @59e7c0b line 11137: `GAME( 2000, ninjaslt, naomi,
naomim2,naomi, naomi_state, init_naomi, ROT0, "Namco", "Ninja Assault (World, NJA2 Ver.A)",
GAME_FLAGS )`) — plain digital joystick/button bits (`INPUT_PORTS_START(naomi)`, lines 1506–1565),
**not** the `hotd2`-style `IPT_LIGHTGUN_X`/`IPT_LIGHTGUN_Y` port set `mok`/`lupinsho` get. MAME's
own hardware-notes table settles the real cabinet hardware independently of the input-port
assignment, though: line 804 reads "Ninja Assault (Japan, NJA1 Ver.A) ... uses Namco JYU JVS I/O",
and the table's caveat at lines 812–813 states "games that require a special I/O board or
controller will not boot at all with a standard NAOMI I/O board" — confirming this is genuinely
dedicated gun hardware, not a generic control panel MAME just hasn't modeled as analog.

Flycast's own source corroborates this directly and **`ninjaslt` is *not* in the lightgun-as-analog
group** `mok`/`lupinsho`/`hotd2`/Confidential Mission/Death Crimson OX belong to (`core/hw/maple/
maple_jvs.cpp:1532–1542`, `../cleopatra/tools/flycast-src`) — quoting exactly what's there,
`ninjaslt` gets its own dedicated branch immediately above that group:
```
else if (gameId == "NINJA ASSAULT")
{
    // Light-gun game
    INFO_LOG(MAPLE, "Enabling lightgun setup for game %s", gameId.c_str());
    io_boards.push_back(std::make_unique<jvs_namco_jyu>(1, this));
    settings.input.lightgunGame = true;
}
```
(lines 1525–1531). `jvs_namco_jyu` (lines 1028–1042) is a purpose-built I/O-board class with
`light_gun_count = 2` (native two-gun positional support, one gun per player) and
`get_id() == "namco ltd.;JYU-PCB;Ver1.00;JPN,2Coins 2Guns"` — a *more* direct native-lightgun
emulation path than the `lightgun_as_analog` fallback flag the Sega-title group uses (that group
reuses a generic `jvs_837_13551` board and flips one bool; `ninjaslt` gets its own board class
built around Namco's real JYU-PCB). This is honest, not spun: MAME's port assignment alone would
suggest plain digital controls, but MAME's own hardware-notes citation plus Flycast's dedicated
native board both independently confirm real positional gun hardware — the two primary sources
agree even though they arrived at the classification through different code paths than the
`mok`/`lupinsho` precedent.

Namco shipped Ninja Assault on PlayStation 2 in 2002 with GunCon 2 support — verified: the PS2
release supports Namco's GunCon 2 peripheral ([retrovgames.com GunCon 2 listing](https://retrovgames.com/namcoguncon2gun/):
"Compatible with PS2 shooters including - Ninja Assault, Resident Evil: Dead Aim, Time Crisis 2 and
3, Vampire Night"), confirming a genuine 2-axis screen-position light-gun lineage — the same
hardware class of peripheral the DC Gun (HKT-7800) serves on Dreamcast, just on a different console
(no DC release exists, §2). Two sources (MAME notes + Flycast native board) plus two web sources
(Wikipedia, retrovgames.com), all recorded in sidecar `controls.sources`. `controls.device_class =
dc_peripheral` — on-ladder, so controls do **not** currently gate and would not gate G2 even if ARAM
cleared; ARAM alone is the blocker.
Proposed DC mapping mirrors `mok`/`lupinsho`: DC Gun (HKT-7800) screen-position aim = X/Y, trigger =
P1 Trigger, side/B button = P1 Screen-In (reload, per the tutorial banner in `shot-121s.png`) — a
direct 1:1 hardware mapping, though ported inputs would need remapping from a Namco JYU-PCB 2-gun
board rather than the Sega analog-fallback path `mok`/`lupinsho` use.

What would unblock it: ARAM content would need to shrink below the 2× cap — `ninjaslt`'s 3.341×
sits in the lower-middle of the parked cohort (above `inunoos` 3.206×, below `pokasuka` 3.368×).
Both other regions already clear (main 0.745×, VRAM 0.900×), and controls are on-ladder
(`dc_peripheral`) — ARAM is the *only* blocker; a sound-asset trim sufficient to bring
`content_total` under 2,097,152 B would clear the title outright with no other work needed.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — light-gun cohort, fresh v9 capture; controls dc_peripheral (native Namco JYU-PCB gun board per Flycast, not the Sega lightgun-as-analog group — ARAM sole blocker) |
