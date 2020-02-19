"""
Driver (main program) for symbolic calculator.
"""

from rpn_parse import parse, InputError
from lexer import LexicalError
import expr

help = """Type 'quit' to quit.
Assignment: 'var expression ='
Form expressions with +, -, *, /, ~ (negation)
Use a space between each element, e.g.,
for y_not gets z + 3:
  yes:  y_not z 3 + =
   no:  y_not z3+=
Identifiers can be any_valid_P7thon_identifier
"""


def main():
    """Evaluate expressions typed at the command line"""
    while True:
        try:
            inp = input("expression/'help'/'quit': ")
            if inp == "quit":
                break
            elif inp == "dump":
                expr.env.dump()
            elif inp in ["help", "?", "Help"]:
                print(help)
            else:
                exp = parse(inp)
                print("{} -> ".format(exp), end="")
                print(exp.eval())
        except InputError as e:
            print(e)
            print(help)
        except LexicalError as e:
            print(e)
            print(help)
        except NotImplementedError as e:
            print(e)


if __name__ == "__main__":
    main()
