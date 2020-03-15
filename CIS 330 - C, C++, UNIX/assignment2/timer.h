#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "clock.h"
#ifndef TIMER_H_
#define TIMER_H_

int min;
int sec;
ClockType cl;

// Initialize the timer with the user-provided input
void initTimer(ClockType *clock, int minutes, int seconds);

// Run the timer -- print out the time each second
void runTimer();

// Clean up memory (as needed)
void cleanTimer(ClockType  *clock);

#endif /* TIMER_H_ */
