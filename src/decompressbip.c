#include "my_mmap.h"

int main(int argc, char **argv) {
    assert2(argc==3, "usage: %s in.bip out\n", argv[0]);
    off_t in_size;
    uint8_t *in = mmap_file(argv[1], &in_size);
    int out_size = *(int*)in;

    uint8_t *out = malloc(out_size);
    int actual_size = decompress_lzss(out, in+4, in_size-4);
    //printf("out file size actual: %d, expected: %d.\n", actual_size, out_size);
    
//    uint8_t *out = malloc(out_size+18);
//    memset(out, 0, 18);
//    out += 18;
//    int i = 4;
//    int o = 0;
//    int mask = 0;
//    int j;
//    while(i < in_size) {
//        mask >>= 1;
//        if(mask < 0x100)
//            mask = in[i++] | 0x8000;
//        if(mask & 1) { // literal
//            assert2(o < out_size, "overrun\n");
//            out[o++] = in[i++];
//        } else { // run
//            int off = ((in[i+1]>>4)<<8)+in[i]+18;
//            int len = (in[i+1]&0xf)+3;
//            int m = (o&~0xfff)|(off&0xfff);
//            if(m >= o) m -= 0x1000;
//            if(m < -18) fprintf(stderr, "invalid match %d len %d at %x/%x\n", m, len, i, o);
//            assert2(o+len <= out_size, "overrun\n");
//            i += 2;
//            for(j=0; j<len; j++)
//                out[o++] = out[m++];
//        }
//    }
    
    write_file(argv[2], out, actual_size);
    free(out);
    return 0;
}
