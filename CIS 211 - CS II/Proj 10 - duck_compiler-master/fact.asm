# Lovingly crafted by robots
   LOAD r3,const5_2
  STORE  r3,x_1
   LOAD r3,const1_4
  STORE  r3,fact_3
loop_5:  #While loop
   LOAD r3,x_1
  SUB  r0,r3,r0 
  JUMP/Z endloop_6
   LOAD r4,x_1
   LOAD r5,fact_3
TIMES r4,r4,r5
  STORE  r4,fact_3
   LOAD r4,x_1
   LOAD r5,const1_4
MINUS r4,r4,r5
  STORE  r4,x_1
  JUMP loop_5
endloop_6: 
   LOAD r3,fact_3
   STORE r3,r0,r0[1026] # Print
   HALT  r0,r0,r0
x_1: DATA 0 #x
fact_3: DATA 0 #fact
const5_2:  DATA 5
const1_4:  DATA 1
