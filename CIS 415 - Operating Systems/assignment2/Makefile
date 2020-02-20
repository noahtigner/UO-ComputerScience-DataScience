SOURCES = part1.c part2.c part3.c part4.c
HEADERS = header.h
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS =  -std=c11 -g -fPIC

%.o: %.c
	$(CC) -c $(CFLAGS) $<

part1.exe: part1.o 
	$(CC) $(CFLAGS) -o $@ $^

part2.exe: part2.o 
	$(CC) $(CFLAGS) -o $@ $^

part3.exe: part3.o 
	$(CC) $(CFLAGS) -o $@ $^

part4.exe: part4.o 
	$(CC) $(CFLAGS) -o $@ $^



clean:
	$(RM) $(OBJECTS) *.exe