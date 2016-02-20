#include "my_mmap.h"
#include "lzss.h"

int main(int argc, char **argv) {
    assert2(argc==3, "usage: %s in out.bip\n", argv[0]);
    off_t in_size;
    uint8_t *in = mmap_file(argv[1], &in_size);
	printf("Original size: %d bytes\n", (int)in_size);
	off_t out_size = (in_size*9+7)/8 + 4; //worst case
    uint8_t *out;

	out = malloc(out_size);
    *(int*)out = in_size;
	uint8_t *out_end = compress_lzss(out+4, out_size-4, in, in_size);
	off_t compressed_size = out_end - out;
	
	/*
	// this code doesn't do any compression
	out = malloc(out_size+18);
	*(int*)out = in_size;
	int i=0, o=4;
    while(i<in_size) {
        if(!(i&7))
            out[o++] = 0xff;
        out[o++] = in[i++];
    }
    assert(o == out_size);
	off_t compressed_size = o;
	*/
	
	printf("Compressed size: %d bytes\n", (int)compressed_size);
    write_file(argv[2], out, compressed_size);
	free(out);
    return 0;
}