# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <dirent.h>
# include <stdbool.h>
# include <sys/types.h>
# include "command.h"

void dealloc(char *buffer, FILE *infile, FILE *outfile ) {
    /* Utility to free memory, close files */
    if(buffer != NULL) { free(buffer); }
    if(infile != NULL) { fclose(infile); }
    if(outfile != NULL) { fclose(outfile); }
}

int startsWith(char *string, char *prefix) {
    /* Utility to check if a string has a prefix */
    return strncmp(string, prefix, strlen(prefix));
}

int endsWith(char *string, char *suffix) {
    /* Utility to check if a string has a suffix */
    return (strcmp(string+strlen(string)-strlen(suffix), suffix));
}

void parseLine(char *buffer, size_t bufferSize, FILE *infile, FILE *outfile) {
    /* Steps through line by line, token by toke, calling the appropriate commands */

    // Variables
    char *token;
    char *next;
    char *arg1;// = (char*)calloc(64, sizeof(char));
    char *arg2;// = (char*)calloc(64, sizeof(char));
    char whitespace[2] = " ";
    size_t input;
    bool command = false;
   

    if(infile == NULL) {
        infile = stdin;
        command = true;
        printf(">>> "); 
    }

    while((input = getline(&buffer, &bufferSize, infile)) != -1) {
            
        // Remove newline
        char *newline = strchr(buffer, '\n');
        if(newline) {
            *newline = 0;
        }

        // Tokenize the input string
        token = strtok(buffer, whitespace);

        while(token != NULL) {

            if(strncmp(token, "exit", 4) == 0) {
                dealloc(buffer, infile, outfile);
                exit(0);
            }

            else if(strncmp(token, ";", 1) == 0) {
                write(1, "Error! Unrecognized command: \n", 31);
                token = NULL;
            }


            else if(strcmp(token, "ls") == 0) {
                
                next = strtok(NULL, whitespace);
                if(next != NULL) {
                    if(strncmp(next, ";", 1) == 0) {
                        listDir();
                        next = NULL;
                        token = strtok(NULL, whitespace);
                        if(token == NULL) {
                            write(1, "Error! Unrecognized command: \n", 31);
                        }
                    }
                    else {
                        write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                        next = NULL;
                        token = NULL;
                    }
                }
                else {
                    listDir();
                    next = NULL;
                    token = strtok(NULL, whitespace);
                }                    

            }
            else if(strcmp(token, "pwd") == 0) {
                
                next = strtok(NULL, whitespace);
                if(next != NULL) {
                    if(strncmp(next, ";", 1) == 0) {
                        showCurrentDir();
                        next = NULL;
                        token = strtok(NULL, whitespace);
                        if(token == NULL) {
                            write(1, "Error! Unrecognized command: \n", 31);
                        }
                    }
                    else {
                        write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                        next = NULL;
                        token = NULL;
                    }
                }
                else {
                    showCurrentDir();
                    next = NULL;
                    token = strtok(NULL, whitespace);
                } 

            }
            else if(strcmp(token, "cat") == 0) {
                arg1 = strtok(NULL, whitespace);
                if(arg1 == NULL) { 
                    write(1, "Error: no file listed\n", 23);
                }
                else {

                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            displayFile(arg1);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        displayFile(arg1);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                }
                arg1 = NULL;
            }
            else if(strcmp(token, "mv") == 0) {
                arg1 = strtok(NULL, whitespace);
                arg2 = strtok(NULL, whitespace);

                if(arg1 == NULL || arg2 == NULL) {
                    write(1, "Error: missing arguments\n", 26);
                }
                else {
                    char *temp = calloc(32, sizeof(char));
                    strcpy(temp, arg2);

                    if(startsWith(arg1, "../") == 0 && strcmp(arg2, ".") == 0) {
                        strcpy(temp, arg1+3);
                    }

                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            moveFile(arg1, temp);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        moveFile(arg1, temp);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                    free(temp);

                }
                arg1 = NULL;
                arg2 = NULL;
                
            }
            else if(strcmp(token, "cp") == 0) {
                arg1 = strtok(NULL, whitespace);
                arg2 = strtok(NULL, whitespace);

                if(arg1 == NULL || arg2 == NULL) {
                    write(1, "Error: missing arguments\n", 26);
                }
                else {
                    
                    char *temp = calloc(32, sizeof(char));
                    strcpy(temp, arg2);

                    if(startsWith(arg1, "../") == 0 && strcmp(arg2, ".") == 0) {
                        strcpy(temp, arg1+3);
                    }

                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            copyFile(arg1, temp);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        copyFile(arg1, temp);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                    free(temp);

                }
                arg1 = NULL;
                arg2 = NULL;
                   
            }
            else if(strcmp(token, "mkdir") == 0) {
         
                arg1 = strtok(NULL, whitespace);
                if(arg1 == NULL) {
                    write(1, "Error: missing arguments\n", 26);
                }
                else {
                
                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            makeDir(arg1);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        makeDir(arg1);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                }
                arg1 = NULL;
            }
            else if(strcmp(token, "rm") == 0) {
                arg1 = strtok(NULL, whitespace);

                if(arg1 == NULL) {
                    write(1, "Error: missing arguments\n", 26);
                }                
                else {

                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            deleteFile(arg1);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        deleteFile(arg1);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                }
                arg1 = NULL; 

            }
            else if(strcmp(token, "cd") == 0) {
                arg1 = strtok(NULL, whitespace);

                if(arg1 == NULL) {
                    write(1, "Error: missing arguments\n", 26);
                }
                else {

                    next = strtok(NULL, whitespace);
                    if(next != NULL) {
                        if(strncmp(next, ";", 1) == 0) {
                            changeDir(arg1);
                            next = NULL;
                            token = strtok(NULL, whitespace);
                            if(token == NULL) {
                                write(1, "Error! Unrecognized command: \n", 31);
                            }
                        }
                        else {
                            write(1, "Error! Incorrect syntax. No control code found.\n", 49);
                            next = NULL;
                            token = NULL;
                        }
                    }
                    else {
                        changeDir(arg1);
                        next = NULL;
                        token = strtok(NULL, whitespace);
                    }

                }
                arg1 = NULL;
            }
            else if(strcmp(token, "\n") != 0) {
                write(1, "Error: Unrecognized command!\n", 30);                
                token = strtok(NULL, whitespace);
            }

        }
        if(command) {
            write(1, ">>> ", 4);
        }
    }
    dealloc(buffer, infile, outfile);
}

int main(int argc, char *argv[]) {
    setbuf(stdout, NULL);
    
    // Variables
    FILE *infile;
    FILE *outfile;

    // Allocate memory for the buffer
    char *buffer;
    size_t bufferSize = 32;
    size_t input;
    buffer = (char*)malloc(bufferSize * sizeof(char));

    // File Mode
    if(argc == 3 && (strncmp(argv[1], "-f", 2) == 0 || strncmp(argv[1], "-file", 5) == 0)) {

        outfile = freopen("output.txt", "w+", stdout);

        infile = fopen(argv[2], "r");
        if(infile == NULL) {
            write(1, "Input file missing\n", 20);
            dealloc(buffer, NULL, NULL);
            exit(1);
        }

        parseLine(buffer, bufferSize, infile, outfile);

        return 0;
    }

    // Command Mode
    else {

        parseLine(buffer, bufferSize, NULL, NULL);

        return 0;
    }
}
