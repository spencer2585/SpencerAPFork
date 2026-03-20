from .Data.DelveData import DELVE_DATA
from .Data.ZoneData import ZONE_DATA
from .Data.FillerData import FILLER_DATA
from BaseClasses import Item, ItemClassification
from . import constants, regions

class ESOItem(Item):
    game = "Elder Scrolls Online"

def get_item_name_to_id():
    item_table = {
        **{f"{zone_name} Access": constants.ZONE_ACCESS_OFFSET+ zone_data.zone_id for zone_name, zone_data in ZONE_DATA.items()},
        **{f"{delve_name} Access": constants.ZONE_ACCESS_OFFSET + delve_data.delve_id for delve_name, delve_data in DELVE_DATA.items()},
    }

    return item_table

def get_filler_item_name(world):
    if world.options.gold_cap:
        return "Gold Capacity Upgrade"
    else:
        return "Skyshard"

def create_filler(world, filled_locations):
    fillerpool: list[Item] = []
    unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
    needed_items = len(unfilled_locations) - filled_locations
    for i in range(needed_items):
        if world.options.gold_cap:
            fillerpool.append(create_item_with_data(world, "Wallet Capacity Upgrade"))
        else:
            fillerpool.append(create_item_with_data(world, "Skyshard"))

    return fillerpool




def create_items(world):
    itempool: list[Item] = []
    for zone_name, zone_data in ZONE_DATA.items():
        if zone_name in world.selected_zones and zone_name != regions.get_starting_zone(world.options.alliance):
            itempool.append(world.create_item(f"{zone_name} Access"))

    for delve_name, delve_data in DELVE_DATA.items():
        if delve_name in world.selected_delves:
            itempool.append(world.create_item(f"{delve_name} Access"))

    if world.options.main_quests_enabled:
        for _ in range(world.max_main_quest - 1):
            itempool.append(world.create_item("Progressive Main Quest"))

    itempool.extend(create_filler(world, len(itempool)))

    world.multiworld.itempool += itempool


def create_item_with_data(world, name):
    #zone access Items
    if "Access" in name:
        classification = ItemClassification.progression
        real_name = name.replace(" Access","")
        if real_name in ZONE_DATA:
            item_data = ZONE_DATA[real_name]
            item_id = constants.ZONE_ACCESS_OFFSET + item_data.zone_id
        else:
            item_data = DELVE_DATA[real_name]
            item_id = constants.ZONE_ACCESS_OFFSET+ item_data.delve_id

    #Progressive Main Quest
    elif name == "Progressive Main Quest":
        classification = ItemClassification.progression
        item_id = 149996
    #filler Items
    else:
        item_data = FILLER_DATA[name]
        item_id =  item_data.id
        classification = ItemClassification.filler

    return ESOItem(name, classification, item_id, world.player)


