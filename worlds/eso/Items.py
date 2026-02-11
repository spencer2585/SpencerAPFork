from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

ALLIANCE_STARTING_REGIONS = {
    0: "Khenarthi's Roost Access",  # AD
    1: "Stros M'kai Access",        # DC
    2: "Bleakrock Isle Access",     # EP
}

eso_base_id: int = 150000
eso_region_unlock_id: int = eso_base_id

class ESOItem(Item):
    game: str = "Elder Scrolls Online"

class ESOItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1
    zone: Optional[str] = None  # If set, item is only included when this zone is selected

def get_items_by_category(category: str) -> Dict[str, ESOItemData]:
    item_dict: Dict[str, ESOItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict

def get_starting_region_item_name(alliance_value: int) -> str:
    return ALLIANCE_STARTING_REGIONS[alliance_value]

item_table: Dict[str, ESOItemData] = {
    "Skyshard":                 ESOItemData("Filler",       eso_base_id-6),
    "Victory":                  ESOItemData("Main Quest",   eso_base_id - 5,            ItemClassification.progression, 0),
    "Progressive Main Quest":   ESOItemData("Main Quest",   eso_base_id-4,              ItemClassification.progression,11),
    "Stros M'kai Access":       ESOItemData("Zone Access",  eso_region_unlock_id+534,   ItemClassification.progression, 1, 1, "Stros M'kai"),
    "Glenumbra Access":         ESOItemData("Zone Access",  eso_region_unlock_id+3,     ItemClassification.progression, 1, 1 , "Glenumbra"),
    "Stormhaven Access":        ESOItemData("Zone Access",  eso_region_unlock_id+19,    ItemClassification.progression, 1, 1, "Stormhaven"),
    "Rivenspire Access":        ESOItemData("Zone Access",  eso_region_unlock_id+20,    ItemClassification.progression, 1, 1, "Rivenspire"),
    "Bangkorai Access":         ESOItemData("Zone Access",  eso_region_unlock_id+92,    ItemClassification.progression, 1, 1, "Bangkorai"),
    "Alik'r Desert Access":     ESOItemData("Zone Access",  eso_region_unlock_id+104,   ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Betnikh Access":           ESOItemData("Zone Access",  eso_region_unlock_id+535,   ItemClassification.progression, 1, 1, "Betnikh"),
    "Khenarthi's Roost Access": ESOItemData("Zone Access",  eso_region_unlock_id+537,   ItemClassification.progression, 1, 1, "Khenarthi's Roost"),
    "Bleakrock Isle Access":    ESOItemData("Zone Access",  eso_region_unlock_id+280,   ItemClassification.progression, 1, 1, "Bleakrock Isle"),
    "Auridon Access":           ESOItemData("Zone Access",  eso_region_unlock_id+381,   ItemClassification.progression, 1, 1, "Auridon"),
    "Grahtwood Access":         ESOItemData("Zone Access",  eso_region_unlock_id+383,   ItemClassification.progression, 1, 1, "Grahtwood"),
    "Greenshade Access":        ESOItemData("Zone Access",  eso_region_unlock_id+108,   ItemClassification.progression, 1, 1, "Greenshade"),
    "Malabal Tor Access":       ESOItemData("Zone Access",  eso_region_unlock_id+58,    ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Reaper's March Access":    ESOItemData("Zone Access",  eso_region_unlock_id+382,   ItemClassification.progression, 1, 1, "Reaper's March"),
    "Bal Foyen Access":         ESOItemData("Zone Access",  eso_region_unlock_id+281,   ItemClassification.progression, 1, 1, "Bal Foyen"),
    "Stonefalls Access":        ESOItemData("Zone Access",  eso_region_unlock_id+41,    ItemClassification.progression, 1, 1, "Stonefalls"),
    "Deshaan Access":           ESOItemData("Zone Access",  eso_region_unlock_id+57,    ItemClassification.progression, 1, 1, "Deshaan"),
    "Shadowfen Access":         ESOItemData("Zone Access",  eso_region_unlock_id+117,   ItemClassification.progression, 1, 1, "Shadowfen"),
    "The Rift Access":          ESOItemData("Zone Access",  eso_region_unlock_id+103,   ItemClassification.progression, 1, 1, "The Rift"),
    "Eastmarch Access":         ESOItemData("Zone Access",  eso_region_unlock_id+101,   ItemClassification.progression, 1, 1, "Eastmarch"),
    "Coldharbour Access":        ESOItemData("Zone Access",  eso_region_unlock_id+347,   ItemClassification.progression, 1, 1, "Coldharbour"),
    "Craglorn Access":          ESOItemData("Zone Access",  eso_region_unlock_id+888,   ItemClassification.progression, 1, 1, "Craglorn"),
    }
