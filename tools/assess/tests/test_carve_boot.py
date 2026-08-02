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

if __name__ == "__main__":
    test_carve_at_0(); print("test_carve_at_0 OK")
    test_carve_at_800000(); print("test_carve_at_800000 OK")
    test_carve_fallback(); print("test_carve_fallback OK")
    print("ALL OK")
