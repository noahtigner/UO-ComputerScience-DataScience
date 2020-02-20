import re
p = re.compile("[a-zA-Z]+")     # any character a-z can appear 1 or more times ex: abcBAD

print(p.match("abcBAD"))




""" Repetition """

p = re.compile("ca+t")          # +: >1 times
# ex: cat, caat, caaaaaat
print(p.match("cat"))

p = re.compile("ca*t")          # *: >=0 times
# ex: ct, cat, caaat
print(p.match("ct"))

p = re.compile("ca?t")          # ?: 0-1 times
# ex: ct, cat
print(p.match("ct"))


""" Metacharacters """

p = re.compile("\w+")           # \w: any alphanumeric characters
# ex: 9, 999999, 9cat9
print(p.match("ct9"))

p = re.compile("\d")            # \d: digits only
# ex: (integers)
print(p.match("0"))

p = re.compile("\s")            # \s: whitespace
# ex:
print(p.match(" "))

p = re.compile("\bword\b")   # \bword\b requires exactly word
print(p.match("word"))




p = re.compile(r"(?P<word>\b\w+\b)")
m = p.search("(((( Lots of punctuation))))")
g = m.group("word")
print(g)


