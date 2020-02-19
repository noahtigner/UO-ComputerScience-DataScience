# The Duck Machine

The Duck Machine model 2018W (DM2018W) is a virtual computer architecture.  It is much simpler than most current CPU  architectures, but introduces some basic concepts of computer architecture: 

* A central processing unit (CPU) with a limited number of high-speed registers, separate from a random-access memory (RAM) with much higher capacity.
* General purpose registers and a small number of registers dedicated to special purposes, including a program counter. 
* Storage of instructions and data together, indistinguishably, in the random access memory. 
* Operation codes and references to operands packed together in bit fields of instruction words. 
* A fetch/decode/execute cycle for program execution. 

Our Duck Machine simulation lacks several features of a more complete or realistic CPU: 

* The Duck Machine is modeled at the level of instruction set architecture (ISA).  We do not model pipelines, caches, or many other important parts of the hardware implementation of an ISA.  You will learn about these in CIS 314. 
* While most modern computer memories are addressed at the granularity of bytes, the RAM memory of the Duck Machine is addressed at the granularity of 32-bit words.  
* The Duck Machine does not support virtual memory. All memory addresses are indexes of the (simulated) physical RAM.  You will learn about mapping virtual memory addresses to physical memory addresses in CIS 415. 
* The Duck Machine does not support asynchronous execution or interrupts.  It lacks any protection mechanisms (there is no "supervisor mode").  You will learn more about these in CIS 415. 

Duck Machine projects were introduced many years ago in the 21x series by Amr Sabry, now at Indiana University.  Arthur Farley extended and refined them for a series of CIS 212 projects which included a simple assembler and compiler.  Model 2018W is thus a revival of sorts. 

### Based on a true story

The DM2018W is based on the ARM (Advanced Risc Machines) instruction set architecture to approximately the same extent that The Hobbit is based on The Odyssey (with elements drawn also from Beowulf).  The ARM processor is found in many small devices including phones and the Raspberry Pi computer. 

Notable features of the ARM instruction set architecture that have been adopted by the DM2018W include: 

* A simple load/store architecture (like many reduced instruction set computers). 
* Uniform treatment of the program counter (PC) as any other general purpose register. 
* Conditional execution of all instructions

Together these allow a very compact instruction set.  For example, a conditional jump is just a 'move' instruction, conditionally moving a new value into the program counter register. 

## Register Set

The DM2018W has 16 registers, 0..15.  The following registers have special uses (but are still addressable as general purpose registers): 

* R15 is also referred to as PC, the Program Counter
* R14 is also referred to as LR, the Link Register or Return Address Register. (We are not currently using the return address register.) 
* R13 is also referred to as the stack pointer. (We are not using it as a stack pointer yet.) 
* R0 always holds zero.  Moving or loading another value into R0 does not change the value of R0.  R0 is useful in memory addressing and as a target when we wish to set a condition code without saving a value. 

In addition to the general purpose registers, there are three special purpose flag registers, called the condition codes: 

* The N flag indicates the prior instruction produced a negative result
* The Z flag indicates the prior instruction produced a result of zero
* The P flag indicates the prior instruction produced a positive result

Note that every result produced by an arithmetic instruction must set exactly one of the condition codes.  

## The Instruction Word

All random access memory is organized as 32-bit words. Each instruction word is a concatenation of the following fields, where bits are numbered from 0..31 with bit 0 being the low order bit and each bit k representing 2^k in an unsigned integer.  All bit fields are treated as unsigned integers except the displacement field, which is interpreted a 10-bit integer in twos complement form. 

The bit fields are: 

* 27..31 (5 bits) operation code (e.g., add, store, etc)
* 24..26 (3 bits) conditional execution masks (mN,mZ,mP).  Conceptually, we treat each bit as a boolean variable, True for 1 and False for 0.  We combine them with the condition code registers N, Z, P,  and execute the instruction only if ((mN and N) or (mZ and Z) or (mP or P)).  Note that if all three mask bits are 1, the instruction will always be executed, and an instruction with all three mask bits 0 will never be executed.  
* 20..23 (4 bits) index of target register (where the result of an operation should be stored).  Note that if the target register is r0 (ZERO), the result is effectively discarded, but the condition codes are still set.  Also, if the target register is r15, also known as PC, the instruction is effectively a control flow jump. 
* 16..19 (4 bits) index of first source register
* 12..15 (4 bits) index of the second source register
* 0..11 (12 bits) a displacement, interpreted as a *signed* 12 bit twos-complement integer ranging from -2048 (-2^11) to 2047 (2^11 - 1).  

Most operations combine the first source register with the sum of the second source register and the displacement, placing the result in the target register. 


## Notation

In documentation we will write a Duck18W instruction word as 

```
    OP/cc  rX,rY,rZ[disp]
```

where OP is the operation code (e.g., ADD, SUB, STORE), cc is the condition mask (and /cc is omitted when the mask bits are all 1), rX is the target register, and rY and rZ are the operand registers.  The ```[disp]``` part is omitted when the displacement is zero. 

For example, 

```
	ADD  r1,r1,r2
```

denotes an unconditional addition of the values in register 1 and register 2, storing the result in register 1 and also setting one of the three condition code registers to 1 (e.g., only the P condition code if the sum is a positive number) while setting the other two condition code registers to zero. 

## Arithmetic operations

The arithmetic operations are ADD, SUB, MUL, DIV. 
```ADD rX,rY,rZ[disp]```  stores the sum of rY,rZ, and disp in rX and sets the condition codes. 

```SUB rX,rY,rZ[disp]``` stores (rY-(rZ+disp)) in rX and sets the condition codes. 

Multiplication and integer division (like the Python operation // ) work likewise, and in general all arithmetic operations OP 
```
	OP/cc  rx,ry,rz[disp]
```
may be thought of as expressing
```
  if cc:
     rx = OP(ry,rz+disp)
```
Each arithmetic operation sets the condition code. 

## Using the Special Registers for Control Flow

Register 0 (r0) always holds zero.  We may make r0 the target register when we want to obtain a condition code (negative, zero, or positive result) but we don't want to save any arithmetic result.  So we don't need a separate operation for comparison; we can just subtract and throw away the result.  For example, we can compare the contents of register 1 to the constant 16 this way: 

```
	SUB  r0,r1,r0[16]
```

If the value in r1 is greater than 16, the P (positive) condition code flag will be set.  If the value is equal to 16, the Z (zero) condition code flag will be set.  If the value in register 1 is less than 16, the N (negative) condition code flag will be set. 

Register 15 is the program counter.  We can store a value into register 15 to change the flow of execution (called a "branch"). In particular, we can calculate the address to be executed by adding a displacement to the current program counter value.  This is called a "relative branch". 

```
	ADD  r15,r0,r15[-8]
```
The instruction above describes a branch to the address 8 instructions before the current instruction.   Combining these two techniques with conditional execution based on condition codes, we can easily make a comparison and conditional branch: 

```
	SUB  	r0,r1,r0[16]
	ADD/Z	r15,r0,r15[-8]
```
The sequence above expresses "if the value in r1 is equal to 16, branch to the location 8 instructions back."  


## Load and Store

As is usual in a reduced instruction set architecture, values move between main memory (RAM) and the CPU only through load and store operations and through instruction fetch.  The memory access instructions are: 

```LOAD  rX,rY,rZ[disp]``` loads the memory value at address rY + rZ + disp into rX. 

```STORE  rX,rY,rZ[disp]``` stores the value in rX into main memory at address rY + rZ + disp.

