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