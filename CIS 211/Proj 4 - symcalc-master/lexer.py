"""
Lexical analysis to convert input strings into
streams of tokens.  Input string must delimit tokens
by spaces.  See end of this file for notes on why that is,
and alternatives for future development.

Author: Michal Young (michal@cs.uoregon.edu), January 2018
"""
import typing
from typing import Sequence, Type
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

    def __init__(self, s: str):
        self.tokens = lex(s)
        log.debug("Tokens: {}".format(self.tokens))

    def __str__(self) -> str:
        return "[{}]".format("|".join(self.tokens))

    def has_more(self) -> bool:
        """True if there are more tokens in the stream"""
        return len(self.tokens) > 0

    def peek(self) -> Token:
        """Examine next token without consuming it. """
        if len(self.tokens) > 0:
            token = self.tokens[0]
        else:
            token = END
        return token

    def take(self) -> Token:
        """Consume next token"""
        if len(self.tokens) > 0:
            token = self.tokens.pop(0)
        else:
            token = END
        return token


def lex(s: str) -> Sequence[Token]:
    """Break string into a list of Token objects"""
    words = s.split()
    tokens = []
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


"""
Developer notes:
Currently this module requires strings in which the tokens are
seprated by spaces.  That is unfortunate, but the alternatives in
Python are all rather unweildy.

Alternative 1:  Use the built in Python tokenizer, tokenizer.tokenizer.
Issues:  tokenizer.tokenizer is really designed to read from a file. You
can wrap a StringIO object around a string, but StringIO.readline returns
a string, and tokenizer.tokenizer expects a bytes object. Thus it takes a
lot of scaffolding.  Also, it creates a dependency on Python syntax (we
would not be able to define any operations that Python doesn't have or doesn't
represent in the same way).

Alternative 2: Regular expression hell (one big regex).  A reasonable
choice if I were writing the regular expression for tokenizing a fixed
language, but too involved if I want to allow extensible syntax.

Alternative 3: Regular expression per token.  Slow, stupid, and it would
require trying them in order from longest to shortest, but that might be
acceptable.

Alternative 4: Write the deterministic finite-state acceptor directly, with
a little parameterization for adding new operators.  Also slow, but probably
acceptable for a language this small.

A combination of 3 and/or 4 is probably the right approach, but that
will have to wait at least until Spring 2018.
"""
