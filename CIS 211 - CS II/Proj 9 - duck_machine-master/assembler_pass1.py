"""
Assembler for DM2018W assembly language.

This assembler is for fully resolved instructions,
which may be the output of assm_xform.py, which
transforms instructions with symbolic addresses into
instructions with fully resolved (PC-relative) addresses.

Assembly instruction format with all options is 

label: instruction

Labels are resolved (translated into addresses) in
assm_xform.py; in this pass of the interpreter they
are only for documentation.

Both parts are optional:  A label may appear without 
an instruction, and an instruction may appear without 
a label. 

A label is just an alphabetic string, eg.,
  myDogBoo but not Betcha_5_Dollars

An instruction has the following form: 

  opcode/predicate  target,src1,src2[disp]

Opcode is required, and should be one of the DM2018W 
instruction codes (ADD, MOVE, etc); case-insensitive

/predicate is optional.  If present, it should be some 
combination of N,Z,P, e.g., /NP would be "execute if 
not zero".  If /predicate is not given, it is interpreted 
as /ALWAYS, which is an alias for /NZP. 

target is a register number (r0,r1, ... r15) or one of the
register aliases ZERO, PC, SP, etc. 

src1 and src2 are likewise register specifiers. 

[disp] is optional.  If present, it is a 12 bit 
signed integer displacement.  If absent, it is 
treated as [0]. 

DATA is a pseudo-operation:
   myvar:  DATA   18
indicates that the integer value 18
should be stored at this location, rather than
a DM2018W instruction.

"""
from instr_format import Instruction
import memory
import argparse

from typing import Union, List
from enum import Enum, auto

import sys
import io
import re
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Configuration constants
ERROR_LIMIT = 5  # Abandon assembly if we exceed this


# Exceptions raised by this module
class SyntaxError(Exception):
    pass


###
# The whole instruction line is encoded as a single
# regex with capture names for the parts we might
# refer to. Error messages will be crappy (we'll only
# know that the pattern didn't match, and not why), but 
# we get a very simple match/process cycle.  By creating
# a dict containing the captured fields, we can determine
# which optional parts are present (e.g., there could be
# label without an instruction or an instruction without
# a label).
###


# To simplify client code, we'd like to return a dict with
# the right fields even if the line is syntactically incorrect. 
DICT_NO_MATCH = {'label': None, 'opcode': None, 'predicate': None,
                 'target': None, 'src1': None, 'src2': None,
                 'offset': None, 'comment': None}


###
# Although the DM2018W instruction set is very simple, a source
# line can still come in several forms.  Each form (even comments)
# can start with a label.
###

class AsmSrcKind(Enum):
    """Distinguish which kind of assembly language instruction
    we have matched.  Each element of the enum corresponds to
    one of the regular expressions below.
    """
    # Blank or just a comment, optionally
    # with a label
    COMMENT = auto()
    # Fully specified  (all addresses resolved)
    FULL = auto()
    # A data location, not an instruction
    DATA = auto()
    SYM = auto()


# Lines that contain only a comment (and possibly a label).
# This includes blank lines and labels on a line by themselves.
#
ASM_COMMENT_PAT = re.compile(r"""
   # Optional label 
   (
     (?P<label> [a-zA-Z]\w*):
   )?
   \s*
   # Optional comment follows # or ; 
   (
     (?P<comment>[\#;].*)
   )?       
   \s*$             
   """, re.VERBOSE)

# Instructions with fully specified fields. We can generate
# code directly from these.  In the transformation phase we
# pass these through unchanged, just keeping track of how much
# room they require in the final object code.
ASM_FULL_PAT = re.compile(r"""
   # Optional label 
   (
     (?P<label> [a-zA-Z]\w*):
   )?
   # The instruction proper 
   \s*
    (?P<opcode>    [a-zA-Z]+)           # Opcode
    (/ (?P<predicate> [a-zA-Z]+) )?   # Predicate (optional)
    \s+
    (?P<target>    r[0-9]+),            # Target register
    (?P<src1>      r[0-9]+),            # Source register 1
    (?P<src2>      r[0-9]+)             # Source register 2
    (\[ (?P<offset>[-]?[0-9]+) \])?     # Offset (optional)
   # Optional comment follows # or ; 
   (
     \s*
     (?P<comment>[\#;].*)
   )?       
   \s*$             
   """, re.VERBOSE)

# Defaults for values that ASM_FULL_PAT makes optional
INSTR_DEFAULTS = [('predicate', 'ALWAYS'), ('offset', '0')]

# A data word in memory; not a DM2018W instruction
#
ASM_DATA_PAT = re.compile(r""" 
   # Optional label 
   (
     (?P<label> [a-zA-Z]\w*):
   )?
   # The instruction proper  
   \s*
    (?P<opcode>    DATA)           # Opcode
   # Optional data value
   \s*
   (?P<value>  (0x[a-fA-F0-9]+)
             | ([0-9]+))?
    # Optional comment follows # or ; 
   (
     \s*
     (?P<comment>[\#;].*)
   )?       
   \s*$             
   """, re.VERBOSE)

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

PATTERNS = [(ASM_FULL_PAT, AsmSrcKind.FULL),
            (ASM_DATA_PAT, AsmSrcKind.DATA),
            (ASM_COMMENT_PAT, AsmSrcKind.COMMENT),
            (ASM_SYM_PAT, AsmSrcKind.SYM)
            ]


def parse_line(line: str) -> dict:
    """Parse one line of assembly code.
    Returns a dict containing the matched fields,
    some of which may be empty.  Raises SyntaxError
    if the line does not match assembly language
    syntax. Sets the 'kind' field to indicate
    which of the patterns was matched.
    """
    log.debug("\nParsing assembler line: '{}'".format(line))
    # Try each kind of pattern
    for pattern, kind in PATTERNS:
        match = pattern.fullmatch(line)
        if match:
            fields = match.groupdict()
            fields["kind"] = kind
            log.debug("Extracted fields {}".format(fields))
            return fields
    raise SyntaxError("Assembler syntax error in {}".format(line))


def resolve_labels(lines: List[str]):

    error_count = 0
    symtab = {}
    address_counter = 0

    for lnum in range(len(lines)):
        line = lines[lnum]
        try:
            fields = parse_line(line)
            if fields["label"]:
                label = fields["label"]
                if label in symtab:
                    print("Dupl label {} on line {}".format(label, lnum))
                    error_count += 1
                else:
                    symtab[label] = address_counter
            if fields["kind"] != AsmSrcKind.COMMENT:
                address_counter += 1

        except SyntaxError as e:
            error_count += 1
            print("Syntax error in line {}: {}".format(lnum, line))
        except KeyError as e:
            error_count += 1
            print("Unknown word in line {}: {}".format(lnum, e))
        except Exception as e:
            error_count += 1
            print("Exception encountered in line {}: {}".format(lnum, e))
        if error_count > ERROR_LIMIT:
            print("Too many errors; abandoning")
            sys.exit(1)

    return (symtab, error_count)


def transform_instructions(lines: List[str], symtab) -> None:
    address = 0
    for lnum in range(len(lines)):
        line = lines[lnum]

        fields = parse_line(line)
        if fields["kind"] == AsmSrcKind.SYM:
            try:
                lines[lnum] = build_resolved(fields, address, symtab)
            except KeyError as e:
                print("Unknown word in line {}: {}".format(lnum, e))

        if fields["kind"] != AsmSrcKind.COMMENT:
            address += 1
    return None


def build_resolved(fields, address, symtab):
    op = fields["opcode"]
    predicate = fields["predicate"]
    if predicate:
        predicate = "/{}".format(predicate)
    else:
        predicate = " "
    target = fields["target"] or "r0"
    if fields["label"] is None:
        label = " "
    else:
        label = "{}:".format(fields["label"])

    #pc_relative = symtab[0]["symbol"] - address
    pc_relative = symtab[fields["symbol"]] - address

    if op == "STORE" or op == "LOAD":
        # operand = fields["target"]
        return "{} {}{} {},r0,r15[{}]".format(label, op, predicate, target, pc_relative)
    elif op == "JUMP":
        return "{} ADD{} {},r0,r15[{}]".format(label, predicate, target, pc_relative)
    else:
        assert False




def cli() -> object:
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Duck Machine Assembler (pass 1)")
    parser.add_argument("sourcefile", type=argparse.FileType('r'),
                        nargs="?", default=sys.stdin,
                        help="Duck Machine assembly code file")
    parser.add_argument("objfile", type=argparse.FileType('w'),
                        nargs="?", default=sys.stdout,
                        help="Object file output")
    args = parser.parse_args()
    return args


def main():
    """"Assemble a Duck Machine program"""
    args = cli()
    lines = args.sourcefile.readlines()
    table, error_count = resolve_labels(lines)
    if error_count == 0:
        transform_instructions(lines, table)

    for line in lines:
        log.debug("Instruction word {}".format(line))
        print(line, file=args.objfile)


if __name__ == "__main__":
    main()





