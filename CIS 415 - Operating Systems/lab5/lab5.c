/*
* Description: A simple lab showing signal processing
*
* Author: Jared Hall
*
* Date: 10/21/2019
*
* Notes:
* 1. to be done in lab
*/

/*-------------------------Preprocessor Directives---------------------------*/
# define _GNU_SOURCE
# include <stdio.h>
# include <stdlib.h>
# include <dirent.h>
# include <string.h>
# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>
/*---------------------------------------------------------------------------*/


void signalHandler(int num) {
    printf("Child Process: %ld - Received signal: %d\n", (long)getpid(), num);

	sigset_t sigset;
	sigemptyset(&sigset);
	sigaddset(&sigset, SIGUSR1);
	sigprocmask(SIG_BLOCK, &sigset, NULL);

	int sig;
	int result = sigwait(&sigset, &sig);
	if(result == 0) {
		printf("Sigwait received signal: %d\n", sig);
	}
}

void signaler(pid_t pidPool[], int sig) {
	write(1, "Signaler Function Called\n", 26);
	for(int i = 0; i < 5; i++) {
		kill(pidPool[i], sig);
	}
}

/*-----------------------------Program Main----------------------------------*/
int	 main() {
	//variable definitions
	pid_t pidPool[5];
	id_t pid, w;
	int wstatus;

	struct sigaction act;
	act.sa_handler = &signalHandler;
	sigaction(SIGUSR1, &act, NULL);

	for(int k = 0; k < 5; k++) {

		pidPool[k]  = fork();
		if (pidPool[k] == 0) {
			int i = 0;


			printf("Child Process: %i - Starting infinite loop...\n", getpid());
			while(1) {
				i++;
				if(i%10000) {
				printf("Child Process: %i - Running infinite loop...\n", getpid());
				i=0;
				}
				sleep(2);
			}
		} 
		// else {
		// 	//else this is an existing proc i.e. the parent

		// 	// signaler(pidPool);
		// 	// signaler(pidPool, SIGUSR1);
		// 	// signaler(pidPool, SIGUSR1);

		// 	printf("Parent Process: %i, Waiting for child to finish...\n", getpid());
		// 	w = waitpid(pid, &wstatus, WUNTRACED | WCONTINUED);
		// 	printf("All child processes joined. Exiting.\n");
		// }
	}

	signaler(pidPool, SIGUSR1);
	sleep(10);
	signaler(pidPool, SIGUSR1);
	sleep(10);
	signaler(pidPool, SIGINT);
	// signaler(pidPool, SIGUSR1);

	printf("Parent Process: %i, Waiting for child to finish...\n", getpid());
	// w = waitpid(pid, &wstatus, WUNTRACED | WCONTINUED);
	w = wait(&wstatus);
	printf("All child processes joined. Exiting.\n");
}
/*-----------------------------Program End-----------------------------------*/
