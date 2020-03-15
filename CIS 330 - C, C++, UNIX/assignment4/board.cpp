#include <iostream>
#include "reversi.hpp"
using namespace std;


int Board::getSize(void) {
	//take input for board dimensions
	cout << "\nPlease enter the size of the board: ";
	
	int size = 0;

	cin >> size;
	
	//handle dimensions too small or large
	while(size < 3 || size > 25) {
		cout << "Error: incorrect board size.\nPlease enter the size of the board: ";		
		
		cin >> size;
	}
	return size;
}

void Board::initBoard(void) {
	size = getSize();
        blackCount = 2;
        whiteCount = 2;
	
	
	int row = size, col = size;
	int i, j;

	int size = size;

	//allocate memory
	char **gB = new char*[size];
	for(i = 0; i < size; i++) {
		gB[i] = new char[size];
	}

	//populate with '.'
	for(i = 0; i < size; i++) {
                for(j = 0; j < size; j++) {
                        gB[i][j] = '.';
                }		
	}
	//set up center of baord
	gB[row/2-1][row/2-1] = 'o';
	gB[row/2-1][row/2] = '*';
	gB[row/2][row/2-1] = '*';
	gB[row/2][row/2] = 'o';
	
	//set board's array to the one created above
	gameBoard = gB;
}

void Board::printBoard(void) {
	int i, j, row = size, col = size;

	//print score
	cout << "\nBlack (*): " << blackCount << "               White (o): " << whiteCount << endl; 


	//print x axis header
	cout << "  ";
	for(j = 0; j < 10 && j < row; j++) {
		cout << j << "   ";
	}
	cout << endl;
	for(i = 0; i < row; i++) {
		if(i < 10) {
			cout << i << " ";
		}
		else {
			cout << "  ";
		}
		//print board symbols
		for(j = 0; j < col; j++) {	
			cout << gameBoard[i][j] << "   ";
		}
		cout << endl;
	cout << endl;
	}
}

void Board::cleanBoard(void) {
	int i;
	//free memory
	for(i = 0; i < size; i++) {
		delete []gameBoard[i];
	}
	delete []gameBoard;
}
