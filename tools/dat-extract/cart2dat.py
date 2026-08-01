#!/usr/bin/env python3
"""cart2dat.py <set> [outdir]

Assemble a Naomi M2 cart's flat .dat (Flycast/Ghidra input) from its MAME ROM
chips. M2 carts store the boot executable + NAOMI header PLAINTEXT; the 315-5881
chip only decrypts selectively-protected sections streamed at runtime (port
0x4001fffe). So the flat image is just the ROM chips placed at their blob offsets
-- no Feistel decryption needed for the boot/header/most data that Ghidra reads.

Blob layout + rules transcribed from Flycast core/hw/naomi/naomi_cart.cpp
(the ROM-load loop) and naomi_roms.cpp (the per-game Games[] table).

M1/M4 carts encrypt the WHOLE ROM (stream cipher) -> assembly alone yields
garbage; this refuses them. GD-ROM games use chd2dat.sh instead.
"""
import os, re, sys, subprocess, tempfile

ROMS = os.environ.get("NAOMI_ROMS",
    "/Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src/core/hw/naomi/naomi_roms.cpp")
HERE = os.path.dirname(os.path.abspath(__file__))
LIB  = os.path.abspath(os.path.join(HERE, "..", "..", "naomi"))
SZ   = "/opt/homebrew/bin/7zz"

def entry_text(src, name):
    """Return the exact { ... } text of the Games[] entry named `name`."""
    m = re.search(r'"%s"\s*,' % re.escape(name), src)
    if not m:
        sys.exit("set %r not found in %s" % (name, ROMS))
    # back up to the '{' that opens this entry, then brace-match forward
    i = src.rfind("{", 0, m.start())
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{": depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0: return src[i:j+1]
        j += 1
    sys.exit("unbalanced braces for %r" % name)

def parse(name):
    src = open(ROMS).read()
    e = entry_text(src, name)
    ct = re.search(r'\b(M1|M2|M4|AW|GD)\s*,', e)
    cart_type = ct.group(1) if ct else "?"
    # blobs: { "file", 0xoff, 0xlen, 0xcrc [, TYPE [, 0xsrc]] }
    blobs = []
    for b in re.finditer(
        r'\{\s*"([^"]*)"\s*,\s*(0x[0-9a-fA-F]+)\s*,\s*(0x[0-9a-fA-F]+)\s*,\s*'
        r'(0x[0-9a-fA-F]+|0)\s*(?:,\s*(InterleavedWord|Copy|Key|Eeprom\w*|Normal|SwapWordBytes)\s*)?'
        r'(?:,\s*(0x[0-9a-fA-F]+)\s*)?\}', e):
        fn, off, ln, crc, typ, src_off = b.groups()
        blobs.append((fn, int(off,16), int(ln,16), typ or "Normal", int(src_off,16) if src_off else 0))
    return cart_type, blobs

def extract(zips, filename, crc):
    """Pull one blob file out of the set/parent zips (by name)."""
    for z in zips:
        d = tempfile.mkdtemp()
        r = subprocess.run([SZ, "e", "-y", "-o"+d, z, filename],
                           capture_output=True, text=True)
        p = os.path.join(d, os.path.basename(filename))
        if os.path.exists(p):
            return open(p, "rb").read()
    return None

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: cart2dat.py <set> [outdir]")
    name = sys.argv[1]
    out  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)

    cart_type, blobs = parse(name)
    if cart_type != "M2":
        sys.exit("%s is cart_type %s -- assembly only valid for M2 "
                 "(M1/M4 encrypt the whole ROM; use runtime dump). Aborting." % (name, cart_type))

    zips = [os.path.join(LIB, name + ".zip")]
    # clones inherit parent files; add every zip as a fallback source
    zips += [os.path.join(LIB, f) for f in os.listdir(LIB) if f.endswith(".zip")]

    size = max((off + (2*ln if typ=="InterleavedWord" else ln))
               for fn,off,ln,typ,src in blobs if typ not in ("Key","Eeprom","EepromBE16"))
    rom = bytearray(size)

    for fn, off, ln, typ, src in blobs:
        if typ in ("Key", "Eeprom", "EepromBE16"):
            continue
        if typ == "Copy":
            rom[off:off+ln] = rom[src:src+ln]
            continue
        data = extract(zips, fn, None)
        if data is None:
            sys.exit("cannot find blob %r in any zip" % fn)
        data = data[:ln]
        if typ in ("Normal", "SwapWordBytes"):
            rom[off:off+len(data)] = data
        elif typ == "InterleavedWord":
            # place source 16-bit words at every OTHER dest word (Flycast loader)
            for i in range(len(data)//2):
                rom[off+i*4    ] = data[i*2]
                rom[off+i*4 + 1] = data[i*2+1]
        else:
            sys.exit("unhandled blob_type %r" % typ)

    # NAOMI header is at offset 0, or at 0x800000 for some carts (Flycast GetBootId fallback)
    hdr = 0 if rom[:5] == b"NAOMI" else (0x800000 if rom[0x800000:0x800005] == b"NAOMI" else None)
    if hdr is None:
        sys.exit("assembled image has no NAOMI header at 0 or 0x800000 (offset 0 = %r) -- layout wrong?" % bytes(rom[:8]))
    dest = os.path.join(out, name + ".dat")
    open(dest, "wb").write(rom)
    title = rom[hdr+0x30:hdr+0x50].decode("latin1").strip()
    print("OK  %s  M2 assembled  %d bytes  hdr@0x%x  title=%r -> %s" % (name, len(rom), hdr, title, dest))

if __name__ == "__main__":
    main()
