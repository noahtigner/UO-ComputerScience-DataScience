"""
The Duck Machine model DM2018W main memory
is an array of 32-bit integers. 

"""

from mvc import MVCEvent, MVCListenable

from typing import Callable

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class SegFault(Exception):
    """Segmentation fault is actually an operating-system 
    level fault, not a hardware fault, but it's what you 
    see when you use a bad address in a program, so we'll 
    use that exception name here.
    """
    pass

class MemoryEvent(MVCEvent):
    pass

class MemoryRead(MemoryEvent):
    """A memory cell at a particular address has been read"""
    def __init__(self, subject: "Memory", addr: int, value: int):
        self.subject = subject
        self.addr = addr
        self.value = value

class MemoryWrite(MemoryEvent):
    """A memory cell at a particular address has been written """
    def __init__(self, subject: "Memory", addr: int, value: int):
        self.subject = subject
        self.addr = addr
        self.value = value


class Memory(MVCListenable):
    """Just an array of integers.  Other values are 
    encoded as integers. 
    """

    def __init__(self, capacity: int=1024) -> None:
        super().__init__()  # Make it listenable
        self.capacity = capacity
        self._mem = capacity * [ 0 ]

    def _check_bounds(self, index):
        if index < 0 or index >= self.capacity:
            raise SegFault("Memory address {} out of bounds".format(index))

    def get(self, index: int) -> int:
        """Fetch a word from memory"""
        log.debug("Fetching word at memory address {}".format(index))
        self._check_bounds(index)
        self.notify_all(MemoryRead(self,index,self._mem[index]))
        return self._mem[index]

    def put(self, index: int, value: int) -> None:
        """Store a word into memory"""
        self._check_bounds(index)
        log.debug("Storing value {} at memory address {}".format(value, index))
        self._mem[index] = value
        self.notify_all(MemoryWrite(self,index,value))


class MemoryMappedIO(Memory):
    """Use a few otherwise unused addresses for input/output. 
    It is a common practice to trigger some input/output or 
    device commands by interpreting some memory addresses as 
    as commands. This is not done in the CPU, but by connecting 
    to the bus (wires) between CPU and memory. 
    """
    def __init__(self, capacity: int=1024) -> None:
        super().__init__(capacity)
        self.hooks_read = { }
        self.hooks_write = { }

    def map_address_in(self, addr: int,
                           hook: Callable[[int], int]) -> None:
        """Memory reads of this address will call the hook function"""
        self.hooks_read[addr] = hook

    def map_address_out(self, addr: int,
                            hook: Callable[[int,int], None]) -> None:
        """Memory writes of this address will call the hook function"""
        self.hooks_write[addr] = hook

    def get(self, index: int) -> int:
        """Hook OR Fetch a word from memory"""
        if index in self.hooks_read:
            hook = self.hooks_read[index]
            return hook(index)
        return super().get(index)

    def put(self, index: int, value: int) -> None:
        """Hook OR Store a word into memory"""
        if index in self.hooks_write:
            hook = self.hooks_write[index]
            hook(index, value)
            return
        super().put(index, value)
