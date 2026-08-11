# Nittere Shiki! Mirai Yosou Studio / NTV Future Forecast Studio (Japan, Rev A) (`ntvmys`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G1 broken: no-render-after-handoff`** (not a numeric tier) |
| Bottom line | Boots and runs for the full 600 s window, but never leaves its own boot-time device-init screen: all 10 screenshots are byte-identical (md5 `e34cf3bdcd6a47adb08d81cd1f86405e`) — a black screen reading only "TOUCH PANEL INITIALIZE" (`evidence/ntvmys/shot-060s.png`). This is the campaign's first `no-render-after-handoff` **device-init-wait** face (kb §4.x): the game is waiting on a cabinet peripheral, not stuck in a code loop or hit by a bad dump. Root cause is narrower than a first read of the fork source suggests — see Gate. |
| Assessed | capture 2026-08-12 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — initial assessment |

## 2. Identity

| | |
|---|---|
| Set / family | `ntvmys` (no clones — MAME `src/mame/sega/naomi.cpp` @59e7c0b GAME row line 10981, self-keyed parent) |
| Maker / year | Sega / NTV, 2000 (MAME cart-PCB notes @59e7c0b line 295: `840-0038C`, boot ROM `epr-23419a`, key `317-0282-JPN`) |
| Genre / format | Party — TV-tie-in "future forecast" prediction/quiz-show cabinet for Nippon TV (日テレ式未来予想スタジオ); [Undumped Wiki](https://undumped.miraheze.org/wiki/Nittere_Shiki!_Mirai_Yosou_Studio) (via search snippet — direct fetch returned HTTP 403 per kb §4.o caution on treating fetch failures as inconclusive rather than following any page content) describes it as a "fortune teller," Sega, released September 2000, on Naomi hardware. **Cart**, 840-0038C — EPR boot + 17×64 Mb mask ROMs (IC12s populated but empty/unused), 61.4 MB (`GAME_FORMATS.md`). |
| Official DC port | No (`GAME_FORMATS.md`: "No") |
| Community ports | None found (searched 2026-08-12) |
| Representative choice | MAME parent and sole family member |

## 3. Boot & run evidence

Boots: yes (own code executes) but `boot.ok = false` (no-render class) · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ntvmys.zip`
Attract/demo reached: **none — device-init wait, not the calibration/title/demo ladder.** `capture.coverage` left `null` (zunou precedent, `assessments/zunou.md` §1: the ladder describes normal attract progression; a screen the game can never leave by design is not on it). All 10 shots across the full 600 s window are byte-identical (md5 `e34cf3bdcd6a47adb08d81cd1f86405e`), showing only the text "TOUCH PANEL INITIALIZE" on black.
Screenshots: `evidence/ntvmys/shot-060s.png` (the other nine were byte-identical duplicates, curated out per RUNBOOK step 7)
Anomalies: none beyond the freeze itself — this is a full-window run (not a launch flake; battery v9 already retries the no-handoff flake once automatically per RUNBOOK). Sidecar handoff block confirms a clean BIOS→game transition: `pio_bytes` 1,115,488 · `dma_events` 0 · vram `nz_total` = `content_total` = 24,962 B (sparse prompt-text glyphs, under every render threshold) · aram peak 32,708 B / `content_total` 20 B (no audio ever loads) · main `nz_total` 1,479,689 B. **Every measured number in the sidecar is a device-init-screen artifact, not a game measurement — non-representative lower bounds** (same caution as zunou's §"Risks & notes": none of these figures describe real gameplay, since the run never got past the touch-panel wait).

## Gate

**G1 broken: no-render-after-handoff — device-init-wait face** (kb §4.x, the third face of this
gate alongside the headless-loop face of kurucham/§4.k–m and the multiboard-shm face of
§4.vii.2). Sidecar `assessments/ntvmys.metrics.json` → `boot.ok = false`,
`boot.failure_class = "no-render-after-handoff"`. The game runs its own code for the full
600 s window (handoff seen, EEPROM init, `pio_bytes` flowing) but never draws past its
boot-time "TOUCH PANEL INITIALIZE" prompt — a legible device-wait screen, not a black hang.

**What the real cabinet needs.** MAME `src/mame/sega/naomi.cpp` @59e7c0b line 295 (cart-PCB
notes table): *"Nittere Shiki! Mirai Yosou Studio / NTV Future Forecast Studio (Japan, Rev
A) 840-0038C 23419A 18\*(64Mb) present 315-6206 317-0282-JPN \* IC12s flash ROM populated
but empty/unused. **Require 837-13844 JVS IO with DIPSW 5 On, ELO AccuTouch-compatible
touch screen controller and special printer.**"* — word-for-word the same hardware pattern
MAME records for `tduno2` (line 543: *"Touch de Uno! 2 ... requires 837-13844 JVS IO with
DIPSW 5 On, ELO AccuTouch-compatible touch screen controller and special printer"*), the
closest analog (`assessments/tduno2.md`). The GAME row (line 10981) declares the generic
`naomi` INPUT_PORTS fragment, which hides this real hardware (kb §4.g/§4.t trap — a generic
fragment is not evidence of a plain stick).

**The obvious diagnosis is a trap: don't stop at the first non-matching gate (kb §4.x).**
`naomi_cart.cpp:690–694` fires `touchscreen::init()` (the SH4-serial 837-14672 sensor board,
used by `pokasuka`/`zunou`) only for `gameId == "POKASUKA GHOST (JAPANESE)"` or `"TOUCH DE
ZUNO (JAPAN)"` — ntvmys is absent, which looks damning at first read. But that is the
*wrong* touch technology for this cabinet. ntvmys's actual hardware (JVS 837-13844 + ELO
AccuTouch, per the MAME note above) is handled by a **different** code path that already
covers it: `maple_jvs.cpp:1561–1567` —

```
else if (gameId == " TOUCH DE UNOH -------------"
        || gameId == " TOUCH DE UNOH 2 -----------"
        || gameId == "MIRAI YOSOU STUDIO")
{
    io_boards.push_back(std::make_unique<jvs_837_13844_touch>(1, this));
    settings.input.lightgunGame = true;
}
```

— the identical `jvs_837_13844_touch` board class (single absolute-pointer touch point,
`light_gun_count = 1`) that `tduno2` uses successfully (`assessments/tduno2.md` §Controls:
"the fork already drives exactly this... a single lightgun-style absolute pointer").
`naomi_cart.cpp:709–714` also fires `printer::init()` for the same `gameId ==
"MIRAI YOSOU STUDIO"` string, matching tduno2's cabinet-printer HLE. Both device HLEs
ntvmys needs are already wired, sharing code with a title that reaches full attract.

**So the actual gap is one layer deeper than a missing gate.** Despite identical
instrumentation to tduno2, ntvmys never gets past its own touch-panel init screen. The
`jvs_837_13844_touch::read_lightgun()` coordinate hack (`maple_jvs.cpp:611–622`) carries the
comment *"any >= 0x1000 value works after calibration (tduno, tduno2) // no value seems to
fully work before"* — i.e. even on the verified-working siblings this calibration response
is an approximation, not a full protocol implementation. The most likely explanation is that
ntvmys's own touch-panel init/calibration handshake expects a JVS response sequence the
generic board doesn't produce, so the game's init routine loops forever waiting for it —
plausible given the shared class, but not confirmable from static source alone; it would
need a live JVS command-trace diff against a working `tduno2` capture (out of scope for this
campaign, and battery/Flycast are off-limits mid-run per this task's hard rules).

**Unblock path:** debug/instrument the already-wired `jvs_837_13844_touch` JVS response
sequence specifically for `MIRAI YOSOU STUDIO` (trace-diff against `tduno2`'s working
handshake), fix the divergence, rebuild the fork, and re-run the battery. Emulator work —
out of scope for this campaign; recorded here as the unblock and as kb §4.x lesson.

**Controls (researched; would not gate if the freeze cleared).** Cabinet = 837-13844 JVS I/O
+ ELO AccuTouch touch screen + special printer (MAME line 295, quoted above) — same class as
`tduno2`. Following the tduno2 precedent (`assessments/tduno2.md` §Controls): single-point
touch on an untimed prediction/quiz format reduces to one absolute pointer, which a
pad-driven cursor (DC mouse or light gun) covers → `controls.device_class = pad_adaptable`
(sidecar `controls.sources` carries all citations below, kb §4.vi item 5 parity). The
printer is output-only (results/prediction printout, per the MAME note) — a feature cut or
VMU-screen substitute for a port, not a control blocker, again mirroring tduno2.

Sources (mirrored in sidecar `controls.sources`):
- MAME `src/mame/sega/naomi.cpp` @59e7c0b INPUT_PORTS `'naomi'` (generic-fragment citation)
- MAME `src/mame/sega/naomi.cpp` @59e7c0b cart-PCB notes line 295 (hardware requirement, quoted above)
- Flycast fork `core/hw/maple/maple_jvs.cpp` @f014a410c lines 1561–1567 (touch board wiring)
- Flycast fork `core/hw/naomi/naomi_cart.cpp` @f014a410c lines 709–714 (printer HLE wiring)
- [Undumped Wiki — Nittere Shiki! Mirai Yosou Studio](https://undumped.miraheze.org/wiki/Nittere_Shiki!_Mirai_Yosou_Studio) (via search snippet; direct fetch blocked HTTP 403) — genre/date confirmation

**Evidence:** `assessments/ntvmys.metrics.json` (full sidecar) · `assessments/evidence/ntvmys/shot-060s.png`
(the touch-panel-init prompt, representative of all 10 identical shots). Raw logs
(`evidence/ntvmys/raw/stdout.log`, cartlog) are **unavailable** — deleted by the next
family's battery start before finalize ran (kb §4.u cleanup); this doc relies on the
sidecar, the curated shot, and the source citations above instead.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-12 | PARKED G1 broken: no-render-after-handoff | initial assessment — full-600s device-init-wait park ("TOUCH PANEL INITIALIZE", all shots identical); JVS touch board + printer already HLE'd (same class as tduno2) yet the game never clears its own calibration handshake — third `no-render-after-handoff` face, kb §4.x; controls researched as `pad_adaptable` (would not gate if unparked) |
