from BaseClasses import Item, ItemClassification
from .data.constants import *
from .data.levels import LEVEL_DATA, LevelData
from .data.skulls import GAME_SKULLS, NON_SCORING, PERM_DISABLED, CE_HARD_REQUIRED, CE_HARDER_REQUIRED
from .mcc_options import SkullSanity

# Ordered list of CE skull disabler items (non-PERM_DISABLED CE skulls, alphabetical)
CE_SKULL_DISABLERS: list[str] = [s for s in GAME_SKULLS["ce"] if s not in PERM_DISABLED]


#create our own item object that has the game set correctly, everything else is the same as the base item object
class MCCItem(Item):
    game = "Halo Master Chief Collection"

#this is what maps items to their ID
def get_item_name_to_id():
    item_table = {
        "filler": 1,
        **{f"{level} Access": data.offset for level, data in LEVEL_DATA.items()},
        **{f"{skull} Skull": SKULL_OFFSET + i + 1 for i, skull in enumerate (CE_SKULL_DISABLERS)}
    }
    return item_table

#gives us the name of a filler item
def get_filler_item_name(world):
    return "filler"

# Get the skulls to include for skullsanity tier selected
def _skulls_for_tier(tier: int):
    if tier == SkullSanity.option_non_scoring:
        return [s for s in CE_SKULL_DISABLERS if s in NON_SCORING]
    if tier in (SkullSanity.option_hard, SkullSanity.option_harder, SkullSanity.option_laso):
        return CE_SKULL_DISABLERS
    return []

#fill unfilled locations with filler from this world
def create_filler(world, filled_locations):
    fillerpool: list[Item] = []
    unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
    needed_items = len(unfilled_locations) - filled_locations
    for i in range(needed_items):
        fillerpool.append(create_item_with_data(world, "filler"))

    return fillerpool

#create all items for the world
def create_items(world):
    itempool: list[Item] = []
    for level, data in LEVEL_DATA.items():
        if level != world.final_mission:
            if level == world.starting_mission:
                world.multiworld.push_precollected(create_item_with_data(world, f"{level} Access"))
            else:
                itempool.append(create_item_with_data(world, f"{level} Access"))

    for skull in _skulls_for_tier(world.options.skullsanity.value):
        itempool.append(create_item_with_data(world, f"{skull} Skull"))

    itempool.extend(create_filler(world, len(itempool)))

    world.multiworld.itempool += itempool

#creates a single item with its classification and ID
def create_item_with_data(world, name):
    if "Access" in name:
        classification = ItemClassification.progression
        real_name = name.replace(" Access", "")
        level_data = LEVEL_DATA[real_name]
        item_id = level_data.offset
    elif "Skull" in name:
        skull = name[:-len(" Skull"):]
        # Non-scoring skulls and Catch are marked useful rather than progression.
        # CE has exactly 13 scoring skull disablers matching the 13 skull locations;
        # keeping Catch and all non-scoring skulls as useful prevents generation
        # failures when skull locations are the only unfilled progression slots.
        # We can change Catch to progression eventually when there are more locations.
        classification = ItemClassification.progression
        return MCCItem(name, classification, SKULL_OFFSET + CE_SKULL_DISABLERS.index(skull) + 1, world.player)

    else:
        classification = ItemClassification.filler
        item_id = 1

    return MCCItem(name, classification, item_id, world.player)