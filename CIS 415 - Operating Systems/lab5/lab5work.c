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
# include <signal.h>

void childHandler(int num) {
    // write(1, "Child\n", 7);
    printf("Child Process: %ld - Received signal: %d", (long)getpid(), num);

    

}

// void signaler(pid_t *pool) {

// }

void execute() {

    int numLines = 5;
    pid_t pidPool[numLines];

    for(int i = 0; i < numLines; i++) {
        pidPool[i] = fork();

        if(pidPool[i] == 0) {
            // printf("Process: %ld - Suspended\n", (long)getpid());
            signal(SIGUSR1, childHandler);

            int success = execlp("./lab5.exe", NULL);
            if(success == -1) {
                // printf("%s\n", errno)
                perror("Error");
            }
            exit(-1);

        }
        else if(pidPool[i] < 0) {
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
    }

    for(int i = 0; i < numLines-1; i++) {
        kill(getpid(pidPool[i]), SIGUSR1);
    }

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
    execute();
    return 0;
}