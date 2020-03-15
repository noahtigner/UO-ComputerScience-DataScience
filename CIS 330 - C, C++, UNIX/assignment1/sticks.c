#include <stdio.h>
#include <stdlib.h>
#include <time.h>      
#include <string.h>

int getUserChoice(int current_sticks) {
   
    printf("Player 1: How many sticks do you take (1-3)? ");
    int player_sticks = 0;
 
    scanf("%d", &player_sticks);
    while(player_sticks < 0 || player_sticks > 3) {
        printf("Error: incorrect number of sticks\n");
	printf("Player 1: How many sticks do you take (1-3)? ");
        scanf("%d", &player_sticks);    
    }
    if (player_sticks > current_sticks) return current_sticks;
    return player_sticks;
}

int getComputerChoice(int current_sticks) {

    int sticks = current_sticks - 1;
    sticks %= 4;
    if(sticks == 0) {
	int rand_choice = rand() % 3 + 1;
        if (rand_choice > current_sticks) return current_sticks;
        return rand_choice;
    }
    return sticks;
}

int main(int argc, char** argv) {
    int user, computer, number_sticks;

    srand (time(NULL)); /* for reproducible results, you can call srand(1); */

    printf("Welcome to the game of sticks!\n");
    printf("How many sticks are there on the table initially (10-100)? \n");
    scanf("%d", &number_sticks);

    if(number_sticks < 10 || number_sticks > 100) {
	    printf("Error: incorrect number of sticks\n ");
	    exit(1);
    }
    while(number_sticks > 0) {
	    if(number_sticks > 0) {
	        number_sticks -= getUserChoice(number_sticks);   
            if(number_sticks < 1) {
		        printf("Computer wins!\n");
                exit(1);
	        }
	        printf("There are %d sticks on the board\n\n", number_sticks);
	    }
	    if(number_sticks > 0) {
	        int pull = getComputerChoice(number_sticks);
            printf("Computer selects %d\n", pull);
            number_sticks -= pull;
	        if(number_sticks < 1) {
		        printf("You win!\n");
	            exit(1);
            }
   	        printf("There are %d sticks on the board\n\n", number_sticks);
	    }
    }

}
