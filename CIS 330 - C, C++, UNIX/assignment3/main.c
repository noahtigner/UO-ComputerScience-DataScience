#include <stdio.h>
#include <stdlib.h>
#include "othello.h"

int main() {
	Board board;

	initBoard(&board);
	gameLoop(&board);

	return 0;
}
