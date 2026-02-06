from typing import Dict, NamedTuple, Optional

from BaseClasses import Location

class DL4Location(Location):
    game: str = "Duck Life 4"


class DL4LocationData(NamedTuple):
    category: str
    code: Optional[int] = None
    loc_type: str = ""
    required_skills: Optional[Dict[str, int]] = None

def get_locations_by_category(category: str, world=None) -> Dict[str, DL4LocationData]:
    return {
        name: data
        for name, data in location_table.items()
        if data.category == category
    }




location_table: dict[str, DL4LocationData] = {
    "Grasslands - Olive Duck Race Won":     DL4LocationData("Grasslands",   1,  "side race", required_skills={"Running":13}),
    "Grasslands - Brown Duck Race Won":     DL4LocationData("Grasslands",   2,  "side race", required_skills={"Running":25}),
    "Swamp - Grey Duck Race Won":           DL4LocationData("Swamp",        3,  "side race", required_skills={"Running":69, "Swimming": 13}),
    "Swamp - Red Duck Race Won":            DL4LocationData("Swamp",        4,  "side race", required_skills={"Running":69, "Swimming": 38}),
    "Swamp - Blue Duck Race Won":           DL4LocationData("Swamp",        5,  "side race", required_skills={"Running":69, "Swimming": 25}),
    "Mountains - Green Duck Race Won":      DL4LocationData("Mountains",    6,  "side race", required_skills={"Running":69, "Swimming": 75, "Flying": 63}),
    "Mountains - Yellow Duck Race Won":     DL4LocationData("Mountains",    7,  "side race", required_skills={"Running":69,"Energy":9, "Swimming": 75, "Flying": 38}),
    "Mountains - White Duck Race Won":      DL4LocationData("Mountains",    8,  "side race", required_skills={"Running":69,"Energy":12, "Swimming": 75, "Flying": 50}),
    "Glacier - Black Spotted Duck Race Won":DL4LocationData("Glacier",      9,  "side race", required_skills={"Running":94,"Energy":18, "Swimming": 94, "Flying": 100, "Climbing": 75}),
    "Glacier - Grey Duck Race Won":         DL4LocationData("Glacier",      10, "side race", required_skills={"Running":94,"Energy":18, "Swimming": 94, "Flying": 100, "Climbing": 88}),
    "Glacier - White Duck Race Won":        DL4LocationData("Glacier",      11, "side race", required_skills={"Running":94,"Energy":18, "Swimming": 94, "Flying": 100, "Climbing": 100}),
    "City - Purple Duck Race Won":          DL4LocationData("City",         12, "side race", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125, "Jumping": 100}),
    "City - Green Duck Race Won":           DL4LocationData("City",         13, "side race", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125, "Jumping": 88}),
    "City - Yellow Duck Race Won":          DL4LocationData("City",         14, "side race", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125, "Jumping": 75}),
    "Volcano - Black Duck Race Won":        DL4LocationData("Volcano",      15, "side race", required_skills={"Running":130,"Energy":18, "Swimming": 150, "Flying": 150, "Climbing": 113, "Jumping": 138}),
    "Volcano - Lilac Duck Race Won":        DL4LocationData("Volcano",      16, "side race", required_skills={"Running":150,"Energy":18, "Swimming": 120, "Flying": 120, "Climbing": 120, "Jumping": 120}),
    "Volcano - Light Blue Duck Race Won":   DL4LocationData("Volcano",      17, "side race", required_skills={"Running":120,"Energy":18, "Swimming": 120, "Flying": 120, "Climbing": 150, "Jumping": 150}),
    "Grasslands - Tournament Race 1 Won":   DL4LocationData("Grasslands",   18, "Tournament", required_skills={"Running":38}),
    "Grasslands - Tournament Race 2 Won":   DL4LocationData("Grasslands",   19, "Tournament", required_skills={"Running":50}),
    "Grasslands - Tournament Race 3 Won":   DL4LocationData("Grasslands",   20, "Tournament", required_skills={"Running":63}),
    "Swamp - Tournament Race 1 Won":        DL4LocationData("Swamp",        22, "Tournament", required_skills={"Running":69,"Energy":5, "Swimming": 50}),
    "Swamp - Tournament Race 2 Won":        DL4LocationData("Swamp",        23, "Tournament", required_skills={"Running":69,"Energy":5, "Swimming": 63}),
    "Swamp - Tournament Race 3 Won":        DL4LocationData("Swamp",        24, "Tournament", required_skills={"Running":69,"Energy":12, "Swimming": 75}),
    "Mountains - Tournament Race 1 Won":    DL4LocationData("Mountains",    26, "Tournament", required_skills={"Running":69,"Energy":12, "Swimming": 71, "Flying": 75}),
    "Mountains - Tournament Race 2 Won":    DL4LocationData("Mountains",    27, "Tournament", required_skills={"Running":81,"Energy":12, "Swimming": 81, "Flying": 88}),
    "Mountains - Tournament Race 3 Won":    DL4LocationData("Mountains",    28, "Tournament", required_skills={"Running":94,"Energy":12, "Swimming": 94, "Flying": 100}),
    "Glacier - Tournament Race 1 Won":      DL4LocationData("Glacier",      30, "Tournament", required_skills={"Running":94,"Energy":18, "Swimming": 94, "Flying": 100, "Climbing": 100}),
    "Glacier - Tournament Race 2 Won":      DL4LocationData("Glacier",      31, "Tournament", required_skills={"Running":106,"Energy":18, "Swimming": 106, "Flying": 106, "Climbing": 113}),
    "Glacier - Tournament Race 3 Won":      DL4LocationData("Glacier",      32, "Tournament", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125}),
    "City - Tournament Race 1 Won":         DL4LocationData("City",         34, "Tournament", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125, "Jumping": 113}),
    "City - Tournament Race 2 Won":         DL4LocationData("City",         35, "Tournament", required_skills={"Running":119,"Energy":18, "Swimming": 119, "Flying": 119, "Climbing": 125, "Jumping": 125}),
    "City - Tournament Race 3 Won":         DL4LocationData("City",         36, "Tournament", required_skills={"Running":131,"Energy":18, "Swimming": 131, "Flying": 131, "Climbing": 131, "Jumping": 138}),
    "Volcano - Fire Duck Race Won":         DL4LocationData("Volcano",      38, "Tournament", required_skills={"Running":120,"Energy":18, "Swimming": 120, "Flying": 120, "Climbing": 120, "Jumping": 120}),
}