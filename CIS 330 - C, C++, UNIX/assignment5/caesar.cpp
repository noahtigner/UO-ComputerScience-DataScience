
#include "cipher.hpp"
#include "caesar.hpp"

CaesarCipher::CaesarCipher(): Cipher() {}

std::string CaesarCipher::encrypt(std::string &inputText) {
	std::string text = inputText;
        std::string::size_type len = text.length();
	int i;
	int shift = this->rotation;


	for(i = 0; i < len; i++) {
		if(inputText[i] == 32) {	//if space, shift past
			text[i] = shift + 96;
		}		
		
		else if(inputText[i] >= 'a' && inputText[i]  <= 'z') {
			if(inputText[i] + shift == '{') {
				text[i] = ' ';	//make z+1 whitespace
			}
		
			else if(inputText[i] + shift > '{') {
				//shift up but keep alphabetic
				text[i] = inputText[i] + shift - 27;
			}
			else {
				//shift up
				text[i] = inputText[i] + shift;
			}
		}	
		else if(inputText[i] >= 'A' && inputText[i]  <= 'Z') {
                        if(inputText[i] + shift == '[') {
                                text[i] = ' ';	//make Z+1 whitespace
                        }
                
                        else if(inputText[i] + shift > '[') {
                        	//shift up but keep alphabetic
				text[i] = inputText[i] + shift - 27;
			}
                        else {
				//shift up
                                text[i] = inputText[i] + shift;
			}
                }
	}
	return text;
}

std::string CaesarCipher::decrypt(std::string &inputText) {
        std::string text = inputText;
        std::string::size_type len = text.length();
        int i;
        int shift = this->rotation;

	//Mirror opposite of encrypt
	//Works for everything except spaces
        for(i = 0; i < len; i++) { 
		
                if(inputText[i] - shift == 64 || inputText[i] - shift == 96) {
			//if @ or ', make whitespace	
                        text[i] = ' ';
                }

                if(inputText[i] >= 97 && inputText[i]  <= 122) {
			//lower case
                        if(inputText[i] - shift < 96) {
                                text[i] = inputText[i] - shift + 27;
                        }
                        else {  
                                text[i] = inputText[i] - shift;
                        }
                }       
		else if(inputText[i] >= 64 && inputText[i]  <= 90) {
			//upper case
			if(inputText[i] - shift < 64) {
                       	        text[i] = inputText[i] - shift + 27;
                       	}
               		else {
                               	text[i] = inputText[i] - shift;
                       	}
               	}
       	}
        return text;
} 

void CaesarCipher::setRotation(int rotation) {
	//set cipher's shift amount
	this->rotation = rotation;
}
