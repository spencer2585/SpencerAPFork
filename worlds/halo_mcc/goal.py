

def set_goal(world):
    player= world.player
    world.multiworld.completion_condition[player] = lambda state: state.can_reach("The Maw Complete","Location", player)