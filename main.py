import classes
import simulation, leaderboard, print_helpers
import V1AI


def main():
    # team = [classes.Pet(name, attack, health, level, exp, pos, held), ...]
    # battle_simulation([classes.Pet("fish", 2, 2, 1, 0, 0, None)], [classes.Pet("mosquito", 2, 2, 1, 0, 0, None)])

    # add_to_leaderboard(1, [classes.Pet("fish", 2, 2, 1, 0, 0, None), classes.Pet("mosquito", 2, 2, 1, 0, 1, None)]

    # simulate_action(["buy_pet", classes.ShopPet("cricket", 1, 2), 1], [classes.Pet("horse", 2, 1, 1, 0, 0, None)], [classes.ShopPet("cricket", 1, 2), classes.ShopPet("fish", 2, 2), classes.ShopPet("beaver", 3, 2)], [classes.ShopFood("apple")], 10)

    # random_player([], 1)

    # random_shop_best_score([], 1)

    given_shop_best_score([[classes.ShopPet("cricket", 1, 2), classes.ShopPet("cricket", 1, 2), classes.ShopPet("cricket", 1, 2)], [classes.ShopFood("apple")], 10], [classes.Pet("cricket", 2, 3, 1, 0, 0, None), classes.Pet("beaver", 3, 2, 1, 0, 1, None), classes.Pet("otter", 1, 2, 1, 0, 2, None)], 2)


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
    score = leaderboard.get_score(team, turn)

    print_helpers.print_team(team)
    print_helpers.print_score(score)


# Before and After of action
def simulate_action(action, team, pet_shop, food_shop, gold):

    (temp_team, temp_shop) = simulation.simulate_action(action, team, [pet_shop, food_shop, gold])

    print("----------Before Action----------")
    print_helpers.print_team(team)
    print_helpers.print_shop(pet_shop, food_shop, gold)

    print("----------After Action----------")
    print_helpers.print_team(temp_team)
    print_helpers.print_shop(temp_shop[0], temp_shop[1], temp_shop[2])


# Randomly moves
def random_player(team, turn):
    V1AI.random_choices(team, turn)


# Creates a random shop and plays until End of Turn based on highest score of moves before needing to roll
def random_shop_best_score(team, turn):
    V1AI.random_shop_best_score(team, turn)


# Given a shop, produces the best moves until Roll or End of Turn based on highest scores
def given_shop_best_score(given_shop, team, turn):
    V1AI.given_shop_best_score(given_shop, team, turn)


if __name__ == "__main__":
    main()