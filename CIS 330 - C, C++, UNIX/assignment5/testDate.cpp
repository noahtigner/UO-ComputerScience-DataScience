#include <iostream>
#include <fstream>

#include "ioutils.hpp"
#include "cipher.hpp"
#include "date.hpp"

int main(int argc, const char *argv[]) {

        IOUtils io;
        io.openStream(argc,argv);
        std::string input, encrypted, decrypted;
        input = io.readFromStream();
        std::cout << "Original text:" << std::endl << input;

        DateCipher date;	//Create DateCipher object
	date.setDate("04/28/98");	//set dat's date w/ hard-coded string
        encrypted = date.encrypt(input);
        std::cout << "Encrypted text:" << std::endl << encrypted;

        decrypted = date.decrypt(encrypted);
        std::cout << "Decrypted text:" << std::endl << decrypted;

        if (decrypted == input) std::cout << "Decrypted text matches input!" << std::endl;
        else {
                std::cout << "Oops! Decrypted text doesn't match input!" << std::endl;
                return 1;   //indicates failure
        }

        return 0;
}
