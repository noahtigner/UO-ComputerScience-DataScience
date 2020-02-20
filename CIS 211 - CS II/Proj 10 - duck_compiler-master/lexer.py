"""
Lexical analysis to convert input file into
streams of tokens.  Input string must delimit tokens
by spaces.  

Based on lexer.py from symbolic calculator project, 
but modified to read from a file. 

Author: Michal Young (michal@cs.uoregon.edu), March 2018
"""
import typing
from typing import Sequence, Type, TextIO
import re
import syntax
import expr

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# The operation symbols we recognize here are
# based on file syntax.py
OPSYMS = syntax.OPS.keys()

class LexicalError(Exception):
    """Raised when we can't extract tokens from the input"""
    pass

class Token(object):
    """One token from the input stream"""

    def __init__(self, value: any, kind: str, clazz: Type(expr.Expr)):
        self.value = value
        self.kind = kind
        self.clazz = clazz

    def __repr__(self) -> str:
        return "Token({}, {}, {})".format(repr(self.value), self.kind,
                                                self.clazz.__name__)
    def __str__(self) -> str:
        return repr(self)

    
class Token_Stream(object):
    """
    Provides the tokens within a string one-by-one.
    """

    def __init__(self, f: TextIO):
        self.file = f
        self.tokens = [ ]
        self._check_fill()
        log.debug("Tokens: {}".format(self.tokens))

    def __str__(self) -> str: 
        return "[{}]".format("|".join(self.tokens))

    def _check_fill(self):
        if len(self.tokens) == 0:
            line = self.file.readline()
            while line == "\n":
                # Skip blank lines
                line = self.file.readline()
            if len(line) > 0:
                # Zero-length line means EOF
                self.tokens = lex(line.strip())
                log.debug("Refilled, tokens: {}".format(self.tokens))


    def has_more(self) -> bool:
        """True if there are more tokens in the stream"""
        self._check_fill()
        return len(self.tokens) > 0

    def peek(self) -> Token:
        """Examine next token without consuming it. """
        self._check_fill()
        if len(self.tokens) > 0:
            token = self.tokens[0]
        else:
            token = END
        return token

    def take(self) -> Token:
        """Consume next token"""
        self._check_fill()
        if len(self.tokens) > 0:
            token = self.tokens.pop(0)
        else:
            token = END
        return token


def lex(s: str) -> Sequence[Token]:
    """Break string into a list of Token objects"""
    words = s.split()
    tokens = [ ]
    for word in words:
        tokens.append(classify(word))
    return tokens

def classify(word: str) -> Token:
    """Convert a textual token into a Token object
    with a value and category.
    """
    if word in OPSYMS:
        category, clazz = syntax.OPS[word]
        return Token(word, category, clazz)
    elif word.isidentifier():
        return Token(word, syntax.IDENT, expr.Var)
    elif word.isdigit():
        return Token(int(word), syntax.CONST, expr.Const)
    elif re.match("[0-9]*.[0-9]+", word):
        return Token(float(word), syntax.CONST, expr.Const)
    else:
        raise LexicalError("Unrecognized token '{}'".format(word))

