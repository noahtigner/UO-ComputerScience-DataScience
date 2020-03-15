#include <iostream>
#ifndef REVERSI_HPP
#define REVERSI_HPP_

//color type w/ options black or white
enum colors{Black, White};

class Player {
        public:
                enum colors color;
                char symbol;
};

class Board { 
	public:
	
		int size, blackCount, whiteCount;
		char **gameBoard;

		int getSize(void);

		void initBoard(void);

		void printBoard(void);

		void cleanBoard(void);

		void gameLoop(void);

		void turn(Player player);

		bool hasTurn(Player player);

		void getMove(Player player);

		bool legalMove(Player player, int x, int y);

		bool onBoard(int x, int y);

		bool outflank(Player player, int x, int y, bool flip);

		char opponent(Player player);

		void place(Player player, int x, int y);

		void gameOver(void);
};

#endif /* REVERSI_HPP_ */
