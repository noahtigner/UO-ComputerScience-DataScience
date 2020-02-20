# Lovingly crafted by robots

  LOAD  r2,r0,r15[16]
  STORE  r2,r0,r15[14]
loop_3:  #While loop

  LOAD  r2,r0,r15[13]
  LOAD  r3,r0,r15[14]
MINUS r2,r2,r3

  SUB  r0,r2,r0 

  ADD/Z r0,r0,r15[8]
  LOAD  r3,r0,r15[8]
   STORE r3,r0,r0[1026] # Print

  LOAD  r3,r0,r15[6]
  LOAD  r4,r0,r15[8]
PLUS r3,r3,r4

  STORE  r3,r0,r15[3]
  ADD  r0,r0,r15[-11]
endloop_4: 

   HALT  r0,r0,r0

x_1: DATA 0 #x

const0_2:  DATA 0

const11_5:  DATA 11

const1_6:  DATA 1

