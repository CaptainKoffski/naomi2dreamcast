# Lupin The Third - The Shooting (Rev A) (GDS-0018A) (`lupinsho`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **77.1** (A) |
| Bottom line | The corpus's first light-gun title clears full memory headroom on main (u 0.567) and VRAM (u 0.499) but binds narrowly on ARAM (u 1.026×, sub 80.3 — 54,633 B over the 2 MB cap). Guts is solid (85.0): 1 MiB code, 2,717 functions, with `serial`/`rtc` MMIO touches beyond the universal `eeprom_bios` — measured after the 2026-08-10 dat-extract sector-size fix (this dump stores plain 2048-byte MODE1 sectors where the extractor assumed 2352-raw, §6). Controls score 75.0 (`dc_peripheral`): MAME assigns `lupinsho` the identical `hotd2` input ports as House of the Dead 2, and Flycast's own source hard-codes `lupinsho` into the same lightgun-as-analog JVS group as `hotd2`, Confidential Mission, and Death Crimson OX — three titles that all officially shipped as Sega Dreamcast Gun (HKT-7800) games (§7). Similarity is 70.0 (SDK overlap partial + GD-ROM loader match, §8). |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — guts/similarity re-scored 2026-08-10 after the dat-extract sector-size fix (see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `lupinsho` (covers: `lupinshoo` — original Japan release GDS-0018; `lupinsho` Rev A GDS-0018A is the MAME parent, only revision differences — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` rows lines 11173–11174, both assigned `input_ports=hotd2`) |
| Maker / year | Manufacturer **Sega / Eighting** (MAME `GAME()` row), developed by **WOW Entertainment, Inc.** ([arcadeitalia MAME DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=lupinsho)), 2001 |
| Genre / format | Light-gun shooter (fixed-position optical lightgun cabinet, §7), **GD-ROM** GDS-0018A, 190.2 MB (`GAME_FORMATS.md`) |
| Official DC port | **No** — Naomi arcade only; no console release found. [LaunchBox Games DB](https://gamesdb.launchbox-app.com/games/details/37263-lupin-the-third-the-shooting) lists the title exclusively under Arcade/NAOMI; [Guardiana Sega retro database](https://www.guardiana.net/MDG-Database/NAOMI/Lupin+The+Third:+The+Shooting/) lists it only under NAOMI (both checked 2026-08-10). A Zophar's Domain music-rip page catalogs the soundtrack under "Sega Dreamcast (DSF)" — this is a rip-format naming artifact, not a console release: DSF applies broadly to AICA-driven titles sharing the DC sound driver, arcade Naomi included (the same shared-driver pattern documented via SDK strings in `assessments/gunsur2.md` §2/§6), and is contradicted by every dedicated games database above; treat it as unverified wiki-tier noise. |
| Community ports | None found (searched 2026-08-10). |
| Representative choice | MAME parent set (Rev A, GDS-0018A); `lupinshoo` (GDS-0018) is the earlier-revision clone sharing identical `hotd2` input ports and `naomigd` machine config — no separate assessment needed. |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/lupinsho.zip`
Attract/demo reached: **demo** — the full 10-shot capture cycles an attract loop: animated Lupin cutscene (`shot-060s.png`) → title card variants building up "PRESS START BUTTON" (`shot-121s.png`, `shot-182s.png`, `shot-243s.png`) → live light-gun gameplay footage with visible aim-reticle lines and a diamond/heart score HUD (`shot-304s.png`) → a RANKING high-score table (`shot-365s.png`) → a boss-encounter demo scene with Japanese dialog subtitles (`shot-426s.png`) → a second RANKING table under a jewel-shower overlay (`shot-487s.png`) → a driving/car-chase demo segment with "Left"/"Right" steering-wheel prompt icons (`shot-548s.png`) → a dark silhouette transition (`shot-609s.png`) → loop restart. No EEPROM/settings prompt appears anywhere in the capture; two distinct gameplay demo segments (gun-aim shooting and a rail-driving segment) confirm attract genuinely reached game content, not just menus. Sidecar `capture.coverage = "demo"`.
Screenshots (5 kept of 10): `evidence/lupinsho/shot-060s.png` · `shot-182s.png` · `shot-304s.png` · `shot-426s.png` · `shot-548s.png` (full 10-shot manifest in sidecar `capture.screenshots`)
Anomalies: none.

## 4. Memory fit (axis: 80.3)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,514,579 | 16,777,216 | 0.5671 | 100.0 | address peak 33,403,968 (informational) · `nz_above_cap` 728,259 · `dma_high_water` 12,649,120 |
| VRAM (FB-masked content + 2×FB) | 4,186,746 (`content_total` 2,957,946 + 2×`fb_bytes` 614,400) | 8,388,608 | 0.4991 | 100.0 | raw address peak 13,484,438 (informational) · `nz_total` 3,516,259 · `nz_above_cap` 3,489,819 · `regs_last` isp_base=0 isp_limit=2fff00 ol_base=3f0280 ol_limit=300000 fb_w_sof1=800000 fb_w_sof2=c00000 fb_r_sof1=c00000 |
| ARAM (compacted content volume, fill-excluded, `content_total`) | 2,151,785 | 2,097,152 | 1.0261 | 80.3 | **binding region** · address peak 8,372,192 (informational) · `nz_above_cap` 185,211 |

Watermarks (informational, content-scan — stale-data prone): main 33,403,968 · vram 13,484,438 · aram 8,388,608 (the boot-time "DMPD" fill, not content — kb §7).
Risk flag: ARAM binds only just over cap — 54,633 B (2.6%) above the 2 MB line, u 1.026× sits near the bottom of the [1.00, 1.25] linear-decay band (sub-score 80.3, close to the 85.0 plateau edge at u=1.00). A minor audio-asset trim would likely bring this region under cap entirely.

## 5. Cart streaming (axis: 68.5)

DMA events 1,263 · total 137,959,424 B (131.6 MiB) · unique 57,192,448 B (54.5 MiB) · re-read ratio 0.5854 ·
steady-state 13.059 MB/min (`short_window: false`) · PIO 1,049,920 B

## 6. Guts (axis: 85.0)

Code 1,048,576 B (1 MiB) · functions 2,717 · MMIO refs: scif 2, rtc 3, g2ext 39 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc` → 85.0.
Carved at base `0x8c020000`, entry `0x8c021000`, header title `LUPIN THE THIRD  -THE SHOOTING-`.
The original v9 scan failed (`guts.error`: `no PIC produced a NAOMI image … read_gdrom failed
at lba 0`, `netpic=1`) — root-caused 2026-08-10 to a sector-format assumption in
`tools/dat-extract`, not the PIC or disc: this dump's CHD stores plain **MODE1 2048-byte**
sectors (`chdman info`: `TRACK:3 TYPE:MODE1`) where `extract_dat` hardcoded 2352-byte raw
sectors with user data at +16 (the format ikaruga/meltyb use, `TYPE:MODE1_RAW`) — so every
read landed at garbage offsets, the PVD walk returned zeros, and the tool aborted. The fix
passes the GDI-declared per-track sector size through `chd2dat.sh` to `extract_dat`;
calibration-guard golden hashes (incl. the GD golden ikaruga) reproduced bit-for-bit across
the fix (kb §10), so no battery version bump. The `netpic=1` byte in the PIC was a red
herring — the disc has a normal PVD at LBA 45016 and carves through the standard GD walk.
SDK strings (sidecar `guts.sdk_strings`, 500 recovered) include the game's asset/model
runtime text (`lpfont.pvr`, `OPKFILE.TBL`, model-bone work errors) plus shared-SDK entries
feeding similarity's `sdk_overlap: partial` (§8).

## 7. Controls (axis: 75.0 — `dc_peripheral`)

Cabinet: fixed-position 2-player optical lightgun cabinet — screen-position X/Y aim, 1 trigger + 1 reload button per player, 2 coin slots ([arcadeitalia MAME DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=lupinsho): "Input Device: Lightgun", 2 buttons/player, up to 2 concurrent players). MAME input ports: `hotd2` — the identical port set used by House of the Dead 2 on Naomi (`INPUT_PORTS_START(hotd2)`, naomi.cpp lines 1588–1624: `IPT_LIGHTGUN_X`/`IPT_LIGHTGUN_Y` per player with `PORT_CROSSHAIR`, `P1 Trigger` (`BUTTON1`), `P1 Screen-In` reload (`BUTTON2`); `GAME()` rows lines 11173–11174 assign this port to both `lupinshoo` and `lupinsho`). The visible aim-reticle lines in `evidence/lupinsho/shot-304s.png` corroborate a true screen-position lightgun mechanic, not an analog-stick aiming scheme.

Flycast's own source settles the classification directly: `core/hw/maple/maple_jvs.cpp:1532–1542` (`../cleopatra/tools/flycast-src`) hard-codes `gameId == "LUPIN THE THIRD  -THE SHOOTING-"` into the *same* branch as `hotd2*` (House of the Dead 2), `" CONFIDENTIAL MISSION ---------"`, and `"DEATH CRIMSON OX"`, setting `settings.input.lightgunGame = true` for all four. Confidential Mission and Death Crimson OX are not hypothetical DC-gun candidates — both officially shipped as Sega Dreamcast Gun (HKT-7800) games, alongside House of the Dead 2 itself ([Wikipedia: Dreamcast light guns](https://en.wikipedia.org/wiki/Dreamcast_light_guns) — the official gun, region-availability and per-title compatibility notes for exactly these three games). `lupinsho` sits in the same emulator-verified input-hardware bucket as three titles with proven official DC gun peripheral support, which is the basis for `dc_peripheral` (75) over `pad_adaptable` (50): unlike `gunsur2`'s 3-axis analog cabinet gun (`assessments/gunsur2.md` §7, no optical position, no official DC peripheral covers it), `lupinsho`'s cabinet is the same 2-axis screen-position + trigger + reload interface the DC Gun already serves.

Proposed DC mapping: DC Gun (HKT-7800) screen-position aim = X/Y, trigger = P1 Trigger, gun side/B button = Screen-In reload, Start = coin/start — a direct 1:1 hardware mapping requiring no control-scheme redesign (contrast `gunsur2`'s `pad_adaptable` case, which needs a genuinely new mapping for a 3-axis analog gun).

Sources: MAME src/mame/sega/naomi.cpp @59e7c0b `INPUT_PORTS 'hotd2'`; MAME src/mame/sega/naomi.cpp @59e7c0b `INPUT_PORTS_START(hotd2)` lines 1588–1624 + `GAME()` rows lines 11173–11174; Flycast `core/hw/maple/maple_jvs.cpp:1532–1542` (`../cleopatra/tools/flycast-src`); [Wikipedia: Dreamcast light guns](https://en.wikipedia.org/wiki/Dreamcast_light_guns); [arcadeitalia MAME machine DB](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=lupinsho).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 80.3^.40 · 68.5^.20 · 85.0^.20 · 75.0^.10 · 70.0^.10 = **77.1 (A)**
Similarity inputs: developer no, SDK overlap **partial**, loader match **yes** → 70.0 —
both recovered by the dat-extract fix (§6): the carved binary's `sdk_strings` share entries
with the reference, and `cart_loader_match` is true (GD-ROM format, `dat_available` truthy).

## 9. Risks & notes

- The initial 64.3 A score was a lower bound from a dat-extract measurement gap, since
  resolved: the 2026-08-10 sector-size fix (§6) restored the guts axis (85.0) and lifted
  similarity 20.0 → 70.0, moving the final to 77.1 A with no change to any captured metric.
- `serial` and `rtc` MMIO touches (§6) are real porting surface beyond the universal
  EEPROM/BIOS path — small, but a DC port must stub or reroute them.
- **ARAM binds barely over the DC cap** (u 1.026×, §4) — the smallest region overage margin in the axis, a minor audio-asset trim target rather than a structural blocker.
- **First light-gun title in the corpus**: the `dc_peripheral` classification rests on MAME's `hotd2` input-port assignment plus Flycast's explicit `lupinsho`/`hotd2`/Confidential Mission/Death Crimson OX grouping (§7) — a well-sourced precedent, but `mok` and `ninjaslt` (next in this cohort) need their own independent MAME/Flycast source checks before assuming the same class carries over.
- Verify on real DC hardware before any port claim (working-style rule) — this is an emulator-only (Flycast) measurement. The DC Gun peripheral itself requires a CRT display ([Dreamcast light guns](https://en.wikipedia.org/wiki/Dreamcast_light_guns) and multiple retailer listings note CRT-only operation) — a port's controls testing needs a CRT, not a modern flat panel.
- `lupinshoo` (GDS-0018) needs no separate assessment: only the revision differs, both share `hotd2` input ports (§2).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 64.3 A | initial assessment — light-gun cohort, fresh v9 capture |
| v9 | 2026-08-10 | 77.1 A | static-only rescore after the dat-extract sector-size fix (`chd2dat.sh` now passes the GDI-declared per-track sector size to `extract_dat`; this dump is plain MODE1 2048 B/sector, the tool assumed 2352-raw; calibration goldens incl. GD reproduced bit-for-bit, no battery bump): guts measured for the first time (85.0 — 1 MiB code, 2,717 funcs, `serial`+`rtc` penalties), similarity 20.0 → 70.0; capture metrics untouched |
