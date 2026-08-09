# Noukone Puzzle Takoron (Japan) (GDL-0042) (`takoron`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **PARKED — `G3 memory: aram content > 2x DC capacity`** (not a numeric tier) |
| Bottom line | A genuinely large sound bank: 6,333,113 B of fill-excluded ARAM content (u = 3.02) stays well past the u > 2.0 gate under either keying, address or volume — and main RAM and VRAM are over cap too; the Wii recompile (*Octomania*) proves the game logic is portable, but DC memory budgets are the wall. |
| Assessed | capture 2026-08-07 · battery v6 · flycast `65f9f7857` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b`; aram-volume re-run 2026-08-07 · battery v7 · flycast `65f9f7857` |

## 2. Identity

| | |
|---|---|
| Set / family | `takoron` (covers: no clones — `parent: null` in controls.json; single ROM_START, security PIC `317-5127-jpn.pic`, standard NAOMIGD_BIOS + NAOMI_DEFAULT_EEPROM — MAME src/mame/sega/naomi.cpp @59e7c0b) |
| Maker / year | Compile Heart, 2006 — their only arcade title. GDL-0042 is the **last entry in MAME's GDL list** (naomi.cpp @59e7c0b line 11290), i.e. the final third-party Naomi GD-ROM release. The "publisher Milestone" hint is disproved: MAME, [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron) and [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37904-noukone-puzzle-takoron) all credit Compile Heart; no Milestone involvement documented ([Wikipedia](https://en.wikipedia.org/wiki/Octomania) silent on it) |
| Genre / format | Puzzle ★ (2×2-cursor octopus-rotating tile matcher), GD-ROM (GDL-0042, 52.6 MB) |
| Official DC port | No — ported to **Wii** instead, as *Octomania* / JP しゃるうぃ〜☆たころん (JP 2007-08-23, NA 2008-03-25; Wii port by Hyper-Devbox Japan, publishers Idea Factory/Conspiracy — [Wikipedia](https://en.wikipedia.org/wiki/Octomania), accessed 2026-08-03). No Dreamcast release |
| Community ports | None found (searched 2026-08-03) — not in the [Dreamcast Junkyard Naomi GD-ROM article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html) (checked: no Takoron/Octomania mention), no dreamcast-talk conversion threads surfaced |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`, GD DIMM ~1 MB bootstrap) · run 600 s ·
rom: `naomi/takoron.zip` (single clean zip leg)
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"`; the tutorial demo
renders (`shot-609s.png`).
Screenshots: `evidence/takoron/shot-060s.png` · `evidence/takoron/shot-365s.png` · `evidence/takoron/shot-609s.png`
Anomalies: the v2-era capture was display-blind (stale TA frame, kb §4.m — the game
verifiably ran underneath); v4+ captures render the demo.

## Gate

**G3 memory: aram content > 2x DC capacity** — the volume-keyed message (`score.py`
reports `metric="content"` whenever `content_total` is present); axes not computed
(`scores: null`).

`memory.aram.content_total = 6,333,113 B` (fill-excluded content volume, battery v7)
against the DC's 2,097,152 B AICA RAM → u = 3.02, still well past `region_score()`'s
`u > 2.0` gate. The §6 checkpoint's volume keying does not change the outcome: the
fill-excluded content-high address is 8,257,552 B (u = 3.94) with `nz_above_cap`
4,341,109 B of genuine sound content above the cap (v6: 4,347,346 B; v4: 4,336,179 B —
run-to-run jitter, not the DMPD fill artifact, kb §7). This is the clearest
reconfirmation in the wave: heavy content stays heavy under either keying — the
address-vs-volume distinction only mattered for the tiny-above-cap cohort (`gwing2`,
`sgtetris`), not for a genuinely large sound bank like this one.

Evidence: `assessments/takoron.metrics.json` → `memory.aram`; `guts.sdk_strings` shows
the Sega Naomi sound stack doing the bank load (`libsnd Ver.1.05a`, NAOMI LIBRARY /
nlam 2005 builds).

The gate is not the only memory problem — context values from the sidecar:
- Main RAM: write-truth peak 30,425,060 B (1.81×) · `nz_total` 17,119,948 B — the
  content volume alone is 1.02× the 16 MB cap (`nz_above_cap` 8,609,276 B), so even v9
  content keying would not clear main · `dma_high_water` 29,360,128 B = exactly
  `0x1C00000` (bit-identical v4→v6→v7) — the suspiciously round 28 MiB that strengthens
  the stream-cache-placement reading of the GD-title main-RAM clustering (kb §6 item 3);
  unlike `kurucham`/`ss2005`/`tetkiwam`, the write-truth peak shows no `0x1F00000`
  signature match here.
- VRAM: write-truth peak 15,222,784 B (1.81×) · nz_total 5,995,967 B with 5,969,423 B
  above the 8 MB line — an address-extent artifact of an asset store parked high (the
  `kurucham` pattern); a port would relocate it.
- Streaming: 75 DMA events · 62,215,616 B total / 39,146,944 B unique · re-read ratio
  0.3708 · steady-state 4.853 MB/min (`short_window: false`) · `pio_bytes` 4,195,648 B.
- Guts: code 4,194,304 B · 809 functions · MMIO refs scif 2 / rtc 4 / g2ext 30 · flags
  `eeprom_bios`/`serial`/`rtc`.
- Similarity inputs: `developer_match: false`, `sdk_overlap: "partial"` (NAOMI LIBRARY /
  NLOBJPUT / NLSPRITE, syHw/syG2 Katana-adjacent builds, KAMUI2/KAMUI-Darkness),
  `cart_loader_match: true`.

What would unblock it: a per-title audio trim (downsample the PCM banks / ADPCM) —
standard porting work with released-port precedent (the official Ikaruga DC port's 4×
sound trim, kb §4.d) — but main RAM and VRAM are over cap too, so a port is
trim-everything work in every region, not just the audio gate.

## Risks & notes

- **The code demonstrably moved off Naomi once** — portability-positive: Hyper-Devbox
  Japan built libraries to *recompile the original arcade source* for the Wii port
  ([Wikipedia](https://en.wikipedia.org/wiki/Octomania)), so the game logic is not
  hardware-welded, though DC memory budgets are the harder wall.
- **Streaming is light** — 75 DMA events, re-read ratio 0.3708, ~4.85 MB/min steady:
  the title is nearly self-contained after boot, a porting positive.
- **Controls are the easy axis**: `controls.device_class = stick`. The game's own INPUT
  TEST menu (in-binary, `guts.sdk_strings`) lists UP/DOWN/LEFT/RIGHT +
  ROTATE(L)/ROTATE(R)/CANCEL + START per player — one 8-way stick and three game
  buttons, 1:1 on a DC pad (d-pad + A/B rotate, X cancel, Start). Sources: MAME
  src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi`;
  [arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron)
  (8-way joystick + 6-button JVS standard declaration, 2P);
  [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37904-noukone-puzzle-takoron)
  (cursor movement + Main button rotate);
  [Wikipedia](https://en.wikipedia.org/wiki/Octomania) (Wii port: pointer + one rotate
  button).
- **Rendering must be verified on real DC hardware** (working-style rule) — the v2-era
  display blindness was a fork display-path gap (kb §4.m); the emulator-side diagnostic
  is the raw-VRAM decode recipe (`FLYCAST_VRAMDUMP` + `vramdump2png.py`, kb §4.m).
- `guts.code_bytes = 4,194,304` — exactly 4 MiB, *at* but not over the `code_over_4mb`
  threshold, so no penalty flag fired; a boundary case worth remembering if the carve
  is ever re-run.
- Main watermark 30,425,060 B (informational, stale-data-prone) is 1.04× the DMA
  high-water — mild; little content above the last DMA'd asset.
- MAME's own status for the set is preliminary / imperfect graphics + sound
  ([arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=takoron)) —
  consistent with a title whose 2D composition trips emulator display paths, not a
  broken game: it shipped in arcades and was recompiled for the Wii.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM (peak) | Full 8 MiB ARAM bank written at boot (4.00×) — fourth boot-time full-bank park in the campaign tally; capture display-blind (kb §4.m); fill root-cause kb §7 |
| v4 | 2026-08-04 | PARKED G3-ARAM (peak) | Park confirmed content-real: 4.14 MiB of genuine sound content above cap after fill exclusion — a real G3, not the fill artifact; tutorial demo renders — kb §7 |
| v6 | 2026-08-07 | PARKED G3-ARAM (peak) | Fresh capture reconfirms (4.15 MiB above cap, within jitter of v4); new datum: `dma_high_water` exactly `0x1C00000` — stream-cache-placement reading, kb §6 item 3 |
| v7 | 2026-08-07 | PARKED G3-ARAM (content) | §6 checkpoint volume keying doesn't clear it: `content_total` 6,333,113 B (u 3.02) — the park survives the re-keying that un-parked the tiny-above-cap cohort — kb §6 |
