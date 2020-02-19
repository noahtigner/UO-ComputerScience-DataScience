
class Animal(object):
    def __init__(self, name):
        self.name = name

    def my_sound(self):
        raise NotImplementedError("No generic animals!")

    def rename(self, name):
        self.name = name


    def __str__(self):
        return self.name

    def __repr__(self):
        clazz = type(self).__name__
        return "{}({})".format(clazz, self.name)

class Goat(Animal):

    def my_sound(self):
        return "mmaaaa"

class Dolphin(Animal):

     def __init__(self, name = "Willy", iq = 250):
         self.name = name
         self.iq = iq

     def my_sound(self):
         return "eeekkeee"


     def is_smart(self):
         return self.iq > 200

class Spinner(Dolphin):

    def jump_style(self):
        return "spin"

my_pets = [Dolphin(), Goat("Marcie"), Spinner(), Goat("Billy")]

for pet in my_pets:
    print("{} says {}".format(pet.name, pet.my_sound()))

for pet in my_pets:
    print("{} says {}".format(pet, pet.my_sound()))





Billy = Goat("Billy")
print(Billy.my_sound())

Willy = Dolphin()
print(Willy.my_sound())
if Willy.is_smart():
    print("yep")


print(my_pets)

Craig = Willy
Willy.rename("Marcia")
print(Craig.name)
