from rule_builder.rules import *

def set_goal(world):
    world.set_completion_rule(CanReachEntrance(f"Menu -> {world.final_mission}"))