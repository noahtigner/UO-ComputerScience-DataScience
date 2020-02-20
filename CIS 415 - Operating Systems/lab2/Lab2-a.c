/*
* Description: Thursday 11am Lab
*
* Author: Noah Tigner
*
* Date: 10/8/19
*
* Notes: 
* 1. <add notes we should consider when grading>
*/

/*-------------------------Preprocessor Directives---------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*---------------------------------------------------------------------------*/

/*-----------------------------Program Main----------------------------------*/
int main() {
	setbuf(stdout, NULL);

	/* Main Function Variables */
	char *token;
	char whitespace[2] = " ";
	/* Allocate memory for the input buffer. */
	char *buffer;
	size_t bufferSize = 32;
	size_t input;
	buffer = (char*)malloc(bufferSize * sizeof(char));

	/*main run loop*/
        while(1) {
		/* Print >>> then get the input string */
		printf(">>> ");
		input = getline(&buffer, &bufferSize, stdin);
		/* Remove newline */
		char *newline = strchr(buffer, '\n');
		if(newline) {
			*newline = 0;
		}
		/* Tokenize the input string */
		token = strtok(buffer, whitespace);
		/* Display each token */
		int i = 0;
		if(token != NULL) {
			printf("\n");
		}
		while(token != NULL) {
		
			/* Exit */
			if(strncmp(token, "exit", 4) == 0) {
				free(buffer);
				exit(0);
			}

			/* Print out the command */
			printf("T%i: %s\n", i, token);
				
			/* Continue */
			token = strtok(NULL, whitespace);
			i++;
		}
		/* If the user entered <exit> then exit the loop */
	}
	
	/*Free the allocated memory*/
	free(buffer);
	return 1;
}
/*-----------------------------Program End-----------------------------------*/
