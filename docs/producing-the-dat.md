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

Also verified for the **netpic** GD games — dragntr / dragntr2 / dragntr3 (their PIC's netpic
byte is unreliable; ignoring it + the standard walk + the NAOMI-header check handles them).

**Known gaps (fix when a target needs them):**
- `wccf*` GD sets fail: CD-media discs (data track @LBA 0, 2048-byte sectors) routed through
  `NetDimm`, not the LBA-45000 GD path. Needs a gdi-driven disc layer. Exotic/network → low priority.
- **Cart games** use `cart2dat.py`, not this tool (they're not GD-ROM). M2 carts (56 of 58)
  assemble from their ROM chips — boot image is plaintext. M1 (5) / M4 (11) encrypt the whole
  ROM and still need a decoder port or the runtime-dump fallback. See the conversion matrix below.

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

## Converting the hard cases (netpic / WCCF / carts)

Every format reduces to the SAME target: a flat image whose start is a `NAOMI` header +
load-entry table. Source: Flycast `naomi_cart.cpp` (`CartridgeType` = M1/M2/M4/AW/GD),
`gdcartridge.cpp`, `m4cartridge.cpp`, `m1cartridge.cpp`, and the per-game `Games[]` table
(`naomi_roms.cpp`, which carries each game's `key` + `cart_type`).

| Case | Convertible? | How | Effort |
|------|-------------|-----|--------|
| GD-ROM, netpic==0 | ✅ done | `chd2dat.sh` | — |
| GD-ROM, netpic!=0 (dragntr…) | ✅ done | netpic byte is unreliable (Flycast note); ignore it, use the LBA-45000 walk, let the NAOMI-header check confirm the right PIC. | done |
| WCCF (wccf*, vf4, mj1) | ✅ but exotic | CD-media (data track @LBA 0, 2048-byte sectors) + routed through `NetDimm` (GDCartridge subclass), not plain GD. Parametrize base-LBA/sector-size from the `.gdi`. | med; low priority |
| Cart — M2 (49→56) | ✅ done | **Boot image + NAOMI header are PLAINTEXT** — the 315-5881 chip only decrypts selectively-protected sections at runtime (port `0x4001fffe`), NOT the boot. So the `.dat` is just the ROM chips assembled at their `Games[]` blob offsets (Normal / InterleavedWord / Copy). `cart2dat.py`. | done |
| Cart — M1 (5) | ⚠ | stream cipher + LZSS over the **whole** ROM; assembly alone = garbage. Port `m1cartridge.cpp`, or runtime-dump. | port decoder / dump |
| Cart — M4 (11) | ⚠ | FPGA 16-bit stream cipher over the **whole** ROM; key from the cart PIC (`key_data[0x5e0]`). Port `m4cartridge.cpp`, or runtime-dump. | port decoder / dump |

**Correction:** M2 was earlier assumed to need a Feistel decode and "0 plain carts → nothing to
concatenate." Both wrong — M2 ROMs are plaintext-boot, so assembling the chips IS the `.dat`.
Verified: 56 of 58 M2 sets assemble to a valid `NAOMI` image with the correct title (header at
offset 0, or 0x800000 for some). Stragglers: `hotd2` (garbage at 0 — inspect per-game),
`gunsur2` (a blob filename differs from the zip — CRC-rename; exotic light-gun title). M1/M4
genuinely encrypt the whole ROM → need the decoder port or the runtime-dump fallback below.

```
tools/dat-extract/cart2dat.py pstone      # -> tools/dat-extract/out/pstone.dat  (M2 only)
```

## Universal fallback (any cipher) — runtime dump for Ghidra

If a game's static decrypt isn't worth porting, dump from Flycast at runtime (cipher-agnostic):
every set is Flycast-runnable, and once booted the BIOS/cart HW has decrypted the boot executable
into SH-4 main RAM (`0x8c010000`+, entry ~`0x8c04xxxx`). Dumping that region gives Ghidra exactly
the running code+data — works for GD/netpic/WCCF/M1/M2/M4 alike. Trade-off vs a static `.dat`:
captures only what's loaded (boot exec + streamed regions), not the whole ROM, and needs a small
Flycast hook (you already have instrumented Flycast from the CFP port). This is the guaranteed
Ghidra-friendly path for any holdout.

## Bottom line

Library = MAME `.chd`/`.zip`, kept for the Flycast boot gate → do not touch it.
`.dat` = `chd2dat.sh <set>` per GD-ROM game, when you assess it. Do NOT batch all 152 blindly
(disk: senko alone is 266 MB; a full GD sweep is many GB). Fill decrypted-image size into
`naomi/GAME_FORMATS.md` as games are assessed. For a port candidate: check its `cart_type` in
Flycast `Games[]` — plain carts → concatenate (instant); GD netpic==0 → `chd2dat.sh`; everything
else → port that one decoder, or fall back to the runtime RAM dump.
