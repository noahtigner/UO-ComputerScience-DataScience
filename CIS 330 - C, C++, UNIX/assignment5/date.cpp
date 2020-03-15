#include "cipher.hpp"
#include "date.hpp"
#include <iostream>

DateCipher::DateCipher(): Cipher() {}	//Constructor

std::string DateCipher::encrypt(std::string &inputText) {
        std::string text = inputText;
        std::string::size_type len = text.length();
	int i;

	//Doesn't account for special characters

	for(i = 0; i < len; i++) {
		//Shifts char by date number, wraps date around
		text[i] = inputText[i] + this->date[i%6];
	}

	return text;
}

std::string DateCipher::decrypt(std::string &inputText) {
        std::string text = inputText;
        std::string::size_type len = text.length();
	int i;

	//Doesn't account for special characters

        for(i = 0; i < len; i++) {
		//Shifts char by date number, wraps date around
                text[i] = inputText[i] - this->date[i%6];
        }
	return text;
}

void DateCipher::setDate(std::string strDate) {
        int i;

	//Converts hard-coded date into int array
        for(i = 0; i < 6; i++) {
                this->date[i] = (int) strDate[i] - 48;
        }
}
