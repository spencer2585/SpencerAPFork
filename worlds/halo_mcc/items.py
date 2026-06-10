from BaseClasses import Item, ItemClassification
from .data.levels import LEVEL_DATA

#create our own item object that has the game set correctly, everything else is the same as the base item object
class MCCItem(Item):
    game = "Halo Master Chief Collection"

#this is what maps items to their ID
def get_item_name_to_id():
    item_table = {
        "filler": 1,
        **{f"{level} Access": data.offset for level, data in LEVEL_DATA.items()},
    }
    return item_table

#gives us the name of a filler item
def get_filler_item_name(world):
    return "filler"

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
        if level != "The Piller of Autumn":
            itempool.append(create_item_with_data(world, f"{level} Access"))
        else:
            world.multiworld.push_precollected(create_item_with_data(world, f"{level} Access"))

    itempool.extend(create_filler(world, len(itempool)))

    world.multiworld.itempool += itempool

#creates a single item with its classification and ID
def create_item_with_data(world, name):
    if "Access" in name:
        classification = ItemClassification.progression
        real_name = name.replace(" Access", "")
        level_data = LEVEL_DATA[real_name]
        item_id = level_data.offset
    else:
        classification = ItemClassification.filler
        item_id = 1

    return MCCItem(name, classification, item_id, world.player)