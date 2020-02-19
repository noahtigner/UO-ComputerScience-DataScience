import re

ASM_SYM_PAT = re.compile(r"""
   # Optional label 
   (
     (?P<label> [a-zA-Z]\w*):
   )?
   # The instruction proper 
   \s*
    (?P<opcode>    (JUMP) | (STORE) | (LOAD) )           # Opcode
    (/ (?P<predicate> [a-zA-Z]+) )?   # Predicate (optional)
    \s+
    ((?P<target>    r[0-9]*), )?          # Target register
    (?P<symbol> \s*[a-zA-Z]\w*)
    (\[ (?P<offset>[-]?[0-9]+) \])?     # Offset (optional)
   # Optional comment follows # or ; 
   (
     \s*
     (?P<comment>[\#;].*)
   )?       
   \s*$             
   """, re.VERBOSE)


def test_match(s: str):
    match = ASM_SYM_PAT.match(s)
    if match:
        print("Matched") # {}, fields {}".format(s, match.groupdict()))
    else:
        print("Didn't match {}".format(s))

test_match("lab: JUMP/Z foo")
test_match("   JUMP/Z foo")
test_match("   LOAD r0,foo")
test_match("STORE r1,bar")
test_match("STORE r1, bar")
test_match("STORE r1,      bar")
test_match("LOAD r3,myvar")