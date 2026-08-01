// Naomi GD-ROM .chd -> decrypted flat .dat extractor.
// Algorithm + DES transcribed verbatim from Flycast core/hw/naomi/gdcartridge.cpp
// (GDCartridge::device_start / find_file / des_*). Primary source, not a wiki.
//
// Input: a game PIC (16KB "real PIC binary") + the disc's high-density data
// track as a raw 2352-byte/sector .bin (chdman extractcd track 3, LBA base 45000).
// Output: the decrypted DIMM image == the .dat Flycast/Ghidra consume.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <string>
typedef uint8_t  u8;
typedef uint32_t u32;
typedef uint64_t u64;

#include "des_block.c"   // DES tables, permutate, des_generate_subkeys, des_encrypt_decrypt<>, rev64, FILENAME_LENGTH

// ---- disc access: track3 raw 2352 sectors, mode1 user data at offset 16, base LBA 45000 ----
static FILE* g_track = nullptr;
static const u32 TRACK_BASE_LBA = 45000;
static const int SECTOR_RAW = 2352, USER_OFF = 16, USER_LEN = 2048;

static void read_gdrom(u32 lba, u8* dst, u32 count) {
    for (u32 i = 0; i < count; i++) {
        long off = (long)(lba + i - TRACK_BASE_LBA) * SECTOR_RAW + USER_OFF;
        if (fseek(g_track, off, SEEK_SET) != 0 || fread(dst + i*USER_LEN, 1, USER_LEN, g_track) != (size_t)USER_LEN) {
            fprintf(stderr, "read_gdrom failed at lba %u\n", lba+i); exit(2);
        }
    }
}

// verbatim from gdcartridge.cpp
static void find_file(const char *name, const u8 *dir_sector, u32 &file_start, u32 &file_size) {
    file_start = 0; file_size = 0;
    for (u32 pos = 0; pos < 2048 && dir_sector[pos] != 0; pos += dir_sector[pos]) {
        if (dir_sector[pos + 25] & 2) continue;
        char fname[FILENAME_LENGTH + 1] = {};
        int len = dir_sector[pos + 32]; if (len > FILENAME_LENGTH) len = FILENAME_LENGTH;
        for (int i = 0; i < len; i++) { u8 c = dir_sector[pos + 33 + i]; if (c == ';') break; fname[i] = c; }
        bool found = false;
        if (name[0] == '*') { char *p = strchr(fname, name[1]); if (p && !strcmp(p, &name[1])) found = true; }
        else found = strcmp(fname, name) == 0;
        if (found) { file_start = *(u32*)&dir_sector[pos + 2]; file_size = *(u32*)&dir_sector[pos + 10]; return; }
    }
}

int main(int argc, char** argv) {
    if (argc != 4) { fprintf(stderr, "usage: %s <pic> <track3.bin> <out.dat>\n", argv[0]); return 1; }
    // ---- PIC: key + rom filename (RomSize >= 0x4000 "real PIC binary" branch) ----
    FILE* pf = fopen(argv[1], "rb"); if (!pf) { perror("pic"); return 1; }
    u8 pic[0x4000]; if (fread(pic, 1, 0x4000, pf) != 0x4000) { fprintf(stderr, "pic must be >=16KB\n"); return 1; } fclose(pf);
    char name[128] = {};
    for (int i = 0; i < 7; i++) name[i]   = pic[0x7c0 + i*2];
    for (int i = 0; i < 7; i++) name[i+7] = pic[0x7e0 + i*2];
    u64 key = 0;
    for (int i = 0; i < 7; i++) key |= (u64)pic[0x780 + i*2] << (56 - i*8);
    key |= pic[0x7a0];
    u8 netpic = pic[0x6ee];
    fprintf(stderr, "key=%08x%08x name='%s' netpic=%u\n", (u32)(key>>32), (u32)key, name, netpic);
    if (netpic) { fprintf(stderr, "netpic!=0 path not implemented (this game routes differently)\n"); return 3; }

    g_track = fopen(argv[2], "rb"); if (!g_track) { perror("track"); return 1; }

    u8 buffer[2048], dir_sector[2048];
    read_gdrom(TRACK_BASE_LBA + 16, buffer, 1);                 // primary volume descriptor
    u32 path_table = *(u32*)&buffer[0x8c];
    read_gdrom(path_table, buffer, 1);                         // path table
    u32 dir = *(u32*)&buffer[0x2];                             // root dir extent (first path table entry)
    read_gdrom(dir, dir_sector, 1);
    u32 file_start = 0, file_size = 0;
    find_file(name, dir_sector, file_start, file_size);
    if (file_start && file_size == 0x100) {                    // indirection: real rom name inside
        read_gdrom(file_start, buffer, 1);
        memset(name, 0, 128); memcpy(name, buffer + 0xc0, FILENAME_LENGTH - 1);
        fprintf(stderr, "indirect rom name='%s'\n", name);
    }
    find_file(name, dir_sector, file_start, file_size);
    if (file_start == 0) find_file("*.BIN", dir_sector, file_start, file_size);
    if (file_start == 0) { fprintf(stderr, "file to decrypt not found (wrong PIC?)\n"); return 4; }
    fprintf(stderr, "file_start=%u file_size=%u\n", file_start, file_size);

    // ---- load file, DES-decrypt every 8 bytes (des_encrypt_decrypt<decrypt=true>) ----
    u32 sectors = (file_size + 2047) / 2048;
    std::vector<u8> data((size_t)sectors * 2048);
    read_gdrom(file_start, data.data(), sectors);
    u32 subkeys[32];
    des_generate_subkeys(rev64(key), subkeys);
    u64* p = (u64*)data.data();
    for (size_t i = 0; i + 8 <= data.size(); i += 8, p++) *p = des_encrypt_decrypt<true>(*p, subkeys);

    FILE* out = fopen(argv[3], "wb");
    fwrite(data.data(), 1, file_size, out);   // write exactly file_size (sector-rounded region)
    fclose(out);
    fprintf(stderr, "wrote %u bytes -> %s\n", file_size, argv[3]);
    // header sanity
    fprintf(stderr, "header magic: '%.16s'\n", (char*)data.data());
    return 0;
}
