
#ifndef DATE_HPP_
#define DATE_HPP_

#include "cipher.hpp"

class DateCipher: public Cipher {
public:
        DateCipher(); //Constructor

        virtual std::string encrypt(std::string &text);
        virtual std::string decrypt(std::string &text);
	virtual void setDate(std::string strDate);

private:
	int date[6];
};

#endif /* DATE_HPP_ */
