

"""
#Food

class Food(object):
    #Abstract Base Class

    def calories(self) -> int:
        #How many calories in this food, per portion?

        raise NotImplementedError("Hey, you need to override this")

class AtomicFood(Food):

    def __init__(self, calories):
        self.calories_per_portion = calories

    def calories(self):
        return self.calories_per_portion

class ComposedFood(Food):

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def calories(self):
        total = 0
        for food in self.ingredients:
            total += food.calories()
        return total

noodles = AtomicFood(100)
cheese = AtomicFood(150)
mac_n_cheese = ComposedFood([noodles, cheese])

dough = AtomicFood(45)
sauce = AtomicFood(50)
pizza = ComposedFood([cheese, sauce, dough])

pizza_mac = ComposedFood([mac_n_cheese, pizza])
print(pizza_mac.calories())
"""


#Linked List
class LinkedList(object):
    pass

class EmptyList(LinkedList):

    def __init__(self):
        return

    def length(self):
        return 0

    def __str__(self):
        return "."

class NonEmptyList(LinkedList):

    def __init__(self, item, li: LinkedList):
        self.item = item
        self.rest = li

    def length(self):
        return 1 + self.rest.length()

    def __str__(self):
        return "{}{}".format(self.item, self.rest)

li = EmptyList()
li = NonEmptyList(1, li)
li = NonEmptyList(2, li)
li = NonEmptyList(3, li)
print(li.length())
print(li)

"""

w = 3|0
w = (7<<4) | w
print(w)
"""




