from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

class DL4Item(Item):
    game: str = "Duck Life 4"

class DL4ItemData(NamedTuple):
    category:str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1

def get_items_by_category(category: str) -> Dict[str, DL4ItemData]:
    item_dict: Dict[str, DL4ItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict

item_table: Dict[str, DL4ItemData] = {
    "Swamp Access":                     DL4ItemData("Region Access",    1,      ItemClassification.progression),
    "Mountains Access":                 DL4ItemData("Region Access",    2,      ItemClassification.progression),
    "Glacier Access":                   DL4ItemData("Region Access",    3,      ItemClassification.progression),
    "City Access":                      DL4ItemData("Region Access",    4,      ItemClassification.progression),
    "Volcano Access":                   DL4ItemData("Region Access",    5,      ItemClassification.progression),
    "Grasslands Tournament Ticket":     DL4ItemData("Ticket",           6,      ItemClassification.progression),
    "Swamp Tournament Ticket":          DL4ItemData("Ticket",           7,      ItemClassification.progression),
    "Mountains Tournament Ticket":      DL4ItemData("Ticket",           8,      ItemClassification.progression),
    "Glacier Tournament Ticket":        DL4ItemData("Ticket",           9,      ItemClassification.progression),
    "City Tournament Ticket":           DL4ItemData("Ticket",           10,     ItemClassification.progression),
    "Red Key":                          DL4ItemData("Key",              11,     ItemClassification.progression),
    "Orange Key":                       DL4ItemData("Key",              12,     ItemClassification.progression),
    "Green Key":                        DL4ItemData("Key",              13,     ItemClassification.progression),
    "Energy Level":                     DL4ItemData("Level",            14,     ItemClassification.progression, 0),
    "Running Level":                    DL4ItemData("Level",            15,     ItemClassification.progression, 0),
    "Swimming Level":                   DL4ItemData("Level",            16,     ItemClassification.progression, 0),
    "Flying Level":                     DL4ItemData("Level",            17,     ItemClassification.progression, 0),
    "Climbing Level":                   DL4ItemData("Level",            18,     ItemClassification.progression, 0),
    "Jumping Level":                    DL4ItemData("Level",            19,     ItemClassification.progression, 0),
    "Victory":                          DL4ItemData("Victory",          20,     ItemClassification.progression, 0),
    "Coins":                            DL4ItemData("Filler",           21,     ItemClassification.filler,      0,      10),
}
