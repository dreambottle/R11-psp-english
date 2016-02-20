#include "my_mmap.h"

int main(int argc, char **argv) {
    assert2(argc==3, "usage: %s in.bip out\n", argv[0]);
    off_t in_size;
    uint8_t *in = mmap_file(argv[1], &in_size);
    int out_size = *(int*)in;
    uint8_t *out = malloc(out_size);
    
	int actual_size = decompress_lzss(out, in+4, in_size-4);
	//printf("out file size actual: %d, expected: %d.\n", actual_size, out_size);
    
	write_file(argv[2], out, actual_size);
    free(out);
    return 0;
}
