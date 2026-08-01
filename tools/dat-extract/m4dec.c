// m4dec <subkey1> <subkey2> <romfile>
// In-place M4 (Naomi FPGA stream cipher) decrypt of an assembled cart ROM.
// Algorithm transcribed verbatim from Flycast core/hw/naomi/m4cartridge.cpp
// (k_sboxes, enc_init/one_round, decrypt_one_round, decrypt). The cipher resets
// iv=0 every 16 words (index-based), so each aligned 32-byte block is independent;
// a single sequential pass from offset 0 reproduces the canonical plaintext ROM.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;

static const u8 k_sboxes[4][16] = {
	{9,8,2,11,1,14,5,15,12,6,0,3,7,13,10,4},
	{2,10,0,15,14,1,11,3,7,12,13,8,4,9,5,6},
	{4,11,3,8,7,2,15,13,1,5,14,9,6,12,0,10},
	{1,13,8,2,0,5,6,14,4,11,15,10,12,3,7,9}
};
static u16 one_round[0x10000];

static void enc_init(void) {
	for (int round_input = 0; round_input < 0x10000; round_input++) {
		u8 in[4], out[4] = {0,0,0,0};
		for (int n = 0; n < 4; n++) in[n] = (round_input >> (n*4)) & 0xf;
		u8 aux = in[3];
		for (int n = 0; n < 4; n++) {
			aux ^= k_sboxes[n][in[n]];
			for (int i = 0; i < 4; i++) out[(n - i) & 3] |= aux & (1 << i);
		}
		u16 r = 0;
		for (int n = 0; n < 4; n++) r |= (out[n] << (4*n));
		one_round[round_input] = r;
	}
}

int main(int argc, char** argv) {
	if (argc != 4) { fprintf(stderr, "usage: m4dec <subkey1> <subkey2> <romfile>\n"); return 1; }
	u16 subkey1 = (u16)strtoul(argv[1], NULL, 0);
	u16 subkey2 = (u16)strtoul(argv[2], NULL, 0);
	enc_init();

	FILE* f = fopen(argv[3], "r+b");
	if (!f) { perror("rom"); return 1; }
	fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
	u8* buf = (u8*)malloc(sz);
	if (fread(buf, 1, sz, f) != (size_t)sz) { fprintf(stderr, "read failed\n"); return 2; }

	u16 iv = 0; u8 counter = 0;
	for (long a = 0; a + 1 < sz; a += 2) {
		u16 enc = buf[a] | (buf[a+1] << 8);
		u16 dec = iv;                                       // decrypt(): dec = old iv
		iv  = one_round[(u16)(enc ^ iv) ^ subkey1] ^ subkey1;   // iv = decrypt_one_round(enc^iv, subkey1)
		dec ^= one_round[iv ^ subkey2] ^ subkey2;               // dec ^= decrypt_one_round(iv, subkey2)
		if (++counter == 16) { counter = 0; iv = 0; }
		buf[a] = dec; buf[a+1] = dec >> 8;
	}
	fseek(f, 0, SEEK_SET);
	fwrite(buf, 1, sz, f);
	fclose(f); free(buf);
	return 0;
}
