# Producing a game's `.dat` (the port/assessment input)

**Do NOT batch-convert the library.** You produce a `.dat` per game, only for the
games you actually decide to assess/port. All 152 sets are already Flycast-runnable
(`naomi/`), which is the *boot gate*; the `.dat` is a *separate* artifact needed for
Ghidra static analysis and as the port build input.

## What a `.dat` is

A **flat, decrypted Naomi image with a `NAOMI` header** — the "netboot" / DIMM-image
representation, the same bytes the DIMM board holds in RAM. NOT a repack of the `.chd`.

Grounded facts (primary sources, not wiki):
- Header layout: `cleopatra/tools/netboot/docs/naomi.md` (RE'd from netdimm firmware).
  `NAOMI` magic @0x000, title table @0x030, load entries @0x360, main entrypoint @0x420.
- Parser: `cleopatra/scripts/parse_header.py` (offsets cross-checked vs `tools/netboot/naomi/rom.py`).
- Cleopatra's was `Cleopatra Fortune Plus.dat`, 109,051,904 bytes, GD-ROM game (GDL-0012),
  loads 1 MB at boot (ROM 0x0 → RAM 0x8c020000, entry 0x8c04ae2c); rest streamed at runtime.
- Flycast accepts the `.dat` directly (no rename); Ghidra loads its first 1 MB as `boot.bin`
  (`SuperH4:LE:32`, BinaryLoader, base 0x8c020000). See `cleopatra/docs/kb/{game,tooling,boot-binary}.md`.

**It is NOT a container transcode of the `.chd`.** Proof: `cleoftp/gdl-0012.chd` is 61 MB
(compressed disc); the `.dat` is 109 MB (decompressed, laid-out DIMM image). Bigger, not smaller.

## How to get one (GD-ROM games) — PROVEN

`tools/dat-extract/chd2dat.sh <set>` builds the `.dat` from the set's OWN `.chd` + PIC.
No netboot romset, no external download, zero coverage gaps — you already own every disc + key.

```
tools/dat-extract/chd2dat.sh cleoftp        # -> tools/dat-extract/out/cleoftp.dat
```

**Control test passed (CLAUDE.md rule 2):** the extractor reproduces the known-good
`cleopatra/Cleopatra Fortune Plus.dat` **byte-for-byte** — SHA1 `08c2666b053d324bca78e204aa876d4bf51fa320`
from `naomi/cleoftp/gdl-0012.chd` + `317-5083-com.pic`. Also verified to emit valid `NAOMI`
images for cvsgd, senko, moeru, quizqgd (distinct per-game keys).

**How it works (all transcribed from Flycast `core/hw/naomi/gdcartridge.cpp`, primary source):**
1. `chdman extractcd` the `.chd` → high-density data track (LBA base 45000, mode-1 sectors).
2. Read the game's DES key + ROM filename from the PIC (`picdata[0x780/0x7c0]`). The wrapper
   tries every PIC in the set zip and keeps the one that yields a `NAOMI`-headed image.
3. Walk the disc's ISO9660 filesystem to find that file (handling the 0x100-byte indirection
   that points to the real `*.BIN`), read it, DES-decrypt every 8 bytes. That's the `.dat`.

**Known gaps (fix when a target needs them):**
- `netpic != 0` games (dragntr / dragntr2 / dragntr3, some others) route through a different
  ISO branch — `extract_dat` reports and skips them. ~20 lines from `device_start` to add.
- `wccf341j` fails (investigate; WCCF is exotic/network, low port priority).
- **Cart games (~75)** are NOT GD-ROM — different decrypt path (`naomi_cart.cpp` M2/M4). Separate
  tool, not built. Tackle when a cart game is actually a port candidate.

### Fallbacks (only if the above can't cover a game)
- **Route A — netboot / DIMM-image romset**: a separate decrypted-flat-image set (how Cleopatra's
  `.dat` was originally obtained). Coverage gaps; superseded by chd2dat for anything we own a disc for.
- **Route C — dump DIMM RAM from instrumented Flycast at runtime**: heaviest; last resort.

## Verify any `.dat` before trusting it

```
python3 cleopatra/scripts/parse_header.py "<game>.dat"   # NAOMI magic, real title, entrypoint
dd if="<game>.dat" of=boot.bin bs=1M count=1             # Ghidra boot binary (first 1 MB)
/Applications/Flycast.app/Contents/MacOS/Flycast "/abs/<game>.dat"   # real boot gate — the only full proof
```

## Bottom line

Library = MAME `.chd`/`.zip`, kept for the Flycast boot gate → do not touch it.
`.dat` = `chd2dat.sh <set>` per GD-ROM game, when you assess it. Do NOT batch all 152 blindly
(disk: senko alone is 266 MB; a full GD sweep is many GB). Fill decrypted-image size into
`naomi/GAME_FORMATS.md` as games are assessed.
