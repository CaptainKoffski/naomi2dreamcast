# Kasei Channel Mars TV (Japan) (840-0025C) (`marstv`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **74.6 (A)** |
| Bottom line | Sega AM3's 3-player Bishi Bashi-style minigame collection (never ported anywhere) whose content fits every DC region under current keying — ARAM is the only tight region (content 0.979× cap) — while the large main/VRAM address extents are placement work, not volume. |
| Assessed | capture 2026-08-07 · battery v8 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` — scored under battery v9 keying (scoring-only re-score 2026-08-08, see History) |

## 2. Identity

| | |
|---|---|
| Set / family | `marstv` (covers: no clones — `parent: null` in controls.json; single GAME line, naomi.cpp @59e7c0b line 10969). M2-type cart 840-0025C, boot ROM `epr-22993.ic22` (2 MB, reloaded) + 15×64 Mb mask ROMs, M2 crypt key `280b8ef5` (317-0274-JPN) — ROM_START lines 5449–5474, comment table line 384 (no special-I/O note). arcadeitalia's "NAOMI GD-ROM" platform label and "BAD DUMP" flag are both wrong: it is a cart, and **0** `BAD_DUMP` flags appear in the ROM_START block (verified @59e7c0b) — same spurious-label class as `inunoos` |
| Maker / year | Sega (MAME GAME line), developed by Sega AM3 ([Play:Right](https://www.playright.dk/arcade/titel/kasei-channel-mars-tv)), 1999 |
| Genre / format | Party — 3-player variety/minigame collection, 16 minigames (button-mashing, timing, reflex, quiz; described in Japan as "セガ版ビシバシ", Sega's Bishi Bashi), **cart** — M2 840-0025C, 57.8 MB |
| Official DC port | No — Japan-only arcade, no home version on any platform ([lifeshipsailing red-data-book entry](https://www.lifeshipsailing.net/entry/2019/05/16/220000): 移植なし / no ports, conservation status "extinct"; no home SKU on [Giant Bomb](https://www.giantbomb.com/kaizen-channel-mars-tv/3030-69400/) or [LaunchBox](https://gamesdb.launchbox-app.com/games/details/37524-kaizen-channel-mars-tv)) |
| Community ports | None found (searched 2026-08-03) — noted as never ported in the [Dreamcast Junkyard Naomi-conversion article](https://www.thedreamcastjunkyard.co.uk/2016/01/guest-article-expanding-dreamcast.html); no dreamcast-talk/Reddit conversion threads. **Name-variant trap for future searches:** databases misspell it "Kaisen" (arcade-history) and "Kaizen" (LaunchBox, Giant Bomb); correct romanization is Kasei (火星 = Mars), Japanese sources also use just 火星チャンネル |
| Representative choice | Only member of its family (MAME parent, no clones) |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/marstv.zip`
Attract/demo reached: **demo** — sidecar `capture.coverage = "demo"` (the v2-era display
blindness stayed fixed from v4 on).
Screenshots: `evidence/marstv/shot-060s.png` · `evidence/marstv/shot-365s.png` ·
`evidence/marstv/shot-609s.png` (title/eerie-face screen ×2, attract camera-minigame
instructions)
Anomalies: none — handoff detected at 20.0 s vs v4's 30.0 s (handoff-detection timing
moved, not the game).

## 4. Memory fit (axis: 86.6)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 9,091,782 | 16,777,216 | 0.542 | 100.0 | address peak 25,984,736 (u 1.549, informational) = `dma_high_water` exactly · nz_above_cap 798,810 — relocation work, not volume |
| VRAM (FB-masked content + 2×FB, `content_total + 2×fb_bytes`) | 6,276,059 (content 5,047,259 + 2×614,400) | 8,388,608 | 0.748 | 100.0 | address peak 14,229,504 (u 1.696, informational) · nz_total 5,641,652 · nz_above_cap 3,281,430 (address extent) · `fb_bytes` = exactly 640×480×2 |
| ARAM (content volume, fill-excluded, `content_total`) | 2,053,563 | 2,097,152 | 0.979 | 86.6 | **binding region** — address peak 2,147,400 (u 1.024) · nz_above_cap 47,694 (~47 KB trim) |

Watermarks (informational, content-scan — stale-data prone): main 25,984,736 ·
vram 14,229,504 · aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 54.3)

DMA events 164 · total 199.8 MB · unique 52.4 MB · re-read ratio 0.7376 ·
steady-state 20.991 MB/min (`short_window: false`) · PIO 2,098,688 B

## 6. Guts (axis: 90.0)

Code 2,097,152 B · functions 1,473 · MMIO refs: scif 0, rtc 4, g2ext 248 ·
BIOS vector refs: none · flags: `eeprom_bios`, `rtc`.
M2 boot blob carved at base `0x0c020000`, entry `0x0c020500`, header title "MARS TV".
SDK strings: `nlam Ver 1.00 Build:Oct 28 1999` + `libintr Ver 1.051` — a 1999 library
stack, the campaign's earliest SDK data point.

## 7. Controls (axis: 100.0)

**Buttons only — no stick, no special hardware** (`controls.device_class = stick`, the
standard-stick/buttons top rung). First title in the campaign with a *dedicated*
per-title MAME INPUT_PORTS (naomi.cpp @59e7c0b lines 1567–1584, `marstv`): per player
Start + three differently-sized buttons — "Red Large Button 大", "Yellow Medium Button
中", "Blue Small Button 小" — everything else `IPT_UNUSED`. The size-graded buttons are
the Bishi Bashi-style cabinet gimmick; electrically they are three plain digital
buttons. The comment `// TODO: Player 3` marks the cabinet's third player as not yet
wired in MAME; the in-binary INPUT TEST screen (`guts.sdk_strings`:
`"PLAYER      1P      2P      3P"`) confirms 3-player, as do operator photos of the
dedicated cabinet. No special I/O: no comment in the naomi.cpp table (unlike
Samba/Marine Fishing rows), no extra firmware in the ROM set, and no marstv
special-casing in Flycast's `maple_jvs.cpp`/`naomi_roms_input.h` — stock JVS digital.

Proposed DC mapping: 3 buttons + Start map 1:1 onto A/B/X + Start on a stock pad, and
3 players fit the DC's 4 ports. Genre precedent: Konami's Bishi Bashi Special shipped
on PS1 standard pads. Note for a port: P3 input is unmapped in current MAME and
Flycast (emulation gap, not a hardware one).

Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `marstv` (1567–1584);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=marstv)
(declared "Buttons only", 3 buttons);
[games.sakura-marche.com](https://games.sakura-marche.com/ac-mars-channel/) (3人同時プレー,
16 minigames); [lifeshipsailing](https://www.lifeshipsailing.net/entry/2019/05/16/220000)
("Sega's Bishi Bashi"); [Play:Right](https://www.playright.dk/arcade/titel/kasei-channel-mars-tv)
("Big button" controls, 3 players);
[Game Center Technopolis on X](https://x.com/GC_Tecnopolis/status/2002210874782851094)
(dedicated cabinet, 3-player simultaneous); in-binary INPUT TEST strings
(`assessments/marstv.metrics.json` → `guts.sdk_strings`). Sega's official history page
exists at https://www.sega.jp/history/arcade/product/9901/ (Cloudflare-blocked to
fetches; cited for existence).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 86.6^.40 · 54.3^.20 · 90.0^.20 · 100.0^.10 · 40.0^.10 = **74.6 (A)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **ARAM is the binding region at 0.979× content** — near cap but no longer a gate;
  the old address view showed only ~47 KB above cap, a trivial trim.
- **Main and VRAM fit by volume but not by address:** main content is 9.1 MB yet
  the write extent reaches 25,984,736 B (1.549× cap, ~0.8 MB of content above the
  16 MB line); VRAM content fits FB-masked (0.748×) but 3.28 MB sits above the 8 MB
  line by address. A port needs layout/relocation work in both regions.
- **Heavy cart streaming:** 199.8 MB total over 600 s, 20.99 MB/min steady, re-read
  0.7376 — from a cart. A GD-ROM-based port needs seek/throughput attention.
- **Rendering must be verified on real DC hardware** (working-style rule): the v2
  capture was display-blind under our fork (stale TA frame, kb §4.m class); v4+
  captures show the game rendering, but emulator-side proof is not hardware proof.
- MAME status is the blanket `GAME_FLAGS` macro (kb §4.r) — no per-title signal;
  arcadeitalia's "preliminary / imperfect gfx+sound" mirrors the driver-wide
  boilerplate, and its "GD-ROM" + "BAD DUMP" labels are refuted in §2.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot (4.00×) with only ~80 KB of content above cap — the gate-metric divergence that argued for content keying (kb §6 item 5); capture display-blind (kb §4.m) |
| v4 | 2026-08-04 | 42.8 (B) | Unparked by the v4 ARAM content metric; display blindness fixed; VRAM address high-water 1.71× binding (root-causes kb §7) |
| v8 | 2026-08-07 | 47.6 (B) | Re-capture. VRAM re-keyed on FB-masked content (sub 100.0) and ARAM measured by content volume for the first time; main write-truth 1.548× became binding (spec `2026-08-07-vram-fb-masking-design.md`) |
| v9 | 2026-08-08 | 74.6 (A) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); binding region moved to ARAM |
