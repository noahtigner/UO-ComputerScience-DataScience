# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <dirent.h>
# include <stdbool.h>
# include <sys/types.h>
# include "command.h"

/*
* Description: Lab3: implement lfcat, a cross between ls and cat system calls
*
* Author: Noah Tigner
*
* Date: 10/17/2019
*
* Notes: 
* 1.
*/

void dealloc(char *buffer, FILE *infile, FILE *outfile ) {
    if(buffer != NULL) { free(buffer); }
    if(infile != NULL) { fclose(infile); }
    if(outfile != NULL) { fclose(outfile); }
}

void parseLine(char *buffer, size_t bufferSize, FILE *infile, FILE *outfile) {
   
    // Variables
    char *token;
    char whitespace[2] = " ";
    //FILE *infile;
    //FILE *outfile;
    int i;
    size_t input;
    bool command = false;

    if(infile == NULL) {
        infile = stdin;
        command = true;
        printf(">>> "); 
    }
    if(outfile == NULL) {
        outfile = stdout;
    }

    while((input = getline(&buffer, &bufferSize, infile)) != -1) {
            
        // Remove newline
        char *newline = strchr(buffer, '\n');
        if(newline) {
            *newline = 0;
        }

        // Tokenize the input string
        token = strtok(buffer, whitespace);
        // Display each token
        i = 0;

        while(token != NULL) {

            // Exit
            if(strncmp(token, "exit", 4) == 0) {
                dealloc(buffer, infile, outfile);
                exit(0);
            }

            // Write to file
            //fprintf(outfile, "T%i: %s\n", i, token);
            //handleCommand(token, outfile);
            else if(strncmp(token, "lfcat", 5) == 0) {
                lfcat();
            }

            else if(strcmp(token, "\n") != 0) {
                printf("Error: Unrecognized command!\n");
            }

            // Continue Loop
            token = strtok(NULL, whitespace);
            i++;       
        }
        if(command) {
            printf(">>> ");
        }
    }
    dealloc(buffer, infile, outfile);
}

int startsWith(char *string, char *prefix) {
    return strncmp(string, prefix, strlen(prefix));
}

int endsWith(char *string, char *suffix) {
    return (strcmp(string+strlen(string)-strlen(suffix), suffix));
}
            

void lfcat() {
	/* Define your variables here */

	FILE *outfile;
    FILE *infile;
    char cwd[256];
    struct dirent *drnt;
    DIR *dir;
    char *filename;

    char *buffer;
    size_t bufferSize = 32;
    size_t input;
    buffer = (char*)malloc(bufferSize * sizeof(char));

	/* Open the file output.txt for writing */
    outfile = fopen("output.txt", "w");

	/* Get the current directory*/
    //if(getcwd(cwd, sizeof(cwd)) != NULL) {
    //    printf("%s\n", cwd);
    //}
    getcwd(cwd, sizeof(cwd));
	
	/* Open the dir using opendir() */
    dir = opendir(cwd);
    // if dir NULL
	
	/* use a while loop to read the dir */
    while ((drnt = readdir(dir)) != NULL) {	
		/* Hint: use an if statement to skip any names that are not readable files 
         * (e.g. ".", "..", "lab-3.c", "lab3.exe", "output.txt" */
		/* Open the file */
        filename = drnt->d_name;
        //if (strcmp(filename, ".") == 0) {
        if ((startsWith(filename, ".") != 0 
                && endsWith(filename, ".c") != 0
                && endsWith(filename, ".h") != 0 
                && endsWith(filename, ".exe") != 0
                && strcmp(filename, "output.txt") != 0)
                && strchr(filename, '.')) {  
            fprintf(outfile, "File: %s\n", filename);

            infile = fopen(drnt->d_name, "r");
			
			/* Read in each line using getline() */
            while((input = getline(&buffer, &bufferSize, infile)) != -1) {
                /* Write each line to output.txt */
                fprintf(outfile, "%s", buffer);
            }
            /* print 80 "-" characters to output.txt */
            fprintf(outfile, "\n"); 
            int j = 0;
            while (j < 80) {
                fprintf(outfile, "-");
                j++;
            }
            fprintf(outfile, "\n");

			/* close the read file and frre/null assign your line buffer */
            fclose(infile);
        }
    }	
	/*close both the output file and the directory you were reading from 
     * using closedir() and fclose() */
    closedir(dir);
    //fclose(outfile);
    dealloc(buffer, NULL, outfile);
}

/* mv:
 * read in file
 * create new file at new location
 * write to new file
 * delete old file
 */

/* pwd (cant use listdirenv)
 *
 */

int main(int argc, char *argv[]) {
    setbuf(stdout, NULL);
    
    // Variables
    //char *token;
    //char whitespace[2] = " ";
    FILE *infile;
    FILE *outfile;
    //int i;
    // Allocate memory for the buffer
    char *buffer;
    size_t bufferSize = 32;
    size_t input;
    buffer = (char*)malloc(bufferSize * sizeof(char));

    // File Mode
    if(argc >= 3 && (strncmp(argv[1], "-f", 2) == 0 || strncmp(argv[1], "-file", 5) == 0)) {

        infile = fopen(argv[2], "r");
        if(infile == NULL) {
            fprintf(stderr, "Input file missing\n");
            dealloc(buffer, NULL, NULL);
            exit(1);
        }
        outfile = fopen("output.txt", "w");

        parseLine(buffer, bufferSize, infile, outfile);

        return 0;
    }
    // Command Mode
    else if(argc >= 2 && (strncmp(argv[1], "-c", 2) == 0 || strncmp(argv[1], "-command", 8) == 0)) {

        parseLine(buffer, bufferSize, NULL, NULL);

        return 0;
    }

    // No Mode Specified
    else {
        printf("Please specify Command Mode (-command or -c), or File Mode (-f or -file) with a valid input file name\n");
    }
    dealloc(buffer, NULL, NULL);
    exit(1);
}

