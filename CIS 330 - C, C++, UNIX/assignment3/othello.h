#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#ifndef OTHELLO_H
#define OTHELLO_H_

//color type w/ options black or white
enum colors{Black, White};

//struct for board
typedef struct{
	int size, blackCount, whiteCount;
	char **gameBoard;
	

} Board;

//struct for player
typedef struct{
	enum colors color;
	char symbol;
} Player;

//function declarations

void initBoard(Board *board);

void printBoard(const Board *board);

void cleanBoard(Board *board);

void gameLoop(Board *board);

void turn(Board *board, Player player);

bool hasTurn(Board *board, Player player);

void getMove(Board *board, Player player);

bool legalMove(Board *board, Player player, int x, int y);

bool onBoard(Board *board, int x, int y);

bool outflank(Board *board, Player player, int x, int y, bool flip);

char opponent(Player player);

void place(Board *board, Player player, int x, int y);

void gameOver(Board *board);

#endif /* OTHELLO_H_ */
