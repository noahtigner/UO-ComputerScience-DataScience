"""
Postfix, a.k.a. Reverse Polish Notation (RPN) parser
for a symbolic calculator.  Produces
Expr objects.

Author: Noah Tigner
"""
import typing
import re
import expr
import syntax
import lexer
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class InputError(Exception):
    """Raised when we can't parse the input"""
    pass


def parse(s: str) -> expr.Expr:
    """Parse s, which should be a sequence of
    blank-separated tokens in RPN, into an Expr
    object.   Example: parse('3 4 * x +') =>
    Plus(Times(Const(3), Const(4)), Var('x'))
    """
    stack = []
    stream = lexer.Token_Stream(s)
    while stream.has_more():
        token = stream.take()
        if token.kind == syntax.ASSIGN:
            if len(stack) < 2:
                raise InputError("Insufficient operands for {}".format(token))
            right = stack.pop()
            left = stack.pop()
            op_class = token.clazz
            if not isinstance(left, expr.Var):
                raise InputError("First operand of assignment must be" +
                                 " a variable, not {}".format(left))
            node = op_class(left, right)
            stack.append(node)

        elif token.kind == syntax.BINOP:
            if len(stack) < 2:
                raise InputError("Insufficient operands for {}".format(token))

            right = stack.pop()
            left = stack.pop()
            op_class = token.clazz

            node = op_class(left, right)
            stack.append(node)




        elif token.kind == syntax.UNOP:
            if len(stack) < 1:
                raise InputError("Insufficient operands for {}"
                                 .format(token))
            left = stack.pop()
            op_class = token.clazz
            node = op_class(left)
            stack.append(node)
        elif token.kind in [syntax.CONST, syntax.IDENT]:
            leaf_class = token.clazz
            node = leaf_class(token.value)
            stack.append(node)
    if len(stack) > 1:
        raise InputError("Unbalanced expression (too many operands)")
    if len(stack) == 0:
        raise InputError("Empty expression")
    return stack[0]
