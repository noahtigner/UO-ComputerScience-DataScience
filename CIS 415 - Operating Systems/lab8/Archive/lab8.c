#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAXNAME 20
#define MAXQUEUES 4
#define BUFSIZE 6

int TICKETNUM = 1;

typedef struct {
    int ticketNum;
    char *dish;
} mealTicket;

typedef struct {
    char *name[MAXNAME];
    mealTicket *const buffer;
    int head;
    int tail;
    const int length;
} MTQ;

MTQ *registry[MAXQUEUES];

void contents() {
    // Print out contents of a Buffer
    int i = 0;
    while(i < MAXQUEUES) {
        // if(strcmp(*registry[i]->name, MTQ_ID) == 0) {
        printf("Buffer %d: ", i);
        for(int j = 0; j < BUFSIZE+1; j++) {
            printf("%d ", registry[i]->buffer[j].ticketNum);
        }
        // printf("\n");
        // printf("Head: %d Tail: %d\n", registry[i]->head, registry[i]->tail);
        printf("\n");
        
        i++;
    }
}


int enqueue(char *MTQ_ID, mealTicket *MT) {
    int i = 0;
    while(i < MAXQUEUES && *registry[i]->name != NULL) {

        if(strcmp(*registry[i]->name, MTQ_ID) == 0) {

            if(registry[i]->buffer[registry[i]->tail].ticketNum == -999) {
                // printf("\nTail %d is -999. (BUFSIZE) %d (BUFSIZE + 1) %d\n", registry[i]->tail, (registry[i]->tail + 1) % (BUFSIZE), (registry[i]->tail + 1) % (BUFSIZE + 1));
                // printf("Buffer Full\n\n");
                return 0;
            }

            MT->ticketNum = TICKETNUM;
            TICKETNUM++;

            // printf("Inserting %s (ticketNum %d) into tail positioned at %d\n", MT->dish, MT->ticketNum, registry[i]->tail);

            registry[i]->buffer[registry[i]->tail] = *MT;

            int next = (registry[i]->tail + 1) % (BUFSIZE + 1);
            registry[i]->tail = next;

            return 1;
        }
        i++;
    }
    return 0;   
}

int dequeue(char *MTQ_ID, int ticketNum, mealTicket *MT) {
    int i = 0;
    while(i < MAXQUEUES && *registry[i]->name != NULL) {

        if(strcmp(*registry[i]->name, MTQ_ID) == 0) {

            if(registry[i]->tail == registry[i]->head) {
                // printf("tail %d head %d\n", registry[i]->tail,registry[i]->head);
                // printf("Buffer Empty\n");
                return 0;
            }

            MT->ticketNum = registry[i]->buffer[registry[i]->head].ticketNum;
            MT->dish = registry[i]->buffer[registry[i]->head].dish;

            if(registry[i]->buffer[registry[i]->tail].ticketNum == -999) {
                // printf("if\n");
                // registry[i]->buffer[registry[i]->tail].ticketNum = -1;
                int prev = (registry[i]->head - 1) % (BUFSIZE + 1);
                registry[i]->buffer[registry[i]->head].ticketNum = -999;
                registry[i]->buffer[prev].ticketNum = 0;

                int next = (registry[i]->head + 1) % (BUFSIZE + 1);
                registry[i]->head = next;


            }
            else {
                // printf("else\n");
                // int prev = (registry[i]->head - 1) % (BUFSIZE + 2);
                int prev = registry[i]->head - 1;
                if(prev == -1) {
                    prev = BUFSIZE;
                }
                // printf("prev %d", prev);
                registry[i]->buffer[prev].ticketNum = 0;
                // registry[i]->buffer[registry[i]->tail].ticketNum = 0;
                registry[i]->buffer[registry[i]->head].ticketNum = -999;

                int next = (registry[i]->head + 1) % (BUFSIZE + 1);
                registry[i]->head = next;
            }
            return 1;
        }
        i++;
    }
    return 0;  
}

int main() {

    mealTicket nullTicket = {
        .ticketNum = -999,
        .dish = NULL,
    };

    mealTicket bufBreakfast[BUFSIZE+1] = {};
    mealTicket bufLunch[BUFSIZE+1] = {};
    mealTicket bufDinner[BUFSIZE+1] = {};
    mealTicket bufBar[BUFSIZE+1] = {};

    bufBreakfast[BUFSIZE] = nullTicket;
    bufLunch[BUFSIZE] = nullTicket;
    bufDinner[BUFSIZE] = nullTicket;
    bufBar[BUFSIZE] = nullTicket;

    MTQ Breakfast = {         
        .name = "Breakfast",
        .buffer = bufBreakfast,      
        .head = 0,          
        .tail = 0,          
        .length = BUFSIZE + 1,
    };

    MTQ Lunch = {         
        .name = "Lunch",
        .buffer = bufLunch,      
        .head = 0,          
        .tail = 0,          
        .length = BUFSIZE + 1,           
    };

    MTQ Dinner = {         
        .name = "Dinner",
        .buffer = bufDinner,      
        .head = 0,          
        .tail = 0,          
        .length = BUFSIZE + 1,           
    };

    MTQ Bar = {         
        .name = "Bar",
        .buffer = bufBar,      
        .head = 0,          
        .tail = 0,          
        .length = BUFSIZE + 1,           
    };

    registry[0] = &Breakfast;
    registry[1] = &Lunch;
    registry[2] = &Dinner;
    registry[3] = &Bar;

    mealTicket breakfast1 = {
        .ticketNum = 0,
        .dish = "eggs",
    };
    mealTicket breakfast2 = {
        .ticketNum = 0,
        .dish = "pancakes",
    };
    mealTicket breakfast3 = {
        .ticketNum = 0,
        .dish = "cereal",
    };

    mealTicket lunch1 = {
        .ticketNum = 0,
        .dish = "sando",
    };
    mealTicket lunch2 = {
        .ticketNum = 0,
        .dish = "salad",
    };
    mealTicket lunch3 = {
        .ticketNum = 0,
        .dish = "burger",
    };

    mealTicket dinner1 = {
        .ticketNum = 0,
        .dish = "pasta",
    };
    mealTicket dinner2 = {
        .ticketNum = 0,
        .dish = "steak",
    };
    mealTicket dinner3 = {
        .ticketNum = 0,
        .dish = "soup",
    };

    mealTicket bar1 = {
        .ticketNum = 0,
        .dish = "beer",
    };
    mealTicket bar2 = {
        .ticketNum = 0,
        .dish = "tequila",
    };
    mealTicket bar3 = {
        .ticketNum = 0,
        .dish = "whiskey",
    };

    // Enqueue 
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    
    enqueue("Lunch", &lunch1);
    enqueue("Lunch", &lunch2);
    enqueue("Lunch", &lunch3);

    enqueue("Dinner", &dinner1);
    enqueue("Dinner", &dinner2);
    enqueue("Dinner", &dinner3);
    
    enqueue("Bar", &bar1);
    enqueue("Bar", &bar2);
    enqueue("Bar", &bar3);

    
    // Round Robin Dequeueing while something left in any queue
    int i = 0;
    int finished = 0;
    while(finished < MAXQUEUES) {
        mealTicket empty = {
            .ticketNum = 0,
            .dish = "",
        };

        i = i % MAXQUEUES;

        if(dequeue(*registry[i]->name, 1, &empty) == 0) {
            finished++;
        }
        else {
            printf("Queue: %s - Ticket Number: %d - Dish: %s\n", *registry[i]->name, empty.ticketNum, empty.dish);
        }

        i++;
    }

    mealTicket empty = {
        .ticketNum = 0,
        .dish = "",
    };

    printf("\n================================================================\n\nTESTS\n");

    // Test A on empty queue Breakfast
    printf("Test Case: A - Result: %d\n", dequeue("Breakfast", 1, &empty));

    // Test B on full queue Breakfast
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    printf("Test Case: B - Result: %d\n", dequeue("Breakfast", 1, &empty));

    // Test C on full queue Breakfast
    enqueue("Breakfast", &breakfast1);
    enqueue("Breakfast", &breakfast2);
    enqueue("Breakfast", &breakfast3);
    printf("Test Case: C - Result: %d\n", enqueue("Breakfast", &breakfast3));

    // Test B on empty queue Bar
    printf("Test Case: D - Result: %d\n", enqueue("Bar", &empty));



    // // Additional Tests
    // printf("\n================================================================\n\nAdditional Tests\n");

    // contents();
    // for(int k = 0; k < BUFSIZE + 1; k++) {
    //     printf("enq: %d\n", enqueue("Lunch", &lunch1));
    //     contents();
    // }

    // // contents();
    // printf("\n\n");

    // for(int k = 0; k < BUFSIZE + 1; k++) {
    //     printf("deq: %d\n", dequeue("Lunch", 1, &empty));
    //     contents();
    // }
    // printf("\n\n");
    // // contents();

    // for(int k = 0; k < BUFSIZE + 1; k++) {
    //     printf("enq: %d\n", enqueue("Lunch", &lunch1));
    // }

    // contents();

    // for(int k = 0; k < BUFSIZE + 1; k++) {
    //     printf("deq: %d\n", dequeue("Lunch", 1, &empty));
    // }

    // // contents();

    // contents("Breakfast");
    // enqueue("Breakfast", &breakfast1);
    // enqueue("Breakfast", &breakfast2);
    // enqueue("Breakfast", &breakfast3);
    // enqueue("Breakfast", &breakfast1);
    // enqueue("Breakfast", &breakfast2);
    // enqueue("Breakfast", &breakfast3);
    // enqueue("Breakfast", &breakfast1);
    // enqueue("Breakfast", &breakfast2);
    // enqueue("Breakfast", &breakfast3);
    // enqueue("Breakfast", &breakfast1);
    // enqueue("Breakfast", &breakfast2);
    // enqueue("Breakfast", &breakfast3);
    // contents();
    // printf("Result: %d\n", dequeue("Breakfast", 1, &empty));
    // contents();


    return 0;
}