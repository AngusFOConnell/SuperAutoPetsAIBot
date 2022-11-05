import actions
import copy
import simulation
import leaderboard
import classes
import math
import print_helpers


# Creates action tree recursively (Multiple actions)
def tree_creator(tree, data):
    # data = [pet_shop, food_shop, gold, team, turn]

    # Gets all actions possible from shop state
    all_actions = actions.all_actions([data[0], data[1], data[2]], data[3])

    temp_actions = []

    for action in all_actions:
        if action[0] not in ["roll", "end_of_turn"]:
            temp_actions.append(action)

    all_actions = temp_actions

    # For every available action, create a child, and then simulate action and get score from simulated action, then repeat for that state
    if len(all_actions) > 0:
        for action in all_actions:
            temp_team = copy.deepcopy(data[3])
            temp_pet_shop = copy.deepcopy(data[0])
            temp_food_shop = copy.deepcopy(data[1])
            temp_gold = copy.deepcopy(data[2])

            (temp_team, temp_pet_shop, temp_food_shop, temp_gold) = simulation.simulate_action(action, temp_team, [temp_pet_shop, temp_food_shop, temp_gold])

            score = leaderboard.get_score(temp_team, data[4])

            child_tree = tree_creator(classes.Tree(action, score), [temp_pet_shop, temp_food_shop, temp_gold, temp_team, data[4]])
            tree.add_child(child_tree)

    return tree


# Find the largest score in action tree
def find_max(tree):
    if len(tree.children) == 0:
        return tree.score

    score = tree.score
    if score is None:
        max_score = -math.inf
    else:
        max_score = score
    for child in tree.children:
        child_score = find_max(child)
        if child_score > max_score:
            max_score = child_score
    return max_score


# Returns the path of actions to the max score
def max_path(tree, arr, max_score):
    if tree.action is not None:
        arr.append(tree.action)
        if tree.score == max_score:
            return True

    if len(tree.children) == 0:
        return False

    for child in tree.children:
        if max_path(child, arr, max_score):
            return True
        else:
            if len(arr) > 0:
                arr.pop(-1)

    if tree.action is not None:
        if len(arr) > 0:
            arr.pop(-1)
    return False

