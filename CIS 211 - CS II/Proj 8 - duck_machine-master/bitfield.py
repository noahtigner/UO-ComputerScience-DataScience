"""
A bit field is a range of binary digits within an
unsigned integer.   Bit 0 is the low-order bit,
with value 1 = 2^0.  Bit 31 is the high-order bit, 
with value 2^31. 

A bitfield object is an aid to encoding and decoding 
instructions by packing and unpacking parts of the 
instruction in different fields within individual 
instruction words. 

Note that we are treating Python integers as if they 
were 32-bit unsigned integers.  They aren't ... Python 
actually uses a variable length signed integer
representation, but we ignore that because we are trying
to simulate a machine-level representation. 
"""

WORD_SIZE = 32 

class BitField(object):
    """A BitField object handles insertion and 
    extraction of one field within an integer.
    """

    def __init__(self, from_bit: object, to_bit: object) -> object: 
        """Tool for inserting and extracting bits 
        from_bit ... to_bit, where 0 is the low-order
        bit and 31 is the high-order bit of an unsigned
        32-bit integer. For example, the low-order 4 bits 
        could be represented by from_bit=0, to_bit=3. 
        """
        assert 0 <= from_bit < WORD_SIZE
        assert from_bit <= to_bit <= WORD_SIZE
        self.from_bit = from_bit
        self.to_bit = to_bit

        self.field_width = 1 + to_bit - from_bit

        # Mask for the field in the low-order bits
        self.low_mask = self._construct_mask(self.field_width)

        # Sign extension complement and mask
        self.comp = 2 ** self.field_width
        self.sign_bit = 2 ** (self.field_width - 1)


    def _construct_mask(self, width: int) -> int: 
        """Construct a mask for the first width bits"""
        assert width >= 0
        mask = 0
        for bit in range(width):
            mask = (mask << 1) + 1
        return mask

    def insert(self, field_value: int, word: int) -> int:
        """Insert value of field into word. 
        For example, 
          if word is   xaa00aa00 and
          field_val is x0000000f
          and the field is bits 4..7
        then insert gives xaa00aaf0
        """
        #eraser = ~(self.low_mask << self.from_bit)
        #field = (self.low_mask & field_value) << self.from_bit
        return (word & ~(self.low_mask << self.from_bit)) | ((self.low_mask & field_value) << self.from_bit)


    def extract(self, word: int) -> int:
        """Extract the bitfield and return it in the 
        low-order bits.  For example, if we are extracting
        the high-order five bits, the result will be an 
        integer between 0 and 31. 
        """
        return self.low_mask & (word >> self.from_bit)


    def extract_signed(self, word: int) -> int:
        """Extract the bitfield and return it in the 
        low order bits, sign-extended.  
        """
        unsigned = self.extract(word)
        # Sign extend if negative
        if unsigned & self.sign_bit:
            return 0 - (self.comp - unsigned)
        else: 
            return unsigned


        
        
    

    


    
        
