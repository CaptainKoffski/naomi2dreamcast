# Kick '4' Cash (Export) (`kick4csh`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G2 controls: medal_hopper`** (not a numeric tier) |
| Bottom line | Kick '4' Cash is a UK/Export **cash-gambling machine**, not a video game with a mappable control surface: a Sega Amusements Europe "CashCube" video SWP (Skill With Prize) cabinet where the player stakes £1.00 per free-kick round and winnings are paid out as real coins by a mandatory 837-14438 "SH I/O BD" hopper controller. The payout hardware **is** the game loop — £ stake / PRIZE / "TODAY'S PAY" accounting on screen, BET/WIN/PAID counters, hopper config menus and the full `_M2H_`/`_H2M_` hopper serial protocol in the ROM — and the battery only ran because the Flycast fork HLE-emulates the hopper board in software. Even ignoring the gate, the provisional pre-gate score was 31.6 (C): ARAM content is 2.00× DC capacity (4,193,334 B vs 2 MB — 970 B under the G3 line) and VRAM content+2·FB is 8.68 MB vs 8 MB. |
| Assessed | 2026-08-11 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `kick4csh` (no clones — single set in MAME @59e7c0b; `mame.lst` line 41057 lists only `kick4csh`) |
| Maker / year | Sega (Sega Amusements Europe), 2004 · cart 840-0140C, security PIC 317-0397-COM (MAME naomi.cpp @59e7c0b line 528) |
| Genre / format | Gambling/medal ⚠ (video SWP — Skill With Prize; football free-kick betting), cart (Naomi M1, 16×64 Mb) |
| Official DC port | No |
| Community ports | None found (searched 2026-08-11; only emulator support exists — the Flycast/DEMUL hopper-board HLE) |
| Representative choice | Only set in the family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`pio` trigger) · run 600 s · rom: `naomi/kick4csh.zip`
Attract/demo reached: **demo reached** — the attract tutorial/demo cycle runs (free-kick
demo with defenders and shot timer, `evidence/kick4csh/shot-487s.png`; trackball tutorial
`shot-243s.png`; payout screens `shot-304s.png`, `shot-365s.png`).
Screenshots: `evidence/kick4csh/shot-{060,243,304,365,487}s.png` (curated from 10).
Anomalies: leg 1 flaked (`emulator-exited`); the automatic retry booted clean and ran the
full 600 s window — sidecar reflects the clean leg.

## Gate

**G2 controls: `medal_hopper` — cash-payout hardware core to the game loop, permanent.**
`score.py` output: `kick4csh PARKED G2 controls: medal_hopper`.

- **Mandatory hopper controller (primary source):** MAME `src/mame/sega/naomi.cpp`
  @59e7c0b line 528 (cart table): Kick '4' Cash, 840-0140C, 317-0397-COM — *"requires
  837-14438 'SH I/O BD' hopper controller"*. The GAME row (line 11029) mounts machine
  `naomim1_hop`, defined at lines 2554–2563 as *"Naomi M1 with 837-14438 'SH I/O BD'
  hopper board"* (`SEGA837_14438` device, `src/mame/sega/segashiobd.cpp` — an SH4-based
  I/O board with its own program ROM). MAME's input ports are the generic `naomi`
  placeholder — not cabinet evidence.
- **Payout is the loop, not a side feature:** £1.00-per-game stake and £ coin-in meter on
  every screen (`shot-060s.png`), PRIZE meter and per-coin-denomination bonus accounting
  (`shot-304s.png`), "TODAY'S PAY" payout tally (`shot-365s.png`). The ROM carries the
  complete main↔hopper serial vocabulary — `_M2H_CONFIG_HOP`, `_H2M_COIN_IN`,
  `_H2M_COIN_OUT`, `_H2M_PAY_WIN`, "WAITING FOR HOPPER BOARD RESPONSE", "HOPPER SIZE",
  "AUTOMATIC PAYOUT", "MEDAL EXCHANGE RATE", "HOPPER EMPTY/JAM", BET0–2/WIN/PAID/CREDIT
  operator counters (sidecar `guts.sdk_strings`). An SWP machine with the payout stubbed
  is a free-play curiosity, not the game.
- **Why the battery could run at all:** the Flycast fork HLEs the hopper board —
  `core/hw/naomi/naomi_cart.cpp` @f014a410c lines 716–721: `gameId == "KICK '4' CASH"` →
  `hopper::init()`; `core/hw/naomi/hopper.cpp` lines 1276–1285 select
  `Sega837_14438Hopper` (lines 345–350) for this gameId and pipe it into the SCIF serial
  port. Matches sidecar `guts.flags` `serial` + `mmio_refs.scif = 39`. The 837-14438
  board supports cash currencies, not just medals (`hopper.cpp:236` currency enum incl.
  pound / "any cash (837-14438 only)") — consistent with the Export £ market.
- **Cabinet controls (for the record):** the real panel is a **trackball + ENTER +
  CHANCE buttons** — the attract tutorial literally instructs "Spin the track ball."
  (`shot-243s.png`) and every panel graphic shows the trackball flanked by the two
  buttons (`shot-060s.png`, `shot-487s.png`). The fork's `kick4csh_inputs`
  (`core/hw/naomi/naomi_roms_input.h:623`) maps only VIEW/CHANCE/START buttons with no
  analog axes — a fork simplification, not cabinet truth. The trackball alone would be
  mappable (DC mouse) — it is **not** the gate; the hopper is.
- **Cabinet identity:** Sega Amusements Europe "CashCube" video SWP cabinet, released
  June 2004 ([Highway Games news](https://www.highwaygames.com/arcade-news/football-swp-winner-with-sega-s-kick-4-cash-1585/)).

**What would unblock:** nothing realistic. A DC build could stub the hopper protocol the
same way the fork does, but a stake→cash-payout machine has no meaningful DC form; G2 is
the campaign's deliberate park for payout hardware core to the game loop.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-11 | PARKED `G2 controls: medal_hopper` | First assessment (⚠ genre, run by explicit user order). Booted and ran the full 600 s window (leg-1 `emulator-exited` flake, auto-retry clean; fork HLEs the 837-14438 hopper board). Controls research ruled the mandatory cash hopper core to the game loop → off-ladder `medal_hopper`, provisional 31.6 C superseded by the G2 park |
