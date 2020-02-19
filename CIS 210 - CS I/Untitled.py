import turtle


turtle = turtle.Turtle()
turtle.speed(100)

def fibbonacci(x):
    if x < 2:
        return x
    elif x < 100:
        turtle.forward(x * 5)
        turtle.right(90)
        print(x)
        return (fibbonacci(x + 2) + fibbonacci(x + 3))
    
    else:
        print(x)

print(fibbonacci(5))

