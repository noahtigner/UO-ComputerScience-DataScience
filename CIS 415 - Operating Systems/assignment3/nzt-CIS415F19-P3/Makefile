all: part1 part2 part3 part4 server
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS =  -pthread -std=c11 -g

part1: part1.c
	$(CC) $(CFLAGS) part1.c -o part1

part2: part2.c 
	$(CC) $(CFLAGS) part2.c -o part2

part3: part3.c 
	$(CC) $(CFLAGS) part3.c -o part3

part4: part4.c 
	$(CC) $(CFLAGS) part4.c -o part4

server: quacker.c 
	$(CC) $(CFLAGS) quacker.c -o server

clean:
	$(RM) $(OBJECTS) *.exe