CXX = g++
CXXFLAGS = -g -std=c++14

%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $<

all: testRot13cipher.exe testCaesar.exe testDate.exe

testRot13cipher.exe: testRot13cipher.o rot13cipher.o ioutils.o
	$(CXX) -o $@ $^

testCaesar.exe: testCaesar.o caesar.o ioutils.o
	$(CXX) -o $@ $^

testDate.exe: testDate.o date.o ioutils.o
	$(CXX) -o $@ $^

clean: 
	$(RM) *.o *.exe
