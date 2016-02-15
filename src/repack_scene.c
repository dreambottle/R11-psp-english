#include "my_mmap.h"

static char *memstr(char *haystack, char *needle, int lenh, int lenn, int step) {
    int i, j;
    for(i=0; i<=lenh-lenn; i+=step)
        for(j=0; haystack[i+j] == needle[j]; j++)
            if(j == lenn-1)
                return haystack+i;
    return NULL;
}

int main(int argc, char **argv) {
    assert2(argc==4, "usage: %s in.ja.bin in.en.txt out.en.bin\n", argv[0]);
    off_t in_size, en_size;
    unsigned char *in = mmap_file(argv[1], &in_size);
    unsigned char *en = mmap_file(argv[2], &en_size);
    int i, j;

    // find the first line
    unsigned char *p = memstr(in, "%K%P", in_size, 5, 1);
    unsigned char *kn = memstr(in, "%K%N", in_size, 5, 1);
    if(!p || (kn && kn < p)) p = kn;
    assert2(p, "can't find start of text\n");
    int l1 = p-in;
    int l2 = l1+5;
    while(in[l1-1]) l1--;

    // find the table of contents
    int toc;
    for(i=12;; i+=2) {
        assert2(i<4000 && i<in_size, "can't find toc\n");
        if(*(uint16_t*)(in+i) == l2) {
            int l1a = *(uint16_t*)(in+i-10);
            if(l1a >= l1 && l1a < l2) {
                // l1 search isn't exact because the preceding data doesn't necessarily end with a 0, so update it with the value from the toc
                l1 = l1a;
                toc = i-10;
                break;
            } else if ((p = memstr(in, "\x73\x00", i-10, 2, 1))) {
                l1a = *(uint16_t*)(p+2);
                if(l1a >= l1 && l1a < l2) {
                    l1 = l1a;
                    toc = p+2-in;
                    break;
                }
            }
        }
    }

    // find all lines
    int lines = 0;
    int in_offs[(in_size-l1)/2];
    in_offs[0] = l1;
    for(i=l1; i<in_size-12; i++)
        if(!in[i])
            in_offs[++lines] = i+1;

    int n1=0, n2=l1;
    unsigned char en2[l1+en_size*3+100];
    memcpy(en2, in, l1);
    int en2_offs[lines];

    toc-=2;
    int prev_toc = toc;
    for(i=0; i<lines; i++) {
        // change toc pointer
        p = memstr(in+toc+2, (char*)&in_offs[i], l1-toc-2, 2, 2);
        assert2(p, "failed to find toc entry #%d (%x) in %x..%x\n", i, in_offs[i], toc, l1);
        if(p-in==0x29f6 && in_offs[i]==0x6030) {
            // kludge: manually resolve an ambiguous case in CO1_10
            p = in+0x2bbe;
            assert(*(uint16_t*)p == 0x6030);
        }
        if(p-in==0x2a2 && in_offs[i]==0x148f) { // CO6_03
            p = in+0x2cc;
            assert(*(uint16_t*)p == 0x148f);
        }
        if(p-in==0x5b4 && in_offs[i]==0x1eff) { // SA2_14
            p = in+0x5c8;
            assert(*(uint16_t*)p == 0x1eff);
        }
        prev_toc = toc;
        toc = p-in;
        p = memstr(in+prev_toc+2, (char*)&in_offs[i-1], toc-prev_toc-2, 2, 2);
        assert2(!p, "ambiguous toc %x=%x %x=%x\n", prev_toc, *(uint16_t*)(in+prev_toc), (int)(p-in), *(uint16_t*)p);
        *(uint16_t*)(en2+toc) = n2;

        // convert en line
        en2_offs[i] = n2;
        for(;;) {
            assert2(n1 < en_size, "line counts don't match <\n");
            int c = en[n1++];
            if(c == '\n') {
                en2[n2++] = 0;
                break;
            } else if(c != '\r') {
                en2[n2++] = c;
                if(c < 0x20 || c >= 0x7f) // 2byte char. this isn't what my shift_jis doc says, but it is what R11 checks for
                    en2[n2++] = en[n1++];
            }
        }

        // replace duplicate lines with a pointer to the previous copy
        for(j=0; j<i; j++) {
            if(!strcmp(en2+en2_offs[j], en2+en2_offs[i])) {
                n2 = en2_offs[i];
                *(uint16_t*)(en2+toc) = en2_offs[i] = en2_offs[j];
                break;
            }
        }
    }
    assert2(n1 == en_size, "line counts don't match >\n");
    assert2(n2 < 0x10000, "script bigger than 64KB\n");

    // output
    memcpy(en2+n2, in+in_size-12, 12);
    write_file(argv[3], en2, n2+12);
    return 0;
}
