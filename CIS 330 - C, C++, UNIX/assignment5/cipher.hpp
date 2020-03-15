/*
 * An abstract class defining the encryption and decryption
 * interface that is implemented by different concrete
 * encryption strategies.
 */

#ifndef CIPHER_HPP_
#define CIPHER_HPP_

#include <string>

class Cipher {
public:

	// Default constructor and destructor

	// Encrypt the text argument and return the encrypted text
	virtual std::string encrypt( std::string &text ) = 0;

	// Decrypt the text argument and return the decrypted text
	virtual std::string decrypt( std::string &text ) = 0;
};


#endif
