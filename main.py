import simulation, leaderboard


def main():
    # team = [classes.Pet(name, attack, health, level, exp, pos, held), ...]
    # battle_simulation([classes.Pet("fish", 2, 2, 1, 0, 0, None)], [classes.Pet("mosquito", 2, 2, 1, 0, 0, None)])

    # add_to_leaderboard(1, [classes.Pet("fish", 2, 2, 1, 0, 0, None), classes.Pet("mosquito", 2, 2, 1, 0, 1, None)]

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

if __name__ == "__main__":
    main()