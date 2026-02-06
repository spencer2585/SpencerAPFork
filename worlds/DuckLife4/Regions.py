import math
from typing import Dict, List, Optional, TYPE_CHECKING

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import DL4Location, location_table, get_locations_by_category

if TYPE_CHECKING:
    from . import DL4World


# ---------------------------------------------------------
#  REGION GRAPH
#  Add your regions here. Each entry defines:
#   - which location category to load
#   - which regions it connects to
#   - which item unlocks it
# ---------------------------------------------------------

REGION_GRAPH: Dict[str, Dict[str, object]] = {
    "Menu": {
        "locations": "Menu",
        "exits": ["Grasslands", "Swamp", "Mountains", "Glacier", "City", "Volcano"],
    },
    "Grasslands": {
        "locations": "Grasslands",
        "exits": ["Menu"],
    },
    "Swamp":{
        "locations": "Swamp",
        "exits": ["Menu"],
        "requires": "Swamp Access",
    },
    "Mountains":{
        "locations": "Mountains",
        "exits": ["Menu"],
        "requires": "Mountains Access",
    },
    "Glacier":{
        "locations": "Glacier",
        "exits": ["Menu"],
        "requires": "Glacier Access",
    },
    "City":{
        "locations": "City",
        "exits": ["Menu"],
        "requires": "City Access",
    },
    "Volcano":{
        "locations": "Volcano",
        "exits": ["Menu"],
        "requires": "Volcano Access",
    },
}


# ---------------------------------------------------------
#  REGION CREATION
# ---------------------------------------------------------

def create_regions(world: "DL4World"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    # ---------------------------------------------------------
    # 1. Create region objects (do NOT append yet)
    # ---------------------------------------------------------
    regions: Dict[str, Region] = {
        name: Region(name, player, multiworld)
        for name in REGION_GRAPH.keys()
    }

    # ---------------------------------------------------------
    # 2. Add static locations
    # ---------------------------------------------------------
    for region_name, data in REGION_GRAPH.items():
        region = regions[region_name]
        category = data.get("locations")

        if category:
            for loc_name, loc_data in location_table.items():
                if loc_data.category == category:
                    region.locations.append(
                        DL4Location(player, loc_name, loc_data.code, region)
                    )

    # ---------------------------------------------------------
    # 3. Add dynamic skill locations BEFORE registering regions
    # ---------------------------------------------------------
    chunk = world.options.skill_size.value
    levels_per_skill = 150
    num_locations = math.ceil(levels_per_skill / chunk)

    # Calculate base ID for this skill level
    def get_skill_location_id(skill_name: str, level: int) -> int:
        SKILL_LOCATION_BASE_ID = 100
        skill_names = ["Running", "Energy", "Swimming", "Flying", "Climbing", "Jumping"]
        skill_offset = skill_names.index(skill_name) * 150
        level_offset = level - 1  # level 1 = offset 0, level 5 = offset 4, etc.
        return SKILL_LOCATION_BASE_ID + skill_offset + level_offset

    def add_dynamic(region_name: str, skill_name: str):
        region = regions[region_name]
        for i in range(1, num_locations + 1):
            level = i * chunk
            loc_name = f"{skill_name} Training {level}"
            loc_id = get_skill_location_id(skill_name, level)
            region.locations.append(
                DL4Location(player, loc_name, loc_id, region)
            )

    add_dynamic("Grasslands", "Running")
    add_dynamic("Menu", "Energy")
    add_dynamic("Swamp", "Swimming")
    add_dynamic("Mountains", "Flying")
    add_dynamic("Glacier", "Climbing")
    add_dynamic("City", "Jumping")

    # ---------------------------------------------------------
    # 4. NOW append regions to the MultiWorld
    # ---------------------------------------------------------
    for region in regions.values():
        multiworld.regions.append(region)

    # ---------------------------------------------------------
    # 5. Create entrances and connect regions
    # ---------------------------------------------------------
    for region_name, data in REGION_GRAPH.items():
        region = regions[region_name]

        for exit_name in data.get("exits", []):
            entrance_name = f"{region_name} -> {exit_name}"
            entrance = Entrance(player, entrance_name, region)
            region.exits.append(entrance)
            entrance.connect(regions[exit_name])
