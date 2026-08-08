# Gun Survivor 2 Biohazard Code: Veronica (World, BHF2 Ver.E) (`gunsur2`) — portability assessment

> **Battery v9 main-content re-score (2026-08-08): 73.0 (A), was 30.0 (C)** — scoring-only blanket re-score, no re-capture: every measurement
> below is still the battery v8 run. §6 item 8 ruling (spec `2026-08-08-main-content-rekey-design.md`,
> adopted to main 2026-08-09): main now keys on write-truth content VOLUME instead of
> the address peak — `nz_total` 15,116,665 B (content-u 0.901) replaces peak 33,553,964 B (u 2.000).
> Memory axis 92.4, binding region now **main** (was memory 10.0). Verdict section below is the capture-time (v≤8) record.

> **Battery v8 vram-fb-masking re-run (2026-08-07): 30.0 (C)** — spec
> `2026-08-07-vram-fb-masking-design.md`. Sidecar: flycast `f014a410c`, battery 8. No
> park, boot ok, PIO handoff at 20.0 s. VRAM flips from address high-water (16,140,288 B,
> u=1.924, sub 13.0) to FB-masked content: `content_total` 4,731,310 B + `2×fb_bytes`
> 1,228,800 B (`fb_bytes` 614,400 B, exactly 640×480×2) = fit 5,960,110 B, u=0.711 → sub
> **100.0** — a rise, as required. ARAM: `content_total` 1,565,884 B, u=0.747 → sub
> **100.0** (v7-class keying, measured here for the first time since this doc's v4
> baseline never ran v6/v7 individually). **MAIN, first write-truth measured (v6
> instrumentation): peak 33,553,964 B — identical to this doc's old "informational"
> watermark figure below, same real-writes-not-noise pattern as chocomk/sgtetris — but
> u = 33,553,964 / 16,777,216 = 1.999972, just 468 bytes under the G3 2× park threshold.**
> Sub-score floors at **10.0** (`AXIS_FLOOR`), now the binding region, well below the v4
> DMA-only main sub of 14.6 and below the design doc's speculative "main 14.6" bound —
> the DMA-high-water metric substantially understated main RAM pressure here (writes
> exist ~1.94 MB above the DMA figure). Memory axis min(10.0, 100.0, 100.0) = **10.0**,
> down from 13.0; final **33.4 → 30.0**, tier unchanged **C**. This is not a stop
> condition (no park — u stayed under 2.0; VRAM's own sub-score rose, satisfying the
> wave's rises-only rule for VRAM specifically) but it is a near-miss worth flagging: 468
> more main-RAM bytes and this title parks G3. Coverage re-annotated `demo` (unchanged).

> **Battery v4 re-assessment (2026-08-04): **33.4 (C)**.**
> 33.4 C reproduced on v4 (was 33.4 C on v2) with researched `pad_adaptable` controls restored after the re-run reset them to the `stick` hint (fixed in run_battery).
> Below the v8 section is the battery v4-era assessment, itself superseding the v2-era
> assessment below that; each section's *measured* figures (boot evidence, memory,
> streaming, score) are **superseded** by the section above it — the identity,
> controls-research and similarity sections remain valid throughout. Instrumentation
> root-cause: `docs/kb/assessment-tooling.md` §7.

## v8 verdict & measurements

| | |
|---|---|
| **Final** | **30.0 (C)** |
| Coverage | demo |
| Assessed | 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/gunsur2.zip` |

| Region | Peak / fit | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (write-truth) | 33,553,964 | 16,777,216 | 1.99997 | first write-truth measurement — 468 B under the G3 2× park threshold; `nz_above_cap` 6,232,660; sub-score floors at 10.0, now binding |
| VRAM (FB-masked content + 2×FB) | 5,960,110 (content_total 4,731,310 + 2×fb_bytes 1,228,800) | 8,388,608 | 0.711 | battery v8 re-keying — sub 100.0, was 13.0 under address high-water (16,140,288, u=1.924) |
| ARAM (content, volume-keyed) | 1,565,884 | 2,097,152 | 0.747 | sub 100.0, was 85.0 under the old near-exact address peak (2,097,136) |

Streaming: 357 DMA events · total 124.3 MB · unique 38.7 MB · re-read 0.6889 · steady 11.664 MB/min (matches v4's re-read 0.6889 / steady 11.662 within run-to-run noise)
Axes: memory 10.0 · streaming 67.9 · guts 80.0 · controls 50.0 · similarity 40.0 → **final 30.0 (C)**
Screenshots: `evidence/gunsur2/shot-060s.png` · `shot-121s.png` · `shot-243s.png` · `shot-365s.png` · `shot-426s.png` (re-curated this run — demo gameplay, DEMO PLAY marker, title, and a second gameplay frame)

**Risk:** main RAM sits 468 bytes under the G3 park threshold (u=1.999972). Any small
further growth in measured main-RAM writes — a different capture window, a later game
state — would park this title. Not a metric artifact (§4/banner sanity: `content_total +
fb_masked_nz` matches `nz_total` exactly in the raw log; `fb_bytes` is exactly 614,400).

---

## v4 verdict & measurements

| | |
|---|---|
| **Final** | **33.4 (C)** |
| Coverage | demo |
| Assessed | 2026-08-04 · battery v4 · flycast `4b59eceff` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |
| Boot | ok=True · handoff 20.0 s · run 600 s · rom `naomi/gunsur2.zip` |

| Region | v4 peak | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (DMA high-water) | 31,610,624 | 16,777,216 | 1.88 |  |
| VRAM (write-truth diff) | 16,140,288 | 8,388,608 | 1.92 | nz_total 5,038,850 |
| ARAM (content, fill-excluded) | 2,097,136 | 2,097,152 | 1.00 | content above cap 0 |

Streaming: 357 DMA events · total 124.3 MB · unique 38.7 MB · re-read 0.6889 · steady 11.662 MB/min
Axes: memory 13.0 · streaming 67.9 · guts 80.0 · controls 50.0 · similarity 40.0 → **final 33.4 (C)**
Screenshots: `evidence/gunsur2/shot-060s.png` · `evidence/gunsur2/shot-365s.png` · `evidence/gunsur2/shot-609s.png`

---

# Historical: battery v2 assessment (measurements superseded)

## 1. Verdict

| | |
|---|---|
| **Final score** | **33.4** (C) |
| Bottom line | Low C on the numbers, but with the queue's strongest asset-lineage story: the game is Nextech's Naomi adaptation of the studio's own **Dreamcast** Code: Veronica — the binary still carries the DC original's VMU save paths and RDT room format, and ARAM peaks at exactly the DC's 2 MiB cap. What drags it down is real: VRAM 1.92× and main RAM 1.88× (both just under the G3 gate), plus a 3-axis cabinet gun that no DC peripheral covers as-is (`pad_adaptable`, 50). |
| Assessed | 2026-08-03 · battery v2 · flycast `9e882cbd2` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

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

Boots: yes · handoff at 20.0 s · run 600 s · rom: `naomi/gunsur2.zip`
Attract/demo reached: **demo reached** — "DEMO PLAY" rendered on-screen (`shot-244s.png`, `shot-542s.png`); sidecar `capture.coverage = "demo"`. The attract loop cycles demo gameplay → title → cutscene across the window.
Screenshots kept (5 of 10): `shot-121s.png` (demo gameplay, first-person corridor with Nemesis timer and Instructions card), `shot-244s.png` (**DEMO PLAY** marker — coverage evidence), `shot-367s.png` (title screen, Capcom + Namco 2001 copyrights), `shot-542s.png` (demo gameplay, second stage), `shot-603s.png` (attract cutscene).
Anomalies: the run initially parked `no-eeprom-180s` — a tooling gap, not the game: gunsur2's Namco-built ROM header is nonstandard (`region ff players 0 vertical 0`) so Flycast's "monitor orientation" log never fires; the battery's boot marker now accepts either `naomi_flashrom.cpp` line (fix `2cc46ce`, kb §4.n second gap). Clean full-window run after the fix.

## 4. Memory fit (axis: 13.0)

| Region | Peak | DC capacity | Utilization | Sub-score | Evidence |
|---|---|---|---|---|---|
| Main RAM (DMA high-water) | 31,610,624 B | 16 MB | 1.88× | 14.6 | grep `CARTDMA` in raw log |
| VRAM (write-truth) | 16,140,288 B | 8 MB | 1.92× | 13.0 | grep `VRAMPROFILE` |
| ARAM (write-truth) | 2,097,152 B | 2 MB | **1.00×** | 85.0 | grep `ARAMPROFILE` |

Watermarks (informational, content-scan — stale-data prone): main 33,553,964 / vram 16,140,288 / aram 2,097,152. Main watermark 1.06× the DMA high-water — mild.

**ARAM peaks at exactly 2,097,152 B — the DC's cap to the byte — with `nz_above_cap = 0`.** Second exact-fit data point after `tetkiwam`: the sound content was authored to a Dreamcast budget, exactly what the Nextech DC lineage (§2) predicts. VRAM and main RAM are the opposite story: both land in the 1.25–2.0× penalty band just under the G3 gate. VRAM nonzero content is only 4,929,040 B (4.70 MiB, `nz_total`) against a 16.1 MB address-extent peak, with 4,365,778 B parked above the 8 MB line — as with kurucham, address extent overstates true content pressure, but unlike ARAM these regions were not held to DC budgets in the arcade build.

## 5. Cart streaming (axis: 68.6)

DMA events 346 · total 126,228,480 B (120.4 MiB) · unique 40,552,448 B (38.7 MiB) · re-read ratio 0.6787 · steady-state 11.305 MB/min (full window, `short_window: false`)

## 6. Guts (axis: 80.0)

Code 6,291,456 B · functions 4,551 · MMIO refs: scif 3, rtc 3, g2ext 902 ·
BIOS vector refs: none · penalties applied: `eeprom_bios`, `serial`, `rtc`, `code_over_4mb` (code 6 MiB > 4 MB → −5) → 80.0

First cart title with `dat_available: true` — full Ghidra carve (base `0x8c020000`, header title ` BIOHAZARD  GUN SURVIVOR2`). `guts.sdk_strings` shows the standard Sega/CRI Naomi-DC stack: Kunoichi Library for NAOMI 0.96, Ninja Ver 012000114, `sd for DC Ver 2.02.11`, manatee.drv 2.02.07, gdRmc 0.92, CRI ADXT 5.93 / Sofdec (mwSfd 2.28), NAOMI LIBRARY FOR AM 2.220550 — plus the DC Code Veronica artifacts quoted in §2. The in-binary test menu names the cabinet hardware directly: `SOLENOID TEST`, `GUN BUTTON`, `PITCH`, `SELECT (UP/DOWN)`, `KEEP GUN CENTER POSITION`, and the FCA-1 I/O ID fragment `Multipurpose + Rotary Encoder` / `NO I/O BORD`. `LINK ERROR` / "Sending Master Data" / "Communication Error!!!" strings are the twin-cabinet comm layer (§9).

## 7. Controls (axis: 50.0 — `pad_adaptable`)

Cabinet: **fixed cabinet-mounted machine-gun assembly on three potentiometers — pitch, roll, yaw — with trigger switch and recoil solenoid**; sliding the whole gun moves the character, rotating it aims (Namco operator's manual). Twin cab, one gun + monitor + Naomi board per player, linked. I/O: **Namco FCA-1 JVS board** ("Multipurpose + Rotary Encoder", 7 analog channels) — MAME: "uses Namco FCA JVS I/O (not dumped)" (naomi.cpp line 745). This is **not an optical lightgun**: "the NAOMI arcade release features no lightgun technology whatsoever… a three-axis joystick in the shape of a gun" (Wikipedia). MAME input ports: `naomi` (generic — the FCA gun is unemulated there). Flycast is the ground truth: `gunsur2_inputs` maps PITCH/ROLL/YAW as Full analog axes with no reload key (`naomi_roms_input.h:208`) and instantiates `jvs_namco_fca` **without** setting `lightgunGame` (`maple_jvs.cpp:1552`) — unlike Ninja Assault, Mazan, or HOTD2 — i.e. it is already played today as an analog-axes controller game.

Not `dc_peripheral` (75): the official DC light gun is an optical screen-position device with no analog axes — it cannot produce yaw/pitch/roll values or the slide-to-move input, so no official DC peripheral covers the cabinet interface as-is. The PS2 port's GunCon2 mode proves a gun peripheral *can* drive the game — but only after Namco/Nextech re-engineered the control layer for consoles (optical aim + button movement), which is exactly the remapping work `pad_adaptable` encodes, and the same port ships fully playable on a standard DualShock 2.

Proposed DC mapping: analog stick = yaw/pitch (aim), d-pad or L/R triggers = third axis (strafe/roll), A = trigger, B = gun button, Start = enter, with select up/down on remaining buttons — workable for a deliberately-paced shooter. A DC-gun control mode following the PS2 GunCon2 redesign is a plausible stretch goal, not the baseline. Recoil solenoid loss is cosmetic.

Sources: [Namco Gun Survivor 2 operator's manual](https://www.manualslib.com/manual/2251116/Namco-Gun-Survivor-2.html) (pitch/roll/yaw pots, trigger, solenoid, FCA PC board); MAME src/mame/sega/naomi.cpp @59e7c0b lines 741–747, 11142–11143; Flycast `naomi_roms_input.h:208` + `maple_jvs.cpp:1074–1089, 1552–1556` (`../cleopatra/tools/flycast-src`); [Wikipedia](https://en.wikipedia.org/wiki/Resident_Evil_Survivor_2_%E2%80%93_Code:_Veronica) (three-axis gun; PS2 GunCon2 + DualShock 2); [Highway Games](https://www.highwaygames.com/arcade-machines/gun-survivor-biohazard-8324/) (fixed guns, Naomi 1, twin cab); [Project Umbrella](https://www.projectumbrella.net/gun-survivor-2-biohazard-codeveronica.html) (Nextech, GunCon2, no NA release); in-binary test-menu strings (sidecar `guts.sdk_strings`).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 13.0^.40 · 68.6^.20 · 80.0^.20 · 50.0^.10 · 40.0^.10 = **33.4** (tier C)
Similarity inputs: developer no, SDK overlap partial, loader match no → 40.
Note: `developer_match = false` is a reference-list artifact — Nextech built both this and the DC Code: Veronica (§2), a stronger real-world match than the flag captures; recorded as a checkpoint data point (kb §6 item 4).

## 9. Risks & notes

- **Memory is the weak axis, and it is two-sided.** VRAM 1.92× and main 1.88× both sit just under the G3 gate. The mitigation path is unusually concrete: the DC original *is* the same game's source material — a port can lean on Code: Veronica's own DC-sized asset versions (models, rooms, textures) rather than inventing reductions. ARAM already fits exactly (§4).
- **Controls need a designed adaptation, not a mapping.** 3-axis gun + slide movement → one-stick DC pad is a real control-scheme design task; the PS2 port is the proven template (pad-native, GunCon2 optional). See kb §6 item 4 for the calibration question this raises.
- **Twin-cab comm layer:** MAME notes the Japan set "will crash if COMM.BOARD not present" (naomi.cpp line 745, BHF1 note). The World set demonstrably boots and attract-loops without any comm board — this clean single-board run is the evidence. Link-play code (`LINK ERROR`, master-data exchange strings) exists in the binary and would be stripped or stubbed in a port.
- `gunsur2j` needs no separate assessment: only the 2f ROM differs (§2).
- Boot-marker tooling gap found and fixed during this run (kb §4.n second gap, `2cc46ce`) — future Namco-header titles (ninjaslt, mazan, wldkicks) would have hit it too.
- Main-RAM v1 limitation carried from the spec: DMA high-water misses CPU-written data above the last DMA'd asset (watermark gap here is mild, 1.06×).
