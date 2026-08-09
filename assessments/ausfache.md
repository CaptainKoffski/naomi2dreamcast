# Akatsuki Blitzkampf Ausf. Achse (Japan) (841-0058C) (`ausfache`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **84.4 (S)** |
| Bottom line | 2D doujin fighter whose 2003–2007 PC-era assets fit DC budgets comfortably — every memory region now measures ≤0.75× cap with nothing over (ARAM the tightest) — and no port of Ausf. Achse exists on any platform, making it uniquely valuable, not redundant. |
| Assessed | capture 2026-08-09 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `ausfache` (single member — `parent: null` in controls.json, no clones in naomi.cpp) |
| Maker / year | Subtle Style, 2008 (arcade debut 2008-02-20). Doujin circle founded April 2000; Ausf. Achse is its only Naomi title ([Wikipedia](https://en.wikipedia.org/wiki/Akatsuki_Blitzkampf)) |
| Genre / format | 2D fighter, **cart, Naomi M4** 841-0058C, rom_board id `5504`, ROT0 — MAME src/mame/sega/naomi.cpp @59e7c0b GAME line 11116 (`naomim4`), ROM_START lines 6808–6822: 2× 64 MiB flash. Clean PIC key `317-05130-jpn.ic3` (CRC `eccdcd59`, no BAD_DUMP; Flycast fork agrees, naomi_roms.cpp:4583). Arcadeitalia's "BAD DUMP" badge is stale metadata refuted by the primary source |
| Official DC port | No — and no port of Ausf. Achse exists **anywhere**. Lineage: doujin PC *Akatsuki Shisei Ichigō* (2003) → *Akatsuki Blitzkampf* (PC, 2007) → *Ausf. Achse* (Naomi, 2008); sequels are the EN-Eins line. A Windows port announced 2019-03-29 was never released ([Wikipedia](https://en.wikipedia.org/wiki/Akatsuki_Blitzkampf), [Akatsuki/En-Eins wiki](https://akatsuki-en1.fandom.com/wiki/Akatsuki_Blitzkampf)) |
| Community ports | None found (searched 2026-08-02) — only generic "can Naomi run on DC" threads ([dreamcast-talk](https://www.dreamcast-talk.com/forum/viewtopic.php?t=2001), [GameFAQs](https://gamefaqs.gamespot.com/boards/916412-dreamcast/73913493)). An active Fightcade/Flycast netplay scene runs the Naomi version ([RetroAchievements](https://retroachievements.org/game/17891), [mainline Flycast video](https://www.youtube.com/watch?v=gBJtj_P6HJE)) |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/ausfache.zip`
Attract/demo reached: **demo** — live attract gameplay in `shot-609s.png` (two characters fighting,
"RECOVER 500pts" HUD; sidecar `capture.coverage = "demo"`)
Screenshots: `evidence/ausfache/shot-060s.png` · `evidence/ausfache/shot-365s.png` · `evidence/ausfache/shot-609s.png`
Anomalies: none — single clean leg (battery log: `leg 1: ausfache.zip attempt 1 -> ran full window`).

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 8,000,910 | 16,777,216 | 0.477 | 100.0 | address peak 16,349,952 (u 0.975, informational — see Risks) · `dma_high_water` 5,065,888 (informational floor) — unchanged from v7 |
| VRAM (FB-masked content volume + 2×framebuffer, `content_total + 2*fb_bytes`) | 4,415,300 | 8,388,608 | 0.526 | 100.0 | `content_total` 3,186,500 + 2×`fb_bytes` 614,400 — **first real measurement of the v8 keying fields** (absent from the v7 sidecar); nz_total 3,699,405 · 0 above cap. Address peak is unchanged from v7 at 7,892,608 (u 0.941) — that peak is what the old (v7) sidecar scored through, as a provably conservative fallback (score.py, kb §6/§11), since it had no `content_total`/`fb_bytes` fields yet |
| ARAM (content volume, fill-excluded, `content_total`) | 1,561,912 | 2,097,152 | 0.745 | 100.0 | address peak 2,097,136 (16 B under cap, informational — full-bank touch is uniform fill) — unchanged from v7; now the tightest-fitting region, still comfortably ≤0.80 |

Watermarks (informational, content-scan — stale-data prone): main 16,349,952 ·
vram 9,692,984 (includes the pre-handoff BIOS boot-screen sheet, kb §9) ·
aram 8,388,608 (the boot-time "DMPD" fill, not content).

## 5. Cart streaming (axis: 79.8)

DMA events 457 · total 50.2 MB (50,165,760 B) · unique 24.7 MB (24,721,408 B) ·
re-read ratio 0.5072 · steady-state 5.052 MB/min (`short_window: false`) ·
PIO 1,051,200 B — sub-score unchanged at 79.8 (v7 was 458 events / 50,184,192 B /
24,739,840 B / 0.507 / 5.055 MB/min; run-to-run capture noise, same axis score)

## 6. Guts (axis: 85.0)

Code 1,048,576 B · functions 2,111 · MMIO refs: scif 2, rtc 3, g2ext 227 ·
BIOS vector refs: none · flags: `eeprom_bios`, `serial`, `rtc`.
M4 boot blob carved at base `0x8c020000`, entry `0x8c021000` — needs the
`carve_boot.py` bit-30 mask (M4 encrypted-read flag, MAME
`src/mame/sega/naomim4.cpp:124-125` @59e7c0b, Flycast `m4cartridge.cpp:115,132`; kb §4.q).
SDK strings: Kunoichi2 Library for NAOMI 2.07, syStartCwKn 2.08, AIPKN 0.91 (Sega
libraries, Mar 2001 builds).

## 7. Controls (axis: 100.0)

Cabinet: 8-way stick + 3 attack buttons (A/B/C = Weak/Medium/Strong; throw and
Reflector parry are mechanics on the same buttons), 2P. `controls.device_class = stick`.
Proposed DC mapping: 1:1 on a stock DC pad (A/B/X + Start); native on the DC Arcade Stick.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (line 11116);
Flycast `naomi_roms_input.h:195` `INPUT_3_BUTTONS("Weak Attack", "Medium Attack",
"Strong Attack")` (strongest citation);
[Mizuumi Controls](https://mizuumi.wiki/w/Akatsuki_Blitzkampf/Controls);
[arcadeitalia](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=ausfache)
(the "6 buttons" there is the generic JVS standard declaration).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 79.8^.20 · 85.0^.20 · 100.0^.10 · 40.0^.10 = **84.4 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match no.

## 9. Risks & notes

- **Port-planning takeaway: everything fits, comfortably now.** With the v8 VRAM
  FB-mask fields measured for real (§4), no region is binding under the
  `region_score` piecewise map — main 0.477×, VRAM 0.526×, ARAM 0.745× (the
  tightest), all with zero bytes above cap. Main content volume is under half the
  DC's 16 MB; ARAM still has the Ikaruga 4× audio-trim precedent (kb §4.d) in
  reserve if a real port needs margin.
- **Main RAM is address-sparse:** write-truth content is 8.0 MB but the touched
  address peak reaches 16,349,952 B (0.975× cap). Volume fits easily; a port may
  still need layout/relocation attention for the sparse high-address writes.
- **Rendering must be verified on real DC hardware** (working-style rule). Mainline
  Flycast demonstrably renders the title (§2 links); our fork's early captures were
  display-blind (kb §4.m) though v5+ captures show live gameplay.
- MAME status is the blanket naomi.cpp `GAME_FLAGS` (no per-title signal, kb §4.r);
  the game runs under our fork regardless.

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v2 | 2026-08-03 | PARKED G3-ARAM | Full 8 MiB ARAM bank at boot read as 4.00× cap; capture was display-blind (stale TA frame, kb §4.m) |
| v4 | 2026-08-04 | 58.4 (B) | Pre-handoff BIOS boot-screen texture charged to game VRAM — sampling hole, root-cause kb §9 |
| v5 | 2026-08-06 | 79.1 (A) | v4 VRAM artifact fixed; same day the `carve_boot.py` bit-30 fix unlocked M4 guts (85.0) + similarity (40.0) via `rescore_static.py` |
| v7 | 2026-08-07 | 79.8 (A) | Re-capture. ARAM re-keyed on content volume (kb §6 checkpoint) — no longer binding; main write-truth measured for the first time (address peak 0.975× became binding) |
| v9 | 2026-08-08 | 80.7 (S) | Scoring-only re-key (no re-capture): main scored on content volume `nz_total` (spec `2026-08-08-main-content-rekey-design.md`); binding region moved to VRAM |
| v9 | 2026-08-09 | 84.4 S | ranking-groom chunk 2: fresh v9 capture (was v7) — first real measurement of v8 VRAM FB-mask fields replaces conservative fallback; 80.7→84.4 |
