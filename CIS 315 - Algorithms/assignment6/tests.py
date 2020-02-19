import sys
from a6 import MCAL

def test1():
    f = open('inSample1.txt')
    N = int(f.readline())
    W = int(f.readline())
    v = []  # v[i] is i's cost
    c = []  # c[i] is i's calories
    s = []  # s[i] is i's name
    for i in range(N):
        # print(i)
        line = f.readline().split()
        v.append(int(line[0]))
        c.append(int(line[1]))
        s.append(line[2])

    assert MCAL(N, W, v, c) == 2400

if __name__ == "__main__": 
    
    test1()



