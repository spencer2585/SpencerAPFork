from BaseClasses import MultiWorld
from rule_builder.rules import *
from worlds.Destiny2.Data.destination_data import DESTINATION_DATA


def set_rules(world):
    for destination, data in DESTINATION_DATA.items():
        if not data.social:
            entrance = world.multiworld.get_entrance(f"Orbit -> {destination}", world.player)
            world.set_rule(entrance, Has(f"{destination} Access"))