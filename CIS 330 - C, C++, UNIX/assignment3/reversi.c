#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "othello.h"

//Player vs. Player

void gameLoop(Board *board) {

	Player player1;
        player1.color = Black;
        player1.symbol = '*';

        Player player2;
        player2.color = White;
        player2.symbol = 'o';

	//Main Game Loop. Breaks when neither player can make a turn
	while(board->blackCount + board->whiteCount < 64) {
		if(board->blackCount + board->whiteCount < 64 && hasTurn(board, player1)) {
			turn(board, player1);
		}
		else {
			printf("Player1 cannot make a move and skips a turn\n");
		}
		if(board->blackCount + board->whiteCount < 64 && hasTurn(board, player2)) {
                        turn(board, player2);
                }
		else {
                        printf("Player2 cannot make a move and skips a turn\n");
                }
		if((64 - (board->blackCount+board->whiteCount) <= 1) 
				|| !hasTurn(board, player1) || !hasTurn(board, player2)) {
			printf("No more moves can be made\n");
			break;
		}
	}
	gameOver(board);
}

void turn(Board *board, Player player) {
	printBoard(board);
	getMove(board, player);
}

bool hasTurn(Board *board, Player player) {
	//iterate through board, see if player has any vali flanking moves
	int i, j;

	for(i = 0; i < board->size; i++) {
		for(j = 0; j < board->size; j++) {
			if(board->gameBoard[i][j] == '.') {
				if(outflank(board, player, i, j, false)) {
					return true;
				}
			}
		}
	}
	return false;
}

void getMove(Board *board, Player player) {
	//take input
	char in1[2], in2[2];
	int coordinates[2];
	bool goodMove = false;

	//handle bad input
	while(!goodMove) {
		printf("Enter the coordinates for your %c (x y): ", player.symbol);

		scanf("%s", in1);
		scanf("%s", in2);

		coordinates[1] = (int)in1[0] - 48;
		coordinates[0] = (int)in2[0] - 48;

		if(legalMove(board, player, coordinates[0], coordinates[1])) {
			goodMove = true;
			outflank(board, player, coordinates[0], coordinates[1], true);
		}
		else {
			printf("Try again. ");
		}
	}
}

bool legalMove(Board *board, Player player, int x, int y) {
	//checks if move is valid
	char opposite = opponent(player);

	if(board->gameBoard[x][y] != '.') {
		return false;
	}

	if(!onBoard(board, x, y)) {
		return false;
	}

	if(!outflank(board, player, x, y, false)) {
		return false;
	}
	return true;

}

bool onBoard(Board *board, int x, int y) {
	//checks if move is on the board
	return!(x < 0 || y < 0 || x > board->size-1 || x > board->size-1);
}

bool outflank(Board *board, Player player, int x, int y, bool flip) {
	//if !flip: checks for flanking moves
	//if flip:  makes the flanking move
	int i, j, k, l;

	if(flip) {
		place(board, player, x, y);
	}

	//case 1.1: flank below
	for(i = x+1; i < board->size; i++) {
		if(board->gameBoard[i][y] == opponent(player)) {
			j = i;
			while(board->gameBoard[i][y] == opponent(player) && i < board->size-1) {
				i++;
			}
			if(board->gameBoard[i][y] == player.symbol) {
				if(!flip) {
					return true;
				}
				//flip all opponent's discs between original spot and other spot
				for(k = j; k < i; k++) {
					place(board, player, k, y);
				}
			}
		}
	}
	//case 1.2: flank above
	for(i = x; i > 0; i--) {
		if(board->gameBoard[i][y] == opponent(player)) {
			j = i;
			while(board->gameBoard[i][y] == opponent(player) && i > 0) {
				i--;
			}
			if(board->gameBoard[i][y] == player.symbol) {
				if(!flip) {
					return true;
				}
				for(k = j; k > i; k--) {
					place(board, player, k, y);
				}
			}
		}
	}
	//case 2.1 flank right
	for(i = y+1; i < board->size; i++) {
		if(board->gameBoard[x][i] == opponent(player)) {
                        j = i;
                        while(board->gameBoard[x][i] == opponent(player) && i < board->size-1) {
                                i++;
                        }
                        if(board->gameBoard[x][i] == player.symbol) {
                                if(!flip) {
                                        return true;
                                }
                                for(k = j; k < i; k++) {
                                        place(board, player, x, k);
                                }
                        }
                }
	}
	//case 2.2: flank left
	for(i=y; i > 0; i--) {
		if(board->gameBoard[x][i] == opponent(player)) {
			j = i;
			while(board->gameBoard[x][i] == opponent(player) && i > 0) {
				i--;
			}
			if(board->gameBoard[x][i] == player.symbol) {
				if(!flip) {
					return true;
				}
				for(k = j; k > i; k--) {
				       place(board, player, x, k);
			      	}
		 	}
		}
        }
	//case 3.1: flank down,right
	for(i = x+1; i < board->size; i++) {
		for(j = y+1; j < board->size; j++){
			if(board->gameBoard[i][j] == opponent(player)) {
				k = i;
				l = j;
			
				while(board->gameBoard[i][j] == opponent(player) 
						&& i < board->size-1 && j < board->size-1) {
					i++;
					j++;
				}
				if(board->gameBoard[i][j] == player.symbol) {
					if(!flip) {
						return true;
					}
					while(k < i && l < j) {
						place(board, player, k, l);
						k++;
						l++;
					}
				}
			}
		}
	}
	//case 3.2: flank up, left
	for(i = x-1; i > 0; i--) {
                for(j = y-1; j > 0; j--){
                        if(board->gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(board->gameBoard[i][j] == opponent(player)
                                                && i > 0 && j > 0) {
                                        i--;
                                        j--;
                                }
                                if(board->gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
					while(k > i && l > j) {
                                                place(board, player, k, l);
                                                k--;
                                                l--;
                                        }
                                }
                        }
                }
        }
	//case 3.3: flank down, left
	for(i = x+1; i < board->size; i++) {
                for(j = y-1; j > 0; j--){
                        if(board->gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(board->gameBoard[i][j] == opponent(player)
                                                && i < board->size-1 && j > 0) {
                                        i++;
                                        j--;
                                }
                                if(board->gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
                                        while(k < i && l > j) {
                                                place(board, player, k, l);
                                                k++;
                                                l--;
                                        }
                                }
                        }
                }
        }
	//case 3.4: flank up, right
	for(i = x-1; i > 0; i--) {
                for(j = y+1; j < board->size; j++){
                        if(board->gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(board->gameBoard[i][j] == opponent(player)
                                                && i > 0 && j < board->size) {
                                        i--;
                                        j++;
                                }
                                if(board->gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
                                        while(k > i && l < j) {
                                                place(board, player, k, l);
                                                k--;
                                                l++;
                                        }
                                }
                        }
                }
     	}
	return false;
}

char opponent(Player player) {
	//return symbol of opponent
	char opposite;
	switch(player.color) {
		case 0: opposite = 'o';	//Black
			    break;
			
		case 1: opposite = '*';	//White
			    break;
	}
	return opposite;
}

void place(Board *board, Player player, int x, int y) {
	//update score
	switch(player.symbol) {
		case 'o': 
			board->whiteCount++;
			if(board->gameBoard[x][y] != '.') {
			       	board->blackCount--;
			}
			break;
		case '*': 
			board->blackCount++;
			if(board->gameBoard[x][y] != '.') {
			       	board->whiteCount--;
			}
		      	break;
	}
	//place symbol on board
	board->gameBoard[x][y] = player.symbol;
}

void gameOver(Board *board) {
	printBoard(board);

	//print winner
	if(board->blackCount > board->whiteCount) {
		printf("Game over... %c wins!\n", '*');
	}
	else {
		printf("Game over... %c wins!\n", 'o');
	}

	//free and exit
	cleanBoard(board);
	exit(0);
}
