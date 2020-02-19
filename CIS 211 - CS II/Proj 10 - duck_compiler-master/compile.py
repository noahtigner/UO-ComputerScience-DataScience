"""
Driver (main program) for
Duck Machine Basic Operations Language (Dumbol).
Input is a postfix expression.  Output is an
assembly language program for making the 
same calculation, provided each variable value 
is assigned before it is used.  (That is, 
these calculations are not symbolic --- they 
are like working in a conventional programming
language in which you must put the instructions 
in the necessary order.) 
"""

from rpn_parse import parse, InputError
from lexer import LexicalError
import expr
import codegen_context

import argparse
import sys

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli() -> object:
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Expression Compiler")
    parser.add_argument("sourcefile", type=argparse.FileType('r'),
                        help="Source program text")
    parser.add_argument("outfile", type=argparse.FileType('w'),
                        nargs="?", default=sys.stdout,
                        help="Output file for assembly code")
    args = parser.parse_args()
    return args


def main():
    args = cli()
    context = codegen_context.Context()
    context.add_line("# Lovingly crafted by robots")
    ok = True
    try:
        exp = parse(args.sourcefile)
        log.debug("Parsed to: {}".format(exp))
        exp.gen(context, target=context.alloc_reg())
        context.add_line("   HALT  r0,r0,r0")
        assm = context.get_lines()
        log.debug("assm = {}".format(assm))
        for line in assm:
            print(line, file=args.outfile)
        print("#Compilation complete")
    except InputError as e:
        print("Failed!")
        print(e)


if __name__ == "__main__":
    main()
