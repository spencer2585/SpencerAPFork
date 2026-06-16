from .data.levels import LEVEL_DATA
from rule_builder.rules import *

missions = [
        "The Pillar of Autumn",
        "Halo (CE)",
        "Truth and Reconciliation",
        "The Silent Cartographer",
        "Assault on the Control Room",
        "343 Guilty Spark",
        "The Library",
        "Two Betrayals",
        "Keyes",
        "The Maw",
    ]

def set_rules(world):
    for level, data in LEVEL_DATA.items():
        if level != world.final_mission:
            entrance = world.multiworld.get_entrance(f"Menu -> {level}", world.player)
            required_item = f"{level} Access"
            #entrance.access_rule = lambda state, item=required_item, p=world.player: state.has(item, p)
            world.set_rule(entrance, Has(required_item))
        else:
            entrance = world.multiworld.get_entrance(f"Menu -> {level}", world.player)
            world.set_rule(entrance, HasAll(*[f"{m} Access" for m in world.missions]))