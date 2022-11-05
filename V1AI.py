import random
import shop
import leaderboard
import simulation
import print_helpers
import actions
import math
import classes
import action_tree


# Plays randomly
def random_choices(team, turn):

    (pet_shop, food_shop, gold) = shop.start_of_turn_shop(team, turn)

    # Repeats until End of Turn
    while True:

        # Gets all actions
        all_actions = actions.all_actions([pet_shop, food_shop, gold], team)

        # Picks random action
        action = random.choice(all_actions)

        print_helpers.print_action(action)

        # End of Turn
        if action[0] == "end_of_turn":
            score = leaderboard.get_score(team, turn)

            print_helpers.print_team(team)
            print_helpers.print_score(score)

            return team, score

        # Roll
        elif action[0] == "roll":
            (team, pet_shop, food_shop, gold) = simulation.simulate_action(action, team, [pet_shop, food_shop, gold])
            (pet_shop, food_shop) = shop.generate_shop(turn)

            print_helpers.print_shop(pet_shop, food_shop, gold)

        # Buy pet, Buy food, Sell pet, Level-Up
        else:
            (team, pet_shop, food_shop, gold) = simulation.simulate_action(action, team, [pet_shop, food_shop, gold])

            print_helpers.print_team(team)
            print_helpers.print_shop(pet_shop, food_shop, gold)


# Creates a random shop and plays until End of Turn based on highest score of moves before needing to roll
def random_shop_best_score(team, turn):

    (pet_shop, food_shop, gold) = shop.start_of_turn_shop(team, turn)

    # Any action is better than none!
    action_worth_score = -math.inf

    # Repeats until End of Turn
    while True:

        # Creates action tree
        actions_tree = action_tree.tree_creator(classes.Tree(None, None), [pet_shop, food_shop, gold, team, turn])

        # Finds max score of all action paths
        max_score = action_tree.find_max(actions_tree)

        arr = []

        # Completes actions if they make the team better
        if max_score > action_worth_score:
            action_worth_score = max_score

            # Generates the best sequence of actions
            action_tree.max_path(actions_tree, arr, max_score)

            # Simulates each action
            for action in arr:
                print_helpers.print_action(action)

                (team, pet_shop, food_shop, gold) = simulation.simulate_action(action, team, [pet_shop, food_shop, gold])

                print_helpers.print_team(team)

        # Roll
        if gold > 0 and len(arr) == 0:
            (team, pet_shop, food_shop, gold) = simulation.simulate_action(['roll'], team, [pet_shop, food_shop, gold])
            (pet_shop, food_shop) = shop.generate_shop(turn)

        # End of Turn
        elif gold == 0 and len(arr) == 0:

            score = leaderboard.get_score(team, turn)

            print_helpers.print_team(team)
            print_helpers.print_score(score)

            return team, score


# Given a shop, produces the best moves until Roll or End of Turn based on highest scores
def given_shop_best_score(given_shop, team, turn):
    # given_shop = [pet_shop, food_shop, gold]

    pet_shop = given_shop[0]
    food_shop = given_shop[1]
    gold = given_shop[2]

    # Any action is better than none!
    action_worth_score = -math.inf

    # Repeats until End of Turn
    while True:
        # Creates action tree
        actions_tree = action_tree.tree_creator(classes.Tree(None, None), [pet_shop, food_shop, gold, team, turn])
        # Finds max score of all action paths
        max_score = action_tree.find_max(actions_tree)
        arr = []
        # Completes actions if they make the team better
        if max_score > action_worth_score:
            action_worth_score = max_score

            # Generates the best sequence of actions
            action_tree.max_path(actions_tree, arr, max_score)

            # Simulates each action
            for action in arr:
                print_helpers.print_action(action)

                (team, pet_shop, food_shop, gold) = simulation.simulate_action(action, team,
                                                                               [pet_shop, food_shop, gold])

                print_helpers.print_team(team)

        # Roll
        if gold > 0 and len(arr) == 0:
            print_helpers.print_action(["roll"])

            score = leaderboard.get_score(team, turn)

            print_helpers.print_team(team)
            print_helpers.print_score(score)

            return team, score

        # End of Turn
        elif gold == 0 and len(arr) == 0:
            print_helpers.print_action(["end_of_turn"])

            score = leaderboard.get_score(team, turn)

            print_helpers.print_team(team)
            print_helpers.print_score(score)

            return team, score
