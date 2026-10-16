from BaseClasses import Item, ItemClassification

from dataclasses import dataclass

from .Data.destination_data import DESTINATION_DATA
from .Data.exotic_weapons import EXOTIC_WEAPON_DATA
from .Data.constants import BASE_ID
from .Data.filler_data import FILLER_DATA
from .Data.weapon_frame_data import WEAPON_FRAME_DATA


class ItemIds:
    WEAPONFRAMEID = BASE_ID
    EXOTICID = BASE_ID + 1000
    DESTINATION_ACCESSID = BASE_ID + 2000

class ItemTypes:
    WEAPONFRAME = "Weapon Frame"
    EXOTIC = "Exotic"
    FILLER = "Filler"
    DESTINATION_ACCESS = "Destination Access"
    DUNGEON_ACCESS = "Dungeon Access"
    RAID_ACCESS = "Raid Access"

class D2Item(Item):
    game = "Destiny 2"

@dataclass
class D2ItemData:
    type:str
    id:int
    classification:ItemClassification


items_dict = {
    **{name: D2ItemData(type = ItemTypes.WEAPONFRAME, id = ItemIds.WEAPONFRAMEID + data.id, classification= ItemClassification.progression) for name, data in WEAPON_FRAME_DATA.items()},
    **{name: D2ItemData(type = ItemTypes.EXOTIC, id = ItemIds.EXOTICID + data.id,classification= ItemClassification.useful) for name, data in EXOTIC_WEAPON_DATA.items()},
    **{name: D2ItemData(type = ItemTypes.DESTINATION_ACCESS, id = ItemIds.DESTINATION_ACCESSID + data.id, classification= ItemClassification.progression) for name, data in DESTINATION_DATA.items()}
}

filler_dict = {
    **{name: D2ItemData(type = ItemTypes.FILLER, id = BASE_ID + data.id, classification= ItemClassification.filler) for name, data in FILLER_DATA.items()},
}

def get_item_name_to_id():
    return {
        **{name: data.id for name, data in items_dict.items()},
        **{name: data.id for name, data in filler_dict.items()},
        }

def create_items(world):
    itempool: list[Item] = []
    for name, data in items_dict.items():
        itempool.append(D2Item(name, data.classification, data.id, world.player))

    itempool.extend(create_filler(world, len(itempool)))
    world.multiworld.itempool += itempool

def create_filler(world, filled_locations):
    fillerpool: list[Item] = []
    unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
    needed_items = len(unfilled_locations) - filled_locations
    for i in range (needed_items):
        random_item = world.random.choice(list(filler_dict.keys()))
        data = filler_dict[random_item]
        fillerpool.append(D2Item(random_item, data.classification, data.id, world.player))

    return fillerpool