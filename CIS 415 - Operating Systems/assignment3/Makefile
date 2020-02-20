SOURCES = part1.c part2.c part3.c part4.c part5.c
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS =  -pthread -std=c11 -g -fPIC

%.o: %.c
	$(CC) -c $(CFLAGS) $<

part1: part1.o 
	$(CC) $(CFLAGS) -o $@ $^

part2: part2.o 
	$(CC) $(CFLAGS) -o $@ $^

part3: part3.o 
	$(CC) $(CFLAGS) -o $@ $^

part4: part4.o 
	$(CC) $(CFLAGS) -o $@ $^

part5: part5.o 
	$(CC) $(CFLAGS) -o $@ $^

server: part5.o 
	$(CC) $(CFLAGS) -o $@ $^

clean:
	$(RM) $(OBJECTS) *.exe