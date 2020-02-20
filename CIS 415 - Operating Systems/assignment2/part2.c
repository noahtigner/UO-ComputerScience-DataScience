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

void signalHandler(int num) {
    printf("Child Process: %ld - Received signal: %d\n", (long)getpid(), num);
}

void parseFile(char *buffer, size_t bufferSize, char *in) {

    char whitespace[2] = " ";

    FILE *infile = fopen(in, "r");
    if(infile == NULL) {
        write(1, "Input file missing\n", 20);
        free(buffer);
        exit(1);
    }

    size_t input;
    size_t numLines = 0;

    // Get lenght of files = number of processes
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

    pid_t pidPool[numLines];

    struct sigaction act = {0};
    act.sa_handler = &signalHandler;
    sigaction(SIGUSR1, &act, NULL);

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

        printf("ARGS[0] %s\n", args[0]);
        
        pidPool[lineNum] = fork();

        if(pidPool[lineNum] == 0) {

            sigset_t sigset;
            sigemptyset(&sigset);
            sigaddset(&sigset, SIGUSR1);
            sigprocmask(SIG_BLOCK, &sigset, NULL);

            printf("%d Hit sig wait\n", pidPool[lineNum]);
            int sig;
            int result = sigwait(&sigset, &sig);
            while(result != 0) {
                result = sigwait(&sigset, &sig);
            }
            
            printf("Process: %ld - Suspended\n", (long)getpid());

            int success = execvp(args[0], args);
            if(success == -1) {
                perror("Error");
            }
            exit(-1);

        }
        else if(pidPool[lineNum] < 0) {
            printf("Fail\n");
        }

        lineNum++;
    }

    fclose(infile2);
    free(buffer2);

    for(int i = 0; i < numLines; i++) {
        printf("Calling SIGUSR1 on %d\n", pidPool[i]);
        kill(pidPool[i], SIGUSR1);
    }
    sleep(7);
    for(int i = 0; i < numLines; i++) {
        printf("Calling SIGUSR1 on %d\n", pidPool[i]);
        kill(pidPool[i], SIGUSR1);
    }
    sleep(5);
    for(int i = 0; i < numLines; i++) {
        printf("Calling SIGSTOP on %d\n", pidPool[i]);
        kill(pidPool[i], SIGSTOP);
    }
    sleep(5);
    for(int i = 0; i < numLines; i++) {
        printf("Calling SIGCONT on %d\n", pidPool[i]);
        kill(pidPool[i], SIGCONT);
    }
    sleep(5);

    printf("Process: %ld - Joined\n", (long)getpid());
    int stat;
    wait(&stat);
    if (WIFEXITED(stat)) {
        printf("Exit status: %d\n", WEXITSTATUS(stat));
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