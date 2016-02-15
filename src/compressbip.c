#include "my_mmap.h"

// Ok, so I don't actually do any compression.
// There are better algorithms out there; no point in saving a few kb of
// installed hdd space at the cost of increasing bandwidth by a similar amount...

int main(int argc, char **argv) {
    assert2(argc==3, "usage: %s in out.bip\n", argv[0]);
    off_t in_size;
    uint8_t *in = mmap_file(argv[1], &in_size);
    int out_size = (in_size*9+7)/8 + 4;
    uint8_t *out = malloc(out_size);
    *(int*)out = in_size;
    int i=0, o=4;
    while(i<in_size) {
        if(!(i&7))
            out[o++] = 0xff;
        out[o++] = in[i++];
    }
    assert(o == out_size);
    write_file(argv[2], out, out_size);
    return 0;
}
