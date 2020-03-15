#include <iostream>
#include "reversi.hpp"

int main() {
	Board board;

	board.initBoard();
	board.gameLoop();

	return 0;
}
