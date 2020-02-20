# bitfields
Packing and extracting bit fields in Python integers

A BitField object is a tool for inserting a field into an integer or extracting a field from an integer. 

For example, suppose we wanted to keep some values in the first four bits (bits 0..3) and other values in the second four bits (bits 4..7) of integers.  We would define two BitField objects: 

```
low4 = BitField(0,3)
mid4 = BitField(4,7)
```

Then we could pack two small numbers, each between 0 and 15 inclusive, into one integer: 

```
packed = 0
packed = low4.insert(7, packed)
packed = mid4.insert(8, packed)
```

At this point the value of packed is 135, but let's not think about it in decimal.  Think in hex, where each hexadecimal digit represents 4 binary bits.  Now the value is clear: 

```
>>> hex(packed)
'0x87'
```
There is our 7, in the low digit, and our 8, in the high digit.  

We can also use the BitField object to extract the individual fields: 

```
>>> low4.extract(packed)
7
>>> mid4.extract(packed)
8
```

## To Do

There is very little code to write.  The only tricky part is sign extension for negative bit fields, but I've provided that code for you.  If you find yourself writing more than a few lines for either of the two incomplete methods in bitfield.py, you are probably on the wrong track. 