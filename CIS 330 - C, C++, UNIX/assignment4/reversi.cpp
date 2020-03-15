#include <iostream>
#include "reversi.hpp"
using namespace std;

//Player vs. Player

void Board::gameLoop(void) {

	Player player1;
        player1.color = Black;
        player1.symbol = '*';

        Player player2;
        player2.color = White;
        player2.symbol = 'o';

	//Main Game Loop. Breaks when neither player can make a turn
	while(blackCount + whiteCount < 64) {
		if(blackCount + whiteCount < 64 && hasTurn(player1)) {
			turn(player1);
		}
		else {
			cout << "Player1 cannot make a move and skips a turn" << endl;

		}
		if(blackCount + whiteCount < 64 && hasTurn(player2)) {
                        turn(player2);
                }
		else {
                        cout << "Player2 cannot make a move and skips a turn" << endl;
                }
		if((64 - (blackCount+whiteCount) <= 1) 
				|| !hasTurn(player1) || !hasTurn(player2)) {
			cout << "No more moves can be made" << endl;
			break;
		}
	}
	gameOver();
}

void Board::turn(Player player) {
	printBoard();
	getMove(player);
}

bool Board::hasTurn(Player player) {
	//iterate through board, see if player has any vali flanking moves
	int i, j;

	for(i = 0; i < size; i++) {
		for(j = 0; j < size; j++) {
			if(gameBoard[i][j] == '.') {
				if(outflank(player, i, j, false)) {
					return true;
				}
			}
		}
	}
	return false;
}

void Board::getMove(Player player) {
	//take input
	char *in1 = new char[2];
       	char *in2 = new char[2];
	int *coordinates = new int[2];
	bool goodMove = false;

	//handle bad input
	while(!goodMove) {
		cout << "Enter the coordinates for your " << player.symbol << " (x y): ";

		
		cin >> in1;
		cin >> in2;
		
		coordinates[1] = (int)in1[0] - 48;
		coordinates[0] = (int)in2[0] - 48;

		if(legalMove(player, coordinates[0], coordinates[1])) {
			goodMove = true;
			outflank(player, coordinates[0], coordinates[1], true);
		}
		else {
			cout << "Try again. ";
		}
	}
}

bool Board::legalMove(Player player, int x, int y) {
	//checks if move is valid
	char opposite = opponent(player);

	if(gameBoard[x][y] != '.') {
		return false;
	}

	if(!onBoard(x, y)) {
		return false;
	}

	if(!outflank(player, x, y, false)) {
		return false;
	}
	return true;

}

bool Board::onBoard(int x, int y) {
	//checks if move is on the board
	return!(x < 0 || y < 0 || x > size-1 || x > size-1);
}

bool Board::outflank(Player player, int x, int y, bool flip) {
	//if !flip: checks for flanking moves
	//if flip:  makes the flanking move
	int i, j, k, l;

	if(flip) {
		place(player, x, y);
	}

	//case 1.1: flank below
	for(i = x+1; i < size; i++) {
		if(gameBoard[i][y] == opponent(player)) {
			j = i;
			while(gameBoard[i][y] == opponent(player) && i < size-1) {
				i++;
			}
			if(gameBoard[i][y] == player.symbol) {
				if(!flip) {
					return true;
				}
				//flip all opponent's discs between original spot and other spot
				for(k = j; k < i; k++) {
					place(player, k, y);
				}
			}
		}
	}
	//case 1.2: flank above
	for(i = x; i > 0; i--) {
		if(gameBoard[i][y] == opponent(player)) {
			j = i;
			while(gameBoard[i][y] == opponent(player) && i > 0) {
				i--;
			}
			if(gameBoard[i][y] == player.symbol) {
				if(!flip) {
					return true;
				}
				for(k = j; k > i; k--) {
					place(player, k, y);
				}
			}
		}
	}
	//case 2.1 flank right
	for(i = y+1; i < size; i++) {
		if(gameBoard[x][i] == opponent(player)) {
                        j = i;
                        while(gameBoard[x][i] == opponent(player) && i < size-1) {
                                i++;
                        }
                        if(gameBoard[x][i] == player.symbol) {
                                if(!flip) {
                                        return true;
                                }
                                for(k = j; k < i; k++) {
                                        place(player, x, k);
                                }
                        }
                }
	}
	//case 2.2: flank left
	for(i=y; i > 0; i--) {
		if(gameBoard[x][i] == opponent(player)) {
			j = i;
			while(gameBoard[x][i] == opponent(player) && i > 0) {
				i--;
			}
			if(gameBoard[x][i] == player.symbol) {
				if(!flip) {
					return true;
				}
				for(k = j; k > i; k--) {
				       place(player, x, k);
			      	}
		 	}
		}
        }
	//case 3.1: flank down,right
	for(i = x+1; i < size; i++) {
		for(j = y+1; j < size; j++){
			if(gameBoard[i][j] == opponent(player)) {
				k = i;
				l = j;
			
				while(gameBoard[i][j] == opponent(player) 
					&& i < size-1 && j < size-1) {
					i++;
					j++;
				}
				if(gameBoard[i][j] == player.symbol) {
					if(!flip) {
						return true;
					}
					while(k < i && l < j) {
						place(player, k, l);
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
                        if(gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(gameBoard[i][j] == opponent(player)
                                                && i > 0 && j > 0) {
                                        i--;
                                        j--;
                                }
                                if(gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
					while(k > i && l > j) {
                                                place(player, k, l);
                                                k--;
                                                l--;
                                        }
                                }
                        }
                }
        }
	//case 3.3: flank down, left
	for(i = x+1; i < size; i++) {
                for(j = y-1; j > 0; j--){
                        if(gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(gameBoard[i][j] == opponent(player)
                                                && i < size-1 && j > 0) {
                                        i++;
                                        j--;
                                }
                                if(gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
                                        while(k < i && l > j) {
                                                place(player, k, l);
                                                k++;
                                                l--;
                                        }
                                }
                        }
                }
        }
	//case 3.4: flank up, right
	for(i = x-1; i > 0; i--) {
                for(j = y+1; j < size; j++){
                        if(gameBoard[i][j] == opponent(player)) {
                                k = i;
                                l = j;

                                while(gameBoard[i][j] == opponent(player)
                                                && i > 0 && j < size) {
                                        i--;
                                        j++;
                                }
                                if(gameBoard[i][j] == player.symbol) {
                                        if(!flip) {
                                                return true;
                                        }
                                        while(k > i && l < j) {
                                                place(player, k, l);
                                                k--;
                                                l++;
                                        }
                                }
                        }
                }
     	}
	return false;
}

char Board::opponent(Player player) {
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

void Board::place(Player player, int x, int y) {
	//update score
	switch(player.symbol) {
		case 'o': 
			whiteCount++;
			if(gameBoard[x][y] != '.') {
			       	blackCount--;
			}
			break;
		case '*': 
			blackCount++;
			if(gameBoard[x][y] != '.') {
			       	whiteCount--;
			}
		      	break;
	}
	//place symbol on board
	gameBoard[x][y] = player.symbol;
}

void Board::gameOver() {
	printBoard();

	//print winner
	if(blackCount > whiteCount) {
		cout << "Game over... * wins!" << endl;
	}
	else {
		cout << "Game over... o wins!" << endl;
	}

	//free and exit
	cleanBoard();
	exit(0);
}

