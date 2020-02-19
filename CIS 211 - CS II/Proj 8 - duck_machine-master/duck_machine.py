"""
Duck Machine model DM2018W, 
a simulated computer. 

Interprets Duck Machine object code. 
"""

from memory import Memory, MemoryMappedIO
from cpu import CPU

import view

import argparse
import sys
import io

from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def cli() -> object:
    """Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Duck Machine Simulator")
    parser.add_argument("objfile", type=argparse.FileType('r'),
                            help="Object file to execute")
    parser.add_argument("-d", "--display", help="Graphical display",
                        action="store_true")
    args = parser.parse_args()
    return args

def load(file: io.IOBase, memory: Memory) -> None:
    addr = 0
    for line in file:
        word = int(line)
        memory.put(addr, word)
        addr += 1

def duck_out(addr: int, value: int) -> None:
    print("Quack!: {}".format(value))

# Caution!  I have not tested input.
def duck_in(addr: int) -> int:
    return int(input("Quack! Gimme an int!"))

def main():
    """"Run a Duck Machine program from
    object code file.
    """
    args = cli()
    mem = MemoryMappedIO(1024)
    mem.map_address_in(1025,duck_in)
    mem.map_address_out(1026,duck_out)
    cpu = CPU(mem)
    if args.display:
        display = view.MachineStateView(cpu,800,600)
    load(args.objfile, mem)
    cpu.run(limit=10000)  # Limit for debugging only
    print("Halted")
    if args.display:
        input("Press enter to end")


if __name__ == "__main__":
    main()
