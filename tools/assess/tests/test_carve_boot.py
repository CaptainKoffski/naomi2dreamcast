#!/usr/bin/env python3
"""Run: python3 tools/assess/tests/test_carve_boot.py"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import carve_boot

def synth(hdr_at=0):
    img = bytearray(hdr_at + 0x2000)
    img[hdr_at:hdr_at + 5] = b"NAOMI"
    img[hdr_at + 0x30:hdr_at + 0x36] = b"TESTGM"                      # Japan title
    # two load entries: rom -> ram (absolute file offsets for rom)
    struct.pack_into("<III", img, hdr_at + 0x360, hdr_at + 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<III", img, hdr_at + 0x360 + 12, hdr_at + 0x1800, 0x8c020200, 0x80)
    struct.pack_into("<I", img, hdr_at + 0x360 + 24, 0xFFFFFFFF)      # terminator
    struct.pack_into("<II", img, hdr_at + 0x420, 0x8c020000, 0x8c020100)
    img[hdr_at + 0x1000:hdr_at + 0x1100] = b"A" * 0x100
    img[hdr_at + 0x1800:hdr_at + 0x1880] = b"B" * 0x80
    return bytes(img)

def test_carve_at_0():
    blob, meta = carve_boot.carve(synth(0))
    assert meta["hdr_at"] == 0 and meta["title"] == "TESTGM"
    assert meta["base"] == "0x8c020000" and meta["entry"] == "0x8c020000"
    assert len(blob) == 0x280                       # span 0x8c020000..0x8c020280
    assert blob[0:0x100] == b"A" * 0x100
    assert blob[0x100:0x200] == b"\x00" * 0x100     # gap zero-filled
    assert blob[0x200:0x280] == b"B" * 0x80

def test_carve_at_800000():
    blob, meta = carve_boot.carve(synth(0x800000))
    assert meta["hdr_at"] == 0x800000 and blob[0:0x100] == b"A" * 0x100

def test_carve_fallback():
    # Test hdr-relative fallback: small rom values (< 0x100000) are treated as hdr-relative
    # when hdr = 0x800000. Entry stored with rom=0x1000 means real file offset 0x801000.
    hdr_at = 0x800000
    img = bytearray(hdr_at + 0x2000)
    img[hdr_at:hdr_at + 5] = b"NAOMI"
    img[hdr_at + 0x30:hdr_at + 0x36] = b"HDRREL"                      # Title
    # Entry with small rom (will be treated as hdr-relative: 0x800000 + 0x1000 = 0x801000)
    struct.pack_into("<III", img, hdr_at + 0x360, 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<I", img, hdr_at + 0x360 + 12, 0xFFFFFFFF)      # Terminator
    struct.pack_into("<II", img, hdr_at + 0x420, 0x8c020000, 0x8c020000)
    # Payload at hdr_at + 0x1000 (file offset 0x801000)
    img[hdr_at + 0x1000:hdr_at + 0x1100] = b"C" * 0x100
    blob, meta = carve_boot.carve(bytes(img))
    assert meta["hdr_at"] == 0x800000 and meta["title"] == "HDRREL"
    assert blob[0:0x100] == b"C" * 0x100  # Payload was correctly read from hdr-relative offset

def test_carve_rejects_illegal_flag_bits():
    # Bits 31/29 are never legitimate in a cart load-entry offset (legal = 29-bit
    # address + bit-30 encrypted-read flag). Without this guard, garbage like
    # 0x80001000 masks into bounds and carves wrong bytes silently.
    for bad in (0x80001000, 0x20000000):
        img = bytearray(0x2000)
        img[0:5] = b"NAOMI"
        img[0x30:0x36] = b"BADBIT"
        struct.pack_into("<III", img, 0x360, bad, 0x8c020000, 0x100)
        struct.pack_into("<I", img, 0x360 + 12, 0xFFFFFFFF)
        struct.pack_into("<II", img, 0x420, 0x8c020000, 0x8c020000)
        img[0x1000:0x1100] = b"X" * 0x100
        try:
            carve_boot.carve(bytes(img))
            assert False, "expected ValueError for illegal flag bits 0x%x" % bad
        except ValueError:
            pass

def test_carve_rejects_entry_point_outside_blob():
    # A mis-carve that survives the bounds checks almost always leaves the
    # header entrypoint outside [base, top) — make that loud.
    img = bytearray(0x2000)
    img[0:5] = b"NAOMI"
    img[0x30:0x36] = b"BADENT"
    struct.pack_into("<III", img, 0x360, 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<I", img, 0x360 + 12, 0xFFFFFFFF)
    struct.pack_into("<II", img, 0x420, 0x8c100000, 0x8c020000)  # entry outside blob
    img[0x1000:0x1100] = b"Y" * 0x100
    try:
        carve_boot.carve(bytes(img))
        assert False, "expected ValueError for entrypoint outside carved image"
    except ValueError:
        pass

def test_carve_garbage_raises_valueerror():
    # Documents the exception type run_battery.py's static_scan() now catches (final-review
    # IMPORTANT-2): a malformed-but-produced .dat must degrade to dat_available=False, not
    # traceback out and lose the capture.
    try:
        carve_boot.carve(b"garbage")
        assert False, "expected ValueError on a non-NAOMI blob"
    except ValueError:
        pass

def test_carve_m4_encrypted_entry():
    # M4 load entries set bit 30 of the rom offset as the "read via decryption
    # stream" flag, not an address bit (kb §4.q: rom=0x40000000 across 5 sets).
    # For cart images (hdr at 0) carve must apply the hardware address decode.
    img = bytearray(0x2000)
    img[0:5] = b"NAOMI"
    img[0x30:0x36] = b"M4TEST"
    struct.pack_into("<III", img, 0x360, 0x40000000 | 0x1000, 0x8c020000, 0x100)
    struct.pack_into("<I", img, 0x360 + 12, 0xFFFFFFFF)      # terminator
    struct.pack_into("<II", img, 0x420, 0x8c020000, 0x8c020000)
    img[0x1000:0x1100] = b"M" * 0x100
    blob, meta = carve_boot.carve(bytes(img))
    assert meta["hdr_at"] == 0 and meta["title"] == "M4TEST"
    assert blob[0:0x100] == b"M" * 0x100
    assert meta["entries"] == [[0x1000, 0x8c020000, 0x100]]   # masked offset recorded

if __name__ == "__main__":
    test_carve_at_0(); print("test_carve_at_0 OK")
    test_carve_at_800000(); print("test_carve_at_800000 OK")
    test_carve_fallback(); print("test_carve_fallback OK")
    test_carve_garbage_raises_valueerror(); print("test_carve_garbage_raises_valueerror OK")
    test_carve_rejects_illegal_flag_bits(); print("test_carve_rejects_illegal_flag_bits OK")
    test_carve_rejects_entry_point_outside_blob(); print("test_carve_rejects_entry_point_outside_blob OK")
    test_carve_m4_encrypted_entry(); print("test_carve_m4_encrypted_entry OK")
    print("ALL OK")
