DIGITS = "0123456789ABCDEF"

def hexify(i: int) -> str:
    #return "00"
    # FIXME
    string = ""
    if i == 0:
        return "0"
    while i > 0:
        x_low = i & 15
        string = DIGITS[x_low] + string
        # x_high = (i >> 4) & 15
        i = i >> 4
    return string



print(hexify(0x0)) # Expected Out: 0
print(hexify(0xf3e45a)) # Expected Out: F3E45A
