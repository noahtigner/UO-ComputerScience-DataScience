/*
* Description: <write a brief description of your lab>
*
* Author: <your name>
*
* Date: <today's date>
*
* Notes: 
* 1. <add notes we should consider when grading>
*/

/*-------------------------Preprocessor Directives---------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include "command.h"
/*---------------------------------------------------------------------------*/

/*----------------------------Function Definitions---------------------------*/
void lfcat()
{
	/* Define your variables here */
	
	/* Open the file output.txt for writing */
	
	/* Get the current directory*/
	
	/* Open the dir using opendir() */
	
	/* use a while loop to read the dir */
	
		/* Hint: use an if statement to skip any names that are not readable files (e.g. ".", "..", "lab-3.c", "lab3.exe", "output.txt" */
			
			/* Open the file */
			
			/* Read in each line using getline() */
				/* Write each line to output.txt */
			
			/* print 80 "-" characters to output.txt */
			
			/* close the read file and frre/null assign your line buffer */
	
	/*close both the output file and the directory you were reading from using closedir() and fclose() */
}

/*---------------------------------------------------------------------------*/
/*-----------------------------Program Main----------------------------------*/
int main() {
	setbuf(stdout, NULL);
	
	/*function vars */
	char *cBuffer;
	size_t bufferSize;
	size_t inputSize;
	char *token;
	
	/* Allocate memory to the input buffer. */
	cBuffer = (char *)malloc(bufferSize * sizeof(char));
	if( cBuffer == NULL)
	{
		printf("Error! Unable to allocate input buffer. \n");
		exit(1);
	}
	
	/*main run cycle*/
	do {
	
	printf( ">>> ");
	inputSize = getline(&cBuffer, &bufferSize, stdin);
	
	/* tokenize the input string */
	token = strtok(cBuffer, " ");
	while(token != NULL && strcmp(token, "\n")) {
		
		/*if the command is 'exit then close the program*/
		if(strcmp(token, "exit\n") == 0 || strcmp(token, "exit") == 0) { break; }
		
		/*Display any commands */
		if(strcmp(token, "lfcat\n") == 0) {lfcat();}
		else {printf("Error: Unrecognized command! \n"); break;}
		token = strtok(NULL, " ");
	}
	if(token != NULL) {if(strcmp(token, "exit\n") == 0 || strcmp(token, "exit") == 0) { break; }}
	} while (1);
	/*Free the allocated memory*/
	free(cBuffer);
	return 0;
}
/*-----------------------------Program End-----------------------------------*/
