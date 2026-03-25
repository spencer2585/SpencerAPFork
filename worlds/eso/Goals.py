from .data.DelveData import DELVE_DATA
from .data.ZoneQuestData import ZONE_QUEST_DATA


def set_goal(world):
    goal = world.options.goal
    player = world.player

    if goal == 0:
        world.multiworld.completion_condition[player] = lambda state: state.can_reach("Main Quest - God of Schemes", "Location", player)

    elif goal == 1:
        final_quest = next(name for name, data in ZONE_QUEST_DATA.items() if data.zone == world.goal_zone and data.is_final)
        world.multiworld.completion_condition[player] = lambda state, q=final_quest: state.can_reach(f"{world.goal_zone} - {q} Zone Quest", "Location", player)

    elif goal == 2:
        world.multiworld.completion_condition[player] = lambda state: all(state.can_reach(f"{DELVE_DATA[delve].zone} - {delve} Delve Complete", "Location", player)for delve in world.selected_delves)