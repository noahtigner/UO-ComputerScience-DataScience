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
int main(int argc, char **argv) {
	setbuf(stdout, NULL);

	/* Main Function Variables */
	char *token;
	char whitespace[2] = " ";
	FILE *infile;
	FILE *outfile;
	/* Allocate memory for the input buffer. */
	char *buffer;
	size_t bufferSize = 32;
	size_t input;
	buffer = (char*)malloc(bufferSize * sizeof(char));

	/*main run loop*/
	if(argc >= 2) {
		infile = fopen(argv[1], "r");
		if(infile == NULL) {
			fprintf(stderr, "Input file missing");
			free(buffer);
			exit(0);
		}
	}
	else {
		fprintf(stderr, "Please enter input and output file names");
		free(buffer);
		exit(0);
	}
        while((input = getline(&buffer, &bufferSize, infile)) != -1) {
		
		/* Remove newline */
		char *newline = strchr(buffer, '\n');
		if(newline) {
			*newline = 0;
		}
		/* Tokenize the input string */
		token = strtok(buffer, whitespace);
		/* Display each token */
		int i = 0;

		/* File for output */
		outfile = fopen("output.txt", "w");
		
		while(token != NULL) {
		
			/* Exit */
			if(strncmp(token, "exit", 4) == 0) {
				free(buffer);
				fclose(infile);
				fclose(outfile);
				exit(0);
			}

			/* Print out the command */
			fprintf(outfile, "T%i: %s\n", i, token);
				
			/* Continue */
			token = strtok(NULL, whitespace);
			i++;
		}
		/* If the user entered <exit> then exit the loop */
	}
	
	/*Free the allocated memory*/
	free(buffer);
	fclose(infile);
	fclose(outfile);
	return 1;
}
/*-----------------------------Program End-----------------------------------*/
