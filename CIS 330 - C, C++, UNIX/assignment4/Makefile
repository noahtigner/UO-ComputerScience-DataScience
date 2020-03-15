CXX=g++
CXXFLAGS=-g -std=c++14

all: reversi.exe

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

reversi.exe: reversi.o board.o main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	$(RM) -r *.o *.exe*
