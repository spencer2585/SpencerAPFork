from .data.levels import LEVEL_DATA

def set_rules(world):
    for level, data in LEVEL_DATA.items():
        if level != "The Piller of Autumn":
            entrance = world.multiworld.get_entrance(f"Menu -> {level}", world.player)
            required_item = f"{level} Access"
            entrance.access_rule = lambda state, item=required_item, p=world.player: state.has(item, p)