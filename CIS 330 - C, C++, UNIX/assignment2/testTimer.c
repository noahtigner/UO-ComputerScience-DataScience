#include <stdio.h>
#include <stdlib.h>
#include "clock.h"
#include "clock.c"

int main() {
	ClockType clock;
	char in[6], char1[3], char2[3];
	long minutes, seconds;
	
	// User Input
	printf("How long should the timer run? (MM:SS) ");
	fgets(in, 6, stdin);

       	char1[0] = in[0];
	char1[1] = in[1];

	char2[0] = in[3];
	char2[1] = in[4];

	// Convert char arrays (strings) to longs
	minutes = strtol(char1, NULL, 10);
	seconds = strtol(char2, NULL, 10);

	initClock(&clock);
	initTimer(&clock, (int)minutes, (int)seconds);
	runTimer();
	cleanTimer(&clock);

	return 0;
}
