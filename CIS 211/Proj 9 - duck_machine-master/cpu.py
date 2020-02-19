"""
Duck Machine model DM2018W CPU
"""

from instr_format import Instruction, OpCode, CondFlag
from memory import Memory
from register import Register, ZeroRegister
from mvc import MVCEvent, MVCListenable

from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ALU(object):
    """The arithmetic logic unit (also called a "functional unit"
    in a modern CPU) executes a selected function but does not
    otherwise manage CPU state. A modern CPU core may have several
    ALUs to boost performance by performing multiple operatons
    in parallel.
    """
    # The ALU chooses one operation to apply based on a provided
    # operation code.  These are just simple functions of two arguments;
    # in hardware we would use a multiplexer circuit to connect the
    # inputs and output to the selected circuitry for the operation.
    ALU_OPS = {
        OpCode.ADD: lambda x, y: x + y,
        OpCode.MUL: lambda x, y: x * y,
        OpCode.SUB: lambda x, y: x - y,
        OpCode.DIV: lambda x, y: x // y,
        OpCode.SHL: lambda x, y: (x << y) & 0xffffffff,
        OpCode.SHR: lambda x, y: x >> y, 
        # For memory access operations load, store, the ALU
        # performs the address calculation
        OpCode.LOAD: lambda x, y: x + y,
        OpCode.STORE: lambda x, y: x + y,
        # Some operations perform no operation
        OpCode.HALT: lambda x, y: 0
    }

    def exec(self, op, in1: int, in2: int) -> Tuple[int, CondFlag]:
        result = self.ALU_OPS[op](in1, in2)
        if result < 0:
            cc = CondFlag.N
        elif result == 0:
            cc = CondFlag.Z
        elif result > 0:
            cc = CondFlag.P
        else:
            assert False, "Shouldn't reach this point"
        return result, cc

class CPUStep(MVCEvent):
    """CPU is beginning step with PC at a given address"""
    def __init__(self, subject: "CPU", pc_addr: int,
                 instr_word: int, instr: Instruction)-> None:
        self.subject = subject
        self.pc_addr = pc_addr
        self.instr_word = instr_word
        self.instr = instr

class CPU(MVCListenable):
    """Duck Machine central processing unit (CPU)
    has 16 registers (including r0 that always holds zero
    and r15 that holds the program counter), a few
    flag registers (condition codes, halted state),
    and some logic for sequencing execution.  The CPU
    does not contain the main memory but has a bus connecting
    it to a separate memory.
    """

    def __init__(self, memory):
        super().__init__()
        self.memory = memory  # Not part of CPU; what we really have is a connection
        self.registers = [ ZeroRegister(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register(),
                           Register(), Register(), Register(), Register() ]
        self.condition = CondFlag.ALWAYS
        self.halted = False
        self.alu = ALU()
        # Convenient aliases
        self.pc = self.registers[15]

    def step(self):
        log.debug("Step at PC={}".format(self.pc.get()))

        # Fetch
        instr_addr = self.pc.get()
        instr_word = self.memory.get(instr_addr)

        # Decode
        instr = Instruction.decode(instr_word)
        log.debug("Instruction: {}".format(instr))
        # Display the CPU state when we have decoded the instruction,
        # before we have executed it
        self.notify_all(CPUStep(self, instr_addr, instr_word, instr))

        # Execute
        predicate = instr.cond
        if predicate & self.condition:
            log.debug("Predicate passed")
            opcode = instr.op
            """
            extract the values from the registers in instr 
            and have them be the integers for target, left and right
            
            in cpu.py, notice that the CPU object has a field called 
            "registers" that contains 16 Register objects.  
            This is the list you should be indexing with the RegIndex object.  
            Each register has a "get" operation and a "put" operation.  
            2(In the case of r0, the "put" operation has been overridden so that it never changes.)"""

            target = self.registers[instr.reg_target]
            left = self.registers[instr.reg_src1].get()
            right = self.registers[instr.reg_src2].get() + instr.offset

            # Step program counter after forming operands but before
            # storing execution result
            self.pc.put(self.pc.get() + 1)
            # Now a store into PC will overwrite the stepped value
            result, cc = self.alu.exec(opcode, left, right)
            self.condition = cc
            # Load and store are special
            if opcode == OpCode.LOAD:
                memval = self.memory.get(result)
                target.put(memval)
            elif opcode == OpCode.STORE:
                self.memory.put(result,target.get())
            elif opcode == OpCode.HALT:
                self.halted = True
            else:
                target.put(result)
        else:
            # The program counter still moves forward, with no
            # other computation
            log.debug("Predicated instruction will not execute")
            self.pc.put(self.pc.get() + 1)

    def run(self, from_addr=0, limit=None) -> None:
        self.halted = False
        self.pc.put(from_addr)
        step_count = 0
        while not self.halted:
            self.step()
            step_count += 1
            if limit and step_count >= limit:
                break

