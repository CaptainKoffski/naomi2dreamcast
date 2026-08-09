# Naomi library — inventory & porting triage

Every ROM set in the `naomi/` library folder: format, set relationship, size, genre, and porting-assessment status. Purpose: **range games by ease of Naomi→Dreamcast porting**, then port the easy ones (ref: the Cleopatra Fortune Plus port in `../cleopatra`).

- **Source of truth:** MAME driver `src/mame/sega/naomi.cpp`. GD-ROM = `ROM_START` declares a `DISK_IMAGE`; else cartridge. Set type = `GAME()` parent field.
- **Layout (now uniform):** GD-ROM = `<set>.zip` (Naomi BIOS + PIC) + `<set>/<disc>.chd`; cart = `<set>.zip`. Folders hold only disc images.
- **Size** = the set's own disc(s) + its own `<set>.zip`. Clones share the parent's zip, so their size is just the disc.
- **Genre legend:** ★ = easy-port candidate lane (small 2D / puzzle / shmup, like Cleopatra) · ⚠ = exotic, likely exclude (mahjong, football-card, horse-race, typing, gambling, quiz, fishing) · ? = unclassified, fill during assessment.
- **DC port column:** did this exact game get an **official, licensed consumer Dreamcast release**? `Yes (year)` · `No` · `Partial` (a related-but-not-identical version reached DC — see the note under the table). Sourced per-game (Wikipedia/GDRI/Sega Retro), 2026-08-02. A `Yes` means an official DC binary of the same game exists — **not a reason to skip it**, but a ready-made reference/validation target (compare a port's behaviour against the real DC build); an official port also means the community port is redundant for players. The porting lane still cares most about the `No`/★ games (never on DC, small enough to fit).
- **Why keep full runnable sets (not disc-only):** the port pipeline's Phase 1–2 need the game to **boot in instrumented Flycast** to dump the decrypted DIMM image + capture cart/input/EEPROM traces. That needs disc + BIOS + PIC. See memory `porting-workflow-and-library-grooming`.
- **Assessment status:** per-set cell in the last column; sorted scores in [assessments/RANKING.md](assessments/RANKING.md), work queue in [assessments/QUEUE.md](assessments/QUEUE.md), method in the [spec](docs/superpowers/specs/2026-08-02-portability-assessment-design.md).

> **⚠ `parent` ≠ newer/better, `clone` ≠ older/worse.** MAME's parent/clone flag is a reference-dump pick, not a version rank. It often lines up with "parent = latest rev" (e.g. `senko` Rev A parent, `senkoo` base clone) but breaks on **region** splits: `cvs2` parent = USA, `cvs2mf` clone = Japan original; `puyofev` parent = World, `puyofevj` clone = Japan. To judge "latest", read the Rev letter / Ver number in the title *within the same region* — not the flag.

## Summary

| | |
|---|---|
| Cartridge | 75 |
| GD-ROM | 77 |
| **Total sets** | **152** (16 clones) |
| Official DC ports | **58 Yes** · 3 Partial · 91 No |
| Local size | ~22 GB total (516 MB of it is images/videos/manuals) |
| Missing discs | none — all present & hash-verified |

**Triage at a glance:** ★ candidates ≈ 33 (13 puzzle + 20 shmup) · ⚠ exotic ≈ 28 (12 football-card, 4 horse-race, 3 mahjong, 3 typing, 2 quiz, 2 gambling, 1 fishing, 1 card) · fighting 29 · sports 13 · light-gun 9 · driving 7 · rhythm 6 · ? 21.

## Completeness

**All 152 sets are complete and Flycast-runnable** — every GD-ROM set has disc + BIOS + PIC, all hash-verified against MAME. The 9 sets that were previously PIC-less (`wccf116`, `wccf1dup`, `wccf212e`, `wccf234j`, `wccf310j`, `wccf322e`, `wccf341j`, `dragntr`, `quizqgd`) were completed from their romset archives; clones `wccf331e`/`wccf331j`/`dragntra` inherit the parent zips.

## Full inventory / triage sheet

Fill the **Status** column during assessment (e.g. `candidate`, `too big`, `needs cut`, `ported`).

| Title (MAME) | Shortname | Format | Set | Size | Genre | DC port | Status |
|---|---|---|---|---|---|---|---|
| Azumanga Daioh Puzzle Bobble (GDL-0018) | `azumanga` | **GD-ROM** | parent | 86.7 MB | Puzzle ★ | No | **49.6** B · [assessment](assessments/azumanga.md) |
| Border Down (Rev A) (GDL-0023A) | `bdrdown` | **GD-ROM** | parent | 203.3 MB | Shmup ★ | Yes (2003) | not assessed |
| Capcom Vs. SNK 2: Mark Of The Millennium 2001 (USA) (GDL-0008) | `cvs2` | **GD-ROM** | parent | 157.4 MB | Fighting | Yes (2001) | not assessed |
| Capcom Vs. SNK 2: Millionaire Fighting 2001 (Japan, Rev A) (GDL-0007A) | `cvs2mf` | **GD-ROM** | clone of `cvs2` | 149.5 MB | Fighting | Yes (2001) | not assessed |
| Capcom Vs. SNK: Millennium Fight 2000 Pro (Japan) (GDL-0004) | `cvsgd` | **GD-ROM** | parent | 125.2 MB | Fighting | Yes (2001) | not assessed |
| Chaos Field (Japan) (GDL-0025) | `cfield` | **GD-ROM** | parent | 142.9 MB | Shmup ★ | Yes (2004) | not assessed |
| Cleopatra Fortune Plus (GDL-0012) | `cleoftp` | **GD-ROM** | parent | 65.8 MB | Puzzle ★ | No | **85.8** S · [assessment](assessments/cleoftp.md) |
| Confidential Mission (GDS-0001) | `confmiss` | **GD-ROM** | parent | 126.4 MB | Light-gun | Yes (2001) | not assessed |
| Doki Doki Idol Star Seeker (GDL-0005) | `starseek` | **GD-ROM** | parent | 37.2 MB | ? | Yes (2002) | not assessed |
| Dragon Treasure (Rev A) (GDS-0030A) | `dragntra` | **GD-ROM** | clone of `dragntr` | 142.4 MB | Medal | No | see [`dragntr`](assessments/dragntr.md) |
| Dragon Treasure (Rev B) (GDS-0030B) | `dragntr` | **GD-ROM** | parent | 142.3 MB | Medal | No | parked G1 · [notes](assessments/dragntr.md) |
| Dragon Treasure 2 (Rev A) (GDS-0037A) | `dragntr2` | **GD-ROM** | parent | 231.6 MB | Medal | No | parked G1 · [notes](assessments/dragntr2.md) |
| Dragon Treasure 3 (Rev A) (GDS-0041A) | `dragntr3` | **GD-ROM** | parent | 290.1 MB | Medal | No | parked G1 · [notes](assessments/dragntr3.md) |
| Guilty Gear XX #Reload (Japan) (GDL-0019) | `ggxxrlo` | **GD-ROM** | clone of `ggxxrl` | 246.9 MB | Fighting | No | not assessed |
| Guilty Gear XX #Reload (Japan, Rev A) (GDL-0019A) | `ggxxrl` | **GD-ROM** | parent | 254.8 MB | Fighting | No | not assessed |
| Guilty Gear XX (GDL-0011) | `ggxx` | **GD-ROM** | parent | 250.2 MB | Fighting | No | **55.4** B · [assessment](assessments/ggxx.md) |
| Guilty Gear XX Accent Core (Japan) (GDL-0041) | `ggxxac` | **GD-ROM** | parent | 255.1 MB | Fighting | No | **65.4** A · [assessment](assessments/ggxxac.md) |
| Guilty Gear XX Slash (Japan, Rev A) (GDL-0033A) | `ggxxsla` | **GD-ROM** | parent | 249.6 MB | Fighting | No | **58.6** B · [assessment](assessments/ggxxsla.md) |
| Ikaruga (GDL-0010) | `ikaruga` | **GD-ROM** | parent | 40.5 MB | Shmup ★ | Yes (2002) | **88.7** S · [assessment](assessments/ikaruga.md) |
| Jingi Storm - The Arcade (Japan) (GDL-0037) | `jingystm` | **GD-ROM** | parent | 141.4 MB | Rhythm | No | not assessed |
| Karous (Japan) (GDL-0040) | `karous` | **GD-ROM** | parent | 126.5 MB | Shmup ★ | Yes (2007) | **85.0** S · [assessment](assessments/karous.md) |
| Kurukuru Chameleon (Japan) (GDL-0034) | `kurucham` | **GD-ROM** | parent | 41.6 MB | Puzzle ★ | No | **85.2** S · [assessment](assessments/kurucham.md) |
| La Keyboard (GDS-0017) | `keyboard` | **GD-ROM** | parent | 33.6 MB | Typing ⚠ | No | not assessed |
| Lupin The Third - The Shooting (GDS-0018) | `lupinshoo` | **GD-ROM** | clone of `lupinsho` | 199.7 MB | Light-gun | No | not assessed |
| Lupin The Third - The Shooting (Rev A) (GDS-0018A) | `lupinsho` | **GD-ROM** | parent | 190.2 MB | Light-gun | No | not assessed |
| Lupin The Third - The Typing (Rev A) (GDS-0021A) | `luptype` | **GD-ROM** | parent | 153.9 MB | Typing ⚠ | No | not assessed |
| Melty Blood Act Cadenza (Japan) (GDL-0028) | `meltyblo` | **GD-ROM** | clone of `meltybld` | 207.1 MB | Fighting | No | not assessed |
| Melty Blood Act Cadenza Ver. A (Japan) (GDL-0028C) | `meltybld` | **GD-ROM** | parent | 214.9 MB | Fighting | No | not assessed |
| Melty Blood Act Cadenza Version B (Japan) (GDL-0039) | `meltybo` | **GD-ROM** | clone of `meltyb` | 189.5 MB | Fighting | No | see [`meltyb`](assessments/meltyb.md) |
| Melty Blood Act Cadenza Version B2 (Japan) (GDL-0039A) | `meltyb` | **GD-ROM** | parent | 202.9 MB | Fighting | No | **52.4** B · [assessment](assessments/meltyb.md) |
| Mobile Suit Gundam: Federation Vs. Zeon (GDL-0001) | `gundmgd` | **GD-ROM** | parent | 142.3 MB | Fighting | Yes (2002) | not assessed |
| Mobile Suit Gundam: Federation Vs. Zeon DX (USA, Japan) (GDL-0006) | `gundmxgd` | **GD-ROM** | parent | 172.9 MB | Fighting | Yes (2002) | not assessed |
| Moeru Casinyo (Japan) (GDL-0013) | `moeru` | **GD-ROM** | parent | 98.0 MB | ? | No | **85.9** S · [assessment](assessments/moeru.md) |
| Monkey Ball (GDS-0008) | `monkeyba` | **GD-ROM** | parent | 82.5 MB | Action | No | not assessed |
| Musapey's Choco Marker (Rev A) (GDL-0014A) | `chocomk` | **GD-ROM** | parent | 68.5 MB | Puzzle ★ | Yes (2002) | **90.5** S · [assessment](assessments/chocomk.md) |
| Noukone Puzzle Takoron (Japan) (GDL-0042) | `takoron` | **GD-ROM** | parent | 52.6 MB | Puzzle ★ | No | parked G3 · [notes](assessments/takoron.md) |
| Psyvariar 2 - The Will To Fabricate (Japan) (GDL-0024) | `psyvar2` | **GD-ROM** | parent | 136.7 MB | Shmup ★ | Yes (2004) | not assessed |
| Puyo Pop Fever (World) (GDS-0034) | `puyofev` | **GD-ROM** | parent | 150.3 MB | Puzzle ★ | Yes (2004) | not assessed |
| Puyo Puyo Fever (Japan) (GDS-0031) | `puyofevj` | **GD-ROM** | clone of `puyofev` | 141.1 MB | Puzzle ★ | Yes (2004) | not assessed |
| Quiz Keitai Q mode (GDL-0017) | `quizqgd` | **GD-ROM** | parent | 126.4 MB | Quiz ⚠ | No | not assessed |
| Radirgy (Japan) (GDL-0032) | `radirgyo` | **GD-ROM** | clone of `radirgy` | 124.3 MB | Shmup ★ | Yes (2006) | not assessed |
| Radirgy (Japan, Rev A) (GDL-0032A) | `radirgy` | **GD-ROM** | parent | 132.4 MB | Shmup ★ | Yes (2006) | not assessed |
| Senko no Ronde (Japan) (GDL-0030) | `senkoo` | **GD-ROM** | clone of `senko` | 215.3 MB | Shmup ★ | No | see [`senko`](assessments/senko.md) |
| Senko no Ronde (Japan, Rev A) (GDL-0030A) | `senko` | **GD-ROM** | parent | 241.0 MB | Shmup ★ | No | **89.9** S · [assessment](assessments/senko.md) |
| Senko no Ronde Special (Export, Japan) (GDL-0038) | `senkosp` | **GD-ROM** | parent | 237.7 MB | Shmup ★ | No | **91.0** S · [assessment](assessments/senkosp.md) |
| Shakatto Tambourine Cho Powerup Chu (2K1 AUT) (GDS-0016) | `shaktamb` | **GD-ROM** | parent | 180.2 MB | Rhythm | No | not assessed |
| Shikigami no Shiro II / The Castle of Shikigami II (GDL-0021) | `shikgam2` | **GD-ROM** | parent | 111.1 MB | Shmup ★ | Yes (2004) | **87.7** S · [assessment](assessments/shikgam2.md) |
| Slashout (GDS-0004) | `slashout` | **GD-ROM** | parent | 137.4 MB | Beat-em-up | No | not assessed |
| Spikers Battle (GDS-0005) | `spkrbtl` | **GD-ROM** | parent | 147.3 MB | Sports | No | not assessed |
| Sports Jam (GDS-0003) | `sprtjam` | **GD-ROM** | parent | 124.4 MB | Sports | Yes (2001) | not assessed |
| Street Fighter Zero 3 Upper (Japan) (GDL-0002) | `sfz3ugd` | **GD-ROM** | parent | 112.1 MB | Fighting | No | not assessed |
| Super Shanghai 2005 (Japan) (GDL-0031) | `ss2005o` | **GD-ROM** | clone of `ss2005` | 54.2 MB | Puzzle ★ | No | see [`ss2005`](assessments/ss2005.md) |
| Super Shanghai 2005 (Japan, Rev A) (GDL-0031A) | `ss2005` | **GD-ROM** | parent | 63.1 MB | Puzzle ★ | No | **54.8** B · [assessment](assessments/ss2005.md) |
| Tetris Kiwamemichi (Japan) (GDL-0020) | `tetkiwam` | **GD-ROM** | parent | 62.3 MB | Puzzle ★ | No | **87.5** S · [assessment](assessments/tetkiwam.md) |
| The Maze of the Kings (GDS-0022) | `mok` | **GD-ROM** | parent | 140.0 MB | Light-gun | No | not assessed |
| Trigger Heart Exelica (Japan) (GDL-0036) | `trghearto` | **GD-ROM** | clone of `trgheart` | 80.1 MB | Shmup ★ | Yes (2007) | see [`trgheart`](assessments/trgheart.md) |
| Trigger Heart Exelica Ver.A (Japan) (GDL-0036A) | `trgheart` | **GD-ROM** | parent | 91.6 MB | Shmup ★ | Yes (2007) | **86.5** S · [assessment](assessments/trgheart.md) |
| Trizeal (Japan) (GDL-0026) | `trizeal` | **GD-ROM** | parent | 129.4 MB | Shmup ★ | Yes (2005) | **72.5** A · [assessment](assessments/trizeal.md) |
| Under Defeat (Japan) (GDL-0035) | `undefeat` | **GD-ROM** | parent | 150.9 MB | Shmup ★ | Yes (2006) | not assessed |
| Usagi - Yamashiro Mahjong Hen (Japan) (GDL-0022) | `usagiym` | **GD-ROM** | parent | 110.4 MB | Mahjong ⚠ | No | not assessed |
| Virtua Athletics / Virtua Athlete (GDS-0019) | `vathlete` | **GD-ROM** | parent | 86.3 MB | Sports | Yes (2000) | not assessed |
| Virtua Golf / Dynamic Golf (Rev A) (GDS-0009A) | `dygolf` | **GD-ROM** | parent | 70.6 MB | Sports | No | not assessed |
| Virtua Tennis / Power Smash (GDS-0011) | `vtennisg` | **GD-ROM** | parent | 52.5 MB | Sports | Yes (2000) | not assessed |
| Virtua Tennis 2 / Power Smash 2 (Rev A) (GDS-0015A) | `vtennis2` | **GD-ROM** | parent | 121.6 MB | Sports | Yes (2001) | not assessed |
| World Club Champion Football European Clubs 2004-2005 (Asia) (CDV-10013) | `wccf310j` | **GD-ROM** | parent | 662.8 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2004-2005 Ver.1.1 (Export) (CDV-10015) | `wccf331e` | **GD-ROM** | clone of `wccf322e` | 638.7 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2004-2005 Ver.1.1 (Japan) (CDV-10020) | `wccf331j` | **GD-ROM** | clone of `wccf341j` | 704.5 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2004-2005 Ver.1.2 (Japan) (CDV-10021) | `wccf341j` | **GD-ROM** | parent | 704.3 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2004-2005 Ver.3.22 (Export) (CDV-10015P) | `wccf322e` | **GD-ROM** | parent | 638.4 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2005-2006 (Export) (CDV-10027) | `wccf420e` | **GD-ROM** | parent | 657.6 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football European Clubs 2005-2006 (Japan) (CDV-10025) | `wccf400j` | **GD-ROM** | parent | 784.3 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football Serie A 2001-2002 DIMM FIRM Ver.3.03 (CDP-10003) | `wccf1dup` | **GD-ROM** | parent | 1.0 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football Serie A 2001-2002 Ver.2 (Japan) (CDP-10001C) | `wccf116` | **GD-ROM** | parent | 349.9 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football Serie A 2002-2003 Drive Checker (CDV-10007) | `wccf2chk` | **GD-ROM** | parent | 103 KB | Football-card ⚠ | No | not assessed |
| World Club Champion Football Serie A 2002-2003 Ver.2.12 (Italy) (CDV-10002) | `wccf212e` | **GD-ROM** | parent | 490.9 MB | Football-card ⚠ | No | not assessed |
| World Club Champion Football Serie A 2002-2003 Ver.2.34 (Japan) (CDV-10008) | `wccf234j` | **GD-ROM** | parent | 521.5 MB | Football-card ⚠ | No | not assessed |
| World Series Baseball / Super Major League (GDS-0010) | `wsbbgd` | **GD-ROM** | parent | 157.8 MB | Sports | No | not assessed |
| 18 Wheeler: American Pro Trucker (deluxe, Rev A) | `18wheelr` | **cart** | parent | 105.3 MB | Driving | Yes (2000) | not assessed |
| Airline Pilots (World, Rev B) | `alpilot` | **cart** | parent | 41.3 MB | Driving | No | not assessed |
| Akatsuki Blitzkampf Ausf. Achse (Japan) | `ausfache` | **cart** | parent | 75.4 MB | ? | No | **84.4** S · [assessment](assessments/ausfache.md) |
| Alien Front (Rev T) | `alienfnt` | **cart** | parent | 45.9 MB | Action | Partial | not assessed |
| Asian Dynamite / Dynamite Deka EX | `asndynmt` | **cart** | parent | 148.0 MB | Beat-em-up | No | not assessed |
| Cannon Spike / Gun Spike | `cspike` | **cart** | parent | 63.6 MB | Shmup ★ | Yes (2000) | **42.8** B · [assessment](assessments/cspike.md) |
| Capcom Vs. SNK: Millennium Fight 2000 (Rev C) | `capsnk` | **cart** | parent | 95.6 MB | Fighting | Yes (2000) | not assessed |
| Cosmic Smash (Rev A) | `csmash` | **cart** | parent | 42.8 MB | ? | Yes (2001) | not assessed |
| Crackin' DJ | `crackndj` | **cart** | parent | 108.0 MB | Rhythm | No | not assessed |
| Crackin' DJ Part 2 (Japan) | `crakndj2` | **cart** | parent | 105.5 MB | Rhythm | No | not assessed |
| Crazy Taxi | `crzytaxi` | **cart** | parent | 62.3 MB | Driving | Yes (2000) | not assessed |
| Cyber Troopers Virtual-On: Oratorio Tangram M.S.B.S. ver 5.66 2000 Edition | `vonot` | **cart** | parent | 91.6 MB | ? | Partial | not assessed |
| Dead or Alive 2 | `doa2` | **cart** | clone of `doa2m` | 113.7 MB | Fighting | Yes (2000) | not assessed |
| Dead or Alive 2 Millennium | `doa2m` | **cart** | parent | 113.7 MB | Fighting | Yes (2000) | not assessed |
| Death Crimson OX (USA) | `deathcox` | **cart** | parent | 62.5 MB | Light-gun | Yes (2001) | not assessed |
| Dengen Tenshi Taisen Janshi Shangri-la | `shangril` | **cart** | parent | 98.6 MB | Mahjong ⚠ | No | not assessed |
| Derby Owners Club (Japan, Rev B) | `derbyoc` | **cart** | parent | 52.5 MB | Horse-race sim ⚠ | No | not assessed |
| Derby Owners Club 2000 Ver.2 (Japan, Rev A) | `derbyo2k` | **cart** | parent | 60.7 MB | Horse-race sim ⚠ | No | not assessed |
| Derby Owners Club II Ver.2.1 (Japan, Rev B) | `derbyoc2` | **cart** | parent | 118.9 MB | Horse-race sim ⚠ | No | not assessed |
| Derby Owners Club World Edition EX (Rev D) | `derbyocw` | **cart** | parent | 46.7 MB | Horse-race sim ⚠ | No | not assessed |
| Dynamite Baseball '99 (Japan, Rev B) | `dybb99` | **cart** | parent | 106.4 MB | Sports | No | not assessed |
| Dynamite Baseball NAOMI (Japan) | `dybbnao` | **cart** | parent | 114.8 MB | Sports | No | not assessed |
| Ferrari F355 Challenge (deluxe, no link) | `f355` | **cart** | clone of `f355dlx` | 98.4 MB | Driving | Yes (2000) | not assessed |
| Ferrari F355 Challenge 2 - International Course Edition (twin/deluxe) | `f355twn2` | **cart** | parent | 104.7 MB | Driving | No | not assessed |
| Giant Gram 2000 | `gram2000` | **cart** | parent | 114.8 MB | Fighting | Yes (2000) | not assessed |
| Giant Gram: All Japan Pro Wrestling 2 (Japan) | `ggram2` | **cart** | parent | 57.0 MB | Fighting | Yes (1999) | not assessed |
| Giga Wing 2 | `gwing2` | **cart** | parent | 57.6 MB | Shmup ★ | Yes (2001) | **79.0** A · [assessment](assessments/gwing2.md) |
| Guilty Gear X | `ggx` | **cart** | parent | 89.1 MB | Fighting | Yes (2000) | not assessed |
| Gun Survivor 2 Biohazard Code: Veronica (World, BHF2 Ver.E) | `gunsur2` | **cart** | parent | 175.7 MB | Gun (3-axis) | No | **73.0** A · [assessment](assessments/gunsur2.md) |
| Heavy Metal: Geomatrix (Rev B) | `hmgeo` | **cart** | parent | 74.4 MB | Fighting | Yes (2001) | not assessed |
| Idol Janshi Suchie-Pai 3 (Japan) | `suchie3` | **cart** | parent | 102.3 MB | Mahjong ⚠ | Partial | not assessed |
| Illvelo (Illmatic Envelope) (Japan) | `illvelo` | **cart** | parent | 88.4 MB | Shmup ★ | No | **79.8** A · [assessment](assessments/illvelo.md) |
| Inu no Osanpo / Dog Walking (Japan, Export, Rev A) | `inunoos` | **cart** | parent | 79.7 MB | Simulation | No | parked G3 · [notes](assessments/inunoos.md) |
| Jambo! Safari (Rev A) | `jambo` | **cart** | parent | 31.7 MB | Sports | No | not assessed |
| Kasei Channel Mars TV (Japan) | `marstv` | **cart** | parent | 57.8 MB | Party | No | **74.6** A · [assessment](assessments/marstv.md) |
| Kick '4' Cash (Export) | `kick4csh` | **cart** | parent | 42.6 MB | Gambling/medal ⚠ | No | not assessed |
| Mamoru-kun wa Norowarete Shimatta! (Japan) | `mamonoro` | **cart** | parent | 146.1 MB | Shmup ★ | No | **76.7** A · [assessment](assessments/mamonoro.md) |
| Marvel Vs. Capcom 2: New Age of Heroes (Export, Korea, Rev A) | `mvsc2` | **cart** | parent | 87.5 MB | Fighting | Yes (2000) | not assessed |
| Mazan: Flash of the Blade (World, MAZ2 Ver.A) | `mazan` | **cart** | parent | 73.7 MB | Light-gun | No | not assessed |
| Melty Blood Actress Again Version A (Japan, Rev A) | `mbaa` | **cart** | parent | 233.9 MB | Fighting | No | **55.9** B · [assessment](assessments/mbaa.md) |
| Mushiking The King Of Beetles - Mushiking II / III / III+ (Ver. 2.001) (World) | `mushik2e` | **cart** | parent | 72.8 MB | Card battle ⚠ | No | not assessed |
| Ninja Assault (World, NJA2 Ver.A) | `ninjaslt` | **cart** | parent | 81.2 MB | Light-gun | No | not assessed |
| Oinori-daimyoujin Matsuri | `oinori` | **cart** | parent | 36.4 MB | Gambling/medal ⚠ | No | not assessed |
| OutTrigger | `otrigger` | **cart** | parent | 82.1 MB | Action | Yes (2001) | not assessed |
| Pokasuka Ghost! (Japan) | `pokasuka` | **cart** | clone of `manicpnc` | 142.3 MB | ? | No | parked G3 · [notes](assessments/pokasuka.md) |
| Power Stone | `pstone` | **cart** | parent | 43.6 MB | ? | Yes (1999) | not assessed |
| Power Stone 2 | `pstone2` | **cart** | parent | 56.7 MB | ? | Yes (2000) | not assessed |
| Project Justice / Moero! Justice Gakuen (Rev B) | `pjustic` | **cart** | parent | 126.1 MB | Fighting | Yes (2000) | not assessed |
| Puyo Puyo Da! (Japan) | `puyoda` | **cart** | parent | 111.0 MB | Puzzle ★ | Yes (1999) | **81.8** S · [assessment](assessments/puyoda.md) |
| Quiz Aa! Megami-sama ~Tatakau Tsubasa to Tomoni~ (Japan) | `qmegamis` | **cart** | parent | 60.0 MB | Quiz ⚠ | No | not assessed |
| Radirgy Noa (Japan) | `radirgyn` | **cart** | parent | 107.4 MB | Shmup ★ | No | **79.0** A · [assessment](assessments/radirgyn.md) |
| Rhythm Tengoku (Japan) | `rhytngk` | **cart** | parent | 119.9 MB | Rhythm | No | not assessed |
| Ring Out 4x4 (Rev A) | `ringout` | **cart** | parent | 39.0 MB | ? | No | not assessed |
| Samba de Amigo ver. 2000 (Japan) | `samba2k` | **cart** | parent | 159.5 MB | Rhythm | Yes (2000) | not assessed |
| Sega Marine Fishing | `smarinef` | **cart** | parent | 35.6 MB | Fishing ⚠ | Yes (2000) | not assessed |
| Sega Strike Fighter (Rev A) | `sstrkfgt` | **cart** | parent | 75.9 MB | Fighting | No | not assessed |
| Sega Tetris | `sgtetris` | **cart** | parent | 33.7 MB | Puzzle ★ | Yes (2000) | **67.6** A · [assessment](assessments/sgtetris.md) |
| Shin Nihon Pro Wrestling Toukon Retsuden 4 Arcade Edition (Japan, TRF1 Ver.A) | `toukon4` | **cart** | parent | 217.0 MB | Fighting | Yes (1999) | not assessed |
| Shooting Love 2007 (Japan) | `sl2007` | **cart** | parent | 109.3 MB | Light-gun | No | not assessed |
| Shootout Pool | `shootopl` | **cart** | parent | 16.6 MB | ? | No | not assessed |
| Spawn: In the Demon's Hand (Rev B) | `spawn` | **cart** | parent | 58.5 MB | Fighting | Yes (2000) | not assessed |
| The House of the Dead 2 (USA) | `hotd2` | **cart** | parent | 100.2 MB | Light-gun | Yes (1999) | not assessed |
| The Typing of the Dead (Rev A) | `totd` | **cart** | parent | 89.4 MB | Typing ⚠ | Yes (2000) | not assessed |
| Tokyo Bus Guide (Japan, Rev A) | `tokyobus` | **cart** | parent | 81.8 MB | Driving | Yes (1999) | not assessed |
| Touch de Uno! 2 (Japan) | `tduno2` | **cart** | parent | 49.9 MB | ? | No | not assessed |
| Touch De Zunou (Japan, Rev A) | `zunou` | **cart** | parent | 61.9 MB | Puzzle ★ | No | parked G1 · [notes](assessments/zunou.md) |
| Toy Fighter | `toyfight` | **cart** | parent | 46.0 MB | Fighting | No | not assessed |
| Virtua NBA (USA) | `virnba` | **cart** | parent | 100.2 MB | Sports | No | not assessed |
| Virtua Striker 2 Ver. 2000 (Rev C) | `vs2_2k` | **cart** | parent | 60.9 MB | ? | Yes (2000) | not assessed |
| Wave Runner GP | `wrungp` | **cart** | parent | 48.1 MB | Driving | No | not assessed |
| World Kicks (World, WK2 Ver.A) | `wldkicks` | **cart** | parent | 74.3 MB | Sports | No | not assessed |
| World Series 99 / Super Major League 99 | `smlg99` | **cart** | parent | 109.7 MB | Sports | No | not assessed |
| WWF Royal Rumble | `wwfroyal` | **cart** | parent | 104.6 MB | ? | Yes (2000) | not assessed |
| Zero Gunner 2 | `zerogu2` | **cart** | parent | 46.6 MB | Shmup ★ | Yes (2001) | **34.3** C · [assessment](assessments/zerogu2.md) |
| Zombie Revenge (Rev A) | `zombrvn` | **cart** | parent | 97.2 MB | Beat-em-up | Yes (1999) | not assessed |

### Partial DC-port notes

- **`alienfnt`** — only *Alien Front Online* reached DC (NA), a retooled online-centric version, not a straight port of this arcade game.
- **`vonot`** (Virtual-On Oratorio Tangram) — the game reached DC (JP 1999 / US 2000), but as an **earlier revision**; this exact *ver 5.66* set shipped on Xbox 360, not DC.
- **`suchie3`** — DC version was retitled and substantially altered (adult content removed, extra modes), Japan-only.

Also flagged **No** despite near-misses: `cleoftp` (only the unrelated Taito *Cleopatra Fortune* hit DC, not this NAOMI "Plus"), `sfz3ugd` (DC got base *Street Fighter Zero 3*, never the "Upper" revision), the `ggxx*` family (all went PS2/Xbox, never DC), and cancelled-but-unreleased DC ports `dygolf` / `spkrbtl` / `toyfight` / `sl2007` / `wrungp` / `wldkicks` / `dybbnao` / `illvelo`.
