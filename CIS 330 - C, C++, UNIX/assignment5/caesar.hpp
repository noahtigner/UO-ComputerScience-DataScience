
#ifndef CAESAR_HPP_
#define CAESAR_HPP_

#include "cipher.hpp"

class CaesarCipher: public Cipher {
public:
	CaesarCipher();	//Constructor

	virtual std::string encrypt(std::string &text);
        virtual std::string decrypt(std::string &text);
	virtual void setRotation(int rotation);

private:
	int rotation;
};

#endif /* CAESAR_HPP_ */
