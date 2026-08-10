# Street Fighter Zero 3 Upper (Japan) (GDL-0002) (`sfz3ugd`) — portability assessment

## 1. Verdict

| | |
|---|---|
| **Final score** | **89.2** (S) |
| Bottom line | The NAOMI "Upper" revision of Capcom's CPS2 fighter clears the full 0.80u memory plateau on all three regions — main content-volume 0.6460×, VRAM FB-masked content+2×FB 0.6046×, ARAM compacted content 0.7320× — for a 100.0 memory axis, a perfect stick+6-button controls fit (100.0), and 85.0 guts, pushing the final to 89.2 (S): by far the strongest result in the fighter cohort measured so far (next-best `ggxxac` 65.4 A, `assessments/ggxxac.md`) and new rank 4 overall. Unlike every other assessed fighter, this family already has a proven DC foothold — the base CPS2 game shipped on Dreamcast in 1999 (*Street Fighter Alpha 3: Saikyo Dojo*), and Upper's own arcade cabinet reads DC-created character data straight off a VMU inserted into a cabinet card slot. |
| Assessed | capture 2026-08-10 · battery v9 · flycast `f014a410c` · Ghidra 12.1.2_PUBLIC · MAME `59e7c0b` |

## 2. Identity

| | |
|---|---|
| Set / family | `sfz3ugd` (no clones — `parent: null` in controls.json, single set; MAME src/mame/sega/naomi.cpp @59e7c0b `ROM_START(sfz3ugd)` line 8389, `GAME()` row line 11237: `GAME( 2001, sfz3ugd, naomigd, naomigd, naomi, naomi_state, init_naomigd, ROT0, "Capcom", "Street Fighter Zero 3 Upper (Japan) (GDL-0002)", GAME_FLAGS )`) |
| Maker / year | Capcom, 2001 (sidecar `maker`/`year`; matches MAME `GAME()` row year) |
| Genre / format | Fighting (2D versus fighter, CPS2-lineage engine ported to NAOMI) — **GD-ROM** GDL-0002, 112.1 MB, machine `naomigd`. Carve title `STREET FIGHTER ZERO3 UPPER` (sidecar `guts.carve_meta.title`) |
| Official DC port | **No** direct port of Upper's own arcade content — but the family has unusually deep DC lineage for this cohort: (1) the base CPS2 game shipped on DC in 1999 as *Street Fighter Alpha 3: Saikyo Dojo* (JP: *Street Fighter Zero 3: Saikyō-ryū Dōjō*), carrying over the PlayStation-console content plus an added Saikyo Dojo mode ([Street Fighter Alpha 3, Wikipedia](https://en.wikipedia.org/wiki/Street_Fighter_Alpha_3), accessed 2026-08-10); (2) this Naomi Upper's own arcade cabinet reads customized fighter data created in that DC release's World Tour mode via a VMU inserted into a cabinet memory-card slot ([Game Watch, 2001-01-31, "セガ、「オレISM」キャラがアーケードで使える! AC「ストリートファイター ZERO3↑（UPPER）」"](https://game.watch.impress.co.jp/docs/20010131/zero3.htm) — contemporary trade-press report from the week of Upper's Jan 2001 launch, matching this sidecar's own `guts.sdk_strings` build-date string "Jan 11 2001"); (3) revisions elsewhere also carrying the "Upper" name are **not** this content — GBA *Street Fighter Alpha 3 Upper* (2002, adds Eagle/Maki/Yun) and PSP *Street Fighter Zero 3 Double Upper* / *Street Fighter Alpha 3 MAX* (2006, adds Ingrid, 37 chars total) are separate derivative revisions; per the Wikipedia article's Home-versions section, this NAOMI Upper's own arcade content specifically "was never ported" to a home platform |
| Community ports | None found for Upper→DC (searched 2026-08-10). An active fan project runs the *opposite* direction — extracting the updated Zero3 build from the 2024 *Capcom Fighting Collection 2* PC/console re-release and porting it back onto real NAOMI hardware ([arcade-projects.com forum thread, 2024](https://www.arcade-projects.com/threads/capcom-fighting-collection-2-street-fighter-zero-3-upper-sega-naomi-p-o-r-t.34097/)) — not a DC target |
| Representative choice | Only member of its family |

## 3. Boot & run evidence

Boots: yes · handoff at 20.0 s (`trigger = "pio"`) · run 600 s · rom: `naomi/sfz3ugd.zip`
Attract/demo reached: **demo** — the full attract cycle plays out across the 10 battery shots: character-roster splash over the "STREET FIGHTER ZERO3" wordmark (`shot-060s.png`) → black transition (`shot-121s.png`) → a live attract-demo battle under a tree with the "http://www.capcom.co.jp/" URL splash (`shot-182s.png`) → a story cutscene, Ryu confronting M. Bison (`shot-243s.png`) → a HISCORE RANKING table (`shot-304s.png`) → a second live demo battle at a Japanese shrine stage (`shot-365s.png`) → the "STREET FIGHTER ZERO3" title logo card (`shot-426s.png`) → a second ranking table (`shot-487s.png`) → black transition (`shot-548s.png`) → a stylized "CLASH DIE BROKE" tagline card (`shot-609s.png`) → loop restart. No EEPROM/settings prompt appears anywhere in the capture. Sidecar `capture.coverage = "demo"`.
Screenshots (5 kept of 10): `evidence/sfz3ugd/shot-060s.png` · `evidence/sfz3ugd/shot-182s.png` · `evidence/sfz3ugd/shot-243s.png` · `evidence/sfz3ugd/shot-304s.png` · `evidence/sfz3ugd/shot-426s.png` (full 10-shot manifest in sidecar `capture.screenshots`)
Anomalies: none — two of the ten raw shots (`shot-121s.png`, `shot-548s.png`) are plain black attract-transition frames between segments, not a stuck/blank screen; every other shot shows distinct rendered content, confirming continuous full-attract rendering under the fork.

## 4. Memory fit (axis: 100.0)

| Region | Scored value | DC cap | u | Sub-score | Evidence / note |
|---|---|---|---|---|---|
| Main RAM (write-truth content volume, `nz_total`) | 10,838,473 | 16,777,216 | 0.6460 | 100.0 | address peak 33,538,022 (u 1.999, informational) · `nz_above_cap` 6,790,436 (content bytes above the 16 MB line, informational) · `dma_high_water` 6,439,136 (informational-only from v6 on — DMA-only view, undercounts the CPU-written content `nz_total` captures) |
| VRAM (FB-masked content + 2×FB) | 5,071,910 (content_total 3,843,110 + 2×fb_bytes 614,400) | 8,388,608 | 0.6046 | 100.0 | raw address peak 15,659,040 (u 1.867, informational) · `nz_total` 4,223,699 · `nz_above_cap` 4,197,257 · `regs_last` isp_base=0 isp_limit=28f700 ol_base=35a280 ol_limit=28f800 fb_w_sof1=800000 fb_w_sof2=c00000 fb_r_sof1=c00000 |
| ARAM (compacted content volume, fill-excluded, `content_total`) | 1,535,155 | 2,097,152 | 0.7320 | 100.0 | address peak 2,097,136 (u 1.000 raw, informational — the familiar near-full-bank boot pattern seen elsewhere in the campaign, e.g. `senkosp`'s identical peak, not this title's own content) · `nz_above_cap` 0 — comfortable headroom under the plateau, not a near-miss |

Watermarks (informational, content-scan — stale-data prone): main 33,538,022 · vram 15,659,040 · aram 8,388,608 (the boot-time "DMPD" fill, not content — kb §7).
Main watermark (33,538,022) diverges from `dma_high_water` (6,439,136, 5.2×) — expected, not a regression: `dma_high_water` is DMA-only and informational since v6, while the scored `nz_total` (10,838,473) sits between the two and satisfies `nz_total <= peak + 1`, confirming the content metric is intact and simply captures CPU-written main-RAM state the pure-DMA view misses.

## 5. Cart streaming (axis: 79.6)

DMA events 2,155 · total 56,100,864 B (53.5 MiB) · unique 27,080,704 B (25.8 MiB) · re-read ratio 0.5173 ·
steady-state 5.121 MB/min (`short_window: false`) · PIO bootstrap `pio_bytes` 4,453,696 B (4.2 MiB, GD DIMM PIO boot-load, handoff `trigger=pio`).
Bandwidth is comfortably in the full-score band (5.121 MB/min, well under the 6 MB/min plateau edge); the re-read ratio (0.5173) is the sole drag on this axis, sitting just past the 0.50 knee where the scoring curve's slope shallows — the streaming axis's 79.6 is the main contributor holding the final below `senkosp`'s 91.0.

## 6. Guts (axis: 85.0)

Code 4,194,304 B (4.0 MiB) · functions 3,866 · MMIO refs: scif 6, rtc 3, g2ext 85 · BIOS vector refs: none (`bios_refs: {}`) ·
penalties applied: `eeprom_bios` (−5) + `serial` (−5) + `rtc` (−5) = −15 → 100 − 15 = 85.0.
Carve base `0x8c021000`, entry `0x8c021000`, size 4,194,304 B, header title `STREET FIGHTER ZERO3 UPPER` (`guts.carve_meta`).
SDK strings corroborate both the shared Zero3/Alpha3 codebase and the Jan 2001 Upper build: disc file names `SFZ3_MT_.SYS`, `STFZERO3.SYS`, `SFALPHA3.SYS`; copyright strings spanning "CAPCOM CO.,LTD. 1998,1999" (base CPS2 game) through "1998, 2001" / "1998,2001" (Upper's rebuild); a `"DEVELOP VERSION"` debug-build string; and a `"Jan 11 2001"` build-date string that lines up with the Game Watch launch report dated 11 days later (2001-01-31, cited in §2) — internal build-date evidence corroborating the external citation.

## 7. Controls (axis: 100.0)

Cabinet: standard NAOMI 2P panel, 8-way joystick + 6 buttons per player (3 punch + 3 kick, the classic Capcom fighter layout), 2 coin chutes (`controls.device_class = stick`). MAME input ports: `naomi` (`INPUT_PORTS_START(naomi)` at naomi.cpp @59e7c0b line 1506 — P1/P2 blocks each carry `IPT_JOYSTICK_UP/DOWN/LEFT/RIGHT PORT_8WAY` + `IPT_BUTTON1`..`IPT_BUTTON6`; `sfz3ugd`'s `GAME()` row at line 11237 declares `input_ports=naomi`).
Proposed DC mapping: X/Y/B/A for the four face buttons (LP/MP/MK/LK) + L/R analog triggers pressed digitally for the two heavy attacks (HP/HK), D-pad or analog stick for the 8-way joystick — not a hypothetical: it is the exact scheme the official 1999/2000 DC release of the base game shipped with (X=LP, Y=MP, B=MK, A=LK, L=HP, R=HK), scanned from the retail manual.
Sources: MAME src/mame/sega/naomi.cpp @59e7c0b INPUT_PORTS `naomi` (line 1506) and `GAME()` row `sfz3ugd` (line 11237);
[arcadeitalia MAME machine DB](https://adb.arcadeitalia.net/?mame=sfz3ugd) ("Joystick 8 ways", 6 buttons LP/MP/HP/LK/MK/HK, "Up to 2 players (solo, 2 concurrents)", 2 coin slots);
[Internet Archive, SEGA Dreamcast Manuals — Street Fighter Alpha 3 (USA), "CONTROLS (DEFAULT)"](https://archive.org/stream/SEGADreamcastManuals_201812/Street%20Fighter%20Alpha%203%20(USA)_djvu.txt) (DC pad mapping precedent for the same 6-button Capcom fighter scheme, confirming the proposed mapping already shipped once).

## 8. Score computation

final = memory^.40 · streaming^.20 · guts^.20 · controls^.10 · similarity^.10
      = 100.0^.40 · 79.6^.20 · 85.0^.20 · 100.0^.10 · 70.0^.10 = **89.2 (S)**
Similarity inputs: developer no, SDK overlap partial, loader match yes → 70.0. The developer `false` is the known
reference-list artifact — the calibration reference's `makers` list (`assessments/reference/similarity-reference.json`)
is Altron/Taito only, so no third-party developer (Capcom included) can ever match — same caveat noted for
`senko`/`senkosp`/`illvelo`.

## 9. Risks & notes

- **Fighter cohort's strongest result by far**: 89.2 S is nearly 24 points clear of the next-best fighter (`ggxxac`
  65.4 A, `assessments/ggxxac.md`) and clears every other fighter assessed so far (`ggxxsla` 58.6 B, `mbaa` 55.9 B,
  `ggxx` 55.4 B, `meltyb` 52.4 B, `meltybld` 45.3 B). The gap is the memory axis: all three of sfz3ugd's regions sit
  under the 0.80u full-score plateau (u 0.6460 / 0.6046 / 0.7320) where every Guilty Gear/Melty Blood title measured
  so far binds on VRAM or ARAM above 1.0×. This CPS2-lineage 2D sprite engine — 34-character roster notwithstanding —
  carries a lighter per-frame asset footprint than the GGXX/Melty Blood NAOMI-native engines.
- **Main-RAM watermark diverges sharply from `dma_high_water`** (33,538,022 vs 6,439,136, 5.2×) — expected per §4,
  not an instrumentation concern: `dma_high_water` is DMA-only and informational since v6; the scored `nz_total`
  captures CPU-written state the DMA-only view misses, and `nz_total <= peak + 1` holds.
- **DC lineage is unusually direct for this cohort**: the base game already shipped on DC (1999 Saikyo Dojo), and
  Upper's own arcade cabinet physically reads DC-created character data over a VMU slot (§2) — a hardware-level
  interop precedent none of the other fighter-cohort titles have. A DC port project inherits a proven control-mapping
  precedent (§7, the same 6-button scheme already shipped on the same base game) and a demonstrated content
  compatibility bridge, not just genre similarity.
- **Similarity axis capped by a reference-list artifact, not a real dissimilarity signal** — see §8.
- Rendering must be verified on real DC hardware per working-style rule — this is an emulator-only (Flycast)
  measurement.
- MAME emulation status: blanket naomigd `GAME_FLAGS` — no per-title signal; the title runs and renders fully under
  our fork regardless (kb §4.r convention).

## 10. History

| Battery | Date | Final | What changed |
|---|---|---|---|
| v9 | 2026-08-10 | 89.2 S | initial assessment — fighter cohort, fresh v9 capture |
