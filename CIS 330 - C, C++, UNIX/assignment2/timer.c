#include <stdlib.h> // for malloc
#include <string.h> // for strcpy and strlen
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include "timer.h" // interface header

// Initialize the timer with the user-provided input
void initTimer(ClockType *clock, int minutes, int seconds) {
	extern int min;
        extern int sec;
	extern ClockType cl;
	
	cl = *clock;
	cl.minutes = minutes;
	cl.seconds = seconds;
	cl.hours = 99;	//special value so that printClock drops the hours
}

// Run the timer -- print out the time each second
void runTimer() {
	extern int min;
        extern int sec;
	extern ClockType cl;

	// Count-Down
	while(cl.minutes > 0 || cl.seconds > 0) {
		printClock(cl.now, &cl);	
		printf("\n");
		sleep(1);

		if(cl.seconds > 0) {
			cl.seconds -= 1;
		}
		else {
			cl.minutes -= 1;
			cl.seconds = 59;
		}
	}
	printClock(cl.now, &cl);
}

// Clean up memory (as needed)
void cleanTimer(ClockType  *clock) {
	// Nothing to free
}


