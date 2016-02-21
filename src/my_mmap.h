#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>

#ifndef MY_MMAP_H
#define MY_MMAP_H

#define assert2(cond, ...) if(!(cond)) { fprintf(stderr, __VA_ARGS__); exit(1); }

static void *mmap_file(const char *name, off_t *size)
{
    int fd = open(name, O_RDONLY);
    assert2(fd>=0, "mmap can't open '%s'\n", name);
    struct stat stats;
    stat(name, &stats);
    *size = stats.st_size;
    assert2(*size>0, "empty '%s'\n", name);
    void *map = mmap(0, *size, PROT_READ|PROT_WRITE, MAP_PRIVATE, fd, 0);
	close(fd);
    assert2(map, "can't mmap '%s'\n", name);
    return map;
}

static void write_file(const char *name, void *buf, off_t size)
{
    FILE *fh = fopen(name, "wb");
    assert2(fh, "can't open '%s' for writing\n", name);
    assert2(size == fwrite(buf, 1, size, fh), "can't write to '%s'\n", name);
    fclose(fh);
}

#endif // MY_MMAP_H
