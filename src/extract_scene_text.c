#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "my_mmap.h"

// Scene layout:
// x0 - control table, 4byte-aligned. Some bytes here are offsets to strings in the text area.
// The text offset is often followed by an int with xffff in the upper half.
// Text offsets in the table don't always go in same order as the strings.

// Text section start can be found by 8 0xff bytes right before it.
// In 16 bytes before the text area, there is an int32 with an approximate number of text entries.
// It is duplicated right after the text section.
// Strings are null-terminated. Section and everything after it is unaligned
// Tail always has different content, but same size - 24 bytes:
//   int32 entries count(again)
//   int32[5] - unknown


typedef struct
{
    uint32_t num_entries;
    uint32_t unknown1;
    uint32_t unknown2;
    uint32_t unknown3;
    uint32_t unknown4;
    uint32_t unknown5;
} table_tail_t;

// start and end offsets should be aligned to 4 bytes
off_t find_addr_in_mem(uint32_t addr, void *mem, off_t start_off, off_t end_off)
{
    start_off &= -(off_t)4;
    off_t p, ret = -1;
    for(p = start_off + 4; p < end_off; p += 4)
    {
        if (*(uint32_t *)(mem + p) == addr
                && (   (*(uint32_t *)(mem + p - 4) & 0xff) == 0x61
                    || (*(uint32_t *)(mem + p + 4) & 0xffff0000) == 0xffff0000 // common patterns
                    ))
        {
            if (ret != -1)
            {
                printf("Ambiguous addr:%X! found at %x and %x\n", addr, (int)ret, (int)p);
            }
            else ret = p;
        }
    }

    return ret;
}

int main(int argc, char **argv)
{
    assert(sizeof(table_tail_t) == 0x18);
    assert2(argc == 3, "usage: %s in_scene out_txt\n", argv[0]);
    char *in_name = argv[1];
    char *out_name = argv[2];

    off_t size;
    void *scn = mmap_file(in_name, &size);

    //read tail
    table_tail_t *tail = (table_tail_t *)(scn + size - 0x18);
    uint32_t entries_expected_tail = tail->num_entries + tail->unknown1;
    // printf("%s: Tail: entry count: %d\n", argv[0], tail->num_entries);

    // find text area offset
    off_t control_area_off = 0x0;
    off_t text_area_off = -1;
    uint32_t entries_expected_head = 0;
    for (off_t i = control_area_off + 8; i < size - 4; i += 4)
    {
        if (0xffffffff == *(uint32_t *)(scn + i)
                && 0xffffffff == *(uint32_t *)(scn + i + 4))
        {
            text_area_off = i + 8;
            entries_expected_head = *(uint32_t *)(scn + i - 8);
            break;
        }
    }
    if (text_area_off == -1)
    {
        fprintf(stderr, "%s: Text area not found in %s\n", in_name, argv[0]);
        exit(1);
    }

    // find strings
    printf("%s: Text area starts at %X.\n", in_name, (int)text_area_off);
    char *strings[0x1000];
    off_t table_offsets[0x1000]; // simply inserted a big enough number
    int n, entries_detected;
    off_t current_off = text_area_off;
    for(n = 0; current_off < (size - 0x18); ++n)
    {
        strings[n] = (char *)(scn + current_off);

        // manually resolving some cases
        if (current_off == 0x1BBE && text_area_off == 0x1030) table_offsets[n] = 0x550; //COEP_01.SCN
        else if (current_off == 0x1BE9 && text_area_off == 0x1030) table_offsets[n] = 0x558; //COEP_01.SCN
        else if (current_off == 0x543E && text_area_off == 0x25F0) table_offsets[n] = 0x1888; //SA7_09.SCN
        else if (current_off == 0x1682 && text_area_off == 0xF40) table_offsets[n] = 0x434; //SAEP_06.SCN
        //standard search
        else table_offsets[n] = find_addr_in_mem((uint32_t)current_off, scn, control_area_off, text_area_off);

        if (table_offsets[n] == -1) {
            fprintf(stderr, "Error: address %X not found!\n", current_off);
            exit(1);
        }

        current_off += strlen(strings[n]) + 1;
    }
    entries_detected = n;
    printf("Strings read: %d\n", entries_detected);

    // write output
    FILE *outfile = fopen(out_name, "w");
    fprintf(outfile, "text area offset and size:\n0x%X\n0x%X\n", (uint32_t)text_area_off, (uint32_t)(current_off - text_area_off));
    for(n = 0; n < entries_detected; ++n)
    {
        fprintf(outfile, "0x%X\n%s\n\n", (uint32_t)table_offsets[n], strings[n]);
        fflush(outfile);
    }

}