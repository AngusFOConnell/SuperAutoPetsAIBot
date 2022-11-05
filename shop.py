import random
import classes
import simulation


# Generates a random shop at start of turn
def start_of_turn_shop(team, turn):

    gold = 10

    # Start of turn abilities
    (team, gold) = start_of_turn(team, gold)

    # Generate new shop
    (pet_shop, food_shop) = generate_shop(turn)

    return pet_shop, food_shop, gold


# Start of turn abilities
def start_of_turn(team, gold):

    team = simulation.sort_team(team)

    for pet in team:
        if pet.name == "swan":
            gold += pet.level

    return team, gold


# Generates a new shop
def generate_shop(turn):
    tier_1_pets = [("ant", (2, 1)), ("beaver", (3, 2)), ("cricket", (1, 2)), ("duck", (2, 3)), ("fish", (2, 2)),
                   ("mosquito", (2, 2)), ("otter", (1, 2)), ("pig", (4, 1))]
    tier_1_food = ["apple", "honey"]
    tier_2_pets = [("rat", (4, 5)), ("shrimp", (2, 3)), ("hedgehog", (3, 2)), ("flamingo", (4, 2)), ("spider", (2, 2)),
                   ("swan", (1, 3)), ("peacock", (2, 5)), ("dodo", (2, 3)), ("elephant", (3, 5)), ("crab", (3, 1))]
    tier_2_food = ["pill", "cupcake", "meat"]

    # Calculates how many spaces and what can appear in shop relative to turn number
    if turn < 3:
        pet_space = 3
        food_space = 1
        shop_pets = tier_1_pets
        shop_food = tier_1_food

    pet_shop = []
    food_shop = []

    # Pet Shop
    for space in range(0, pet_space):
        pet = random.choice(shop_pets)
        pet_shop.append(classes.ShopPet(pet[0], pet[1][0], pet[1][1]))

    # Food Shop
    for space in range(0, food_space):
        food = random.choice(shop_food)
        food_shop.append(classes.ShopFood(food))

    return pet_shop, food_shop
