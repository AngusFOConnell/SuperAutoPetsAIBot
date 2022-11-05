def print_action(action):
    print("Action: ", action[0])
    if action[0] in ["buy_pet", "buy_food", "level", "sell"]:
        print("\t", action[1].name, action[2])


def print_team(team):
    print("Team :")
    for pet in team:
        print("\t", pet.name, pet.attack, pet.health, pet.level, pet.held)
    print()


def print_score(score):
    print("Score: ", score)
    print()


def print_pet_shop(pet_shop):
    print("Pet Shop:")
    for pet in pet_shop:
        print("\t", pet.name, pet.attack, pet.health)
    print()


def print_food_shop(food_shop):
    print("Food Shop:")
    for food in food_shop:
        print("\t", food.name)
    print()


def print_gold(gold):
    print("Gold: ", gold)
    print()


def print_shop(pet_shop, food_shop, gold):
    print_pet_shop(pet_shop)
    print_food_shop(food_shop)
    print_gold(gold)


def print_tree(tree):
    print("--------Action Tree--------")
    print(tree)
    print()
