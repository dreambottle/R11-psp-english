#include "my_mmap.h"
#include <unistd.h>

struct sta {
    int pos;
    int len;
};

struct stb {
    char name[32];
    int filetype;
    int stuff1;
    int stuff2;
    int len;
};

int main(int argc, char **argv) {
    assert2(argc>=4 && argc<=5, "usage: %s in.afs out.afs en/ [ja/]\n", argv[0]);
    char *endir = argv[3];
    char *jadir = argc==5 ? argv[4] : NULL;
    off_t size;
    void *map = mmap_file(argv[1], &size);
    assert2(map, "can't open %s\n", argv[1]);
    assert2(!strncmp(map,"AFS",4), "not a afs file\n");
    int entries = *(int*)(map+4);
    assert(entries*8+8<=size);
    struct sta *stas = map+8;
    int i;
    
    for(i=0; i<entries; i++) {
        assert(stas[i].pos + stas[i].len <= size);
        // assert(stas[i].len > 0);
    }
    
    // for(i=1; i<entries; i++)
    //     assert(stas[i].pos == ((stas[i-1].pos + stas[i-1].len + 0x7ff) & ~0x7ff));
    
    struct sta *statoc = stas+entries;
    if(*(uint64_t*)statoc == 0)
        statoc = map+stas[0].pos-8;
        
    assert(sizeof(struct stb) == 48);
    assert(statoc->len == entries*48);
    assert(statoc->pos + statoc->len <= size);
    struct stb *stbs = map + statoc->pos;
    
    
    // if(!strcmp(argv[1], "mac.orig.afs")) {
    //     for(i=0; i<entries; i++) {
    //         assert(stbs[i].len == stas[i].len);
    //         assert(stbs[i].stuff0 == 0x107d4);
    //         assert((stbs[i].stuff1 & 0xff00ffff) == 0x1c);
    //     }
    // }
    

    if(jadir) {
        mkdir(jadir, 0755);
        assert2(!chdir(jadir), "chdir failed\n");
        for(i=0; i<entries; i++) {
			if (stas[i].pos == 0) { continue; }
            printf("-> %s\n", stbs[i].name);
            assert2(stbs[i].name[0] != '/' && !strstr(stbs[i].name, ".."), "unsafe filename\n");
            write_file(stbs[i].name, map+stas[i].pos, stas[i].len);
        }
        chdir("..");
    }

    int out_size = size*4;
    void *out = calloc(1, out_size);
    #define ALIGN(x) ((x+0x7ff)&~0x7ff)
    int off = ALIGN(entries*8+16); // 8==sizeof(sta); 16 - header
    
    for(i = 0; i < entries; i++) {
		if (stas[i].pos == 0) { continue; }

        //opening and mapping the file from the table
        char name[1000];
        sprintf(name, "%s/%s", endir, stbs[i].name);
        FILE *fh = fopen(name, "r");
        void *p;
        if(fh) {
            printf("<- %s\n", stbs[i].name);
            p = mmap_file(name, &size); 
        } else {
            // or just copying the current content
            p = map+stas[i].pos;
            size = stas[i].len;
        }

        assert(off+size < out_size);
        memcpy(out+off, p, size);
        stas[i].pos = off;
        stas[i].len = stbs[i].len = size;
        off = ALIGN(off+size);
        if(fh) {
            munmap(p, size);
            fclose(fh);
        }
    }
    memcpy(out, map, entries*8+8);
    memcpy(out+off, stbs, entries*sizeof(struct stb));
    *(int*)(out+stas[0].pos-8) = off;
    *(int*)(out+stas[0].pos-4) = entries*sizeof(struct stb);
    out_size = ALIGN(off+entries*sizeof(struct stb));
    write_file(argv[2], out, out_size);
    return 0;
}
