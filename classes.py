# Stores each information for pets that are in teams
class Pet:
    def __init__(self, name, attack, health, level, exp, pos, held):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        self.exp = exp
        self.held = held
        self.pos = pos
        # Used fdr Hurt ability checks
        self.hurt = health

        # Used for Whale ability
        self.swallowed = None

        # Used for abilities with max number of triggers
        if name == "gorilla":
            self.triggers = level
        elif name == "fly":
            self.triggers = 3
        else:
            self.triggers = None


# Stores information for pets that are in the shop
class ShopPet:
    def __init__(self, name, attack, health):
        self.name = name
        self.attack = attack
        self.health = health

        # Used for future implementation
        self.frozen = False


# Stores information for food that is in the shop
class ShopFood:
    def __init__(self, name):
        self.name = name

        # Used for future implementation
        self.frozen = False


# Node and children of action tree
class Tree:
    def __init__(self, action, score):
        self.action = action
        self.score = score
        # Children trees
        self.children = []

    # Add child to list of children
    def add_child(self, tree):
        self.children.append(tree)

    # Prints tree
    def __str__(self, level=0):
        if self.action is not None:
            ret = "\t" * level + self.action[0] + " " + self.action[1].name + " " + str(self.score) + "\n"
        else:
            ret = "\t" * level + str(self.action) + " " + str(self.score) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
