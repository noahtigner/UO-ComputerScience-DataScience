SOURCES = reversi.c othello.c main.c board.c   
HEADERS = othello.h
OBJECTS = $(SOURCES:.c=.o)
LIBS = -lm

CC = gcc
CFLAGS = -std=c11 -g -fPIC

%.o: %.c
	$(CC) -c $(CFLAGS) $<

tests: reversi.exe othello.exe

reversi.exe: main.o reversi.o board.o
	$(CC) $(CFLAGS) -o $@ $^

othello.exe: main.o othello.o board.o
	$(CC) $(CFLAGS) -o $@ $^


memcheckReversi.exe: reversi.exe
	valgrind --leak-check=yes --track-origins=yes ./reversi.exe

memcheckOthello.exe: othello.exe
	valgrind --leak-check=yes --track-origins=yes ./othello.exe

clean: 
	$(RM) $(OBJECTS) *.exe
