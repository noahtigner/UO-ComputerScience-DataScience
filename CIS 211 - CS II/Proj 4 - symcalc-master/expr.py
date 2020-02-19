"""
Expressions.  An expression is a subtree, which may be
- a numeric value, like 5
- a named variable, like x
- a binary operator, like 'plus', with a left and right subtree operands
- a unary operator, like 'neg', with just one operand

Expressions are interpreted in an environment, which is a
mapping from variable names to values. A variable may evaluate
to its value if its name is mapped to its value in the environment.
If its name is not mapped, a variable evaluates to itself (which
is what we mean calling this a "symbolic" calculator.)
"""
import numbers
import logging
logging.basicConfig
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Env(object):
    """An environment maps from variable names to values.
    Values are expressions, and are evaluated, so for example
    if we bound x to y + 7 and then bound y to 3, we would
    eval(Var("x")) would be 10.

    This evaluation strategy raises the risk of infinite
    recursion, e.g., in case x is bound to y + 3 and y is bound
    to x + 3.  We guard against that by keeping track of the
    variables currently being evaluated.
    """

    def __init__(self):
        self.map = {}
        self.currently_evaluating = []

    def eval(self, var):
        log.debug("Evaluating {} in Env".format(var))
        if var in self.currently_evaluating:
            log.warn("Cyclic reference to {}?  Bailing.".format(var))
            return var
        self.currently_evaluating.append(var)
        if var.name in self.map:
            val = self.map[var.name].eval()
        else:
            val = None
        self.currently_evaluating.pop()
        log.debug("Env returning {}".format(val))
        return val

    def assign(self, var, value):
        assert isinstance(var, Var)
        assert isinstance(value, Expr)
        self.map[var.name] = value

    def dump(self):
        """Command to see what is in the environment"""
        for name in self.map:
            print("{} -> {}".format(name, self.map[name]))


# One global environment, for now.
env = Env()


class Expr(object):
    """Abstract base class. Cannot be instantiated."""

    def eval(self):
        """Each concrete subclass of Expr must define this method"""
        raise NotImplementedError(
            "No eval method has been defined for class {}".format(type(self)))


class Assign(Expr):
    """let x = Expr.  We treat an assignment as an expression
    that returns the value of the right-hand side, but usually
    assignments are evaluated for side effect on the
    environment.
    """

    def __init__(self, var, expr):
        """Representation of 'let var = expr'"""
        assert isinstance(var, Var)
        assert isinstance(expr, Expr)
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "Assign({},{})".format(self.var, self.expr)

    def __str__(self):
        return "let {} = {}".format(self.var, self.expr)

    def eval(self):
        """Stores value of expr (evaluated) in environment"""
        log.debug("Evaluating {} in Assign".format(self))
        val = self.expr.eval()
        env.assign(self.var, val)
        return val


class Var(Expr):
    """A variable has a name and may have a value in the environment."""

    def __init__(self, name):
        """Expression is reference to a variable named name"""
        assert isinstance(name, str)
        self.name = name

    def eval(self):
        """Fetches value from environment."""
        log.debug("Evaluating {} in Var".format(self))
        val = env.eval(self)
        if val is None:
            log.debug("Unbound, returning {}".format(self))
            return self
        else:
            log.debug("Bound, returning {}".format(val))
            return val

    def __repr__(self):
        return "Var('{}')".format(self.name)

    def __str__(self):
        return self.name


class Const(Expr):
    """An expression that is just a constant value, like 5"""

    def __init__(self, value):
        assert isinstance(value, numbers.Number)
        self.val = value

    def eval(self):
        """This is about as evaluated as it can get"""
        log.debug("Evaluating {} in Const".format(self))
        return self

    def value(self):
        """The internal value"""
        return self.val

    def __repr__(self):
        return "Const({})".format(self.val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.val == other.val

#FIXME: You need an abstract base class BinOp.  It should provide
# an eval(self) method that calls self._apply(lval,rval). Each
# concrete subclass should provide its own _apply method.
# The abstract base class BinOp also provides the constructor
# and the __eq__ magic method.  Look at UnOp and at Assign for
# hints on what is needed.
# You also need concrete classes Plus, Minus, Times, Div that
# inherit the constructor (__init__), equality check (__eq__), and
# eval methods from BinOp.  Write appropriate _apply, __str__, and
# __repr__ methods for each concrete subclass of BinOp.

class BinOP(Expr):

    def __init__(self, left: Expr, right: Expr):
        assert isinstance(left, Expr)
        assert isinstance(right, Expr)
        self.left = left
        self.right = right

    def _apply(self, left, right):
        pass

    def eval(self):
        lval = self.left.eval()
        rval = self.right.eval()
        if isinstance(lval, Const) and isinstance(rval, Const):

            log.debug("Apply op to {} and {}".format(lval, rval))
            return self._apply(lval, rval)

        elif lval is self.left and rval is self.right:
            log.debug("No change, returning {}".format(self))
            return self
        else:
            log.debug("Constructing new {}({}, {}".format(type(self), lval, rval))
            return type(self)(lval, rval)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.left == other.left and self.right == other.right

class Plus(BinOP):

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() + right.value())

    def __repr__(self):
        return "Plus({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} + {})".format(self.left, self.right)


class Minus(BinOP):

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() - right.value())

    def __repr__(self):
        return "Minus({},{})".format(repr(self.left), repr(self.right))
    def __str__(self):
        """Print fully parenthesized"""
        return "({} - {})".format(self.left, self.right)


class Times(BinOP):

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() * right.value())

    def __repr__(self):
        return "Times({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} * {})".format(self.left, self.right)


class Div(BinOP):

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() / right.value())

    def __repr__(self):
        return "Divide({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} / {})".format(self.left, self.right)


class UnOp(Expr):
    """Abstract superclass for unary expressions like negation"""

    def __init__(self, left: Expr) -> Expr:
        """A unary operation has only a left  sub-expression"""
        assert isinstance(left, Expr)
        self.left = left

    def eval(self):
        """Evaluation strategy for unary expressions"""
        log.debug("Evaluating {} in UnOp".format(self))
        lval = self.left.eval()
        if isinstance(lval, Const):
            log.debug("Apply op to {}".format(lval, lval))
            return self._apply(lval)
        elif lval is self.left:
            log.debug("No change, returning {}".format(self))
            return self
        else:
            log.debug("Constructing new {}({})"
                      .format(type(self), lval))
            return type(self)(lval)


class Neg(UnOp):
    """Numeric negation"""

    def _apply(self, left):
        """Negation of a numeric value (Const node)"""
        assert isinstance(left, Const)
        return Const(0 - left.value())

    def __repr__(self):
        return "Neg({})".format(repr(self.left))

    def __str__(self):
        """Print fully parenthesized"""
        return "~{}".format(self.left)

