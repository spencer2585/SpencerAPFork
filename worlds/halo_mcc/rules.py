from .data.levels import LEVEL_DATA
from rule_builder.rules import *
from .data.skulls import GAME_SKULLS
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


    if world.options.skullsanity.value == SkullSanity.option_all:
        for level, data in LEVEL_DATA.items():
            if level == world.final_mission:
                continue

            if data.game == "CE":
                rule = HasFromListUnique(*world.ceskulls, count = world.options.skulls_required.value)
                location = world.get_location(f"{level} Complete")
                world.set_rule(location, rule)
