import ast
import classes
import copy


# Calculates score of team and saves to file
def add_to_leaderboard(team):

    team_turn = int(team.split()[0])
    team_data = team.split()[1:]

    # Gets data from files and adds to dictionaries
    leaderboard_dict = leaderboard_file_to_dict()
    scores_dict = scores_file_to_dict()\

    on_file = False

    # Check to see if the team is already in the document (Therefore only need to retrieve score instead of calculating any scores)
    if team_turn in leaderboard_dict.keys():
        if team_data in leaderboard_dict[team_turn]:
            on_file = True

    if on_file is False:

        # Grabs the teams of given turn
        if team_turn in leaderboard_dict.keys():
            teams = copy.deepcopy(leaderboard_dict[team_turn])

            # Loss weight by how many lives one would lose
            if team_turn < 3:
                loss_weight = 1
            elif team_turn < 5:
                loss_weight = 2
            else:
                loss_weight = 3

            count = 0
            team1 = []
            team1_score = 0

            # Transfers string data to list of Pet class
            for data in team_data:
                if count == 0:
                    name = data
                    count += 1
                elif count == 1:
                    attack = data
                    count += 1
                elif count == 2:
                    health = data
                    count += 1
                elif count == 3:
                    level = data
                    count += 1
                elif count == 4:
                    exp = data
                    count += 1
                elif count == 5:
                    pos = data
                    count += 1
                elif count == 6:
                    if data == "None":
                        held = None
                    else:
                        held = data
                    count = 0

                    team1.append(classes.Pet(name, int(health), int(attack), int(level), int(exp), int(pos), held))

            for team in teams:
                team2_data = team

                score_key = tuple([team_turn] + team)
                team2_score = scores_dict[score_key]

                count = 0
                team2 = []

                # Transfers string data to list of Pet classes for all teams on file
                for data in team2_data:
                    if count == 0:
                        name = data
                        count += 1
                    elif count == 1:
                        attack = data
                        count += 1
                    elif count == 2:
                        health = data
                        count += 1
                    elif count == 3:
                        level = data
                        count += 1
                    elif count == 4:
                        exp = data
                        count += 1
                    elif count == 5:
                        pos = data
                        count += 1
                    elif count == 6:
                        if data == "None":
                            held = None
                        else:
                            held = data
                        count = 0

                        team2.append(classes.Pet(name, int(health), int(attack), int(level), int(exp), int(pos), held))

                # Simulates battle between given team and each team on file
                import simulation
                (team1_win, team2_win, draw) = simulation.turn(team1, team2)

                # Calculates score for given team
                team1_score = team1_score + team1_win - team2_win

                # Re-calculates scores for each team on file
                team2_score = team2_score + team2_win - team1_win
                scores_dict[score_key] = team2_score

            # Adds team data to scores dict
            score_key = tuple([team_turn] + team_data)
            scores_dict[score_key] = team1_score

            # Adds team  data to leaderboard dict
            leaderboard_dict[team_turn].append(team_data)

        else:
            leaderboard_dict[team_turn] = [team_data]

            team1_score = 0
            score_key = tuple([team_turn] + team_data)
            scores_dict[score_key] = team1_score

        # Writes the updated teams/scores to file
        with open("leaderboard.txt", "w") as f:
            file_data = list(leaderboard_dict.items())
            f.write(str(file_data))
            f.close()

        with open("scores.txt", "w") as f:
            file_data = list(scores_dict.items())
            file_data = sorted(file_data, key=lambda x: (x[0][0], x[1]))
            f.write(str(file_data))
            f.close()

        return team1_score

    else:
        score_key = tuple([team_turn] + team_data)
        score = scores_dict[score_key]
        return score


# Transfers the data on leaderboard file to dictionary variable of teams
def leaderboard_file_to_dict():
    with open("leaderboard.txt", "r") as f:
        contents = f.read()
        if contents:
            leaderboard_data = ast.literal_eval(contents)
            leaderboard_dict = dict(leaderboard_data)
        else:
            leaderboard_data = []
            leaderboard_dict = dict(leaderboard_data)
        f.close()
    return leaderboard_dict


# Transfers the data on scores file to dictionary variable of scores
def scores_file_to_dict():
    with open("scores.txt", "r") as f:
        contents = f.read()
        if contents:
            scores_data = ast.literal_eval(contents)
            scores_dict = dict(scores_data)
        else:
            scores_data = []
            scores_dict = dict(scores_data)
        f.close()
    return scores_dict


# Formats team into data string and calls leaderboard function
def get_score(team, turn):
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
    return add_to_leaderboard(team_str)
