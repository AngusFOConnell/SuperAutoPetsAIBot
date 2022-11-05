import classes
import simulation, leaderboard


def main():
    # team = [classes.Pet(name, attack, health, level, exp, pos, held), ...]
    # battle_simulation([classes.Pet("fish", 2, 2, 1, 0, 0, None)], [classes.Pet("mosquito", 2, 2, 1, 0, 0, None)])

    # add_to_leaderboard(1, [classes.Pet("fish", 2, 2, 1, 0, 0, None), classes.Pet("mosquito", 2, 2, 1, 0, 1, None)]

    # simulate_action(["buy_pet", classes.ShopPet("cricket", 1, 2), 1], [classes.Pet("horse", 2, 1, 1, 0, 0, None)], [classes.ShopPet("cricket", 1, 2), classes.ShopPet("fish", 2, 2), classes.ShopPet("beaver", 3, 2)], [classes.ShopFood("apple")], 10)


# Battle simulation initiation function
def battle_simulation(team1, team2):
    print("Team 1:")
    for pet in team1:
        print("\t", pet.name, pet.attack, pet.health, pet.level, pet.held)
    print()

    print("Team 2:")
    for pet in team2:
        print("\t", pet.name, pet.attack, pet.health, pet.level, pet.held)
        print()

    (team1_win, team2_win, draw) = simulation.turn(team1, team2)

    print("Team 1 Win %: ", team1_win)
    print("Team 2 Win %: ", team2_win)
    print("Draw %: ", draw)


# Adds team to leaderboard and returns score
def add_to_leaderboard(turn, team):
    team_str = ""
    team_str = team_str + str(turn) + " "
    for pet in team:
        team_str = team_str + str(pet.name) + " "
        team_str = team_str + str(pet.attack) + " "
        team_str = team_str + str(pet.health) + " "
        team_str = team_str + str(pet.level) + " "
        team_str = team_str + str(pet.exp) + " "
        team_str = team_str + str(pet.pos) + " "
        team_str = team_str + str(pet.held) + " "

    return leaderboard.add_to_leaderboard(team_str)


def simulate_action(action, team, pet_shop, food_shop, gold):

    (temp_team, temp_shop) = simulation.simulate_action(action, team, [pet_shop, food_shop, gold])

    print("----------Before Action----------")
    print("Team:")
    for pet in team:
        print("\t", pet.name, pet.attack, pet.health, pet.level, pet.held)
    print()

    print("Pet Shop:")
    for pet in pet_shop:
        print("\t", pet.name, pet.attack, pet.health)
    print()

    print("Food Shop:")
    for food in food_shop:
        print("\t", food.name)
    print()

    print("Gold: ", gold)

    print("----------After Action----------")
    print("Team:")
    for pet in temp_team:
        print("\t", pet.name, pet.attack, pet.health, pet.level, pet.held)
    print()

    print("Pet Shop:")
    for pet in temp_shop[0]:
        print("\t", pet.name, pet.attack, pet.health)
    print()

    print("Food Shop:")
    for food in temp_shop[1]:
        print("\t", food.name)
    print()

    print("Gold: ", temp_shop[2])


if __name__ == "__main__":
    main()