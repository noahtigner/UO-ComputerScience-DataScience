"""
Encoding and decoding the instruction format of 
our simulated computer. 

Instruction words are modeled as an unsigned 32-bit integer
with the following fields (from high-order to low-order bits).  
All are unsigned except offset, which is a signed value in 
range -2^11 to 2^11 - 1. 

See docs/duck_machine.md for details. 
"""

from bitfield import BitField
from enum import Enum, Flag, IntEnum
import typing

# The field bit positions
instr_field = BitField(27,31)
# You need bitfields for the remaining fields of a
# DM2018W instruction word
cond_field = BitField(24, 26)
reg_target_field = BitField(20, 23)
reg_src1_field = BitField(16, 19)
reg_src2_field = BitField(12, 15)
offset_field = BitField(0, 11)

class OpCode(Enum):
    """The operation codes specify what the CPU should do"""
    HALT = 0  # So we'll stop if we hit a zero in memory
    LOAD = 1
    STORE = 2
    ADD = 3
    SUB = 5
    MUL = 6
    DIV = 7
    SHL = 8  # Shift left
    SHR = 9  # Shift right



class CondFlag(Flag):
    """The condition mask in an instruction and the format
    of the condition code register are the same, so we can 
    logically and them to predicate an instruction. 
    """
    N = 1
    Z = 2
    P = 4
    ALWAYS = N | Z | P

    def __str__(self):
        """
        If the exact combination has a name, we return that. 
        Otherwise, we combine bits, e.g., ZP for non-negative. 
        """
        for i in CondFlag:
            if i is self:
                return i.name
        # No exact alias; give name as sequence of bit names
        bits = [ ]
        for i in CondFlag:
            masked = self & i
            if masked is i:
                bits.append(i.name)
        return "".join(bits)
    
class RegIndex(IntEnum):
    """Named r0..r15; some are special"""
    r0 = 0   # r0 always holds zero; never changes
    r1 = 1
    r2 = 2
    r3 = 3
    r4 = 4
    r5 = 5
    r6 = 6
    r7 = 7
    r8 = 8
    r9 = 9
    r10 = 10
    r11 = 11
    r12 = 12
    r13 = 13   
    r14 = 14
    r15 = 15  # r15 is the program counter register

    def __str__(self):
        return self.name
    

class Instruction(object):
    """This class is for a decoded instruction, with fields 
    for each part of the instruction.  That is not the same 
    as the instruction *word* in memory.  We decode an
    instruction word (by extracting bit fields) to form an 
    Instruction object. 
    """

    # This constructor is typically called by one of the
    # 'factory methods' below.  During the fetch/decode/execute
    # cycle, the constructor is called by the decode method. 
    # 
    def __init__(self, op: OpCode, cond: CondFlag,
                     reg_target: RegIndex, reg_src1: RegIndex,
                     reg_src2: RegIndex,
                     offset: int):
        """Assemble an instruction from its fields."""
        self.op = op
        self.cond = cond
        self.reg_target = reg_target
        self.reg_src1 = reg_src1
        self.reg_src2 = reg_src2
        self.offset = offset
        return

    # This factory method is handy for testing and debugging.
    #
    @classmethod
    def make(cls, opcode: str, predicate: str,
                     target: str, src1: str, src2: str,
                     offset: int) -> "Instruction":
        """Construct instruction from mnemonic names"""
        return cls(OpCode[opcode], CondFlag[predicate], RegIndex[target],
                       RegIndex[src1], RegIndex[src2], offset)


    #  'encode' is the inverse of 'decode' --- it converts from a
    #   an Instruction object to an int representing an instruction word.
    #   It is used by the assembler to convert assembly language to
    #   object code. 
    def encode(self) -> int:
        """Encode instruction as 32-bit integer"""
        word = 0
        word = instr_field.insert(self.op.value, word)
        word = cond_field.insert(self.cond.value, word)
        word = reg_target_field.insert(self.reg_target.value, word)
        word = reg_src1_field.insert(self.reg_src1.value, word)
        word = reg_src2_field.insert(self.reg_src2.value, word)
        word = offset_field.insert(self.offset, word)
        return word

    # 'decode' is used in the fetch/decode/execute cycle of the
    # CPU.  Extract each of the fields from the instruction word
    # and then use them to create an Instruction object.
    #
    @classmethod
    def decode(cls, word: int) -> "Instruction": 
        """Decode a memory word (32 bit int) into a new Instruction"""

        """ Use your bitfields module to get the arguments 
        for the constructor of an instruction, and then use the 'cls' 
        variable to create (and return) the actual Instruction object
        Use your bitfield project to extract correct fields."""

        op = instr_field.extract(word)
        cond = cond_field.extract(word)
        reg_target = reg_target_field.extract(word)
        reg_src1 = reg_src1_field.extract(word)
        reg_src2 = reg_src2_field.extract(word)
        offset = offset_field.extract_signed(word)

        # Here's where we call the real constructor to combine
        # these values into an Instruction object
        return cls(OpCode(op), CondFlag(cond),
                       RegIndex(reg_target),
                       RegIndex(reg_src1), RegIndex(reg_src2),
                       offset)

    # The assembler uses the from_dict method to construct an
    # instruction after parsing a line of assembly code
    # 
    @classmethod
    def from_dict(cls, d) -> "Instruction":
        """Create an instruction from a dict containing fields."""
        return cls.make(d["opcode"], d["predicate"],
                            d["target"], d["src1"], d["src2"],
                            int(d["offset"]))


    def __str__(self):
        """String representation looks something like assembly code"""
        if self.cond is CondFlag.ALWAYS:
            cond_codes = ""
        else:
            cond_codes = "/{}".format(self.cond)
        
        return "{}{:4}  {},{},{}[{}]".format(
            self.op.name,  cond_codes,
            self.reg_target.name, self.reg_src1.name, 
            self.reg_src2.name, self.offset)

        
