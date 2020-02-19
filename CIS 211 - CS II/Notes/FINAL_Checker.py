"""
Objects as closures, more or less.
"""

class Checker(object):
    """This checker is abstract"""

    def __init__(self, level):
        """Initialize to thresshold level of some quality"""
        self.level = level

    def check(self, obj):
        raise NotImplementedError("Checker.check must be overridden")


class Fruit(object):

    def __init__(self, name: str, sweet: int, crunch: int, savory: int):
        """With qualities on a scale from 0 to 9"""
        self.name = name
        self.sweet = sweet
        self.crunch = crunch
        self.savory = savory

    def check(self, checker: Checker) -> bool:
        """Apply the checker"""
        return checker.check(self)

    def __repr__(self):
        return "{}(sweet={}, crunch={}, savory={})".format(
            self.name, self.sweet, self.crunch, self.savory)


class CrunchChecker(Checker):
    """Checks for crunchiness above threshhold"""
    #FIXME
    def check(self, obj) -> bool:
        return obj.crunch >= self.level




class SweetChecker(Checker):
    """ Checks for sweetness above threshhold"""
    #FIXME
    def check(self, obj) -> bool:
        return obj.sweet >= self.level


class FruitBowl(object):
    """Just a bowl of fruit"""

    def __init__(self):
        self.contents = [ ]

    def add(self, fruit: Fruit):
        self.contents.append(fruit)

    def choose(self, checker: Checker):
        chosen = [ ]
        # FIXME
        for fruit in self.contents:
            if fruit.check(checker):
                chosen.append(fruit.name)
        return chosen


bowl = FruitBowl()
bowl.add(Fruit("Apple", sweet=5, crunch=7, savory=2))
bowl.add(Fruit("Pear", sweet=7, crunch=3, savory=1))
bowl.add(Fruit("Banana", sweet=7, crunch=0, savory=0))

print(bowl.choose(CrunchChecker(5)))  # Expecting [ "Apple" ]
print(bowl.choose(SweetChecker(6)))   # Expecting [ "Pear", "Banana" ]