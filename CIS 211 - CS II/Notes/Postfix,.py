
""" In class: Postfix, S-expressions"""

ops = {"+": lambda x, y: x + y, # lambda is a compact way of defining a function
       "*": lambda x, y: x * y,
       "-": lambda x, y: x - y,
       "/": lambda x, y: x // y}

def eval_postfix(s: str) -> int:
    """
    if "5 3 + 4 *": eval_postfix("5 3 + 4 *") -> 32

    if eval_postfix("5 3 + 4 - 12 *") -> 48
    """

    stack = []
    tokens = s.split()

    for i in tokens:
        if i.isnumeric(): # if its a number
            stack.append(int(i)) # adds numbers to the stack
        elif i in ops: # or if its in the operator dict
            right = stack.pop()
            left = stack.pop()
            result = ops[i](left, right) # call the correct function in ops, pass it the top 2 of the stack
            stack.append(result) # push the new sum/product/difference/quotient to the stack

    return(stack[0])

    """
        elif i == "+":
            left = stack.pop() # pops the last item off the stack
            right = stack.pop()
            x = right + left
            stack.append(x) # add the sum back to the stack
            
        elif i == "-":
            left = stack.pop()
            right = stack.pop()
            x = right - left
            stack.append(x)
    """


print(eval_postfix("5 3 + 4 - 12 *"))

# 5 is an s-expression
# ["+" 5 4] is an s-expression
# ["+" ["-" 5 4] ["+" 3 7]]

def parse_postfix(s: str) -> list:
    """
    parses the input and builds the s-expression (a tree)
    """

    stack = []
    tokens = s.split()

    for i in tokens:
        if i.isnumeric(): # if its a number
            stack.append(int(i)) # adds numbers to the stack
        elif i in ops: # or if its in the operator dict
            right = stack.pop()
            left = stack.pop()
            result = [i, left, right]
            stack.append(result) # push the new sum/product/difference/quotient to the stack

    return(stack[0])



def eval_sexp(sexp: list) -> int:
    if isinstance(sexp, int):
        return sexp
    else:
        right = eval_sexp(sexp.pop())
        left = eval_sexp(sexp.pop())
        op = sexp.pop()
        return ops[op](left, right)




print(parse_postfix("5 3 - 4 *"))
print(eval_sexp(parse_postfix("5 3 - 4 *")))