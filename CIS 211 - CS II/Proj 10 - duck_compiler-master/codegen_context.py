"""
A container for the context information kept 
for assembly code generation while walking 
an abstract syntax tree. 

The context object is passed around from node to 
node during code generation. Having a context 
object, rather than a set of different pieces
of information passed around, isolates in one 
place several small design decisions:  How 
registers are allocated, how constants and variables
are declared, when and how the code is actually
emitted to the output file. 
"""

from typing import List

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Context(object):
    """The state of code generation"""

    def __init__(self):

        # The range of registers available for code generation;
        # excludes r0 and r15
        self.min_reg = 1
        self.max_reg = 14
        self.cur_reg = 0   # The most recently allocated register

        # A table of integer constants to be declared at
        # the end of the source program.  The table maps
        # values to names, so that we can reuse them. 

        self.consts = { }
        
        # A table of variables to be declared at
        # the end of the source program, with the
        # symbols used for them in the assembly code. 
        self.vars = { } 

        # Instructions in the source code, as a list of
        # strings.
        self.assm_lines = [ ]

        # A counter that we append to each symbol to ensure
        # uniqueness
        self.unique_counter = 0

    def add_line(self, line: str) -> None:
        """Add a line of assembly code"""
        self.assm_lines.append(line)
        log.debug("Added line, now {}".format(self.assm_lines))

    def get_const_symbol(self, value: int) -> str:
        """Returns the name of the label associated
        with a constant value, and remembers to 
        declare it at the end of the source code.
        """
        # To be called on the 'val' attribute of a
        # constant, not the Constant object, which
        # is not hashable.
        assert isinstance(value, int)
        if value in self.consts:
            return self.consts[value]
        symbol = self.new_label("const{}".format(value))
        self.consts[value] = symbol
        return symbol

    def get_var_symbol(self, var_name: str) -> str:
        """Returns name name of a label where the 
        variable var_name will be stored.  Variables
        will be initialized to zero. 
        """
        if var_name in self.vars:
            return self.vars[var_name]
        symbol = self.new_label(var_name)
        self.vars[var_name] = symbol
        return symbol

    def new_label(self, base_name:str) -> str:
        """Return a new symbol (label) starting
        with base_name and suffixed with a 
        counter to ensure uniqueness.  For example, 
        new_label("foo") might return "foo_15".
        """
        self.unique_counter += 1
        label = "{}_{}".format(base_name, self.unique_counter)
        return label

    def get_lines(self) -> List[str]:
        """Get all the generated source code, including 
        declarations of variables and constants.
        """
        code = self.assm_lines.copy()
        for varname in self.vars:
            code.append("{}: DATA 0 #{}"
                            .format(self.vars[varname], varname))
        for constval in self.consts:
            code.append("{}:  DATA {}"
                            .format(self.consts[constval], constval))
        return code

    # Register management:
    #   alloc_reg  reserves and returns a register name.
    #   free_reg   marks the most recently reserved register
    #      as being available again. It requires the name of that
    #      register as a safety check.
    def alloc_reg(self) -> str:
        if self.cur_reg >= self.max_reg: 
            raise RunTimeError("Ran out of registers in code generation")
        self.cur_reg += 1
        return "r{}".format(self.cur_reg)

    def free_reg(self, regname: str) -> None:
        expected = "r{}".format(self.cur_reg)
        assert self.cur_reg >= self.min_reg, (
            "{} is outside range of registers that can be allocated"
            .format(regname))
        assert regname == expected, ("Tried to free {}, expecting {}"
                                   .format(regname, expected))
        self.cur_reg -= 1
        return

    


    
        
        
