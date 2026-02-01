from typing import Dict, NamedTuple, Optional

from BaseClasses import Location

class DL4Location(Location):
    game: str = "Duck Life 4"


class DL4LocationData(NamedTuple):
    category: str
    code: Optional[int] = None
    loc_type: str = ""

def get_locations_by_category(category: str, world=None) -> Dict[str, DL4LocationData]:
    location_dict: Dict[str, DL4LocationData] = {}

    for name, data in location_table.items():
        location_dict[name] = data

    return location_dict



location_table: dict[str, DL4LocationData] = {
    "Grasslands - Olive Duck Race Won":     DL4LocationData("Grasslands",   1,  "side race"),
    "Grasslands - Brown Duck Race Won":     DL4LocationData("Grasslands",   2,  "side race"),
    "Swamp - Grey Duck Race Won":           DL4LocationData("Swamp",        3,  "side race"),
    "Swamp - Red Duck Race Won":            DL4LocationData("Swamp",        4,  "side race"),
    "Swamp - Blue Duck Race Won":           DL4LocationData("Swamp",        5,  "side race"),
    "Mountains - Green Duck Race Won":      DL4LocationData("Mountains",    6,  "side race"),
    "Mountains - Yellow Duck Race Won":     DL4LocationData("Mountains",    7,  "side race"),
    "Mountains - White Duck Race Won":      DL4LocationData("Mountains",    8,  "side race"),
    "Glacier - Black Spotted Duck Race Won":DL4LocationData("Glacier",      9,  "side race"),
    "Glacier - Grey Duck Race Won":         DL4LocationData("Glacier",      10, "side race"),
    "Glacier - White Duck Race Won":        DL4LocationData("Glacier",      11, "side race"),
    "City - Purple Duck Race Won":          DL4LocationData("City",         12, "side race"),
    "City - Green Duck Race Won":           DL4LocationData("City",         13, "side race"),
    "City - Yellow Duck Race Won":          DL4LocationData("City",         14, "side race"),
    "Volcano - Black Duck Race Won":        DL4LocationData("Volcano",      15, "side race"),
    "Volcano - Lilac Duck Race Won":        DL4LocationData("Volcano",      16, "side race"),
    "Volcano - Light Blue Duck Race Won":   DL4LocationData("Volcano",      17, "side race"),
    "Grasslands - Tournament Race 1 Won":   DL4LocationData("Grasslands",   18, "Tournament"),
    "Grasslands - Tournament Race 2 Won":   DL4LocationData("Grasslands",   19, "Tournament"),
    "Grasslands - Tournament Race 3 Won":   DL4LocationData("Grasslands",   20, "Tournament"),
    "Grasslands - Tournament Won":          DL4LocationData("Grasslands",   21, "Tournament"),
    "Swamp - Tournament Race 1 Won":        DL4LocationData("Swamp",        22, "Tournament"),
    "Swamp - Tournament Race 2 Won":        DL4LocationData("Swamp",        23, "Tournament"),
    "Swamp - Tournament Race 3 Won":        DL4LocationData("Swamp",        24, "Tournament"),
    "Swamp - Tournament Won":               DL4LocationData("Swamp",        25, "Tournament"),
    "Mountains - Tournament Race 1 Won":    DL4LocationData("Mountains",    26, "Tournament"),
    "Mountains - Tournament Race 2 Won":    DL4LocationData("Mountains",    27, "Tournament"),
    "Mountains - Tournament Race 3 Won":    DL4LocationData("Mountains",    28, "Tournament"),
    "Mountains - Tournament Won":           DL4LocationData("Mountains",    29, "Tournament"),
    "Glacier - Tournament Race 1 Won":      DL4LocationData("Glacier",      30, "Tournament"),
    "Glacier - Tournament Race 2 Won":      DL4LocationData("Glacier",      31, "Tournament"),
    "Glacier - Tournament Race 3 Won":      DL4LocationData("Glacier",      32, "Tournament"),
    "Glacier - Tournament Won":             DL4LocationData("Glacier",      33, "Tournament"),
    "City - Tournament Race 1 Won":         DL4LocationData("City",         34, "Tournament"),
    "City - Tournament Race 2 Won":         DL4LocationData("City",         35, "Tournament"),
    "City - Tournament Race 3 Won":         DL4LocationData("City",         36, "Tournament"),
    "City - Tournament Won":                DL4LocationData("City",         37, "Tournament"),
    "Volcano - Tournament Race 1 Won":      DL4LocationData("Volcano",      38, "Tournament"),
    "Volcano - Tournament Race 2 Won":      DL4LocationData("Volcano",      39, "Tournament"),
    "Volcano - Tournament Race 3 Won":      DL4LocationData("Volcano",      40, "Tournament"),
    "Volcano - Tournament Won":             DL4LocationData("Volcano",      41, "Tournament"),
#    "Glenumbra - Wyrd Tree Wayshrine":               ESOLocationData("Glenumbra",       eso_node_id ,"wayshrine"),
}