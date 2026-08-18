#!/usr/bin/env python3
"""cart2dat.py <set> [outdir]

Assemble a Naomi M2 cart's flat .dat (Flycast/Ghidra input) from its MAME ROM
chips. M2 carts store the boot executable + NAOMI header PLAINTEXT; the 315-5881
chip only decrypts selectively-protected sections streamed at runtime (port
0x4001fffe). So the flat image is just the ROM chips placed at their blob offsets
-- no Feistel decryption needed for the boot/header/most data that Ghidra reads.

Blob layout + rules transcribed from Flycast core/hw/naomi/naomi_cart.cpp
(the ROM-load loop) and naomi_roms.cpp (the per-game Games[] table).

M1/M4 carts encrypt the WHOLE ROM (stream cipher): M4 is assembled then
stream-decrypted in place via m4dec (subkeys from the PIC Key blob); M1 boot
code is plaintext (asset data stays LZSS-compressed). GD-ROM uses chd2dat.sh.
"""
import os, re, sys, subprocess, tempfile

ROMS = os.environ.get("NAOMI_ROMS",
    "/Users/captainkoffski/AntigravityProjects/cleopatra/tools/flycast-src/core/hw/naomi/naomi_roms.cpp")
HERE = os.path.dirname(os.path.abspath(__file__))
LIB  = os.path.abspath(os.path.join(HERE, "..", "..", "naomi"))
SZ   = "/opt/homebrew/bin/7zz"

def entry_text(src, name):
    """Return the exact { ... } text of the Games[] entry named `name`."""
    # anchor on the entry's own name field ('{' + name); a bare name match also hits
    # clones' parent_name references and would assemble the WRONG set (mushik2e -> mushikc)
    m = re.search(r'\{\s*"%s"\s*,' % re.escape(name), src)
    if not m:
        sys.exit("set %r not found in %s" % (name, ROMS))
    i = src.rfind("{", 0, m.end())
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
        r'\{\s*"([^"]*)"\s*,\s*(0x[0-9a-fA-F]+|\d+)\s*,\s*(0x[0-9a-fA-F]+|\d+)\s*,\s*'
        r'(0x[0-9a-fA-F]+|\d+)\s*(?:,\s*(InterleavedWord|Copy|Key|Eeprom\w*|Normal|SwapWordBytes)\s*)?'
        r'(?:,\s*(0x[0-9a-fA-F]+|\d+)\s*)?\}', e):
        fn, off, ln, crc, typ, src_off = b.groups()
        blobs.append((fn, int(off,0), int(ln,0), typ or "Normal",
                      int(src_off,0) if src_off else 0, int(crc,0)))
    return cart_type, blobs

_crcmap_cache = {}
def _crcmap(z):
    """Map CRC(hex, lower) -> path for a zip (cached)."""
    if z not in _crcmap_cache:
        m, path = {}, None
        out = subprocess.run([SZ, "l", "-slt", z], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.startswith("Path = "): path = line[7:]
            elif line.startswith("CRC = ") and path: m[line[6:].strip().lower()] = path
        _crcmap_cache[z] = m
    return _crcmap_cache[z]

def extract(zips, filename, crc):
    """Pull one blob out of the set/parent zips: by filename, else by CRC (handles
    renamed/extension-swapped dumps, e.g. gunsur2's bhf1ma8.4e <-> .4d)."""
    for z in zips:
        d = tempfile.mkdtemp()
        subprocess.run([SZ, "e", "-y", "-o"+d, z, filename], capture_output=True, text=True)
        p = os.path.join(d, os.path.basename(filename))
        if os.path.exists(p):
            return open(p, "rb").read()
    if crc:
        want = "%08x" % crc
        for z in zips:
            hit = _crcmap(z).get(want)
            if hit:
                d = tempfile.mkdtemp()
                subprocess.run([SZ, "e", "-y", "-o"+d, z, hit], capture_output=True, text=True)
                p = os.path.join(d, os.path.basename(hit))
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
    if cart_type not in ("M1", "M2", "M4"):
        sys.exit("%s is cart_type %s -- this tool handles M1/M2 (assemble) and M4 (assemble+decrypt). "
                 "GD-ROM uses chd2dat.sh. Aborting." % (name, cart_type))

    zips = [os.path.join(LIB, name + ".zip")]
    # clones inherit parent files; add every zip as a fallback source
    zips += [os.path.join(LIB, f) for f in os.listdir(LIB) if f.endswith(".zip")]

    size = max((off + (2*ln if typ=="InterleavedWord" else ln))
               for fn,off,ln,typ,src,crc in blobs if typ not in ("Key","Eeprom","EepromBE16"))
    rom = bytearray(size)
    key_blob = key_crc = None

    for fn, off, ln, typ, src, crc in blobs:
        if typ == "Key":
            key_blob, key_crc = fn, crc
            continue
        if typ in ("Eeprom", "EepromBE16"):
            continue
        if typ == "Copy":
            rom[off:off+ln] = rom[src:src+ln]
            continue
        data = extract(zips, fn, crc)
        if data is None:
            sys.exit("cannot find blob %r (crc %08x) in any zip" % (fn, crc))
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

    dest = os.path.join(out, name + ".dat")
    open(dest, "wb").write(rom)

    if cart_type == "M4" and rom[:5] == b"NAOMI":
        # some M4 dumps (e.g. sl2007) are already stored decrypted -- don't re-encrypt them
        cart_type = "M4-plain"

    if cart_type == "M4":
        # whole-ROM stream cipher; key (subkey1/2) from the PIC Key blob at 0x5e0/0x5e4
        if key_blob is None:
            os.remove(dest); sys.exit("M4 %s: no Key blob in Games[]" % name)
        kd = extract(zips, key_blob, key_crc)
        if kd is None or len(kd) < 0x5e8:
            os.remove(dest); sys.exit("M4 %s: cannot load key blob %r" % (name, key_blob))
        subkey1 = (kd[0x5e2] << 8) | kd[0x5e0]
        subkey2 = (kd[0x5e6] << 8) | kd[0x5e4]
        m4dec = os.path.join(HERE, "m4dec")
        if not os.path.exists(m4dec):
            subprocess.run(["clang", "-O2", "-w", os.path.join(HERE, "m4dec.c"), "-o", m4dec], check=True)
        subprocess.run([m4dec, str(subkey1), str(subkey2), dest], check=True)
        rom = bytearray(open(dest, "rb").read(0x800010))  # reload head for validation

    # NAOMI header is at offset 0, or 0x800000 for some M2 carts (Flycast GetBootId fallback)
    hdr = 0 if rom[:5] == b"NAOMI" else (0x800000 if rom[0x800000:0x800005] == b"NAOMI" else None)
    if hdr is None:
        os.remove(dest)
        sys.exit("%s: no NAOMI header at 0 or 0x800000 after %s (offset 0 = %r)" %
                 (name, "decrypt" if cart_type == "M4" else "assembly", bytes(rom[:8])))
    title = rom[hdr+0x30:hdr+0x50].decode("latin1").strip()
    verb = {"M4": "M4 assembled+decrypted", "M4-plain": "M4 assembled (already plaintext)",
            "M1": "M1 assembled (boot plaintext; asset data stays LZSS-compressed)"}.get(cart_type, "M2 assembled")
    print("OK  %s  %s  %d bytes  hdr@0x%x  title=%r -> %s" % (name, verb, size, hdr, title, dest))

if __name__ == "__main__":
    main()
