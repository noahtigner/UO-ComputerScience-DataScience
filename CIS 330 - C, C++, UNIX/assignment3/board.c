#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "othello.h"

int getSize() {
	//take input for board dimensions
	printf("\nPlease enter the size of the board: ");
	int size = 0;

	scanf("%i", &size);
	//handle dimensions too small or large
	while(size < 3 || size > 25) {
		printf("Error: incorrect board size.\nPlease enter the size of the board: ");
		scanf("%i", &size);
	}
	return size;
}

void initBoard(Board *board) {
	char **gB;
	board->size = getSize();
	int row = board->size, col = board->size;
	size_t i, j;
	board->blackCount = 2; 
	board->whiteCount = 2;

	//allocate array
	gB = (char **) malloc(board->size * sizeof(char *));
	for(i = 0; i < row; i++) {
		gB[i] = (char *) malloc(board->size * sizeof(char));
	}
	//populate with '.'
	for(i = 0; i < row; i++) {
                for(j = 0; j < col; j++) {
                        gB[i][j] = '.';
                }		
	}
	//set up center of baord
	gB[row/2-1][row/2-1] = 'o';
	gB[row/2-1][row/2] = '*';
	gB[row/2][row/2-1] = '*';
	gB[row/2][row/2] = 'o';
	
	//set board's array to the one created above
	board->gameBoard = gB;
}

void printBoard(const Board *board) {
	int i, j, row = board->size, col = board->size;

	//print score
	printf("\nBlack (*): %i		White (o): %i\n", board->blackCount, board->whiteCount);
	
	//print x axis header
	printf("  ");
	for(j = 0; j < 10 && j < row; j++) {
        	printf("%i   ", j);
		
	}
	printf("\n");
	for(i = 0; i < row; i++) {
		//print y axis header
		if(i < 10) {
			printf("%i ", i);
		}
		else {
			printf("  ");
		}
		//print board symbols
		for(j = 0; j < col; j++) {	
			printf("%c   ", board->gameBoard[i][j]);

		}
		printf("\n");
	printf("\n");
	}
}

void cleanBoard(Board *board) {
	int i;
	//free memory
	for(i = 0; i < board->size; i++) {
		free(board->gameBoard[i]);
	}
	free(board->gameBoard);
}
