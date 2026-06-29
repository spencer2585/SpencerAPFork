from .data.levels import LEVEL_DATA
from rule_builder.rules import *
from .data.skulls import CE_HARD_REQUIRED, CE_HARDER_REQUIRED
from .mcc_options import SkullSanity

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

    tier = world.options.skullsanity.value
    if tier in (SkullSanity.option_hard, SkullSanity.option_harder):
        skull_set = CE_HARD_REQUIRED if tier == SkullSanity.option_hard else CE_HARDER_REQUIRED
        disablers = [f"{skull} Skull" for skull in skull_set]
        for level in LEVEL_DATA:
            if level == world.final_mission:
                continue
            location = world.multiworld.get_location(f"{level} Complete", world.player)
            location.access_rule = lambda state, items=disablers, p=world.player: all(
                state.has(item, p) for item in items
            )