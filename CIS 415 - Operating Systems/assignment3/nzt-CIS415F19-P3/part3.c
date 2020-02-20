#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <sys/time.h>
#include <pthread.h>
#include <unistd.h>
#include <sched.h>
#include <errno.h>
#include <stdbool.h>

#define URLSIZE 240
#define CAPSIZE 240
#define MAXENTRIES 100
#define MAXTOPICS 20
#define NUMPROXIES 10

int ENTRYNUM = 1;
int TOPICNUM = 0;
double DELTA = 1.0;
char topicNames[MAXTOPICS][32];
bool CLEANING = true;

typedef struct {
    int entryNum;
    struct timeval timeStamp;
    int pubID;
    char photoURL[URLSIZE];
    char photoCaption[CAPSIZE];
} topicEntry;

typedef struct {
    char *name[32];
    int topicID;
    topicEntry *buffer;
    int head;
    int tail;
    int length;
    pthread_mutex_t lock;
} CRB;

CRB topicStore[MAXTOPICS] = {[0 ... MAXTOPICS-1].lock = PTHREAD_MUTEX_INITIALIZER,};
topicEntry buffers[MAXTOPICS][MAXENTRIES+1] = {};

typedef struct {
    char *topic[20];
    int length;
    int threadID;
    char commandFileName[64];
} arguments;

typedef struct {
    bool free;
    pthread_t thread;
    arguments args;
} threadPool;

threadPool pubThreadPool[NUMPROXIES] = {[0 ... NUMPROXIES-1].free = true, [0 ... NUMPROXIES-1].args.commandFileName = {0}};
threadPool subThreadPool[NUMPROXIES] = {[0 ... NUMPROXIES-1].free = true, [0 ... NUMPROXIES-1].args.commandFileName = {0}};

pthread_cond_t CONDITION = PTHREAD_COND_INITIALIZER;
pthread_mutex_t LOCK = PTHREAD_MUTEX_INITIALIZER;


void viewBufferContents() {
    // Print out contents of a CRB
    int i = 0;
    while(i < MAXTOPICS && *topicStore[i].name != NULL) {
        printf("Buffer %d: ", i);
        for(int j = 0; j < topicStore[i].length + 1; j++) {
            printf("%d ", topicStore[i].buffer[j].entryNum);
        }
        printf("    Head: %d Tail: %d", topicStore[i].head, topicStore[i].tail);
        printf("\n");
        i++;
    }
}

int enqueue(int topicID, topicEntry *Entry) {

    for(int i = 0; i < TOPICNUM + 1; i++) {
        if(topicID == topicStore[i].topicID) {
            
            if(topicStore[i].buffer[topicStore[i].tail].entryNum == -1) {
                return 0;
            }

            struct timeval time;
            gettimeofday(&time, 0);
            Entry->timeStamp = time;

            Entry->entryNum = ENTRYNUM;
            ENTRYNUM++;

            topicStore[i].buffer[topicStore[i].tail] = *Entry;

            int next = (topicStore[i].tail + 1) % (topicStore[i].length + 1);
            topicStore[i].tail = next;

            return 1;
        }
    }
    return 0;
}

int getEntry(int topicID, int lastEntry, topicEntry *emptyEntry) {

    for(int i = 0; i < TOPICNUM + 1; i++) {
        if(topicID == topicStore[i].topicID) {

            if(topicStore[i].head == topicStore[i].tail) {
                return 0;
            }

            if(topicStore[i].buffer[topicStore[i].head].entryNum == lastEntry + 1) {
                *emptyEntry = topicStore[i].buffer[topicStore[i].head];
                return 1;
            }
            if(topicStore[i].buffer[topicStore[i].head].entryNum > lastEntry + 1) {
                *emptyEntry = topicStore[i].buffer[topicStore[i].head];
                return topicStore[i].buffer[topicStore[i].head].entryNum;
            }

            int j = (topicStore[i].head + 1) % (topicStore[i].length + 1);
            while(j != topicStore[i].head) {
                if(topicStore[i].buffer[j].entryNum == lastEntry + 1 && j != topicStore[i].tail) {
                    *emptyEntry = topicStore[i].buffer[j];
                    return 1;
                }
                if(topicStore[i].buffer[j].entryNum > lastEntry + 1 && j != topicStore[i].tail) {
                    *emptyEntry = topicStore[i].buffer[j];
                    return topicStore[i].buffer[j].entryNum;
                }
                j = (j + 1) % (topicStore[i].length + 1);
            }
            return 0;
        }
    }
    return 0;
}

int dequeue(int topicID) {
    // The dequeue only pops 1 entry at a time 
    // and return 1 or 0.
    // The cleanup thread will call dequeue on a topic 
    // until it gets a 0.

    for(int i = 0; i < TOPICNUM + 1; i++) {
        if(topicID == topicStore[i].topicID) {

            if(topicStore[i].tail == topicStore[i].head) {
                return 0;
            }

            struct timeval time_now;
            gettimeofday(&time_now, 0);

            double elapsed = (time_now.tv_sec - topicStore[i].buffer[topicStore[i].head].timeStamp.tv_sec) * 1e6;
            elapsed = (elapsed + (time_now.tv_usec - topicStore[i].buffer[topicStore[i].head].timeStamp.tv_usec)) * 1e-6;

            if(elapsed < DELTA) {
                return 0;
            }
            
            if(topicStore[i].buffer[topicStore[i].tail].entryNum == -1) {
                int prev = topicStore[i].head - 1;
                if(prev == -1) {
                    // prev = MAXENTRIES;
                    prev = topicStore[i].length;
                }

                topicStore[i].buffer[prev].entryNum = 0;

                // Actual dequeueing operation
                topicStore[i].buffer[topicStore[i].head].entryNum = -1;
                strcpy(topicStore[i].buffer[topicStore[i].head].photoURL, "\0");
                strcpy(topicStore[i].buffer[topicStore[i].head].photoCaption, "\0");

                int next = (topicStore[i].head + 1) % (topicStore[i].length + 1);
                topicStore[i].head = next;
            }
            else {
                int prev = topicStore[i].head - 1;
                if(prev == -1) {
                    prev = topicStore[i].length;
                }

                topicStore[i].buffer[prev].entryNum = 0;

                // Actual dequeueing operation
                topicStore[i].buffer[topicStore[i].head].entryNum = -1;
                strcpy(topicStore[i].buffer[topicStore[i].head].photoURL, "\0");
                strcpy(topicStore[i].buffer[topicStore[i].head].photoCaption, "\0");

                int next = (topicStore[i].head + 1) % (topicStore[i].length + 1);
                topicStore[i].head = next;
            }
            return 1;
        }
    }
    return 0;
}

void * subscriberThread(void *arg) {
    arguments *args = arg;
    subThreadPool[args->threadID].free = false;
    printf("Proxy Thread %d - type: Subscriber\n", args->threadID);

    // Wait for signal
    pthread_mutex_lock(&LOCK);
    pthread_cond_wait(&CONDITION, &LOCK);
    pthread_mutex_unlock(&LOCK);

    subThreadPool[args->threadID].free = true;
    return NULL;
}

void * publisherThread(void *arg) {
    arguments *args = arg;
    pubThreadPool[args->threadID].free = false;
    printf("Proxy Thread %d - type: Publisher\n", args->threadID);

    // Wait for signal
    pthread_mutex_lock(&LOCK);
    pthread_cond_wait(&CONDITION, &LOCK);
    pthread_mutex_unlock(&LOCK);

    pubThreadPool[args->threadID].free = true;
    return NULL;
}

void * cleanupThread(void *arg) {
    printf("Cleanup Thread Assigned\n");

    while(CLEANING){
        int i = 0;
        while(i < MAXTOPICS && *topicStore[i].name != NULL) {

            pthread_mutex_lock(&topicStore[i].lock);
            int deq = dequeue(topicStore[i].topicID);
            pthread_mutex_unlock(&topicStore[i].lock);

            // printf("        dequeue on topic queue %d returned %d\n", topicStore[i].topicID, deq);
            while(deq != 0) {

                // Critical Section
                pthread_mutex_lock(&topicStore[i].lock);
                deq = dequeue(topicStore[i].topicID);
                pthread_mutex_unlock(&topicStore[i].lock);

                // printf("        dequeue on topic queue %d returned %d\n", topicStore[i].topicID, deq);
            }
            i++;
        }
        // Wait for a bit
        sleep(10);
    }
    return NULL;
}

int main(int argc, char *argv[]) {

    // Empty Entry
    topicEntry nullEntry = {
        .entryNum = -1,
    };

    pthread_t cleanup;

    // ================================================================
    // Parse Standard Input
    // ================================================================

    // Variables
    FILE *infile;

    // Allocate memory for the buffer
    char *buffer;
    size_t bufferSize = 64;
    buffer = (char*)malloc(bufferSize * sizeof(char));
    size_t input;
    bool command = false;

    // File Input
    if(argc == 2) {
        infile = fopen(argv[1], "r");
        if(infile == NULL) {
            printf("Input file not found\n");
            free(buffer);
            return 1;
        }
    }
    // Console Input
    else {
        infile = stdin;
        command = true;
        printf(">>> "); 
    }

    while((input = getline(&buffer, &bufferSize, infile)) != -1) {
        int argNum = 1;

        for(int i = 0; i < strlen(buffer); i++) {
            if(buffer[i] ==  ' ') {
                argNum++;
            }
        }

        char *args[argNum];
        char *arg = strtok(buffer, " ");

        int i = 0;
        while(arg != NULL && i < argNum) {
            if(arg[strlen(arg)-1] == '\n') {
                arg[strlen(arg)-1] = '\0';
            }
            args[i] = arg;
            
            arg = strtok(NULL, " ");
            
            i++;
        }

        // ================================================================
        // Handle Commands
        // ================================================================

        if(strcmp(args[0], "create") == 0) {
            if(argNum < 5) {
                printf("Error: missing arguments\n");
                continue;
            }

            if(TOPICNUM == MAXTOPICS) {
                printf("Error: the number of topics cannot exceed %d\n", MAXTOPICS);
                continue;
            }

            strcpy(topicNames[TOPICNUM], args[3]);

            int l = atoi(args[4]);
            if(l > MAXENTRIES || l < 1) {
                l = (unsigned int)MAXENTRIES;
                printf("Max length exceeded. Setting to Maximum: %u", l);
            }
            topicStore[TOPICNUM].length = l;

            topicStore[TOPICNUM].buffer = buffers[TOPICNUM];
            *topicStore[TOPICNUM].name = topicNames[TOPICNUM];
            topicStore[TOPICNUM].topicID = atoi(args[2]);
            topicStore[TOPICNUM].head = 0;
            topicStore[TOPICNUM].tail = 0;
            topicStore[TOPICNUM].buffer[topicStore[TOPICNUM].length] = nullEntry; 

            TOPICNUM++;

        }
        else if(strcmp(args[0], "query") == 0) {
            if(argNum < 2) {
                printf("Error: missing arguments\n");
                continue;
            }
            if(strcmp(args[1], "topics") == 0) {
                printf("Topics:\n");
                int i = 0;
                while(i < TOPICNUM && *topicStore[i].name != NULL) {
                    printf("    topicID: %d, length: %d, name: %s\n", topicStore[i].topicID, topicStore[i].length, *topicStore[i].name);
                    i++;
                }
            }
            else if(strcmp(args[1], "publishers") == 0) {
                printf("Publishers:\n");
                int i = 0;
                while(i < NUMPROXIES && pubThreadPool[i].args.commandFileName[0] != '\0') {
                    printf("    Publisher: %d, Command File: %s\n", i, pubThreadPool[i].args.commandFileName);
                    i++;
                }
            }
            

            else if(strcmp(args[1], "subscribers") == 0) {
                printf("Subscribers:\n");
                int i = 0;
                while(i < NUMPROXIES && subThreadPool[i].args.commandFileName[0] != '\0') {
                    printf("    Subscriber: %d, Command File: %s\n", i, subThreadPool[i].args.commandFileName);
                    i++;
                }
            }
            else {
                printf("Error: Unrecognized command!\n");
                continue;
            }
        }
        else if(strcmp(args[0], "add") == 0) {
            if(argNum < 3) {
                printf("Error: missing arguments\n");
                continue;
            }
            if(strcmp(args[1], "publisher") == 0) {
                bool assigned = false;
                for(int i = 0; i < NUMPROXIES; i++) {
                    if(pubThreadPool[i].free) {
                        assigned = true;

                        pubThreadPool[i].free = false;
                        strcpy(pubThreadPool[i].args.commandFileName, args[2]);
                        pubThreadPool[i].args.threadID = i;
                        pthread_create(&pubThreadPool[i].thread, NULL, publisherThread, (void *)&pubThreadPool[i].args);

                        break;
                    }
                }
                if(!assigned) {
                    printf("Could not allocate a proxy publisher thread, waiting for one to free up\n");
                    break;
                }
            }
            else if(strcmp(args[1], "subscriber") == 0) {
                bool assigned = false;
                for(int i = 0; i < NUMPROXIES; i++) {
                    if(subThreadPool[i].free) {
                        assigned = true;

                        subThreadPool[i].free = false;
                        strcpy(subThreadPool[i].args.commandFileName, args[2]);
                        subThreadPool[i].args.threadID = i;
                        pthread_create(&subThreadPool[i].thread, NULL, subscriberThread, (void *)&subThreadPool[i].args);

                        break;
                    }
                }
                if(!assigned) {
                    printf("Could not allocate a proxy subscriber thread, waiting for one to free up\n");
                    break;
                }
            }
            else {
                printf("Error: Unrecognized command!\n");
                continue;
            }
        }
        else if(strcmp(args[0], "delta") == 0) {
            if(argNum < 2) {
                printf("Error: missing arguments\n");
                continue;
            }
            DELTA = atof(args[1]);
        }
        else if(strcmp(args[0], "start") == 0) {
            // begin thread execution
            
            pthread_create(&cleanup, NULL, cleanupThread, NULL);
            sleep(1);

            // pthread_cond_signal(&CONDITION); 
            pthread_mutex_lock(&LOCK);
            pthread_cond_broadcast(&CONDITION);
            pthread_mutex_unlock(&LOCK);

            break;
        }
        else if(strcmp(args[0], "\n") != 0) {
            printf("Error: Unrecognized command!\n");
            continue;
        }
        if(command) {
            printf(">>> ");
        }
    }

    // close file, free memory
    free(buffer);
    if(!command) { fclose(infile); }

    // ================================================================
    // Thread Joining and Exit
    // ================================================================

    // Wait for Pubs and Subs to complete
    for(int i = 0; i < NUMPROXIES; i++) {
        if(pubThreadPool[i].args.commandFileName[0] != '\0') {
            pthread_join(pubThreadPool[i].thread, NULL);
            printf("Publisher Thread %d Joined\n", pubThreadPool[i].args.threadID);
        }
        if(subThreadPool[i].args.commandFileName[0] != '\0') {
            pthread_join(subThreadPool[i].thread, NULL);
            printf("Subscriber Thread %d Joined\n", subThreadPool[i].args.threadID);
        }
    }

    // Clean the Queues once more and join the Topic Cleanup Thread
    sleep(10);
    CLEANING = false;
    pthread_join(cleanup, NULL);
    printf("Cleanup Thread Joined\n");

    // printf("\n");
    // viewBufferContents();

    return 0;
}