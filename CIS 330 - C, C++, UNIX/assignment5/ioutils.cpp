/*
 * ioutils.cpp
 *      Author: norris
 */

#include "ioutils.hpp"

IOUtils::IOUtils() : isFile(false), inputStream(& std::cin) {
	// By default, read from standard input (cin)
}

IOUtils::~IOUtils() {
	this->closeStream();
}

void
IOUtils::openStream(int argc, const char *argv[]) {
	// If a file name is given read from file instead of standard input
	if( argc == 2 ) { //checks for an optional input file name
		inputStream = new std::ifstream( argv[1] );	// open the input file
		isFile = true;
	} else {
		std::cout << "Please type some text to encrypt." << std::endl <<
				"To finish, type CTRL-D on a new line (or CTRL-Z in Windows)." << std::endl;
		inputStream = & std::cin;
		isFile = false;
	}
}

void
IOUtils::closeStream() {
	if (isFile && inputStream != NULL) {
		std::ifstream *fstr = dynamic_cast<std::ifstream *>(inputStream);
		if (fstr != NULL) {
			if (fstr->is_open())
				fstr->close();
			delete fstr;
		}
	}
	inputStream = NULL;
	// if it's not a file (i.e., the stream is cin), don't close it
}

std::string
IOUtils::readFromStream() {
	std::string theInput;
	char ch;

	*(this->inputStream) >> std::noskipws;  // disable skipping of whitespace
	while ( ! this->inputStream->eof() ) {
		*(this->inputStream) >> ch;
	    theInput += ch;
	}

	return theInput;
}

