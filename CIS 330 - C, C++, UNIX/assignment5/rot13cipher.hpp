/*
 * simple.hpp
 *      Author: norris
 */

#ifndef ROT13CIPHER_HPP_
#define ROT13CIPHER_HPP_

#include "cipher.hpp"

class Rot13Cipher : public Cipher {
public:
    Rot13Cipher(); // constructor

	// Default destructor 
    
	virtual std::string encrypt( std::string &text );
	virtual std::string decrypt( std::string &text );
private:
	int rotation;
};

#endif /* ROT13CIPHER_HPP_ */
