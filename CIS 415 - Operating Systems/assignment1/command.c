# include <stdio.h>
# include <string.h>
# include <stdlib.h>
# include <stdbool.h>
# include "command.h"
# include <fcntl.h>
# include <unistd.h>
# include <dirent.h>

void listDir() { // ls
    char ls[256];
    struct dirent *drnt;
    DIR *dir;
    char *filename;

    if(getcwd(ls, sizeof(ls)) == NULL) {
        write(1, "Error: unable to read from current directory\n", 46);
    }
    else {
        if((dir = opendir(ls)) == NULL) {
            write(1, "Error: unable to open current directory\n", 41);
        }
        else {
            while((drnt = readdir(dir)) != NULL) {

                filename = drnt->d_name;
                if(!startsWith(filename, ".") == 0) {
                    strcat(filename, " ");
                    write(1, filename, strlen(filename));

                }
            }
            write(1, "\n", 2);
        }
    }
    closedir(dir);
}

void showCurrentDir() { // pwd
    char ls[256];

    if(getcwd(ls, sizeof(ls)) == NULL) {
        write(1, "Error: unable to read from current directory\n", 46);
    }
    else {
        strcat(ls, "\n");
        write(1, ls, strlen(ls));
    }
}

void makeDir(char *dirName) { // mkdir
    int status;
    char cd[64];
    char path[256];

    // path/dirName
    getcwd(cd, sizeof(cd));
    strcpy(path, "");
    strcat(path, cd);
    strcat(path, "/");
    strcat(path, dirName);

    int success = mkdir(path, 0777);
    if(success != 0) {
        write(1, "Error: couldn't create directory\n", 34);
    }
}

void changeDir(char *dirName) { // cd
    int success = chdir(dirName);  

    if(success != 0) {
        write(1, "Error: coudn't change directory\n", 33);
    }
}

void copyFile(char *sourcePath, char *destinationPath) { // cp
    int in_size, in_descriptor, out_size, out_descriptor;
    char *in_buffer = (char*)calloc(2048, sizeof(char));

    in_descriptor = open(sourcePath, O_RDONLY);
    if(in_descriptor < 0) {
        write(1, "Error: can't open file\n", 24);
    }
    else {
        in_size = read(in_descriptor, in_buffer, 2048);

        out_descriptor = open(destinationPath, O_WRONLY | O_CREAT, 0777);
        if(out_descriptor < 0) {
            write(1, "Error: can't open file\n", 24);
            close(in_descriptor);
        }
        else {
            out_size = write(out_descriptor, in_buffer, strlen(in_buffer));

            close(in_descriptor);
            close(out_descriptor);
        }
    }
    free(in_buffer);
}

void moveFile(char *sourcePath, char *destinationPath) { // mv
    int success = rename(sourcePath, destinationPath);
    
    if(success != 0) {
        write(1, "Error: can't move file\n", 24);
    } 
}

void deleteFile(char *filename) { // rm
    int status = unlink(filename);
    
    if(status != 0) {
        write(1, "Error: can't delete file\n", 26);
    }
}

void displayFile(char *filename) { // cat

        int size, descriptor;
        char *buffer = (char*)calloc(2048, sizeof(char));
        strcpy(buffer, "");

        descriptor = open(filename, O_RDONLY);
        if(descriptor < 0) {
            write(1, "Error: can't open file\n", 24);
        }
        else {
            size = read(descriptor, buffer, 2048);
            write(1, buffer, strlen(buffer));

            close(descriptor);  
        }

        free(buffer);
}
