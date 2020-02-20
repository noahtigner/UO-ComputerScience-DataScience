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

#define URLSIZE 100
#define CAPSIZE 240
#define MAXENTRIES 8
#define MAXTOPICS 4
#define DELTA 1.0

int ENTRYNUM = 1;

typedef struct {
    int entryNum;
    struct timeval timeStamp;
    int pubID;
    char photoURL[URLSIZE];
    char photoCaption[CAPSIZE];
} topicEntry;

typedef struct {
    char *name[20];
    topicEntry *const buffer;
    int head;
    int tail;
    const int length;
    pthread_mutex_t lock;
} CRB;

CRB *topicStore[MAXTOPICS];
    
typedef struct {
    char *topic[20];
    topicEntry entries[15];
    int length;
    int threadID;
} arguments;

void viewBufferContents() {
    // Print out contents of a CRB
    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        printf("Buffer %d: ", i);
        for(int j = 0; j < MAXENTRIES+1; j++) {
            printf("%d ", topicStore[i]->buffer[j].entryNum);
        }
        printf("    Head: %d Tail: %d", topicStore[i]->head, topicStore[i]->tail);
        printf("\n");
        
        i++;
    }
}

int enqueue(char *CRB_ID, topicEntry *Entry) {
    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        if(strcmp(*topicStore[i]->name, CRB_ID) == 0) {
            
            if(topicStore[i]->buffer[topicStore[i]->tail].entryNum == -1) {
                return 0;
            }

            struct timeval time;
            gettimeofday(&time, 0);
            Entry->timeStamp = time;

            Entry->entryNum = ENTRYNUM;
            ENTRYNUM++;

            topicStore[i]->buffer[topicStore[i]->tail] = *Entry;

            int next = (topicStore[i]->tail + 1) % (MAXENTRIES + 1);
            topicStore[i]->tail = next;

            return 1;
        }
        i++;
    }

    return 0;

}

int getEntry(char *CRB_ID, int lastEntry, topicEntry *emptyEntry) {
    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        if(strcmp(*topicStore[i]->name, CRB_ID) == 0) {

            if(topicStore[i]->head == topicStore[i]->tail) {
                return 0;
            }

            if(topicStore[i]->buffer[topicStore[i]->head].entryNum == lastEntry + 1) {
                *emptyEntry = topicStore[i]->buffer[topicStore[i]->head];
                return 1;
            }
            if(topicStore[i]->buffer[topicStore[i]->head].entryNum > lastEntry + 1) {
                *emptyEntry = topicStore[i]->buffer[topicStore[i]->head];
                return topicStore[i]->buffer[topicStore[i]->head].entryNum;
            }

            int j = (topicStore[i]->head + 1) % (MAXENTRIES + 1);
            while(j != topicStore[i]->head) {
                if(topicStore[i]->buffer[j].entryNum == lastEntry + 1 && j != topicStore[i]->tail) {
                    *emptyEntry = topicStore[i]->buffer[j];
                    return 1;
                }
                if(topicStore[i]->buffer[j].entryNum > lastEntry + 1 && j != topicStore[i]->tail) {
                    *emptyEntry = topicStore[i]->buffer[j];
                    return topicStore[i]->buffer[j].entryNum;
                }
                j = (j + 1) % (MAXENTRIES + 1);
            }
            return 0;
        }
        i++;
    }
    return 0;
}

int dequeue(char *CRB_ID) {
    // The dequeue only pops 1 entry at a time 
    // and return 1 or 0.
    // The cleanup thread will call dequeue on a topic 
    // until it gets a 0.
    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        if(strcmp(*topicStore[i]->name, CRB_ID) == 0) {
            if(topicStore[i]->tail == topicStore[i]->head) {
                return 0;
            }

            struct timeval time_now;
            gettimeofday(&time_now, 0);

            double elapsed = (time_now.tv_sec - topicStore[i]->buffer[topicStore[i]->head].timeStamp.tv_sec) * 1e6;
            elapsed = (elapsed + (time_now.tv_usec - topicStore[i]->buffer[topicStore[i]->head].timeStamp.tv_usec)) * 1e-6;

            // printf("Elapsed: %f\n", elapsed);

            if(elapsed < DELTA) {
                // printf("elapsed not greater than delta\n");
                return 0;
            }
            
            if(topicStore[i]->buffer[topicStore[i]->tail].entryNum == -1) {
                int prev = topicStore[i]->head - 1;
                if(prev == -1) {
                    prev = MAXENTRIES;
                }

                topicStore[i]->buffer[topicStore[i]->head].entryNum = -1;
                topicStore[i]->buffer[prev].entryNum = 0;

                int next = (topicStore[i]->head + 1) % (MAXENTRIES + 1);
                topicStore[i]->head = next;
            }
            else {
                int prev = topicStore[i]->head - 1;
                if(prev == -1) {
                    prev = MAXENTRIES;
                }

                topicStore[i]->buffer[prev].entryNum = 0;
                topicStore[i]->buffer[topicStore[i]->head].entryNum = -1;

                int next = (topicStore[i]->head + 1) % (MAXENTRIES + 1);
                topicStore[i]->head = next;
            }
            return 1;
        }
        i++;
    }
    return 0;


}

void * subscriberThread(void *arg) {
    arguments *args = arg;
    printf("Subscriber Thread Created\n");

    char **passedIn = (char **)args->topic;

    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        if(strcmp(*topicStore[i]->name, *passedIn) == 0) {

            int last = 0;
            
            // keep looping while there is something left in the queue
            int empty = 0;
            while(empty < MAXENTRIES && topicStore[i]->tail != topicStore[i]->head) {

                struct timeval tv;
                gettimeofday(&tv, 0);

                topicEntry nullEntry = {
                    .entryNum = -1,
                    .timeStamp = tv,
                    .pubID = 0,
                    .photoURL = "",
                    .photoCaption = "",
                };

                // Critical Section
                pthread_mutex_lock(&topicStore[i]->lock);
                int get = getEntry(*passedIn, last, &nullEntry);
                pthread_mutex_unlock(&topicStore[i]->lock);


                if(get == 0) {
                    empty++;
                    sched_yield();
                }
                else if(get == 1) {
                    last++;
                    empty = 0;
                    printf("    getEntry on topic queue \"%s\" returned %d\n        queue's lastEntry is now %d\n", *passedIn, get, last);
                    
                }
                else {
                    last = get;
                    empty = 0;
                    printf("    getEntry on topic queue \"%s\" returned %d\n        queue's lastEntry is now %d\n", *passedIn, get, last);
                }
                sleep(1);
            }
            printf("Nothing left for Subscriber Thread to read\n");
            return NULL;
        }
        i++;
    }
    return NULL;
}

void * publisherThread(void *arg) {
    arguments *args = arg;
    printf("Publisher Thread Assigned\n");

    char **passedIn = (char **)args->topic;

    int i = 0;
    while(i < MAXTOPICS && topicStore[i] != NULL) {
        if(strcmp(*topicStore[i]->name, *passedIn) == 0) {

            struct timeval tv;
            gettimeofday(&tv, 0);

            for(int j = 0; j < args->length; j++) {

                // Critical Section
                pthread_mutex_lock(&topicStore[i]->lock);
                int enq = enqueue(*passedIn, &args->entries[j]);
                pthread_mutex_unlock(&topicStore[i]->lock);

                printf("    Enqueue on topic queue \"%s\" returned %d\n", *passedIn, enq);
                sleep(1);

                if(enq == 0) {
                    sched_yield();
                }
            }
            printf("Nothing left for Publisher Thread to enqueue\n");
            return NULL;
        }
        i++;
    }
    return NULL;
}

void * cleanupThread(void *arg) {
    printf("Cleanup Thread Assigned\n");

    while(1){
        int i = 0;
        while(i < MAXTOPICS && topicStore[i] != NULL) {

            pthread_mutex_lock(&topicStore[i]->lock);
            int deq = dequeue(*topicStore[i]->name);
            pthread_mutex_unlock(&topicStore[i]->lock);

            printf("    dequeue on topic queue \"%s\" returned %d\n", *topicStore[i]->name, deq);
            while(deq != 0) {

                // Critical Section
                pthread_mutex_lock(&topicStore[i]->lock);
                deq = dequeue(*topicStore[i]->name);
                pthread_mutex_unlock(&topicStore[i]->lock);

                printf("    dequeue on topic queue \"%s\" returned %d\n", *topicStore[i]->name, deq);
            }
            i++;
        }
        sleep(1);
    }
    return NULL;
}

int main() {

    // ================================================================
    // Initialize topicStore
    // ================================================================

    struct timeval tv;
    gettimeofday(&tv, 0);

    // Empty Entry
    topicEntry nullEntry = {
        .entryNum = -1,
        .timeStamp = tv,
        .pubID = 0,
        .photoURL = "",
        .photoCaption = "",
    };

    // Queue Buffers
    topicEntry top1[MAXENTRIES+1] = {};
    topicEntry top2[MAXENTRIES+1] = {};
    topicEntry top3[MAXENTRIES+1] = {};

    // Set last entry to NULL (nullEntry)
    top1[MAXENTRIES] = nullEntry;
    top2[MAXENTRIES] = nullEntry;
    top3[MAXENTRIES] = nullEntry;

    // Initialize CRBs
    CRB TopicQ1 = {
        .name = "Top1",
        .buffer = top1,
        .head = 0,
        .tail = 0,
        .length = MAXENTRIES+1,
        .lock = PTHREAD_MUTEX_INITIALIZER,
    };
    
    CRB TopicQ2 = {
        .name = "Top2",
        .buffer = top2,
        .head = 0,
        .tail = 0,
        .length = MAXENTRIES+1,
        .lock = PTHREAD_MUTEX_INITIALIZER,
    };
    
    CRB TopicQ3 = {
        .name = "Top3",
        .buffer = top3,
        .head = 0,
        .tail = 0,
        .length = MAXENTRIES+1,
        .lock = PTHREAD_MUTEX_INITIALIZER,
    };

    // Add CRBs to topicStore
    topicStore[0] = &TopicQ1;
    topicStore[1] = &TopicQ2;
    topicStore[2] = &TopicQ3;

    // ================================================================
    // Initialize Threads
    // ================================================================

    pthread_t cleanup, pub1, pub2, pub3, sub1, sub2, sub3;

    // ================================================================
    // Arguments for thread functions (topic, list of entries to enqueue, etc)
    // ================================================================

    arguments pubArgs1;
    *pubArgs1.topic = "Top1";
    pubArgs1.length = 15;
    for(int j = 0; j < pubArgs1.length; j++) {

        topicEntry entry = {
            .entryNum = 0,
            .timeStamp = tv,
            .pubID = 0,
            .photoURL = "Enqueued URL",
            .photoCaption = "Enqueued Cap",
        };

        pubArgs1.entries[j] = entry;
    }

    arguments pubArgs2;
    *pubArgs2.topic = "Top2";
    pubArgs2.length = 15;
    for(int j = 0; j < pubArgs2.length; j++) {

        topicEntry entry = {
            .entryNum = 0,
            .timeStamp = tv,
            .pubID = 0,
            .photoURL = "Enqueued URL",
            .photoCaption = "Enqueued Cap",
        };

        pubArgs2.entries[j] = entry;
    }

    arguments pubArgs3;
    *pubArgs3.topic = "Top3";
    pubArgs3.length = 15;
    for(int j = 0; j < pubArgs3.length; j++) {

        topicEntry entry = {
            .entryNum = 0,
            .timeStamp = tv,
            .pubID = 0,
            .photoURL = "Enqueued URL",
            .photoCaption = "Enqueued Cap",
        };

        pubArgs3.entries[j] = entry;
    }

    arguments subArgs1;
    *subArgs1.topic = "Top1";

    arguments subArgs2;
    *subArgs2.topic = "Top2";

    arguments subArgs3;
    *subArgs3.topic = "Top3";

    // ================================================================
    // Begin Assigning Threads and Testing
    // ================================================================

    pthread_create(&pub1, NULL, publisherThread, &pubArgs1);
    pthread_create(&pub2, NULL, publisherThread, &pubArgs2);
    pthread_create(&pub3, NULL, publisherThread, &pubArgs3);
    sleep(8);
    pthread_create(&sub1, NULL, subscriberThread, &subArgs1);
    pthread_create(&sub2, NULL, subscriberThread, &subArgs2);
    pthread_create(&sub3, NULL, subscriberThread, &subArgs3);
    sleep(2);
    pthread_create(&cleanup, NULL, cleanupThread, NULL);

    // ================================================================
    // Thread Joining
    // ================================================================

    // Wait for Pubs and Subs to complete
    pthread_join(pub1, NULL);
    pthread_join(pub2, NULL);
    pthread_join(pub3, NULL);
    printf("Publisher Thread Joined\n");
    printf("Publisher Thread Joined\n");
    printf("Publisher Thread Joined\n");
    sleep(2);
    pthread_join(sub1, NULL);
    pthread_join(sub2, NULL);
    pthread_join(sub3, NULL);
    printf("Subscriber Thread Joined\n");
    printf("Subscriber Thread Joined\n");
    printf("Subscriber Thread Joined\n");
    sleep(2);

    // ================================================================
    // Testing
    // ================================================================

    sleep(2);
    printf("\nAdditional Tests\n\n");
    
    // Fill the Queue before letting subs get entries
    pthread_cancel(cleanup);
    printf("Cleanup Thread Halted\n");
    pthread_join(cleanup, NULL);
    printf("Cleanup Thread Joined\n");
    pthread_create(&pub1, NULL, publisherThread, &pubArgs1);
    pthread_join(pub1, NULL);
    printf("Publisher Thread Joined\n");
    pthread_create(&sub1, NULL, subscriberThread, &subArgs1);
    pthread_create(&cleanup, NULL, cleanupThread, NULL);
    pthread_join(sub1, NULL);
    printf("Subscriber Thread Joined\n");
    sleep(2);

    printf("\n\n");

    // Sub tries to get an entry from a queue when it is empty
    pthread_create(&sub1, NULL, subscriberThread, &subArgs1);
    pthread_join(sub1, NULL);
    printf("Subscriber Thread Joined\n");
    sleep(2);

    // ================================================================
    // Exit
    // ================================================================

    // Clean the Queues once more and then cancel and join the Topic Cleanup Thread
    sleep(2);
    pthread_cancel(cleanup);
    printf("Cleanup Thread Halted\n");
    pthread_join(cleanup, NULL);
    printf("Cleanup Thread Joined\n");

    // Confirm CRBs are empty at termination
    printf("\n");
    viewBufferContents();

    return 0;
}