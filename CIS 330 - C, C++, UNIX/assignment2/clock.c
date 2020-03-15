#include <stdlib.h> // for malloc
#include <string.h> // for strcpy and strlen
#include <stdio.h>
#include <time.h>
#include "clock.h" // interface header

void initClock(ClockType *clock) {

	// Use time.h
	time(&clock->now);
	struct tm*local = localtime(&clock->now);
	// Set ClockType object's member variables
	clock->hours = local->tm_hour;
	clock->minutes = local->tm_min;
	clock->seconds = local->tm_sec;

	// Change to 12-hour style
	if(clock->hours > 12) {
		clock->hours = clock->hours % 12;
	}


}

void printClock(const time_t cur_time, const ClockType *clock) {
	
	const int numRows = 8, numColumns = 5;
	int i, j, min0, min1, sec0, sec1;

	// Split tens/ones of minutes and seconds (easer to handle cases)
	min0 = clock->minutes / 10;
	min1 = clock->minutes - (clock->minutes / 10) * 10;

	sec0 = clock->seconds / 10;
	sec1 = clock->seconds - (clock->seconds / 10) * 10;
	
	// Statically allocated ascii Arrays
	char* zero[] = {" @@@ ",
			"@   @",
			"@   @",
			"@   @",
			"@   @",
			"@   @",
			"@   @",
			" @@@ "};
	

	char* one[] =  {"  @  ",
			" @@  ",
			"  @  ",
			"  @  ",
			"  @  ",
			"  @  ",
			"  @  ",
			"@@@@@"};

	char* two[] =  {" @@@ ",
			"@   @",
			"    @",
			"    @",
			"   @ ",
			"  @  ",
			" @   ",
			"@@@@@"};

	char* three[] ={" @@@ ",
			"@   @",
			"    @",
			"  @@ ",
			"  @@ ",
			"    @",
			"@   @",
			" @@@ "};

	char* four[] = {"   @ ",
			"  @@ ",
			" @ @ ",
			"@@@@@",
			"   @ ",
			"   @ ",
			"   @ ",
			"   @ "};

	char* five[] = {"@@@@@",
			"@    ",
			"@    ",
			"@@@@ ",
			"    @",
			"    @",
			"@   @",
			" @@@ "};

	char* six[] =  {" @@@ ",
			"@   @",
			"@    ",
			"@@@@ ",
			"@   @",
			"@   @",
			"@   @",
			" @@@ "};

	char* seven[] ={"@@@@@",
			"    @",
			"    @",
			"    @",
			"   @ ",
			"  @  ",
			" @   ",
			"@    "};

	char* eight[] ={" @@@ ",
			"@   @",
			"@   @",
			"  @@ ",
			" @@  ",
			"@   @",
			"@   @",
			" @@@ "};

	char* nine[] = {" @@@ ",
			"@   @",
			"@   @",
			" @@@@",
			"    @",
			"    @",
			"    @",
			"    @"};

	char* colon[] ={"     ",
			"     ",
			"  @  ",
			"     ",
			"     ",
			"  @  ",
			"     ",
			"     "};

	// Iterate through ascii arrays, print line by line
	for(i = 0; i < numRows; i++) {
		if(clock->hours != 99) {	// Skip for timer
			switch(clock->hours){
				case 1: printf("%s %s", zero[i], one[i]);
					break;
				case 2: printf("%s %s", zero[i], two[i]);
					break;
				case 3: printf("%s %s", zero[i], three[i]);
					break;
				case 4: printf("%s %s", zero[i], four[i]);
					break;
				case 5: printf("%s %s", zero[i], five[i]);
					break;
				case 6: printf("%s %s", zero[i], six[i]);
					break;
				case 7: printf("%s %s", zero[i], seven[i]);
					break;
				case 8: printf("%s %s", zero[i], eight[i]);
					break;
				case 9: printf("%s %s", zero[i], nine[i]);
					break;
				case 10: printf("%s %s", one[i], zero[i]);
					break;
				case 11: printf("%s %s", one[i], one[i]);
					break;
				case 12: printf("%s %s", one[i], two[i]);
					break;
			}
		printf("%s", colon[i]);
		}

		switch(min0) {
			case 0: printf("%s ", zero[i]);
			      break;
			case 1: printf("%s ", one[i]);
                              break;
			case 2: printf("%s ", two[i]);
                              break;
			case 3: printf("%s ", three[i]);
                              break;
			case 4: printf("%s ", four[i]);
                              break;
			case 5: printf("%s ", five[i]);
                              break;	
		}

		switch(min1) {
			case 0: printf("%s", zero[i]);
                              break;
                        case 1: printf("%s", one[i]);
                              break;
                        case 2: printf("%s", two[i]);
                              break;
                        case 3: printf("%s", three[i]);
                              break;
                        case 4: printf("%s", four[i]);
                              break;
                        case 5: printf("%s", five[i]);
                              break;
			case 6: printf("%s", six[i]);
                              break;
                        case 7: printf("%s", seven[i]);
                              break;
                        case 8: printf("%s", eight[i]);
                              break;
                        case 9: printf("%s", nine[i]);
                              break;
		}

		printf("%s", colon[i]);

		switch(sec0) {
                        case 0: printf("%s ", zero[i]);
                              break;
                        case 1: printf("%s ", one[i]);
                              break;
                        case 2: printf("%s ", two[i]);
                              break;
                        case 3: printf("%s ", three[i]);
                              break;
                        case 4: printf("%s ", four[i]);
                              break;
                        case 5: printf("%s ", five[i]);
                              break;
                }

                switch(sec1) {
                        case 0: printf("%s", zero[i]);
                              break;
                        case 1: printf("%s", one[i]);
                              break;
                        case 2: printf("%s", two[i]);
                              break;
                        case 3: printf("%s", three[i]);
                              break;
                        case 4: printf("%s", four[i]);
                              break;
                        case 5: printf("%s", five[i]);
                              break;
                        case 6: printf("%s", six[i]);
                              break;
                        case 7: printf("%s", seven[i]);
                              break;
                        case 8: printf("%s", eight[i]);
                              break;
                        case 9: printf("%s", nine[i]);
                              break;
                }
		printf("\n");
	}
}

void cleanClock(ClockType *clock) {
	// Arrays allocated statically, does nothing
}


