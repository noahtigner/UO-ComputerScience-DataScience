SOURCES = main.c command.c
HEADERS = command.h
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS = -g -fPIC

%.o: %.c
	$(CC) -c $(CFLAGS) $<

pseudo-shell: main.o command.o
	$(CC) $(CFLAGS) -o $@ $^

clean:
	$(RM) $(OBJECTS) *.exe
