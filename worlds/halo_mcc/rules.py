from .data.levels import LEVEL_DATA
from .data.skulls import CE_HARD_REQUIRED, CE_HARDER_REQUIRED
from .mcc_options import SkullSanity


def set_rules(world):
    for level, data in LEVEL_DATA.items():
        if level != "The Piller of Autumn":
            entrance = world.multiworld.get_entrance(f"Menu -> {level}", world.player)
            required_item = f"{level} Access"
            entrance.access_rule = lambda state, item=required_item, p=world.player: state.has(item, p)

    tier = world.options.skullsanity.value
    if tier in (SkullSanity.option_hard, SkullSanity.option_harder):
        skull_set = CE_HARD_REQUIRED if tier == SkullSanity.option_hard else CE_HARDER_REQUIRED
        disablers = [f"Disable {skull}" for skull in skull_set]
        for level in LEVEL_DATA:
            location = world.multiworld.get_location(f"{level} Complete", world.player)
            location.access_rule = lambda state, items=disablers, p=world.player: all(
                state.has(item, p) for item in items
            )
