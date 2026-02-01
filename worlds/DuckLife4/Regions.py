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
        "exits": [],
    },
    "Grasslands": {
        "locations": "Grasslands",
        "exits": [],
    },
    "Swamp":{
        "locations": "Swamp",
        "exits": [],
        "requires": "Swamp Access",
    },
    "Mountains":{
        "locations": "Mountains",
        "exits": [],
        "requires": "Mountain Access",
    },
    "Glacier":{
        "locations": "Glacier",
        "exits": [],
        "requires": "Glacier Access",
    },
    "City":{
        "locations": "City",
        "exits": [],
        "requires": "City Access",
    },
    "Volcano":{
        "locations": "Volcano",
        "exits": [],
        "requires": "Volcano Access",
    },
    #Daggerfall covenant
#    "Stros M'kai": {
#        "locations": "Stros M'kai",
#        "exits": ["Betnikh","Glenumbra"],
#        "requires": "Stros M'kai Access",
#    },
}


# ---------------------------------------------------------
#  REGION CREATION
# ---------------------------------------------------------

def create_regions(world: "DL4World"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    print("=== REGION CONNECTIVITY CHECK ===")
    for region in world.multiworld.regions:
        print(region.name, "exits:", [e.name for e in region.exits])

    print("=== LOCATION COUNT CHECK ===")
    for region_name, data in REGION_GRAPH.items():
        category = data["locations"]
        if category:
            locs = get_locations_by_category(category, world)
            print(region_name, "->", len(locs), "locations")
        else:
            print(region_name, "-> Menu (no locations)")



    # 1. Create all region objects
    for region_name, data in REGION_GRAPH.items():
        region = Region(region_name, player, multiworld)

        # Add locations automatically
        category = data.get("locations")
        if category:
            for loc_name in get_locations_by_category(category, world).keys():
                loc_data = location_table.get(loc_name)
                region.locations.append(
                    DL4Location(
                        player,
                        loc_name,
                        loc_data.code if loc_data else None,
                        region
                    )
                )

        multiworld.regions.append(region)

    # 2. Create entrances and connect them
    for region_name, data in REGION_GRAPH.items():
        region = world.get_region(region_name)

        for exit_name in data.get("exits", []):
            entrance_name = f"{region_name} -> {exit_name}"
            entrance = Entrance(player, entrance_name, region)
            region.exits.append(entrance)
            entrance.connect(world.get_region(exit_name))

