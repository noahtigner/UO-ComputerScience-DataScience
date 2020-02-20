#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    long long i;
    int minutes = 1, j;
    char name[128];

/*
 * process environment variable and command line arguments
 */
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-minutes") == 0) {
            i++;
            minutes = atoi(argv[i]);
        } else if (strcmp(argv[i], "-name") == 0) {
            i++;
            strcpy(name, argv[i]);
        } else {
            fprintf(stderr, "Illegal flag: `%s'\n", argv[i]);
            exit(1);
        }
    }
    for (j = 0; j < minutes; j++) {
        for (i = 0; i < 30000000000; i++) {
            ;
        }
    }
    return 0;
}
