/*
 * simple.cpp
 *      Author: norris
 */

#include "cipher.hpp"
#include "rot13cipher.hpp"

// Single-argument constructor
Rot13Cipher::Rot13Cipher() : Cipher(), rotation(13) {
	// Nothing else to do in the constructor
}


// Overloaded encrypt method
std::string
Rot13Cipher::encrypt( std::string &inputText ) {
	std::string text = inputText;
	std::string::size_type len = text.length();
	for (int i = 0; i != len; ++i) {
        if (text[i] >= 'a' && text[i] <= 'm') {
            text[i] = text[i] + 13;
        } else if (text[i] >= 'n' && text[i] <= 'z') {
            text[i] = text[i] - 13;
        } else if(text[i] >= 'A' && text[i] <= 'M') {
            text[i] = text[i] + 13;
        } else if(text[i] >= 'N' && text[i] <= 'Z') {
            text[i] = text[i] - 13;
        }
	}
	return text;
}

std::string
Rot13Cipher::decrypt( std::string &text ) {
	// A Rot13 encryption is also a decryption (26 letters in the English alphabet)
	return this->encrypt(text);
}


