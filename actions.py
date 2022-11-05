# Generates all possible actions from given shop state
def all_actions(shop, team):
    # shop = [[pets], [food], gold]

    actions = []

    pets = shop[0]
    foods = shop[1]
    gold = shop[2]

    if gold > 3:

        # Buy Shop Pet onto team
        if len(team) < 5:
            for pet in pets:
                actions.append(["buy_pet", pet, len(team)])

        # level an existing pet on team from pet in shop
        for shop_pet in pets:
            for team_pet in team:
                if shop_pet.name == team_pet.name and team_pet.level < 3:
                    actions.append(["level", shop_pet, team_pet.pos])

        # Buy food from shop
        for food in foods:
            for pet in team:
                actions.append(["buy_food", food, pet.pos])

    # Sell pet on team
    for pet in team:
        actions.append(["sell", pet, pet.pos])

    # Roll shop
    if gold > 1:
        actions.append(["roll"])

    # End turn
    actions.append(["end_of_turn"])

    return actions


