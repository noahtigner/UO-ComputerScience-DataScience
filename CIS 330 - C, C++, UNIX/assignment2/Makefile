# Define some variables: 
SOURCES = clock.c timer.c     # could also use patterns $(wildcard *.c)
HEADERS = clock.h timer.h
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS = -std=c11 -g -fPIC

# Next, we have the rules defining how the action corresponding to each target 
# should be performed. 
#
# Anatomy of a rule:
# Target : Dependencies
#    Bash commands (must be indented using TAB)

%.o: %.c
	$(CC) -c $(CFLAGS) $<

tests: clock.exe timer.exe

clock.exe: testClock.o clock.o
	$(CC) $(CFLAGS) -o $@ $^

timer.exe: testTimer.o timer.o
	$(CC) $(CFLAGS) -o $@ $^

# The target below is used with the third-party main in alien.o
alien.exe: alienClock.o clock.o 
	$(CC) $(CFLAGS) -o $@ $^

memcheckClock.exe: clock.exe
	valgrind --leak-check=yes --track-origins=yes ./clock.exe

memcheckTimer.exe: timer.exe
	valgrind --leak-check=yes --track-origins=yes ./timer.exe

clean: 
	$(RM) $(OBJECTS) *.exe
