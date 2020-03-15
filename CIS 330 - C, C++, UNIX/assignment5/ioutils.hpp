/*
 * ioutils.hpp
 *      Author: norris
 *
 *  Input/Output utility functions for reading input from files or standard input.
 */

#ifndef IOUTILS_HPP_
#define IOUTILS_HPP_

#include <fstream>
#include <iostream>
#include <string>

class IOUtils {
public:
	IOUtils();
	virtual ~IOUtils();

	// If no argument given, open standard in
	void openStream(int argc, const char *argv[]);

	// Close the input stream
	void closeStream();

	// Read from the open input stream and return the contents as a string
	std::string readFromStream();

	// Get the currently open input stream
	std::istream getStream();
private:
	bool isFile;
	std::istream *inputStream;
};

#endif /* IOUTILS_HPP_ */
