from typing import Dict, TYPE_CHECKING

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import ESOLocation, location_table, get_locations_by_category

if TYPE_CHECKING:
    from . import ESOWorld

REGION_GRAPH: Dict[str, Dict[str, object]] = {
    "Menu": {
        "locations": "Menu",
        "exits": ["Stros M'kai", "Bleakrock Isle", "Khenarthi's Roost", "Main Quest"],
    },
    #Daggerfall covenant
    "Stros M'kai": {
        "locations": "Stros M'kai",
        "exits": ["Betnikh","Glenumbra"],
        "requires": "Stros M'kai Access",
    },
    "Betnikh": {
        "locations": "Betnikh",
        "exits": ["Stros M'kai","Glenumbra"],
        "requires": "Betnikh Access",
    },
    "Glenumbra": {
        "locations": "Glenumbra",
        "exits": ["Betnikh","Stros M'kai","Stormhaven","Bangkorai","Stonefalls","Auridon"],
        "requires": "Glenumbra Access",
    },
    "Stormhaven": {
        "locations": "Stormhaven",
        "exits": ["Glenumbra","Rivenspire","Bangkorai","Deshaan","Grahtwood","Alik'r Desert","Craglorn"],
        "requires": "Stormhaven Access",
    },
    "Rivenspire": {
        "locations": "Rivenspire",
        "exits": ["Stormhaven","Alik'r Desert","Greenshade","Shadowfen"],
        "requires": "Rivenspire Access",
    },
    "Bangkorai": {
        "locations": "Bangkorai",
        "exits": ["Stormhaven","Craglorn","The Rift"],
        "requires": "Bangkorai Access",
    },
    "Alik'r Desert": {
        "locations": "Alik'r Desert",
        "exits": ["Bangkorai","Eastmarch","Malabal Tor","Rivenspire","Stormhaven"],
        "requires": "Alik'r Desert Access",
    },
    #Aldmeri Dominion
    "Khenarthi's Roost": {
        "locations": "Khenarthi's Roost",
        "exits": ["Auridon"],
        "requires": "Khenarthi's Roost Access",
    },
    "Auridon": {
        "locations": "Auridon",
        "exits": ["Khenarthi's Roost","Glenumbra","Grahtwood","Reaper's March","Stonefalls"],
        "requires": "Auridon Access",
    },
    "Grahtwood": {
        "locations": "Grahtwood",
        "exits": ["Auridon","Deshaan","Greenshade","Stormhaven","Malabal Tor","Craglorn"],
        "requires": "Grahtwood Access",
    },
    "Greenshade": {
        "locations": "Greenshade",
        "exits": ["Grahtwood","Malabal Tor","Rivenspire","Shadowfen"],
        "requires": "Greenshade Access",
    },
    "Malabal Tor": {
        "locations": "Malabal Tor",
        "exits": ["Grahtwood","Reaper's March","Greenshade","Alik'r Desert","Eastmarch"],
        "requires": "Malabal Tor Access",
    },
    "Reaper's March": {
        "locations": "Reaper's March",
        "exits": ["Malabal Tor","Auridon","Bangkorai","The Rift"],
        "requires": "Reaper's March Access",
    },
    #Ebonheart Pact
    "Bleakrock Isle": {
        "locations": "Bleakrock Isle",
        "exits": ["Bal Foyen","Stonefalls"],
        "requires": "Bleakrock Isle Access",
    },
    "Bal Foyen": {
        "locations": "Bal Foyen",
        "exits": ["Stonefalls","Bleakrock Isle"],
        "requires": "Bal Foyen Access",
    },
    "Stonefalls": {
        "locations": "Stonefalls",
        "exits": ["Bal Foyen","The Rift","Deshaan","Glenumbra","Bleakrock Isle","Auridon","Craglorn"],
        "requires": "Stonefalls Access",
    },
    "Deshaan": {
        "locations": "Deshaan",
        "exits": ["Stonefalls","Shadowfen","Grahtwood","Stormhaven"],
        "requires": "Deshaan Access",
    },
    "Shadowfen": {
        "locations": "Shadowfen",
        "exits": ["Deshaan","Eastmarch","Greenshade","Rivenspire"],
        "requires": "Shadowfen Access",
    },
    "Eastmarch": {
        "locations": "Eastmarch",
        "exits": ["The Rift","Alik'r Desert","Malabal Tor","Shadowfen","Auridon"],
        "requires": "Eastmarch Access",
    },
    "The Rift": {
        "locations": "The Rift",
        "exits": ["Eastmarch","Stonefalls"],
        "requires": "The Rift Access",
    },
    #Misc
    "Craglorn": {
        "locations": "Craglorn",
        "exits": ["Bangkorai","Grahtwood","Stormhaven","Stonefalls"],
        "requires": "Craglorn Access",
    },
    "Coldharbor": {
        "locations": "Coldharbor",
        "exits": ["Main Quest"],
        "requires": "Coldharbor Access",
    },
    "Main Quest": {
        "locations": "Main Quest",
        "exits": ["Menu","Coldharbor"],
    },
}

def create_regions(world: "ESOWorld"):
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



    # Create all region objects
    for region_name, data in REGION_GRAPH.items():
        region = Region(region_name, player, multiworld)

        # Add locations
        category = data.get("locations")
        if category:
            for loc_name in get_locations_by_category(category, world).keys():
                loc_data = location_table.get(loc_name)
                region.locations.append(
                    ESOLocation(
                        player,
                        loc_name,
                        loc_data.code if loc_data else None,
                        region
                    )
                )

        multiworld.regions.append(region)

    # Create entrances and connect them
    for region_name, data in REGION_GRAPH.items():
        region = world.get_region(region_name)

        for exit_name in data.get("exits", []):
            entrance_name = f"{region_name} -> {exit_name}"
            entrance = Entrance(player, entrance_name, region)
            region.exits.append(entrance)
            entrance.connect(world.get_region(exit_name))

