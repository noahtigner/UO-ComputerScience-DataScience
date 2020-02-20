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

// Global
pid_t pidPool[10];
int running = 0;

// Round Robin
void alarmHandler(int num) {

    int count = 0;
    while(pidPool[count] != -999) {
        count++;
    }

    int index = 0;
    while(index < count) {
        kill(pidPool[index], SIGSTOP);
        index++;
    }

    int stat;
    int i = 1;
    while( i < count+1) {
        running = (running + 1) % count;

        if(waitpid(pidPool[running], &stat, WNOHANG) == 0 && pidPool[running] != 0) {
            printf("Sending %d SIGCONT\n", pidPool[running]);

            kill(pidPool[running], SIGCONT);
            break;
        }
        i++;
    }
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

    for(int i = 0; i < 10; i++) {
        pidPool[i] = -999;
    }

    size_t numLines = 10;

    char **argsList[10];
    int lineNum = 0;

    struct sigaction al = {0};
    al.sa_handler = &alarmHandler;
    sigaction(SIGALRM, &al, NULL);

    while(((input = getline(&buffer, &bufferSize, infile)) != -1) && lineNum < numLines) {
        
        int argNum = 1;

        for(int i = 0; i < strlen(buffer); i++) {
            if(buffer[i] ==  ' ') {
                argNum++;
            }
        }

        char *args[argNum+1];
        char *arg = strtok(buffer, whitespace);

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
        
        pidPool[lineNum] = fork();

        if(pidPool[lineNum] == 0) {
            
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

    fclose(infile);
    free(buffer);

    sleep(2);


    bool stillGoing = true;
    while(stillGoing == true) {

        // checks if theres still processes
        stillGoing = false;
        int j = 0;
        while(pidPool[j] != -999) {
            int response = kill(pidPool[j], 0);
            if(response != -1) {
                stillGoing = true;
            }
            j++;
        }

        int quantum = 5;

        alarm(quantum);
        sleep(quantum);
    }

    printf("Process: %ld - Joined\n", (long)getpid());
    int stat = 0;
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