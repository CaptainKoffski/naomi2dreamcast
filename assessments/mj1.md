# Sega Yonin Uchi Mahjong MJ (Update Disc Ver.1.008, Japan) (CDP-10002B) (`mj1`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G1 broken: no-render-after-handoff`** (not a numeric tier) |
| Bottom line | Runs a full 600 s window (`assessments/mj1.metrics.json` → `boot.ok = false`, `boot.failure_class = "no-render-after-handoff"`) but never leaves its own network-bring-up screen: all 10 screenshots are byte-identical (md5 `5dc29db92ca6f5a3972f823544ce66fc`) — a black screen reading "DHCP error. retry." (`evidence/mj1/shot-060s.png`). A DHCP-wait park, the network sibling of the device-init-wait face documented for `ntvmys` (kb §4.x) — but even a fixed network stack has nowhere to dial: this cabinet is a satellite terminal of Sega's own 2002-era MJ online matchmaking service, decommissioned for two decades, and a CRP-1231 magnetic-card terminal, same reader family as the excluded `wccf` card-terminal titles. |
| Assessed | 2026-08-12 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `mj1` — covers `mj1a`–`mj1e` (CDP-10002A–E, all owned, MAME `naomi.cpp` @59e7c0b ROM_STARTs lines 10502–10562, GAME rows lines 11296–11300). **Note:** `mj1` is *also* the softname MAME uses for the true parent, CDP-10002F/Ver.3.000 (GAME line 11301) — **not owned** by this dump (GAME_FORMATS.md footnote, 2026-08-12 Nikita import). This doc's `mj1` is a different thing: it is Flycast's **catalog** entry name (`../cleopatra/tools/flycast-src/core/hw/naomi/naomi_roms.cpp` line 6117), which is independently pinned to CDP-10002B content — i.e. MAME's `mj1b` revision, not MAME's `mj1` (CDP-10002F) parent. Two different games share the softname `mj1` across MAME and Flycast; see Gate for how that was resolved. |
| Maker / year | Sega, 2002 (MAME GAME line 11297: `mj1b`, year 2002; CDP-10002B is the earliest owned revision) |
| Genre / format | Mahjong ⚠, GD-ROM (`naomigd`) |
| Official DC port | No (GAME_FORMATS.md: `No` on every `mj1a`–`mj1e` row) |
| Community ports | None found (searched 2026-08-12) |
| Representative choice | **Override, not the newest-owned-revision default.** QUEUE.md originally picked `mj1e` (CDP-10002E, newest owned) as representative. `mj1e` parks instantly (`emulator-exited`) because Flycast's catalog (`naomi_roms.cpp`) has exactly one entry for this whole family, hardcoded to the set name `mj1` and pinned to disc `cdp-10002b` + PIC `317-0352-jpn.pic` — none of `mj1a`–`mj1e` are catalog set names Flycast recognizes, so all five park identically as "Unknown game" (verified for `mj1e`; the identical-PIC, catalog-miss condition applies to all five by construction). To get a real measurement instead of a naming artifact, this assessment presents owned CDP-10002B content under Flycast's catalog name `mj1` (method below) — content-equivalent to MAME's `mj1b`. `mj1e` is therefore superseded as representative by `mj1` for this doc; see QUEUE.md addenda for the formal override note. |

## 3. Boot & run evidence

**Run 1 (superseded, both legs `mj1e`):** exited instantly, `PARKED G1 broken: emulator-exited`. Root cause: `../cleopatra/tools/flycast-src/core/ui/gui.cpp:1358` → `ERROR_LOG(BOOT, "%s", ex.what())` printing `E[BOOT]: Unknown game`, thrown by `naomi_cart.cpp:218` (`throw NaomiCartException(Ts("Unknown game"))`) when the loader can't match the mounted set name against the catalog. Not a measurement of the game — a catalog-naming miss (see Gate).

**Run 2 (this doc's measurement, set `mj1`):** Boots: yes (own code executes, `boot.ok = false` is the no-render class, not a boot failure) · handoff at 20.0 s (`trigger = "pio"`) · run 600 s (full window; battery v9's automatic no-handoff-flake retry was not needed — this is a deterministic full-window park) · rom: `naomi/mj1.zip`. Game identification confirmed in `assessments/evidence/mj1/raw/stdout.log:17`: `hw/naomi/naomi_cart.cpp:666 N[NAOMI]: NAOMI GAME ID [MJ JAPAN] region 1 players 0 vertical 0`.
Attract/demo reached: **none — network-bring-up wait, not the calibration/title/demo ladder** (ntvmys/zunou precedent, `assessments/ntvmys.md` §3). `capture.coverage` left `null` in the sidecar; **every figure below is a non-representative lower bound** — the run never reached gameplay.
Screenshots: `evidence/mj1/shot-060s.png` (the other nine were byte-identical duplicates, curated out per RUNBOOK step 7). All 10 shots md5 `5dc29db92ca6f5a3972f823544ce66fc`: black screen, text "DHCP error. retry." — the game boots, brings up its own network stack, fails to get a DHCP lease from Flycast's (non-existent) virtual network, and loops the retry screen forever.
Anomalies: none beyond the freeze itself. Sidecar confirms a clean BIOS→game handoff and active but non-productive execution: `pio_bytes` 2,100,096 · `dma_events` 2 (63,456 B total/unique, `reread_ratio` 0.0) · vram `content_total` 18,035 B (sparse prompt-text glyphs, under every render threshold) · aram peak 8,257,552 B but `content_total` only 37,070 B (audio bank loaded, barely touched — consistent with a title screen jingle, not gameplay) · main `nz_total` 1,588,901 B, `dma_high_water` 23,656,448 B (~22.6 MB, over the 16 MB DC cap — informational watermark only, not a scored figure for a parked title).

## Gate

**G1 broken: no-render-after-handoff — DHCP-wait face, network sibling of the device-init-wait face (kb §4.x).** Sidecar `assessments/mj1.metrics.json` → `boot.ok = false`, `boot.failure_class = "no-render-after-handoff"`. `score.py assessments/mj1.metrics.json` → `mj1 PARKED G1 broken: no-render-after-handoff`.

**How the measurement was obtained (catalog-naming artifact, then a reproducible shim — kb lesson, item y).** Flycast's fork catalog (`../cleopatra/tools/flycast-src/core/hw/naomi/naomi_roms.cpp` lines 6113–6129) carries exactly **one** entry for this entire five-revision update-disc family:

```
    // Sega Yonin Uchi Mahjong MJ (セガ四人打ち麻雀MJ), "Sega The 4Players Mah-Jong"
    // uses CRP-1231 card RW connected via 838-13661 RS422/RS232C converter BD, and 2x JVS I/O boards (or one special I/O ?).
    {
        "mj1",
        nullptr,
        "Sega Yonin Uchi Mahjong MJ (Update Disc Ver.1.008, Japan) (CDP-10002B)",
        0x4000, 0, "naomi", GD, ROT0,
        { { "317-0352-jpn.pic", 0, 0x4000, 0xc2c45f9c } },
        "cdp-10002b",
    },
```

— set name `mj1`, disc `cdp-10002b`, PIC `317-0352-jpn.pic` (0x4000, CRC `c2c45f9c`). That disc/PIC pair is content-identical to MAME's `mj1b` (MAME `naomi.cpp` @59e7c0b lines 10514–10524: `ROM_START( mj1b )`, disc `cdp-10002b`, same PIC filename/CRC). None of `mj1a`–`mj1e` (the actual owned set names) match this catalog entry, so mounting any of them under their own name throws `naomi_cart.cpp:218`'s `Unknown game` exception (confirmed for `mj1e`, run 1 above) — a catalog-naming miss, not a dump or emulation problem.

The reproducible fix (all gitignored, per CLAUDE.md rule 5 — never commit the copyrighted bytes, only the method):
1. `naomi/mj1.zip` = copy of `naomi/mj1b.zip` — contains exactly `317-0352-jpn.pic` (16,384 B), the same PIC file present in every `mj1a`–`mj1e` zip (byte-identical across all five revisions, confirmed by the shared CRC `c2c45f9c` in every MAME ROM_START for this family).
2. `naomi/mj1/cdp-10002b.chd` = symlink → `../mj1b/cdp-10002b.chd`.
3. `python3 tools/assess/run_battery.py mj1` — Flycast now recognizes the set, mounts real owned content (CDP-10002B, MAME `mj1b`-equivalent), and the run proceeds to a genuine 600 s measurement instead of an instant catalog-miss exit.

This presents **owned bytes** under Flycast's catalog name; no ROM content was altered, invented, or sourced externally — only container naming (zip/symlink) changed, entirely within the gitignored `naomi/` tree.

**Structural blockers beyond the DHCP wait (would still park even with a perfect network stack):**
1. **Magnetic-card terminal.** The same catalog comment above: *"uses CRP-1231 card RW connected via 838-13661 RS422/RS232C converter BD, and 2x JVS I/O boards (or one special I/O ?)."* CRP-1231 (Sanwa CRP-1231BR-10/LR-10NAB) is a magnetic-stripe card reader/dispenser, 3 data tracks × 69 B ([GXTX/YACardEmu](https://github.com/GXTX/YACardEmu)) — the same reader family as the excluded `wccf` card-terminal titles (`assessments/dragntr.md` §Gate cites the analogous SAXA HW210 IC-reader case for `dragntr`; `campaign-family-exclusions` ruling excludes `wccf` outright for this reason). A player card is how the cabinet tracks identity/points/ranking across the network.
2. **Decommissioned matchmaking service.** This is a client of Sega's original MJ network service launched with this 2002 cabinet generation — the era the DHCP-wait screen is trying to reach. [Wikipedia — Sega Network Taisen Mahjong MJ](https://en.wikipedia.org/wiki/Sega_Network_Taisen_Mahjong_MJ) documents the franchise's satellite-terminal / national-ranking network architecture across its NAOMI2 → Chihiro → Lindbergh → RingEdge lifespan; the original 2002-era NAOMI service this cabinet dials into is long retired. Even a fully correct virtual-network implementation in Flycast has no live server on the other end.

**What would unblock:** MJ network-service emulation (a from-scratch server reimplementation of a 24-year-old proprietary protocol) *and* CRP-1231 card-reader HLE, simultaneously — both out of scope for this campaign. Structurally the same category as `dragntr` (net-medal) and `wccf` (card-terminal): a networked satellite terminal, not a standalone game with a DC-mappable control surface.

**Controls (researched; would not clear the gate above even if satisfied).** `controls.device_class = "card_reader"` (off-ladder, dragntr-style raw-hardware-name convention — `score.py`'s `CONTROLS` ladder only covers `stick`/`dc_peripheral`/`pad_adaptable`/`awkward`; a physically unmappable input surface gets the raw hardware name instead, per RUNBOOK §2 and `assessments/dragntr.md`'s `medal_hopper` precedent). Sources (mirrored in sidecar `controls.sources`, kb §4.vi item 5 parity):
- MAME `src/mame/sega/naomi.cpp` @59e7c0b line 10501 (cart-PCB comment, quoted above): CRP-1231 card RW + 838-13661 RS422/RS232C converter + 2x JVS I/O boards.
- Flycast fork `core/hw/naomi/naomi_roms.cpp` @f014a410c line 6115 (identical catalog comment).
- [GXTX/YACardEmu](https://github.com/GXTX/YACardEmu) — CRP-1231BR-10/LR-10NAB confirmed as a magnetic-stripe card reader/dispenser (3 tracks × 69 B), the same reader family used across Sega NAOMI/Chihiro/Triforce network cabinets (Initial D3, WMMT, Mario Kart Arcade GP).
- [sega.jp official arcade history page](https://www.sega.jp/history/arcade/product/17883/) (via search snippet; direct fetch blocked HTTP 403 per kb §4.o — not followed as page content per that caution) — describes the cabinet control panel as touchscreen tile-selection plus dedicated hard buttons (an "agari"/win button specifically called out), consistent with the MJ1-era panel style.
- [Wikipedia — Sega Network Taisen Mahjong MJ](https://en.wikipedia.org/wiki/Sega_Network_Taisen_Mahjong_MJ) — series/network-architecture confirmation; notes MJ5 (a later hardware generation) added multi-touch, implying this MJ1-era cabinet used the touchscreen+hard-button combo above rather than full multi-touch.

Even granting a mappable touchscreen+button surface, the card-reader identity/points system and the dead matchmaking service are the actual, permanent gates — controls research is recorded for completeness only, mirroring `dragntr`'s treatment.

**Evidence:** `assessments/mj1.metrics.json` (full sidecar) · `assessments/evidence/mj1/shot-060s.png` (the DHCP-retry screen, representative of all 10 identical shots) · `assessments/evidence/mj1/raw/stdout.log` (GAME ID line 17; not committed, gitignored raw capture per RUNBOOK).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-12 | PARKED G1 broken: emulator-exited (as `mj1e`) | Run 1: catalog-naming miss — `mj1e` not a Flycast catalog set name, "Unknown game" (`gui.cpp:1358` / `naomi_cart.cpp:218`). Superseded, not a measurement. |
| v9 | 2026-08-12 | PARKED G1 broken: no-render-after-handoff (as `mj1`) | Run 2: owned CDP-10002B content presented under Flycast's catalog name `mj1` (gitignored zip+symlink shim); full 600 s run, deterministic DHCP-wait park — network sibling of ntvmys's device-init-wait face (kb §4.x/§4.y). Structural blockers (CRP-1231 card terminal, decommissioned MJ network service) recorded as the real, permanent gate. Representative overridden from `mj1e` (newest owned, uncatalogued) to `mj1` (catalog-recognized, `mj1b`-equivalent content). |
