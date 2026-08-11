# Oinori-daimyoujin Matsuri (`oinori`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | ARAM `content_total` = 7,845,933 B → utilization **3.741** — **3rd-highest of the now 26-strong parked ARAM cohort** (only `slashout` 3.756 and `vonot` 3.746 run hotter), and the **18th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1), the first from the ⚠ tail. Not a sole-blocker: main content u **1.214** is also over cap (VRAM **0.767** fits). And unlike the cohort's unpark candidates, softening the ARAM rule would only advance it to the next wall: this is satellite software for the OND CRX MATSURI **medal pusher** machine (MAME 837-14391-01 SATL BD) — `medal_hopper` controls, the `kick4csh` G2 class; here G3 simply fired first. Not a port target under any plausible rule change. |
| Assessed | capture 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `oinori` (no clones — MAME src/mame/sega/naomi.cpp @59e7c0b `GAME()` line 11023, `/* 0126 */`, parent `naomi`, machine `naomim2`) |
| Maker / year | Sega, 2003 (MAME `GAME()` row) — in-cart version string `OND - MATSURI -  VER 2003/08/26` |
| Genre / format | Gambling/medal ⚠ (`GAME_FORMATS.md`) — satellite software of the *Oinori-daimyoujin Matsuri* multi-station medal pusher (ROM comment lines 6135–6136: "(medal)", "837-14391-01 SATL BD OND CRX MATSURI"; stations networked via ARC-NET per [Arcade-Projects NetBoot list](https://www.arcade-projects.com/threads/sega-naomi-netboot-games-list-working-not-working-untested-missing.15076/page-2)), **cart** 36.4 MB, Naomi M2 (315-5881 not populated, key `-1`) — carve title `OINORI DAIMYOJIN - MATSURI -` |
| Official DC port | No |
| Community ports | None found (searched 2026-08-11) — even emulation stalls at the satellite error screen ([libretro/flycast #897](https://github.com/libretro/flycast/issues/897)) |
| Representative choice | Sole set of the family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/oinori.zip`
Attract/demo reached: **calibration-class static screen** — sidecar `capture.coverage = "calibration"`
(battery wrote `null`; set after screenshot review). The satellite boots into its self-test and sits
in **ERROR MODE** for the entire run: `SATE. [004] RAM IS BAD — B.RAM READ/WRITE ERROR (EVEN)`,
"PRESS RESET SWITCH TO ERROR CLEAR" (`shot-060s.png`). All ten shots show the identical screen with
only the on-screen RTC advancing 21:36:01 → 21:45:07 (error latched 21:35:18, pre-first-shot) —
a live 600 s run, not a hang. Attract was never reached; a `--secs 900` re-run per the
representativeness rule would not help — clearing the error needs the cabinet's physical RESET
switch and the satellite's battery-backed B.RAM, not more time.
Screenshots: `evidence/oinori/shot-060s.png` · `shot-304s.png` · `shot-609s.png` (first/mid/last;
the other seven identical frames curated out).
Anomalies: the error screen is expected under emulation, not a tooling fault — the game probes the
satellite board's backup RAM, which Flycast does not emulate (same symptom reported in
[libretro/flycast #897](https://github.com/libretro/flycast/issues/897)). `kick4csh` only ran
because the fork HLEs its 837-14438 hopper board (`core/hw/naomi/hopper.cpp` `init()` is gated on
gameId `"KICK '4' CASH"`, line 1279 @4b59eceff); no such HLE exists for the OND SATL BD. All
memory figures are therefore **error-mode lower bounds** — which only strengthens an over-cap park
(the 7.85 MB ARAM bank was loaded at boot, before the satellite check failed).

## Gate

**G3 memory: aram content > 2x DC capacity.** `memory.aram.content_total = 7,845,933 B`
(fill-excluded content volume, §6 volume keying) against the DC's 2,097,152 B AICA RAM →
utilization **3.741** — past `region_score()`'s `u > 2.0` gate, **3rd-highest of the 26-strong
parked ARAM cohort**: between `vonot` 3.746 and `dybbnao` 3.729, under cohort max `slashout` 3.756.
This is the **18th G3-aram park of the 2026-08-11 sweeps** (kb §6 item 1 tallied 17 in the non-⚠
sweep; oinori extends it into the ⚠ tail) and the cohort's first Gambling/medal ⚠ member.
`nz_above_cap` = 5,854,186 B (address-keyed placement figure, informational). Address peak
8,282,256 B (u 3.949, pre-volume-keying read — the usual near-full 8 MiB bank, loaded at boot even
though the run never left the error screen).

The other two regions, quoted from the sidecar — **not a sole-blocker**: main content is over cap
too (only VRAM fits), so oinori sits outside the cohort's 10-member ARAM-sole-blocker unpark
shortlist:

| Region | Fit value | DC cap | u | Note |
|---|---|---|---|---|
| Main RAM (content volume) | 20,368,724 | 16,777,216 | **1.214** | `nz_total` — over cap, under the 2× gate; `nz_above_cap` (address-placement) 10,603,661 B · `dma_high_water` 31,169,824 B (u 1.858) · watermark/peak 31,504,320 B (u 1.878) |
| VRAM (content volume + 2×fb) | 6,430,876 | 8,388,608 | **0.767** | `content_total` 5,202,076 + 2×`fb_bytes` (2×614,400, standard double-buffered 640×480×2) — fits with 23% headroom; raw `nz_total` 5,395,193 (u 0.643) · address peak 10,646,828 (u 1.269) |
| ARAM (content volume) | 7,845,933 | 2,097,152 | **3.741** | the gate — see above |

Streaming context: 5,683 DMA events · 71,962,624 B total · 37,388,288 B unique · re-read ratio
0.4804 · steady-state 0.0 MB/min (`short_window: false`) · `pio_bytes` 92,144,960 B (PIO-heavy
loader, consistent with the error-mode idle after boot).
Guts: carve 4,063,232 B (`carve_meta.title = "OINORI DAIMYOJIN - MATSURI -"`) · 2,720 functions ·
MMIO refs rtc 3 / g2ext 110 / scif 2 · flags `eeprom_bios`/`serial`/`rtc` — the g2ext count and the
cart's `GAPSG2-MEMORY IF` / ARC-NET error strings reflect the multi-satellite network wiring.
Similarity: `developer_match: false`, `sdk_overlap: "partial"`, `cart_loader_match: false`.

**Controls (one line, off-ladder — `medal_hopper`, does not gate because G3 fired first):** a
medal/matsuri pusher satellite — MAME's machine config wires **no** hopper board (plain `naomim2` +
generic `naomi` inputs, naomi.cpp @59e7c0b line 11023 — unlike `kick4csh`'s `naomim1_hop` with the
837-14438 "SH I/O BD" hopper controller, line 11029); the medal hardware instead sits behind the
837-14391-01 SATL BD (ROM comment lines 6135–6136), and the cart's own I/O test menu names it:
`MEDAL_IN_SENSOR_L/R`, `CHECKER_SENSOR_L/R`, `WINDMILL_SENSOR/MOTOR`, `TRAY`/`PUSHER`
sensors+motors, `BELL_STRING_X/Y/LIMIT`, shutter, M/B HOPPER error table, "PLEASE SETUP SATELLITE
ID" (sidecar `guts.sdk_strings`). `kick4csh` precedent parked **G2 `medal_hopper`**; here the same
class is recorded in `controls.device_class` but `score.py` checks memory before controls, so G3
fired first. Sources (full parity in sidecar `controls.sources`): MAME naomi.cpp GAME()/ROM rows ·
cart I/O strings · [Arcade-Projects NetBoot list](https://www.arcade-projects.com/threads/sega-naomi-netboot-games-list-working-not-working-untested-missing.15076/page-2) ·
[libretro/flycast #897](https://github.com/libretro/flycast/issues/897).

**What would unblock it:** nothing plausible — the blockers stack. A kb §6 item 1 ARAM-gate
softening (the sound-trim argument) still leaves main content 1.214× over cap in error-mode idle
(a lower bound), and clearing G3 only advances the sidecar to **G2 `medal_hopper`**: the physical
game *is* the pusher floor — medals, hoppers, windmill, bell strings — with no DC-mappable core
loop, and it demands its satellite board (B.RAM + ARC-NET master) just to leave the error screen.
Mirror of `kick4csh`: excluded by hardware class, not by trimmable assets.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED G3 memory: aram content > 2x DC capacity | initial assessment — ARAM u 3.741, 3rd-highest of 26-strong cohort, 18th G3-aram park of the 2026-08-11 sweeps (first ⚠); not sole-blocker (main 1.214 over, VRAM 0.767 fits); medal-pusher satellite (837-14391-01 SATL BD, naomi.cpp 6135-6136) ran 600 s in B.RAM ERROR MODE (coverage calibration ⚠, flycast#897) — figures are lower bounds; `medal_hopper` recorded, G3 fired before kick4csh's G2 |
