# Duck Compiler

This project is a compiler for Dumbol, the Duck Machine Basic Operations Language. 

## Recycled code

Out of a sense of environmental responsibility, this compiler is constructed largely from post-consumer waste code, primarily from the Symbolic Calculator project. 

## New language features

A couple of operations have been added: 

* SEQ  (written ';') executes two expressions in sequence and returns the value of the second.  For example: 
```
x 5 =  y 6 = ;
```
which we might write in a more conventional language as 
```
x = 5;  y = 6;
```

* while, for writing loops. Its left operand is the expression to be evaluated.  Its right operand is the loop condition.  The loop will halt if the condition is zero, and continue if the loop has any other value. 

* print, because programs with no output are boring. It has one operand. 

For example, we can print each integer from 0 to 10 like this: 

```
x 0 = 
  x print
  x x 1 + = ;
x 11 - while ;
```

When I compile this program with the Dumbol compiler and then assemble it to create object code, and finally execute the object code with the duck machine simulator, I get this output: 

```
Quack!: 0
Quack!: 1
Quack!: 2
Quack!: 3
Quack!: 4
Quack!: 5
Quack!: 6
Quack!: 7
Quack!: 8
Quack!: 9
Quack!: 10
Halted
```

## How to proceed

The only file you should need to change (and the file you will turn in) is expr.py.   I have provided code generation methods for several classes, but you need to provide it for BinOp and its subclasses.  

Recall that in the symbolic calculator project we factored out most of the 'eval' functionality from PLUS, MINUS, etc. into BinOp, delegating just the _apply method to the concrete subclasses.  You must do something similar here:  The concrete subclasses (Plus, Minus, etc) should have an _opcode method that returns the DM2018W opcode for the instruction they generate. Write one 'gen' method in BinOp and inherit it in the concrete subclasses.  Do not write a 'gen' method in each concrete subclass of BinOp. 
