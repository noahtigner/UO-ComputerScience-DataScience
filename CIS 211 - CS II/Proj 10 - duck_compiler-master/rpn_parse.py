"""
Postfix, a.k.a. Reverse Polish Notation (RPN) parser.
Based on calculator parser, but revised to read
from a file.

Author: Michal Young March 2018
"""
import typing
from typing import TextIO
import re
import expr
import syntax
from lexer import Token_Stream

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class InputError(Exception):
    """Raised when we can't parse the input"""
    pass


def parse(srcfile: TextIO ) -> expr.Expr:
    """Convert text in srcfile into an Expr object
    (also known as an Abstract Syntax Tree)
    """
    stack = [ ]
    stream = Token_Stream(srcfile)
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

        # Anything with two operands
        elif token.kind in [ syntax.SEQ, syntax.WHILE, syntax.BINOP ]:
            if len(stack) < 2:
                raise InputError("Insufficient operands for {}".format(token))
            op_class = token.clazz
            right = stack.pop()
            left = stack.pop()
            node = op_class(left, right)
            stack.append(node)

        elif token.kind in [ syntax.UNOP, syntax.PRINT ]:
            if len(stack) < 1:
                raise InputError("Insufficient operands for {}".format(token))
            left = stack.pop()
            op_class = token.clazz
            node = op_class(left)
            stack.append(node)

        elif token.kind in [syntax.CONST, syntax.IDENT]:
            leaf_class = token.clazz
            node = leaf_class(token.value)
            stack.append(node)
        else:
            print("Unrecognized token {}".format(token))
    if len(stack) > 1:
        raise InputError("Unbalanced expression (too many operands)")
    if len(stack) == 0:
        raise InputError("Empty expression")
    return stack[0]


    
