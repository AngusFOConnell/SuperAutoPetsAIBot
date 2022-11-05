import copy
import random
import classes


# Simulates a turn/battle between two teams
import print_helpers


def turn(team_1, team_2):
    # Used to print debug information
    debug = False

    # Stores total number of wins for each team and draws
    team1_win = 0
    team2_win = 0
    draw = 0

    # Controls how many battles to simulate between the two teams
    number_of_battles = 50

    for battle in range(0, number_of_battles):
        team1 = copy.deepcopy(team_1)
        team2 = copy.deepcopy(team_2)
        if debug:
            for pet in team1:
                print(pet.name)
            for pet in team2:
                print(pet.name)
            frame = 0
            print("-------------START OF BATTLE -------------")

        # End of Turn abilities
        (team1, team2) = end_of_turn(team1, team2)

        # Start of Battle abilities
        (team1, team2) = start_of_battle(team1, team2)

        # Loops until either team has lost all pets (loses)
        while len(team1) > 0 and len(team2) > 0:
            if debug:
                frame += 1
                print("-------------FRAME " + str(frame) + "-------------")
                print("TEAM 1: ")
                for pet in team1:
                    print(pet.name, end=" ")
                    print(pet.attack, end=" ")
                    print(pet.health, end=" ")
                print()
                print("TEAM 2: ")
                for pet in team2:
                    print(pet.name, end=" ")
                    print(pet.attack, end=" ")
                    print(pet.health, end=" ")
                print()

            # Before Attack abilities
            (team1, team2, team1_attack, team2_attack) = before_attack(team1, team2)

            # Simulates the attack between the two front pets
            if team1_attack and team2_attack:
                (team1, team2, team1_attack, team2_attack) = attack(team1, team2, team1_attack, team2_attack)

        # Reassigns the front pet, next to attack
        if len(team1) > 0:
            team1_attack = team1[0]
        else:
            team1_attack = None

        if len(team2) > 0:
            team2_attack = team2[0]
        else:
            team2_attack = None

        # Counts win/loss/draw
        if team2_attack:
            if debug:
                print("-------------LOSS-------------")
                for pet in team2:
                    if pet is not None:
                        print(pet.name, pet.attack, pet.health)
            team2_win += 1
        elif team1_attack:
            if debug:
                print("-------------WIN-------------")
                for pet in team1:
                    if pet is not None:
                        print(pet.name, pet.attack, pet.health)
            team1_win += 1
        else:
            if debug:
                print("-------------DRAW-------------")
            draw += 1

    if debug:
        print(team1_win, team2_win, draw)

    # Returns proportion of wins for either team and draws
    return float(team1_win / number_of_battles), float(team2_win / number_of_battles), float(draw / number_of_battles)


def get_pos(pet):
    return pet.pos


def get_atk(pet):
    return pet.attack


def get_hp(pet):
    return pet.health


# End of Turn Abilities
def end_of_turn(team1, team2):
    team1_ability_copy = team1.copy()
    team2_ability_copy = team2.copy()

    # Sorts teams by ability order (Highest attack first)
    ability_order = team1_ability_copy + team2_ability_copy
    ability_order.sort(key=get_pos, reverse=True)
    ability_order.sort(key=get_atk, reverse=True)

    # Parrot ability - Copy ability from the nearest pet ahead as level 1/2/3 until end of battle.
    for pet in ability_order:
        if pet.name == "parrot":
            if pet.pos != 0:
                if pet in team1:
                    pet.name = team1[pet.pos - 1].name
                elif pet in team2:
                    pet.name = team2[pet.pos - 1].name

    return team1, team2


# Start of Battle Abilities
def start_of_battle(team1, team2):
    team1_ability_order = team1.copy()
    team2_ability_order = team2.copy()

    # Sorts teams by ability order (Highest attack first)
    ability_order = team1_ability_order + team2_ability_order
    ability_order.sort(key=get_pos, reverse=True)
    ability_order.sort(key=get_atk, reverse=True)

    # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
    for pet in ability_order:
        if pet in team1:
            (ability_repeat, tiger_level) = tiger(pet, team1)
        else:
            (ability_repeat, tiger_level) = tiger(pet, team2)

        # Repeats ability if pet behind is a tiger
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = pet.level
            else:
                level = tiger_level

            # Mosquito ability - Start of battle → Deal 1 damage to 1/2/3 random enemy/enemies.
            if pet.name == "mosquito":
                if pet in team1:
                    choices = random.sample(team2, min(level, len(team2)))
                    for team2_pet in choices:
                        team2_pet = damage(team2_pet, 1)
                        (team1, team2) = post_damage_checks(team1, team2)

                elif pet in team2:
                    choices = random.sample(team1, min(level, len(team1)))
                    for team1_pet in choices:
                        team1_pet = damage(team1_pet, 1)
                        (team1, team2) = post_damage_checks(team1, team2)

            # Dolphin ability - Start of battle → Deal 3 damage to the lowest health enemy. Triggers 1/2/3 time(s).
            if pet.name == "dolphin":
                if pet in team1:
                    for ability_trigger in range(0, level):
                        if len(team2) > 0:
                            team2_copy = team2.copy()
                            team2_copy.sort(key=get_hp)
                            lowest_hp_pets = []
                            for pet in team2_copy:
                                if pet.health == team2_copy[0].health:
                                    lowest_hp_pets.append(pet)
                            choice = random.sample(lowest_hp_pets, 1)
                            choice[0] = damage(choice[0], 3)
                            (team1, team2) = post_damage_checks(team1, team2)

                elif pet in team2:
                    for ability_trigger in range(0, level):
                        if len(team1) > 0:
                            team1_copy = team1.copy()
                            team1_copy.sort(key=get_hp)
                            lowest_hp_pets = []
                            for pet in team1_copy:
                                if pet.health == team1_copy[0].health:
                                    lowest_hp_pets.append(pet)
                            choice = random.sample(lowest_hp_pets, 1)
                            choice[0] = damage(choice[0], 3)
                            (team1, team2) = post_damage_checks(team1, team2)

            # Skunk ability - Start of battle → Reduce the highest health enemy by 33%/66%/99% health.
            if pet.name == "skunk":
                if pet in team1:
                    team2_copy = team2.copy()
                    team2_copy.sort(key=get_hp, reverse=True)
                    highest_hp_pets = []
                    for team2_pet in team2_copy:
                        if team2_pet.health == team2_copy[0].health:
                            highest_hp_pets.append(team2_pet)
                    choice = random.sample(highest_hp_pets, 1)
                    if level == 1:
                        choice[0].health = int(choice[0].health * 0.66)
                    elif level == 2:
                        choice[0].health = int(choice[0].health * 0.33)
                    else:
                        choice[0].health = 1

                elif pet in team2:
                    team1_copy = team1.copy()
                    team1_copy.sort(key=get_hp, reverse=True)
                    highest_hp_pets = []
                    for team1_pet in team1_copy:
                        if team1_pet.health == team1_copy[0].health:
                            highest_hp_pets.append(team1_pet)
                    choice = random.sample(highest_hp_pets, 1)
                    if level == 1:
                        choice[0].health = int(choice[0].health * 0.66)
                    elif level == 2:
                        choice[0].health = int(choice[0].health * 0.33)
                    else:
                        choice[0].health = 1

            # Dodo ability - Start of battle → Give 50%/100%/150% of attack to the nearest friend ahead.
            if pet.name == "dodo":
                if pet in team1:
                    if pet.pos > 0:
                        pre_atk = team1[pet.pos - 1].attack
                        team1[pet.pos - 1].attack = team1[pet.pos - 1].attack + int((pet.attack / 2) * level)

                elif pet in team2:
                    if pet.pos > 0:
                        pre_atk = team2[pet.pos - 1].attack
                        team2[pet.pos - 1].attack = team2[pet.pos - 1].attack + int((pet.attack / 2) * level)

            # Crocodile ability - Start of battle → Deal 8 damage to the last enemy. Triggers 1/2/3 time(s).
            if pet.name == "crocodile":
                if pet in team1:
                    for ability_trigger in range(0, level):
                        team2_copy = team2.copy()
                        team2_copy.sort(key=get_pos, reverse=True)
                        if len(team2_copy) > 0:
                            team2_copy[0] = damage(team2_copy[0], 8)
                            (team1, team2) = post_damage_checks(team1, team2)

                elif pet in team2:
                    for ability_trigger in range(0, level):
                        team1_copy = team1.copy()
                        team1_copy.sort(key=get_pos, reverse=True)
                        if len(team1_copy) > 0:
                            team1_copy[0] = damage(team1_copy[0], 8)
                        (team1, team2) = post_damage_checks(team1, team2)

            # Crab ability - Start of battle → Copy 50%/100%/150% of health from the most healthy friend.
            if pet.name == "crab":
                if pet in team1:
                    team1_copy = team1.copy()
                    team1_copy.sort(key=get_hp, reverse=True)
                    for other_pet in team1_copy:
                        if other_pet.name != pet:
                            pet.health = int((other_pet.health / 2) * level)
                            break

                if pet in team2:
                    team2_copy = team2.copy()
                    team2_copy.sort(key=get_hp, reverse=True)
                    for other_pet in team2_copy:
                        if other_pet.name != pet:
                            pet.health = int((other_pet.health / 2) * level)
                            break

            # Leopard ability - Start of battle → Deal 50% attack damage to 1/2/3 random enemy/enemies.
            if pet.name == "leopard":
                if pet in team1:
                    choices = random.sample(team2, min(level, len(team2)))
                    for team2_pet in choices:
                        team2_pet = damage(team2_pet, int(pet.attack / 2))
                        (team1, team2) = post_damage_checks(team1, team2)

                elif pet in team2:
                    choices = random.sample(team1, min(level, len(team1)))
                    for team1_pet in choices:
                        team1_pet = damage(team1_pet, int(pet.attack / 2))
                        (team1, team2) = post_damage_checks(team1, team2)

        # Whale Ability - Start of turn → Swallow the nearest friend ahead and release it as a level 1/2/3 after fainting.
        if pet.name == "whale":
            if pet in team1:
                if pet.pos > 0:
                    pet.swallowed = copy.copy(team1[pet.pos - 1])
                    pet.swallowed.swallowed = None
                    pet.swallowed.held = None
                    team1[pet.pos - 1].health = 0
                    (team1, team2) = post_damage_checks(team1, team2)

            elif pet in team2:
                if pet.pos > 0:
                    pet.swallowed = copy.copy(team2[pet.pos - 1])
                    pet.swallowed.swallowed = None
                    pet.swallowed.held = None
                    team2[pet.pos - 1].health = 0
                    (team1, team2) = post_damage_checks(team1, team2)

    return team1, team2


# Runs each function that needs to be checked after any damage
def post_damage_checks(team1, team2):
    (team1, team2, team1_fainted, team2_fainted) = faint_check(team1, team2)
    (team1, team2) = hurt(team1, team2)
    (team1, team2) = faint(team1, team2, team1_fainted, team2_fainted)

    return team1, team2


# Checks for any fainted pet and removes them from the team
def faint_check(team1, team2):
    team1_copy = team1.copy()
    team2_copy = team2.copy()

    team1_fainted = []
    team2_fainted = []

    for pet in team1_copy:
        if pet.health <= 0:
            fainted_pet = copy.deepcopy(pet)
            (team1, team2, team1_fainted) = before_faint(team1, team2, pet, team1_fainted)
            if pet in team1:
                team1.remove(pet)
                team1_fainted.append(fainted_pet)

    for pet in team2_copy:
        if pet.health <= 0:
            fainted_pet = copy.deepcopy(pet)
            (team1, team2, team2_fainted) = before_faint(team1, team2, pet, team2_fainted)
            if pet in team2:
                team2.remove(pet)
                team2_fainted.append(fainted_pet)

    return team1, team2, team1_fainted, team2_fainted


# Hurt Abilities
def hurt(team1, team2):
    team1_ability_copy = team1.copy()
    team2_ability_copy = team2.copy()

    # Sorts teams by ability order (Highest attack first)
    ability_order = team1_ability_copy + team2_ability_copy
    ability_order.sort(key=get_pos, reverse=True)
    ability_order.sort(key=get_atk, reverse=True)

    for pet in ability_order:

        # Not fainted
        if pet.health > 0:
            # Has taken damage
            if pet.health < pet.hurt:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                if pet in team1:
                    (ability_repeat, tiger_level) = tiger(pet, team1)
                else:
                    (ability_repeat, tiger_level) = tiger(pet, team2)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = pet.level
                    else:
                        level = tiger_level

                    # Peacock Ability - Hurt → Gain +4/+8/+12 attack.
                    if pet.name == "peacock":
                        pet.attack = pet.attack + (4 * level)
                        pet.hurt = pet.health

                    # Gorilla Ability - Hurt → Gain Coconut 1/2/3 time(s) per battle.
                    elif pet.name == "gorilla":
                        if pet.triggers > 0:
                            pet.held = "coconut"
                            if trigger == 0:
                                pet.triggers = pet.triggers - 1
                            pet.hurt = pet.health
                    else:

                        # Blowfish Ability - Hurt → Deal 2/4/6 damage to one random enemy.
                        if pet.name == "blowfish":
                            if pet in team1:
                                if len(team2) > 0:
                                    attack_target = random.choice(team2)
                                    attack_target = damage(attack_target, (2 * level))
                                    pet.hurt = pet.health
                                    (team1, team2) = post_damage_checks(team1, team2)

                            else:
                                if len(team1) > 0:
                                    attack_target = random.choice(team1)
                                    attack_target = damage(attack_target, (2 * level))
                                    pet.hurt = pet.health
                                    (team1, team2) = post_damage_checks(team1, team2)

                        # Camel ability - Hurt → Give the nearest friend behind +2/+4/+6 attack and +2/+4/+6 health.
                        if pet.name == "camel":
                            if pet in team1:
                                for friendly_pet in team1:
                                    if friendly_pet.pos == pet.pos + 1:
                                        friendly_pet.health = friendly_pet.health + (2 * level)
                                        friendly_pet.attack = friendly_pet.attack + (2 * level)
                            else:
                                for friendly_pet in team2:
                                    if friendly_pet.pos == pet.pos + 1:
                                        friendly_pet.health = friendly_pet.health + (2 * level)
                                        friendly_pet.attack = friendly_pet.attack + (2 * level)

    return team1, team2


# Before Faint Abilities
def before_faint(team1, team2, pet, fainted):
    # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
    if pet in team1:
        (ability_repeat, tiger_level) = tiger(pet, team1)
    else:
        (ability_repeat, tiger_level) = tiger(pet, team2)

    # Repeats abiltiy if pet behind is a tiger
    for trigger in range(0, ability_repeat):
        if trigger == 0:
            level = pet.level
        else:
            level = tiger_level

        # Badger Ability - Before faint → Deal 50%/100%/150% attack damage to adjacent pets.
        if pet.name == "badger":
            if pet in team1:
                if pet.pos == 0 and len(team1) <= 1:  # Back
                    if len(team2) > 0:
                        team2[0] = damage(team2[0], int((pet.attack / 2) * level))
                elif pet.pos == 0 and len(team1) > 1:  # Front
                    if len(team2) > 0:
                        team2[0] = damage(team2[0], int((pet.attack / 2) * level))
                    team1[1] = damage(team1[1], int((pet.attack / 2) * level))
                elif len(team1) != 0:
                    team1[pet.pos - 1] = damage(team1[pet.pos - 1], int((pet.attack / 2) * level))
                    team1[pet.pos + 1] = damage(team1[pet.pos + 1], int((pet.attack / 2) * level))
                if trigger == 0:
                    team1.remove(pet)
                    fainted.append(pet)

            else:
                if pet.pos == 0 and len(team2) <= 1:  # Back
                    if len(team1) > 0:
                        team1[0] = damage(team1[0], int((pet.attack / 2) * level))
                elif pet.pos == 0 and len(team2) > 1:  # Front
                    if len(team1) > 0:
                        team1[0] = damage(team1[0], int((pet.attack / 2) * level))
                    team2[1] = damage(team2[1], int((pet.attack / 2) * level))
                elif len(team2) != 0:
                    team2[pet.pos - 1] = damage(team2[pet.pos - 1], int((pet.attack / 2) * level))
                    team2[pet.pos + 1] = damage(team2[pet.pos + 1], int((pet.attack / 2) * level))
                if trigger == 0:
                    team2.remove(pet)
                    fainted.append(pet)
            (team1, team2) = post_damage_checks(team1, team2)

        # Turtle ability - 	Before faint → Give the nearest 1/2/3 friend(s) behind Melon.
        if pet.name == "turtle":
            if pet in team1:
                turtle_counter = 1
                for melon_target in team1:
                    if (melon_target.pos == pet.pos + turtle_counter) and (turtle_counter <= level):
                        melon_target.held = "melon"
                        turtle_counter += 1
                team1.remove(pet)
                fainted.append(pet)

            else:
                turtle_counter = 1
                for melon_target in team2:
                    if (melon_target.pos == pet.pos + turtle_counter) and (turtle_counter <= level):
                        melon_target.held = "melon"
                        turtle_counter += 1
                team2.remove(pet)
                fainted.append(pet)

    return team1, team2, fainted


# Faint Abilities
def faint(team1, team2, team1_fainted, team2_fainted):
    # Sorts fainted pets by ability order (Highest attack first)
    faint_order = team1_fainted + team2_fainted
    faint_order.sort(key=get_pos, reverse=True)
    faint_order.sort(key=get_atk, reverse=True)

    team1_summons = []
    team2_summons = []

    for pet in faint_order:

        # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
        if pet in team1_fainted:
            (ability_repeat, tiger_level) = tiger(pet, team1)

            # Repeats ability if pet behind is a tiger
            for trigger in range(0, ability_repeat):
                if trigger == 0:
                    level = pet.level
                else:
                    level = tiger_level

                # Ant ability - Faint → Give one random friend +2/+4/+6 attack and +1/+2/+3 health.
                if pet.name == "ant":
                    if len(team1) > 0:
                        buff_target = random.choice(team1)
                        buff_target.attack = buff_target.attack + (2 * level)
                        buff_target.health = buff_target.health + (1 * level)

                # Flamingo Ability - Before faint → Give the two nearest friends behind +1/+2/+3 attack and +1/+2/+3 health.
                if pet.name == "flamingo":
                    buff_targets = []
                    for buff_target in team1:
                        if (buff_target.pos == pet.pos + 1) or (buff_target.pos == pet.pos + 2):
                            buff_targets.append(buff_target)
                    for buff_target in buff_targets:
                        buff_target.attack = buff_target.attack + (1 * level)
                        buff_target.health = buff_target.health + (1 * level)

                # Mammoth ability - Faint → Give all friends +2/+4/+6 attack and +2/+4/+6 health.
                if pet.name == "mammoth":
                    for other_pet in team1:
                        other_pet.health = other_pet.health + (2 * level)
                        other_pet.attack = other_pet.attack + (2 * level)

                # Hedgehog ability - Faint → Deal 2/4/6 damage to all.
                if pet.name == "hedgehog":
                    for target in team1:
                        target = damage(target, (2 * level))
                    for target in team2:
                        target = damage(target, (2 * level))
                    (team1, team2) = post_damage_checks(team1, team2)

                # Cricket ability - Faint → Summon one 1/1 / 2/2 / 3/3 Zombie Cricket.
                if pet.name == "cricket":
                    if len(team1) < 5:
                        summon = classes.Pet("zombie_cricket", 1 * pet.level, 1 * level, level,
                                     (level / 3) + 1, pet.pos, None)
                        team1 = [summon] + team1
                        team1_summons = [summon] + team1_summons
                        team1 = sort_team(team1)

                # Deer ability - Faint → Summon one 5/5 / 10/10 / 15/15 Bus with Chilli
                if pet.name == "deer":
                    if len(team1) < 5:
                        summon = classes.Pet("bus", 5 * level, 5 * level, level,
                                     (level / 3) + 1, pet.pos, "chilli")
                        team1 = [summon] + team1
                        team1_summons = [summon] + team1_summons
                        team1 = sort_team(team1)

                # Sheep ability - Faint → Summon two 2/2 / 4/4 / 6/6 Rams.
                if pet.name == "sheep":
                    for ability_trigger in range(0, 2):
                        if len(team1) < 5:
                            summon = classes.Pet("ram", 2 * level, 2 * level, level,
                                         (level / 3) + 1, pet.pos, None)
                            team1 = [summon] + team1
                            team1_summons = [summon] + team1_summons
                            team1 = sort_team(team1)

                # Rooster ability - Faint → Summon 1/2/3 Chick(s) with 1 health and 50% attack of this.
                if pet.name == "rooster":
                    for ability_trigger in range(0, level):
                        if len(team1) < 5:
                            if pet.attack < 2:
                                summon = classes.Pet("chick", 1, 1, level,
                                             (level / 3) + 1, pet.pos, None)
                            else:
                                summon = classes.Pet("chick", int(pet.attack / 2), 1, level,
                                             (level / 3) + 1, pet.pos, None)
                            team1 = [summon] + team1
                            team1_summons = [summon] + team1_summons
                            team1 = sort_team(team1)

                # Spider ability - Faint → Summon one level 1 tier 3 pet as a 2/2 / 4/4 / 6/6.
                if pet.name == "spider":
                    if len(team1) < 5:
                        tier_3 = ["blowfish", "camel", "dog", "dolphin", "giraffe", "kangaroo", "ox", "rabbit", "sheep",
                                  "snail"]
                        summon = classes.Pet(random.choice(tier_3), 2, 2, level,
                                     (level / 3) + 1, pet.pos, None)
                        team1 = [summon] + team1
                        team1_summons = [summon] + team1_summons
                        team1 = sort_team(team1)

                # Rat ability - Faint → Summon 1/2/3 1/1 Dirty Rat(s) up front for the opponent.
                if pet.name == "rat":
                    for ability_trigger in range(0, min(level, 5 - len(team2))):
                        for team2_pet in team2:
                            team2_pet.pos = team2_pet.pos + 1
                        summon = classes.Pet("dirty_rat", 1, 1, level,
                                     (level / 3) + 1, 0, None)
                        team2 = [summon] + team2
                        team2_summons = [summon] + team2_summons
                        team2 = sort_team(team2)

            # Whale Ability - Start of turn → Swallow the nearest friend ahead and release it as a level 1/2/3 after fainting.
            if pet.name == "whale":
                if len(team1) < 5:
                    summon = pet.swallowed
                    if summon.name == "scorpion":
                        summon.held = "peanuts"
                    team1 = [summon] + team1
                    team1_summons + [summon] + team1_summons

            # Friend Faints abilities
            team1_ability_order = team1.copy()
            team1_ability_order.sort(key=get_pos, reverse=True)
            team1_ability_order.sort(key=get_atk, reverse=True)

            for other_pet in team1_ability_order:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(other_pet, team1)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = other_pet.level
                    else:
                        level = tiger_level

                    # Shark ability - Friend faints → Gain +1/+2/+3 attack and +2/+4/+6 health. Double out of battle.
                    if other_pet.name == "shark":
                        other_pet.attack = other_pet.attack + level
                        other_pet.health = other_pet.health + (2 * level)

                    # Fly ability - Friend faints → Summon one 4/4 / 8/8 / 12/12 Zombie Fly in its place. Works 3 times per turn.
                    if other_pet.name == "fly":
                        if pet.name != "zombie_fly":
                            if len(team1) < 5:
                                if other_pet.triggers > 0:
                                    summon = classes.Pet("zombie_fly", 4 * level, 4 * level,
                                                 level,
                                                 (level / 3) + 1, pet.pos, None)
                                    team1 = [summon] + team1
                                    team1_summons = [summon] + team1_summons
                                    team1 = sort_team(team1)
                                    if trigger == 0:
                                        other_pet.triggers = other_pet.triggers - 1

                    # Ox ability - Friend ahead faints → Gain Melon and +1/+2/+3 attack.
                    if other_pet.name == "ox":
                        if pet.pos == other_pet.pos - 1:
                            other_pet.attack = other_pet.attack + level
                            other_pet.held = "melon"

            # Mushroom - Come back as a 1/1 after fainting.
            if pet.held == "mushroom":
                if len(team1) < 5:
                    summon = classes.Pet(pet.name, 1, 1, level,
                                 (level / 3) + 1, pet.pos, None)
                    if summon.name == 'scorpion':
                        summon.held = "peanuts"
                    team1 = [summon] + team1
                    team1_summons = [summon] + team1_summons
                    team1 = sort_team(team1)

            # Honey - Summon a 1/1 Honey Bee after fainting.
            elif pet.held == "honey":
                if len(team1) < 5:
                    summon = classes.Pet("bee", 1, 1, level,
                                 (level / 3) + 1, pet.pos, None)
                    team1 = [summon] + team1
                    team1_summons = [summon] + team1_summons
                    team1 = sort_team(team1)

        elif pet in team2_fainted:

            # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
            (ability_repeat, tiger_level) = tiger(pet, team2)

            # Repeats ability if pet behind is a tiger
            for trigger in range(0, ability_repeat):
                if trigger == 0:
                    level = pet.level
                else:
                    level = tiger_level

                # Ant ability - Faint → Give one random friend +2/+4/+6 attack and +1/+2/+3 health.
                if pet.name == "ant":
                    if len(team2) > 0:
                        buff_target = random.choice(team2)
                        buff_target.attack = buff_target.attack + (2 * level)
                        buff_target.health = buff_target.health + (1 * level)

                # Flamingo Ability - Before faint → Give the two nearest friends behind +1/+2/+3 attack and +1/+2/+3 health.
                if pet.name == "flamingo":
                    buff_targets = []
                    for buff_target in team2:
                        if (buff_target.pos == pet.pos + 1) or (buff_target.pos == pet.pos + 2):
                            buff_targets.append(buff_target)
                    for buff_target in buff_targets:
                        buff_target.attack = buff_target.attack + (1 * level)
                        buff_target.health = buff_target.health + (1 * level)

                # Mammoth ability - Faint → Give all friends +2/+4/+6 attack and +2/+4/+6 health.
                if pet.name == "mammoth":
                    for other_pet in team2:
                        other_pet.health = other_pet.health + (2 * level)
                        other_pet.attack = other_pet.attack + (2 * level)

                # Hedgehog ability - Faint → Deal 2/4/6 damage to all.
                if pet.name == "hedgehog":
                    for target in team2:
                        target = damage(target, (2 * level))
                    for target in team2:
                        target = damage(target, (2 * level))
                    (team1, team2) = post_damage_checks(team1, team2)

                # Cricket ability - Faint → Summon one 1/1 / 2/2 / 3/3 Zombie Cricket.
                if pet.name == "cricket":
                    if len(team2) < 5:
                        summon = classes.Pet("zombie_cricket", 1 * level, 1 * level, level,
                                     (level / 3) + 1, pet.pos, None)
                        team2 = [summon] + team2
                        team2_summons = [summon] + team2_summons
                        team2 = sort_team(team2)

                # Deer ability - Faint → Summon one 5/5 / 10/10 / 15/15 Bus with Chilli
                if pet.name == "deer":
                    if len(team2) < 5:
                        summon = classes.Pet("bus", 5 * level, 5 * level, level,
                                     (level / 3) + 1, pet.pos, "chilli")
                        team2 = [summon] + team2
                        team2_summons = [summon] + team2_summons
                        team2 = sort_team(team2)

                # Sheep ability - Faint → Summon two 2/2 / 4/4 / 6/6 Rams.
                if pet.name == "sheep":
                    for ability_trigger in range(0, 2):
                        if len(team2) < 5:
                            summon = classes.Pet("ram", 2 * level, 2 * level, level,
                                         (level / 3) + 1, pet.pos, None)
                            team2 = [summon] + team2
                            team2_summons = [summon] + team2_summons
                            team2 = sort_team(team2)

                # Rooster ability - Faint → Summon 1/2/3 Chick(s) with 1 health and 50% attack of this.
                if pet.name == "rooster":
                    for ability_trigger in range(0, level):
                        if len(team2) < 5:
                            if pet.attack < 2:
                                summon = classes.Pet("chick", 1, 1, level,
                                             (level / 3) + 1, pet.pos, None)
                            else:
                                summon = classes.Pet("chick", int(pet.attack / 2), 1, level,
                                             (level / 3) + 1, pet.pos, None)
                            team2 = [summon] + team2
                            team2_summons = [summon] + team2_summons
                            team2 = sort_team(team2)

                # Spider ability - Faint → Summon one level 1 tier 3 pet as a 2/2 / 4/4 / 6/6.
                if pet.name == "spider":
                    if len(team2) < 5:
                        tier_3 = ["blowfish", "camel", "dog", "dolphin", "giraffe", "kangaroo", "ox", "rabbit", "sheep",
                                  "snail"]
                        summon = classes.Pet(random.choice(tier_3), 2, 2, level,
                                     (level / 3) + 1, pet.pos, None)
                        team2 = [summon] + team2
                        team2_summons = [summon] + team2_summons
                        team2 = sort_team(team2)

                # Rat ability - Faint → Summon 1/2/3 1/1 Dirty Rat(s) up front for the opponent.
                if pet.name == "rat":
                    for ability_trigger in range(0, min(level, 5 - len(team2))):
                        for team2_pet in team1:
                            team2_pet.pos = team2_pet.pos + 1
                        summon = classes.Pet("dirty_rat", 1, 1, level,
                                     (level / 3) + 1, 0, None)
                        team1 = [summon] + team1
                        team1_summons = [summon] + team1_summons
                        team1 = sort_team(team1)

            # Whale Ability - Start of turn → Swallow the nearest friend ahead and release it as a level 1/2/3 after fainting.
            if pet.name == "whale":
                if len(team2) < 5:
                    summon = pet.swallowed
                    if summon.name == "scorpion":
                        summon.held = "peanuts"
                    team2 = [summon] + team2
                    team2_summons + [summon] + team2_summons

            # Friend Faints
            team2_ability_order = team2.copy()
            team2_ability_order.sort(key=get_pos, reverse=True)
            team2_ability_order.sort(key=get_atk, reverse=True)

            # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
            for other_pet in team2_ability_order:
                (ability_repeat, tiger_level) = tiger(other_pet, team2)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = other_pet.level
                    else:
                        level = tiger_level

                    # Shark ability - Friend faints → Gain +1/+2/+3 attack and +2/+4/+6 health. Double out of battle.
                    if other_pet.name == "shark":
                        other_pet.attack = other_pet.attack + level
                        other_pet.health = other_pet.health + (2 * level)

                    # Fly ability - Friend faints → Summon one 4/4 / 8/8 / 12/12 Zombie Fly in its place. Works 3 times per turn.
                    if other_pet.name == "fly":
                        if pet.name != "zombie_fly":
                            if len(team2) < 5:
                                if other_pet.triggers > 0:
                                    summon = classes.Pet("zombie_fly", 4 * level, 4 * level,
                                                 level,
                                                 (level / 3) + 1, pet.pos, None)
                                    team2 = [summon] + team2
                                    team2_summons = [summon] + team2_summons
                                    team2 = sort_team(team2)
                                    if trigger == 0:
                                        other_pet.triggers = other_pet.triggers - 1

                    # Ox ability - Friend ahead faints → Gain Melon and +1/+2/+3 attack.
                    if other_pet.name == "ox":
                        if pet.pos == other_pet.pos - 1:
                            other_pet.attack = other_pet.attack + level
                            other_pet.held = "melon"

            # Mushroom - Come back as a 1/1 after fainting.
            if pet.held == "mushroom":
                if len(team2) < 5:
                    summon = classes.Pet(pet.name, 1, 1, pet.level,
                                 (pet.level / 3) + 1, pet.pos, None)
                    if summon.name == 'scorpion':
                        summon.held = "peanuts"
                    team2 = [summon] + team2
                    team2_summons = [summon] + team2_summons
                    team2 = sort_team(team2)

            # Honey - Summon a 1/1 Honey Bee after fainting.
            elif pet.held == "honey":
                if len(team2) < 5:
                    summon = classes.Pet("bee", 1, 1, pet.level,
                                 (pet.level / 3) + 1, pet.pos, None)
                    team2 = [summon] + team2
                    team2_summons = [summon] + team2_summons
                    team2 = sort_team(team2)

    # Friend Summoned abilities
    ability_order = team1.copy() + team2.copy()
    ability_order.sort(key=get_pos, reverse=True)
    ability_order.sort(key=get_atk, reverse=True)

    for other_pet in ability_order:
        if other_pet not in team1_summons and other_pet not in team2_summons:

            # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
            if other_pet in team1:
                (ability_repeat, tiger_level) = tiger(other_pet, team1)

                # Repeats abiltiy if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = other_pet.level
                    else:
                        level = tiger_level

                    # Horse ability - Friend summoned → Give it +1/+2/+3 attack until end of battle
                    if other_pet.name == "horse":
                        for summoned_pet in team1_summons:
                            summoned_pet.attack = summoned_pet.attack + 1 * level

                    # Dog ability - Friend summoned → Gain +1/+2/+3 attack or +1/+2/+3 health until end of battle
                    elif other_pet.name == "dog":
                        for summoned_pet in team1_summons:
                            if (random.randint(0, 1)) == 0:
                                other_pet.attack = other_pet.attack + level
                            else:
                                other_pet.health = other_pet.health + level

                    # Turkey ability - Friend summoned → Give it +3 /+6/+9 attack and +3/+6/+9 health
                    elif other_pet.name == "turkey":
                        for summoned_pet in team1_summons:
                            summoned_pet.attack = summoned_pet.attack + (3 * level)
                            summoned_pet.health = summoned_pet.health + (3 * level)
            else:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(other_pet, team2)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = other_pet.level
                    else:
                        level = tiger_level

                    # Horse ability - Friend summoned → Give it +1/+2/+3 attack until end of battle
                    if other_pet.name == "horse":
                        for summoned_pet in team2_summons:
                            summoned_pet.attack = summoned_pet.attack + 1 * level

                    # Dog ability - Friend summoned → Gain +1/+2/+3 attack or +1/+2/+3 health until end of battle
                    elif other_pet.name == "dog":
                        for summoned_pet in team2_summons:
                            if (random.randint(0, 1)) == 0:
                                other_pet.attack = other_pet.attack + level
                            else:
                                other_pet.health = other_pet.health + level

                    # Turkey ability - Friend summoned → Give it +3 /+6/+9 attack and +3/+6/+9 health
                    elif other_pet.name == "turkey":
                        for summoned_pet in team2_summons:
                            summoned_pet.attack = summoned_pet.attack + (3 * level)
                            summoned_pet.health = summoned_pet.health + (3 * level)

    return team1, team2


# Before attack abilities
def before_attack(team1, team2):

    # Reassigns the front pet, next to attack
    if len(team1) > 0:
        team1_attack = team1[0]
    else:
        team1_attack = None

    if len(team2) > 0:
        team2_attack = team2[0]
    else:
        team2_attack = None

    # Elephant ability - Before attack → Deal 1 damage to the nearest friend behind. Triggers 1/2/3 time(s)
    if team1_attack.name == "elephant":
        (ability_repeat, tiger_level) = tiger(team1_attack, team1)
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team1_attack.level
            else:
                level = tiger_level
            if team1_attack.pos != (len(team1) - 1):
                for ability_trigger in range(0, level):
                    team1[team1_attack.pos + 1] = damage(team1[team1_attack.pos + 1], 1)
                    (team1, team2) = post_damage_checks(team1, team2)
    if team2_attack.name == "elephant":
        (ability_repeat, tiger_level) = tiger(team2_attack, team1)
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team2_attack.level
            else:
                level = tiger_level
            if team2_attack.pos != (len(team2) - 1):
                for abiltiy_trigger in range(0, level):
                    team2[team2_attack.pos + 1] = damage(team2[team2_attack.pos + 1], 1)
                    (team1, team2) = post_damage_checks(team1, team2)

    # Boar ability - Before attack → Gain +4/+8/+12 attack and +2/+4/+6 health.
    if team1_attack.name == "boar":
        (ability_repeat, tiger_level) = tiger(team1_attack, team1)
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team1_attack.level
            else:
                level = tiger_level
            team1_attack.attack = team1_attack.attack + (4 * level)
            team1_attack.health = team1_attack.health + (2 * level)

    if team2_attack.name == "boar":
        (ability_repeat, tiger_level) = tiger(team2_attack, team1)
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team2_attack.level
            else:
                level = tiger_level
            team2_attack.attack = team2_attack.attack + (4 * level)
            team2_attack.health = team2_attack.health + (2 * level)

    # Reassigns the front pet, next to attack
    if len(team1) > 0:
        team1_attack = team1[0]
    else:
        team1_attack = None

    if len(team2) > 0:
        team2_attack = team2[0]
    else:
        team2_attack = None

    return team1, team2, team1_attack, team2_attack


# Simulates attack between two front pets
def attack(team1, team2, team1_attack, team2_attack):

    # Meat Bone - Attack with +4 damage
    if team2_attack.held == "meat":
        team1_attack = damage(team1_attack, team2_attack.attack + 4)

    # Steak - Attack with +20 damage, once
    elif team2_attack.held == "steak":
        team1_attack = damage(team1_attack, team2_attack.attack + 20)
        team2_attack.held = None

    # Peanuts - Knockout any pet attacked and hurt by this.
    elif team2_attack.held == "peanuts":
        if team1_attack.held == "melon":
            if team2_attack.attack > 20:
                team1_attack = damage(team1_attack, 70)
            else:
                team1_attack = damage(team1_attack, team2_attack.attack)
        else:
            team1_attack = damage(team1_attack, 70)
    else:
        team1_attack = damage(team1_attack, team2_attack.attack)

    # Chilli - Attack second enemy for 5 damage.
    if team1_attack.held == "chilli":
        if len(team2) > 1:
            team2[1] = damage(team2[1], 5)

    # Meat Bone - Attack with +4 damage
    if team1_attack.held == "meat":
        team2_attack = damage(team2_attack, team1_attack.attack + 4)

    # Steak - Attack with +20 damage, once
    elif team1_attack.held == "steak":
        team2_attack = damage(team2_attack, team1_attack.attack + 20)
        team1_attack.held = None

    # Peanuts - Knockout any pet attacked and hurt by this.
    elif team1_attack.held == "peanuts":
        if team2_attack.held == "melon":
            if team1_attack.attack > 20:
                team2_attack = damage(team2_attack, 70)
            else:
                team2_attack = damage(team2_attack, team1_attack.attack)
        else:
            team2_attack = damage(team2_attack, 70)
    else:
        team2_attack = damage(team2_attack, team1_attack.attack)

    # Chilli - Attack second enemy for 5 damage.
    if team2_attack.held == "chilli":
        if len(team1) > 1:
            team1[1] = damage(team1[1], 5)

    # Knockout abilities
    (team1, team2) = knockout(team1, team2, team1_attack, team2_attack)

    # Friend ahead attacks abilities
    friend_ahead_attacks_list = []
    ability_order = team1.copy() + team2.copy()
    ability_order.sort(key=get_pos, reverse=True)
    ability_order.sort(key=get_atk, reverse=True)
    for other_pet in ability_order:
        if other_pet.pos == 1:
            if other_pet.name == "kangaroo" or other_pet.name == "snake":
                friend_ahead_attacks_list.append(other_pet)

    (team1, team2) = post_damage_checks(team1, team2)

    for pet in friend_ahead_attacks_list:

        # Kangaroo ability - Friend ahead attacks → Gain +2/+4/+6 attack and +2/+4/+6 health.
        if pet.name == "kangaroo":
            if pet in team1:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(pet, team1)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = pet.level
                    else:
                        level = tiger_level

                    pet.attack = pet.attack + (2 * level)
                    pet.health = pet.health + (2 * level)

            elif pet in team2:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(pet, team2)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = pet.level
                    else:
                        level = tiger_level

                    pet.attack = pet.attack + (2 * level)
                    pet.health = pet.health + (2 * level)

        # Snake ability - Friend ahead attacks → Deal 5/10/15 damage damage to one random enemy.
        if pet.name == "snake":
            if pet in team1:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(pet, team1)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = pet.level
                    else:
                        level = tiger_level

                    choice = random.choice(team2)
                    choice = damage(choice, (5 * level))

                    (team1, team2) = post_damage_checks(team1, team2)
            elif pet in team2:

                # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
                (ability_repeat, tiger_level) = tiger(pet, team2)

                # Repeats ability if pet behind is a tiger
                for trigger in range(0, ability_repeat):
                    if trigger == 0:
                        level = pet.level
                    else:
                        level = tiger_level

                    choice = random.choice(team1)
                    choice = damage(choice, (5 * level))

                    (team1, team2) = post_damage_checks(team1, team2)

    return team1, team2, team1_attack, team2_attack


# Knockout abilities
def knockout(team1, team2, team1_attack, team2_attack):
    team1_copy = team1.copy()
    team2_copy = team2.copy()

    team1_fainted = []
    team2_fainted = []

    for pet in team1_copy:
        if pet.health <= 0:
            fainted_pet = copy.deepcopy(pet)
            team1_fainted.append(fainted_pet)

    for pet in team2_copy:
        if pet.health <= 0:
            fainted_pet = copy.deepcopy(pet)
            team2_fainted.append(fainted_pet)

    # Hippo ability - Knock out → Gain +3/+6/+9 attack and +3/+6/+9 health
    if team1_attack.name == "hippo" and team1_attack not in team1_fainted:

        # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
        (ability_repeat, tiger_level) = tiger(team1_attack, team1)

        # Repeats ability if pet behind is a tiger
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team1_attack.level
            else:
                level = tiger_level

            for ability_trigger in team2_fainted:
                team1_attack.attack = team1_attack.attack + (3 * level)
                team1_attack.health = team1_attack.health + (3 * level)

    # Hippo ability - Knock out → Gain +3/+6/+9 attack and +3/+6/+9 health
    if team2_attack.name == "hippo" and team2_attack not in team2_fainted:

        # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
        (ability_repeat, tiger_level) = tiger(team2_attack, team2)

        # Repeats ability if pet behind is a tiger
        for trigger in range(0, ability_repeat):
            if trigger == 0:
                level = team2_attack.level
            else:
                level = tiger_level

            for ability_trigger in team1_fainted:
                team2_attack.attack = team2_attack.attack + (3 * level)
                team2_attack.health = team2_attack.health + (3 * level)

    # Rhino ability - Knock out → Deal 4/8/12 damage to the first enemy. Double against tier 1 pets.
    if team1_attack.name == "rhino" and team1_attack not in team1_fainted:

        # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
        (ability_repeat, tiger_level) = tiger(team1_attack, team1)
        team1_rhino = 0
        while team1_rhino != len(team2_fainted):

            # Repeats ability if pet behind is a tiger
            for trigger in range(0, (len(team2_fainted) - team1_rhino) * ability_repeat):
                if trigger < (len(team2_fainted) - team1_rhino):
                    level = team1_attack.level
                else:
                    level = tiger_level

                for pet in team2:
                    if pet.health > 0:
                        pet = damage(pet, (4 * level))
                        (team1, team2) = post_damage_checks(team1, team2)
                        break

            team1_rhino = len(team2_fainted)
            team2_fainted = []
            for pet in team2_copy:
                if pet.health <= 0:
                    fainted_pet = copy.deepcopy(pet)
                    team2_fainted.append(fainted_pet)

    # Rhino ability - Knock out → Deal 4/8/12 damage to the first enemy. Double against tier 1 pets.
    if team2_attack.name == "rhino" and team2_attack not in team2_fainted:

        # Tiger ability - The friend ahead repeats their ability in battle as if they were level 1/2/3.
        (ability_repeat, tiger_level) = tiger(team2_attack, team2)
        team2_rhino = 0
        while team2_rhino != len(team1_fainted):

            # Repeats ability if pet behind is a tiger
            for trigger in range(0, (len(team1_fainted) - team2_rhino) * ability_repeat):
                if trigger < (len(team1_fainted) - team2_rhino):
                    level = team2_attack.level
                else:
                    level = tiger_level
                for pet in team1:
                    if pet.health > 0:
                        pet = damage(pet, (4 * level))
                        break

            team2_rhino = len(team1_fainted)
            team1_fainted = []
            for pet in team1_copy:
                if pet.health <= 0:
                    fainted_pet = copy.deepcopy(pet)
                    team1_fainted.append(fainted_pet)

        (team1, team2) = post_damage_checks(team1, team2)

    return team1, team2


# Re-sort team based on position (classes.Pet.pos) attribute
def sort_team(team):
    team.sort(key=get_pos)
    i = 0
    for pet in team:
        pet.pos = i
        i += 1
    return team


# Calculates and updates damage
def damage(pet, dmg):
    # Coconut - Ignore damage once
    if pet.held == "coconut":
        pet.held = None

    # Melon - Take 20 less damage, once
    elif pet.held == "melon":
        pet.held = None
        if dmg > 20:
            pet.health = pet.health - (dmg - 20)

    # Garlic - Take 2 less damage
    elif pet.held == "garlic":
        pet.health = pet.health - max(1, (dmg - 2))
    else:
        pet.health = pet.health - dmg

    return pet


# Checks if pet behind is tiger, and returns number of ability triggers and level of tiger
def tiger(pet, team):
    if pet.pos < len(team) - 1 and (len(team) > 1):
        if team[pet.pos + 1].name == "tiger":
            return 2, team[pet.pos + 1].level
    if pet.pos < len(team):
        if team[pet.pos].name == "tiger" and pet.name != "tiger":
            return 2, team[pet.pos].level

    return 1, None

# ----------------------------------------------------------------------------------------------------------------------


# Simulates changes to team from action
def simulate_action(action, team, shop):
    # shop = [[pets], [food], gold]

    temp_team = copy.deepcopy(team)
    temp_shop = copy.deepcopy(shop)

    # Buy abilities
    if action[0] == "buy_pet":
        (temp_team, temp_shop) = buy_pet(action, temp_team, temp_shop)

    # Sell abilities
    if action[0] == "sell":
        (temp_team, temp_shop) = sell(action, temp_team, temp_shop)

    # Level abilities
    if action[0] == "level":
        (temp_team, temp_shop) = level(action, temp_team, temp_shop)

    # Buy Food abilities
    if action[0] == "buy_food":
        (team, shop) = buy_food(action, temp_team, temp_shop)

    # Roll
    if action[0] == "roll":
        temp_shop[2] = temp_shop[2] - 1

    return temp_team, temp_shop[0], temp_shop[1], temp_shop[2]


# Buy abilities
def buy_pet(action, team, shop):

    if action[0] == "buy_pet":
        pet = action[1]
        level = 1
    else:
        pet = team[action[2]]
        level = pet.level

    # Otter ability - Buy → Give 1/2/3 random friend(s) +1 attack and +1 health.
    if pet.name == "otter":
        if len(team) > 0:
            friendly_pets = []
            for other_pet in team:
                if other_pet is not pet:
                    friendly_pets.append(other_pet)
            choices = random.sample(friendly_pets, min(len(friendly_pets), level))
            for buff_target in choices:
                buff_target.attack = buff_target.attack + 1
                buff_target.health = buff_target.health + 1

    # Buy pet only mechanics - does not work for level-ups
    if action[0] == "buy_pet":

        shop[2] = shop[2] - 3

        # Horse ability - Friend summoned → Give it +1/+2/+3 attack until end of battle
        for other_pet in team:
            if other_pet.name == "horse" and other_pet != pet:
                pet.attack = pet.attack + other_pet.level

        team.append(classes.Pet(pet.name, pet.attack, pet.health, 1, 0, action[2], None))
        shop[0].pop(action[3])
        team = sort_team(team)

    return team, shop


# Sell abilities
def sell(action, team, shop):

    shop[2] += 1
    pet = action[1]

    # Remove pet from team
    team.pop(action[2])
    team = sort_team(team)

    # Beaver ability - Give two random friends +1/+2/+3 health.
    if pet.name == "beaver":
        choices = random.sample(team, min(len(team), 2))
        for buff_target in choices:
            buff_target.health = buff_target.health + pet.level

    # Pig ability - Gain +1/+2/+3 gold.
    if pet.name == "pig":
        shop[2] = shop[2] + pet.level

    # Duck ability - Give shop pets +1/+2/+3 health.
    if pet.name == "duck":
        for shop_pet in shop[0]:
            shop_pet.health = shop_pet.health + pet.level

    return team, shop


# Level-up abilities
def level(action, team, shop):

    shop[2] = shop[2] - 3
    shop_pet = action[1]
    team_pet = team[action[2]]

    # Level-up mechanics
    if team_pet.exp < 2:
        team_pet.exp += 1
        team_pet.attack += 1
        team_pet.health += 1

    elif team_pet.exp == 2:
        team_pet.level += 1
        team_pet.exp = 0
        team_pet.attack += 1
        team_pet.health += 1

        # Fish ability - Level up → Give all friends +1/+2 attack and +1/+2 health.
        if shop_pet.name == "fish":
            for other_pet in team:
                if other_pet is not team_pet:
                    other_pet.health = other_pet.health + team_pet.level
                    other_pet.attack = other_pet.attack + team_pet.level

    shop[0].pop(action[3])

    # Buy abilities
    (team, shop) = buy_pet(action, team, shop)

    return team, shop


# Buy food abilities
def buy_food(action, team, shop):

    shop[2] = shop[2] - 3
    food = action[1]

    # Apple - Give one pet +1 attack and +1 health
    if food.name == "apple":
        team[action[2]].attack += 1
        team[action[2]].health += 1

    # Honey - Summon a 1/1 Honey Bee after fainting
    elif food.name == "honey":
        team[action[2]].held = "honey"

    shop[1].pop(action[3])

    return team, shop


