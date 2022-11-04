import simulation, classes


def main():
    # team = [classes.Pet(name, attack, health, level, exp, pos, held), ...]
    # battle_simulation([classes.Pet("fish", 2, 2, 1, 0, 0, None)], [classes.Pet("mosquito", 2, 2, 1, 0, 0, None)])


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


if __name__ == "__main__":
    main()