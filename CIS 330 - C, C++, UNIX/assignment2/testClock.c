#include "clock.h"

int main() {
	ClockType clock;

	initClock(&clock);
	printClock(clock.now, &clock);
	cleanClock(&clock);

	return 0;
}
