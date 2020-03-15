# define _GNU_SOURCE
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <dirent.h>
# include <stdbool.h>
# include <errno.h>
# include <sys/types.h>
# include <sys/wait.h>
# include "header.h"

void parseFile(char *buffer, size_t bufferSize, char *in) {

    char whitespace[2] = " ";

    FILE *infile = fopen(in, "r");
    if(infile == NULL) {
        write(1, "Input file missing\n", 20);
        // dealloc(buffer, NULL, NULL);
        free(buffer);
        exit(1);
    }

    size_t input;
    // char whitespace[2] = " ";
    size_t numLines = 0;

    while((input = getline(&buffer, &bufferSize, infile)) != -1) {
        numLines++;
    }
    
    fclose(infile);
    free(buffer);
    FILE *infile2 = fopen(in, "r");
    size_t bufferSize2 = 32;
    char *buffer2 = (char*)malloc(bufferSize2 * sizeof(char));
    size_t input2;

    char **argsList[numLines];
    int lineNum = 0;

    // pid_t *pidPool = (pid_t*)malloc(numLines * sizeof(pid_t));
    pid_t pidPool[numLines];

    while(((input2 = getline(&buffer2, &bufferSize2, infile2)) != -1) && lineNum < numLines) {
        
        char whitespace[2] = " ";
        int argNum = 1;

        for(int i = 0; i < strlen(buffer2); i++) {
            if(buffer2[i] ==  ' ') {
                argNum++;
            }
        }

        char *args[argNum+1];
        char *arg = strtok(buffer2, whitespace);

        int i = 0;
        while(arg != NULL && i < argNum) {
            if(arg[strlen(arg)-1] == '\n') {
                arg[strlen(arg)-1] = '\0';
            }
            args[i] = arg;  // strdup or stdcpy??
            
            arg = strtok(NULL, whitespace);
            i++;
        }
        args[argNum] = NULL;
        
        /**************************************************************/
        
        pidPool[lineNum] = fork();

        if(pidPool[lineNum] == 0) {
            // child
            // fclose(infile2);
            // free(buffer2);
            printf("Process: %ld - Suspended\n", (long)getpid());
            int success = execvp(args[0], args);
            if(success == -1) {
                // printf("%s\n", errno)
                perror("Error");
            }
            exit(-1);

        }
        else if(pidPool[lineNum] < 0) {
            printf("Fail");
        }
        // else {
        //     printf("Process: %ld - Joined\n", (long)getpid());
        //     // wait(pidPool[lineNum]);
        //     int stat;
        //     wait(&stat);
        //     if (WIFEXITED(stat)) {
        //         printf("Exit status: %d\n", WEXITSTATUS(stat));
        //     }
        // }


        lineNum++;
    }

    fclose(infile2);
    free(buffer2);

    for(int i = 0; i < numLines-1; i++) {
        printf("Process: %ld - Joined\n", (long)getpid());
        int stat;
        wait(&stat);
        if (WIFEXITED(stat)) {
            printf("Exit status: %d\n", WEXITSTATUS(stat));
        }
    }
}


int main(int argc, char *argv[]) {    

    FILE *infile;

    // Allocate memory for the buffer
    char *buffer;
    size_t bufferSize = 32;
    size_t input;
    buffer = (char*)malloc(bufferSize * sizeof(char));

    if(argc == 2) {

        parseFile(buffer, bufferSize, argv[1]);

        return 0;
    }
    else {
        write(1, "Argument for input file missing\n", 33);
        free(buffer);
        exit(1);
    }
    return 0;
}