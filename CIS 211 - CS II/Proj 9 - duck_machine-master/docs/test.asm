  ADD  r1,r0,r0[0]      # r1 = 0
  LOAD  r2,initial      # We will double this value repeatedly
  ADD  r3,r0,r0[16]     # r3 = 16
Loop:
  STORE r2,r0,r1[32]    # mem[32+r1] = r2
  ADD   r1,r1,r0[1]     # r1 += 1
  SHL   r2,r2,r0[1]     # r2 << 1
  SUB   r0,r1,r3[0]     # r1 < r3 ?
  JUMP/N Loop           # repeat
  STORE r2,r0,r0[1026]  # trigger memory-mapped print
  HALT r0,r0,r0
initial:         DATA 5