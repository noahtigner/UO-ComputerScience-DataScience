"""
Expressions.  An expression is a subtree, which may be
- a numeric value, like 5
- a named variable, like x
- a binary operator, like 'plus', with a left and right subtree

Special operations include:
    SEQ, written ';', which evaluates its left operand and then
    it's right operand  (i.e., it is how we build sequences of
    operations).
    WHILE, written in postfix order as  expr cond while

Based on the symbolic calculator
but I have removed the 'eval' method and
replaced it with 'generate' methods
to generate DM2018W code.

Expressions are evaluated in order.  Each Expr node has a 'gen'
method that returns a list of DM2018W source code lines.  A
'vars' method gathers the list of all variables that must be
declared.

Author: Noah Tigner
"""

# Our modules
from codegen_context import Context

# Python standard libraries
from typing import List
import numbers

import logging
logging.basicConfig
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Expr(object):
    """Abstract base class. Cannot be instantiated."""

    def gen(self, context: Context, target: str):
        """Code generation.  Walk the expression and build
        the instruction stream in the context object.  If a 
        target is given, it is the name of the register into 
        which the generated code should place a value. 
        """
        raise NotImplementedError(
            "No gen method has been defined for class {}".format(type(self)))

class Control(Expr):
    """Control flow nodes (while, if, ...).
    These have a predicate and one or more blocks of statements.
    We take zero as false, and any other value as true.
    """
    pass

class Seq(Control):
    """exp ; exp"""

    def __init__(self, left, right):
        """ exp ; exp """
        self.left = left
        self.right = right

    def __str__(self):
        return "({};\n{})".format(self.left, self.right)


    def gen(self, context: Context, target: str):
        """Just execute the statements in order.
        Discard the results, if any.
        """
        log.debug("Generating code for sequence")
        reg = context.alloc_reg()
        self.left.gen(context, target=reg)
        self.right.gen(context, target=reg)
        context.free_reg(reg)

class While(Control):
    """Classic while loop; in postfix we will write
    while cond do exp as exp cond while
    """

    def __init__(self, expr, cond):
        """While cond do expr"""
        self.cond = cond
        self.expr = expr

    def __str__(self):
        return "while {} do\n{}\nod".format(self.cond, self.expr)

    def gen(self, context: Context, target: str):
        """While loop is implemented by conditional jumps"""
        loop_head = context.new_label("loop")
        loop_exit = context.new_label("endloop")
        context.add_line("{}:  #While loop".format(loop_head))
        self.cond.gen(context, target)
        # Is it zero?
        context.add_line("  SUB  r0,{},r0 ".format(target))
        context.add_line("  JUMP/Z {}".format(loop_exit))
        self.expr.gen(context, target)
        context.add_line("  JUMP {}".format(loop_head))
        context.add_line("{}: ".format(loop_exit))

class Print(Expr):
    """Ducks gotta quack"""
    def __init__(self, left):
        self.left = left

    def __repr__(self):
        return "Print({})".format(repr(self.left))

    def __str__(self):
        return "Print({})".format(self.left)

    def gen(self, context:Context, target: str):
        log.debug("Generating code for Print")
        self.left.gen(context, target)
        context.add_line("   STORE {},r0,r0[1026] # Print".format(target))


class Assign(Expr):
    """x = Expr.  We treat an assignment as an expression
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

    def gen(self, context: Context, target: str):
        """Code generation for assignment: calculate into register,
        then store into memory
        """
        log.debug("Generating code for assignment")
        var_symbol = context.get_var_symbol(self.var.name)
        self.expr.gen(context, target)
        context.add_line("  STORE  {},{}".format(target,var_symbol))

class Var(Expr):
    """A variable has a name and may have a value in the environment."""

    def __init__(self, name):
        """Expression is reference to a variable named name"""
        assert isinstance(name, str)
        self.name = name

    def __repr__(self):
        return "Var('{}')".format(self.name)

    def __str__(self):
        return self.name

    def gen(self, context: Context, target: str):
        """Code generation for a variable reference. 
        Generates code to load the value of that variable 
        from memory.
        """
        log.debug("Generating code for variable reference")
        symbol = context.get_var_symbol(self.name)
        context.add_line("   LOAD {},{}".format(target,symbol))
        return

class Const(Expr):
    """An expression that is just a constant value, like 5"""

    def __init__(self, value):
        assert isinstance(value, numbers.Number)
        self.val = value

    def value(self):
        """The internal value"""
        return self.val

    def __repr__(self):
        return "Const({})".format(self.val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.val == other.val

    def gen(self, context: Context, target: str):
        """Code generation for a constant reference. 
        Generates code to load the value of that constant
        from memory.
        """
        log.debug("Generating code for reference to constant {}"
                      .format(self.val))
        symbol = context.get_const_symbol(self.val)
        context.add_line("   LOAD {},{}".format(target,symbol))
        return


class BinOp(Expr):
    """Abstract superclass for binary expressions like plus, minus"""

    def __init__(self, left, right):
        """A binary operation has a left and right sub-expression"""
        assert isinstance(left, Expr)
        assert isinstance(right, Expr)
        self.left = left
        self.right = right

    def __eq__(self, other):
        """Identical expression"""
        return isinstance(self, type(other)) \
            and self.left == other.left \
            and self.right == other.right

    def gen(self, context: Context, target: str):
        """Code generation for an addition.
        """
        log.debug("Generating code for addition")

        #   - Recursively generate code for the left operand,
        #     using the same target register.
        #   - Allocate a single register for the right operand
        #   - Recursively generate code for the right operand,
        #     using the newly allocated register
        #   - Get the operation code with the _opcode method
        #   - Generate the instruction from the opcode and the registers
        #   - Free the register allocated above

        self.left.gen(context, target)
        alloc = context.alloc_reg()
        self.right.gen(context, alloc)
        op = self._opcode()
        context.add_line("{} {},{},{}".format(op, target, target, alloc))
        context.free_reg(alloc)
        return

    def _opcode(self):
        """Each operation that inherits gen must provide the opcode
        to be used in the instruction. 
        """
        raise NotImplementedError("Class {} doesn't have _opcode mdethod"
                                     .format(type(self)))


class Plus(BinOp):
    """Represents the expression A + B"""

    def _apply(self, left, right):
        """Addition of two numeric values (Const nodes)"""
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() + right.value())

    def __repr__(self):
        return "Plus({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} + {})".format(self.left, self.right)

    def _opcode(self):
        return "PLUS"


class Minus(BinOp):
    """Represents the expression A - B"""

    def _apply(self, left, right):
        """Subtraction of two numeric values (Const nodes)"""
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() - right.value())

    def __repr__(self):
        return "Minus({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} - {})".format(self.left, self.right)

    def _opcode(self):
        return "MINUS"


class Times(BinOp):
    """Represents the expression A * B"""
    # __init__ is inherited from BinOp

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() * right.value())

    def __repr__(self):
        return "Times({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({} * {})".format(self.left, self.right)

    def _opcode(self):
        return "TIMES"


class Div(BinOp):
    """Exact division (not truncating) of two numeric values"""

    def _apply(self, left, right):
        assert isinstance(left, Const)
        assert isinstance(right, Const)
        return Const(left.value() / right.value())

    def __repr__(self):
        return "Div({},{})".format(repr(self.left), repr(self.right))

    def __str__(self):
        """Print fully parenthesized"""
        return "({}/{})".format(self.left, self.right)

    def _opcode(self):
        return "DIV"


class UnOp(Expr):
    """Abstract superclass for unary expressions like negation"""

    def __init__(self, left: Expr) -> Expr:
        """A unary operation has only a left  sub-expression"""
        assert isinstance(left, Expr)
        self.left = left


class Neg(UnOp):
    """Numeric negation"""

    def __repr__(self):
        return "Neg({})".format(repr(self.left))

    def __str__(self):
        """Print fully parenthesized"""
        return "~{}".format(self.left)

    def gen(self, context: Context, target: str):
        """Code generation for negation, implemented by 
        subtracting from zero. 
        """
        log.debug("Generating code for negation")
        self.left.gen(context, target)
        context.add_line("   SUB  {},r0,{}".format(target,target))
        return
    
