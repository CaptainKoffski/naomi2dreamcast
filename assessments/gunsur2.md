# Gun Survivor 2 Biohazard Code: Veronica (World, BHF2 Ver.E) (`gunsur2`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **73.0 (A)** |
| Bottom line | Nextech's Naomi adaptation of the studio's own Dreamcast Code: Veronica — the binary still carries the DC original's VMU save paths and RDT room format, and under content-volume keying every region fits (main is the binding region at 0.901× cap) — with the real drag now the 3-axis cabinet gun that needs a designed pad adaptation (`pad_adaptable`, 50), not memory. |
| Assessed | capture 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `gunsur2` (covers: `gunsur2j` — Japan, BHF1 Ver.E; only the 2f flash ROM differs, all 14 `bhf1ma*` mask ROMs share CRCs — MAME naomi.cpp @59e7c0b ROM_STARTs lines 7013–7060) |
| Maker / year | Capcom / Namco, 2001 — development by **Nextech Co., Ltd** for both arcade and PS2 ([Project Umbrella](https://www.projectumbrella.net/gun-survivor-2-biohazard-codeveronica.html)) |
| Genre / format | Gun shooter (3-axis mounted gun — NOT optical lightgun, §7), **cart** (F1X type, Namco sticker 25709801, M2 crypt board, key `317-5075-COM` — naomi.cpp cart table line 747). First cart title in the campaign with a full static scan (§6) |
| Official DC port | No — arcade (Naomi) and PS2 only ([Wikipedia](https://en.wikipedia.org/wiki/Resident_Evil_Survivor_2_%E2%80%93_Code:_Veronica)). PS2: Japan 2001-11-08, PAL 2002-02-08 as *Resident Evil Survivor 2 Code: Veronica*; **no North American release** (SCEA objected to the content and GunCon2 use — Project Umbrella). PS2 version playable on a standard DualShock 2; GunCon2 optional |
| Community ports | None found (searched 2026-08-02/03) |
| Representative choice | MAME parent set; World is the newer BHF2 release of the two |

**DC-assets lineage (similarity narrative).** Three verified links: (1) *Resident Evil – Code: Veronica* was Dreamcast-native (JP Feb 2000) with "Nextech handled much of the technical development" ([Wikipedia: RE CV](https://en.wikipedia.org/wiki/Resident_Evil_%E2%80%93_Code:_Veronica)); (2) Gun Survivor 2's "actual development [was] handled by Nextech Co., Ltd" ([Project Umbrella](https://www.projectumbrella.net/gun-survivor-2-biohazard-codeveronica.html)) — the same studio, adapting its own DC game onto the DC's arcade twin; (3) the binary itself carries the DC original's plumbing: VMU save paths `RE_CV/CLAIRE/`, `RE_CV/CHRIS/`, `RE_CV000.%03u`, `VERONICA.SYS`, `ICONDATA_VMS`, "VMS File System for Application" (`bu Ver 1.51`), CV disc-flow text ("DISC2 Starting", "Chris's Story"), and Capcom's RE room-data format ("RDT version error.", `r%1d_%1d%02d%1d.rdx`) — all in `guts.sdk_strings` (sidecar). Wiki-tier claims of an "enhanced Quake II engine" base and a *Gunmen Wars* cabinet lineage (Project Umbrella, fandom) find **no** support in the strings — the stack is the standard Sega/CRI Naomi-DC one (§6); treat those claims as unverified. `sysmes.ald` is a Capcom sound/message-archive artifact from the RE lineage, same family of evidence.

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/gunsur2.zip`
Attract/demo reached: **demo** — "DEMO PLAY" rendered on-screen; the attract loop cycles
demo gameplay → title → cutscene (sidecar `capture.coverage = "demo"`)
Screenshots: `evidence/gunsur2/shot-060s.png` · `shot-121s.png` · `shot-243s.png` ·
`shot-365s.png` · `shot-426s.png` (re-curated in the v8 run — demo gameplay, DEMO PLAY
marker, title, and a second gameplay frame)
Anomalies: none in the current run. Historical (v2): the first run parked `no-eeprom-180s`
because gunsur2's Namco-built ROM header is nonstandard (`region ff players 0 vertical 0`)
so Flycast's "monitor orientation" log never fires — the battery's boot marker now accepts
either `naomi_flashrom.cpp` line (fix `2cc46ce`, kb §4.n second gap); future Namco-header
titles (ninjaslt, mazan, wldkicks) would have hit it too.

## 4. Memory fit (axis: 92.4)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 15,116,665 | 16,777,216 | 0.901 | 92.4 | **binding region** · address peak 33,553,964 (u 2.000 — was 468 B under the G3 2× address threshold, informational since v9) · `nz_above_cap` 6,232,660 · `dma_high_water` 31,610,624 |
| VRAM (FB-masked content + 2×FB) | 5,960,110 | 8,388,608 | 0.7105 | 100.0 | `content_total` 4,731,310 + 2×`fb_bytes` 614,400 (exactly 640×480×2; `content_total + fb_masked_nz` matches `nz_total` exactly in the raw log) · address peak 16,140,288 (u 1.924, informational) · nz_total 5,051,952 · nz_above_cap 4,427,374 |
| ARAM (content volume, fill-excluded, `content_total`) | 1,565,884 | 2,097,152 | 0.7467 | 100.0 | address peak 2,097,136 (16 B under cap — sound authored to a DC budget, exactly what the Nextech DC lineage §2 predicts) |

Watermarks (informational, content-scan — stale-data prone): main 33,553,964 ·
vram 16,140,288 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 67.9)

DMA events 357 · total 124.3 MB · unique 38.7 MB · re-read ratio 0.6889 ·
steady-state 11.664 MB/min (`short_window: false`) · PIO 6,329,664 B

## 6. Guts (axis: 80.0)

Code 6,291,456 B · functions 4,551 · MMIO refs: scif 3, rtc 3, g2ext 902 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc`,
`code_over_4mb` (code 6 MiB > 4 MB → −5) → 80.0

First cart title with `dat_available: true` — full Ghidra carve (base `0x8c020000`, header title ` BIOHAZARD  GUN SURVIVOR2`). `guts.sdk_strings` shows the standard Sega/CRI Naomi-DC stack: Kunoichi Library for NAOMI 0.96, Ninja Ver 012000114, `sd for DC Ver 2.02.11`, manatee.drv 2.02.07, gdRmc 0.92, CRI ADXT 5.93 / Sofdec (mwSfd 2.28), NAOMI LIBRARY FOR AM 2.220550 — plus the DC Code Veronica artifacts quoted in §2. The in-binary test menu names the cabinet hardware directly: `SOLENOID TEST`, `GUN BUTTON`, `PITCH`, `SELECT (UP/DOWN)`, `KEEP GUN CENTER POSITION`, and the FCA-1 I/O ID fragment `Multipurpose + Rotary Encoder` / `NO I/O BORD`. `LINK ERROR` / "Sending Master Data" / "Communication Error!!!" strings are the twin-cabinet comm layer (§9).

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: **fixed cabinet-mounted machine-gun assembly on three potentiometers — pitch, roll, yaw — with trigger switch and recoil solenoid**; sliding the whole gun moves the character, rotating it aims (Namco operator's manual). Twin cab, one gun + monitor + Naomi board per player, linked. I/O: **Namco FCA-1 JVS board** ("Multipurpose + Rotary Encoder", 7 analog channels) — MAME: "uses Namco FCA JVS I/O (not dumped)" (naomi.cpp line 745). This is **not an optical lightgun**: "the NAOMI arcade release features no lightgun technology whatsoever… a three-axis joystick in the shape of a gun" (Wikipedia). MAME input ports: `naomi` (generic — the FCA gun is unemulated there). Flycast is the ground truth: `gunsur2_inputs` maps PITCH/ROLL/YAW as Full analog axes with no reload key (`naomi_roms_input.h:208`) and instantiates `jvs_namco_fca` **without** setting `lightgunGame` (`maple_jvs.cpp:1552`) — unlike Ninja Assault, Mazan, or HOTD2 — i.e. it is already played today as an analog-axes controller game.

Not `dc_peripheral` (75): the official DC light gun is an optical screen-position device with no analog axes — it cannot produce yaw/pitch/roll values or the slide-to-move input, so no official DC peripheral covers the cabinet interface as-is. The PS2 port's GunCon2 mode proves a gun peripheral *can* drive the game — but only after Namco/Nextech re-engineered the control layer for consoles (optical aim + button movement), which is exactly the remapping work `pad_adaptable` encodes, and the same port ships fully playable on a standard DualShock 2.

Proposed DC mapping: analog stick = yaw/pitch (aim), d-pad or L/R triggers = third axis (strafe/roll), A = trigger, B = gun button, Start = enter, with select up/down on remaining buttons — workable for a deliberately-paced shooter. A DC-gun control mode following the PS2 GunCon2 redesign is a plausible stretch goal, not the baseline. Recoil solenoid loss is cosmetic.

Sources: [Namco Gun Survivor 2 operator's manual](https://www.manualslib.com/manual/2251116/Namco-Gun-Survivor-2.html) (pitch/roll/yaw pots, trigger, solenoid, FCA PC board); MAME src/mame/sega/naomi.cpp @59e7c0b lines 741–747, 11142–11143; Flycast `naomi_roms_input.h:208` + `maple_jvs.cpp:1074–1089, 1552–1556` (`../cleopatra/tools/flycast-src`); [Wikipedia](https://en.wikipedia.org/wiki/Resident_Evil_Survivor_2_%E2%80%93_Code:_Veronica) (three-axis gun; PS2 GunCon2 + DualShock 2); [Highway Games](https://www.highwaygames.com/arcade-machines/gun-survivor-biohazard-8324/) (fixed guns, Naomi 1, twin cab); [Project Umbrella](https://www.projectumbrella.net/gun-survivor-2-biohazard-codeveronica.html) (Nextech, GunCon2, no NA release); in-binary test-menu strings (sidecar `guts.sdk_strings`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 92.4^.40 · 67.9^.20 · 80.0^.20 · 50.0^.10 · 40.0^.10 = **73.0 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no → 40.
Note: `developer_match = false` is a reference-list artifact — Nextech built both this and the DC Code: Veronica (§2), a stronger real-world match than the flag captures; recorded as a checkpoint data point (kb §6 item 4).

## 9. Risks & notes

- **Main RAM is the binding region and is address-sparse.** Content volume 15.1 MB (0.901×)
  fits, but the address peak reaches 33,553,964 B (2.000× cap) with 6,232,660 B of content
  above the 16 MB line — a port needs real relocation/layout work, and under the old
  address keying this title sat 468 B from a G3 park. The mitigation path is unusually
  concrete: the DC original *is* the same game's source material — a port can lean on Code:
  Veronica's own DC-sized asset versions (models, rooms, textures) rather than inventing
  reductions. ARAM and VRAM fit with headroom (§4).
- **Controls need a designed adaptation, not a mapping.** 3-axis gun + slide movement → one-stick DC pad is a real control-scheme design task; the PS2 port is the proven template (pad-native, GunCon2 optional). See kb §6 item 4 for the calibration question this raises.
- **Twin-cab comm layer:** MAME notes the Japan set "will crash if COMM.BOARD not present" (naomi.cpp line 745, BHF1 note). The World set demonstrably boots and attract-loops without any comm board — this clean single-board run is the evidence. Link-play code (`LINK ERROR`, master-data exchange strings) exists in the binary and would be stripped or stubbed in a port.
- `gunsur2j` needs no separate assessment: only the 2f ROM differs (§2).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | 33.4 (C) | First scored run: VRAM 1.92× and main 1.88× address-keyed, both just under G3; ARAM address peak at the DC cap (sub 85.0); memory axis 13.0. Boot-marker gap for Namco headers found + fixed (`2cc46ce`, kb §4.n) |
| v4 | 2026-08-04 | 33.4 (C) | Reproduced on v4; researched `pad_adaptable` controls restored after the re-run reset them to the `stick` hint (fixed in run_battery; kb §7) |
| v8 | 2026-08-07 | 30.0 (C) | Re-capture. VRAM re-keyed FB-masked content (sub 13.0 → 100.0); main write-truth measured for the first time — address peak 33,553,964 B, 468 B under the G3 2× park, sub floors at 10.0 and binds (spec `2026-08-07-vram-fb-masking-design.md`) |
| v9 | 2026-08-08 | 73.0 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` 15,116,665 (u 0.901) — memory axis 92.4, main still binding (spec `2026-08-08-main-content-rekey-design.md`) |
