from typing import Dict, List, Set, TYPE_CHECKING

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import ESOLocation, location_table, get_locations_by_category

if TYPE_CHECKING:
    from . import ESOWorld

# All playable zones (excluding Menu, Main Quest)
ALL_ZONES: List[str] = [
    "Stros M'kai", "Betnikh", "Glenumbra", "Stormhaven", "Rivenspire",
    "Bangkorai", "Alik'r Desert", "Khenarthi's Roost", "Auridon",
    "Grahtwood", "Greenshade", "Malabal Tor", "Reaper's March",
    "Bleakrock Isle", "Bal Foyen", "Stonefalls", "Deshaan",
    "Shadowfen", "Eastmarch", "The Rift", "Craglorn", "Coldharbour"
]

# Starting zones by alliance
ALLIANCE_STARTING_ZONES: Dict[int, str] = {
    0: "Khenarthi's Roost",  # Aldmeri Dominion
    1: "Stros M'kai",        # Daggerfall Covenant
    2: "Bleakrock Isle",     # Ebonheart Pact
}

# Map of zone -> final quest location name
ZONE_FINAL_QUESTS: Dict[str, str] = {
    "Stros M'kai": "Stros M'kai - Tip of the Spearhead Zone Quest",
    "Betnikh": "Betnikh - On to Glenumbria Zone Quest",
    "Glenumbra": "Glenumbra - Angof the Gravesinger Zone Quest",
    "Rivenspire": "Rivenspire - The Crown of Shormhelm Zone Quest",
    "Stormhaven": "Stormhaven - Vaermina's Gambit Zone Quest",
    "Bangkorai": "Bangkorai - To Walk on far Shores Zone Quest",
    "Alik'r Desert": "Alik'r Desert - Restoring the Ansei Wards Zone Quest",
    "Khenarthi's Roost": "Khenarthi's Roost - The Tempest Unleashed Zone Quest",
    "Auridon": "Auridon - Sever All Ties Zone Quest",
    "Grahtwood": "Grahtwood - The Orrery of Elden Root Zone Quest",
    "Greenshade": "Greenshade - Striking at the Heart Zone Quest",
    "Malabal Tor": "Malabal Tor - Restore the Silvenar Zone Quest",
    "Reaper's March": "Reaper's March - The Den of Lorkhaj Zone Quest",
    "Bleakrock Isle": "Bleakrock Isle - Escape from Bleakrock Zone Quest",
    "Bal Foyen": "Bal Foyen - Breaking The Tide / Zeren in Peril Zone Quest",
    "Stonefalls": "Stonefalls - Salal's Final Defeat Zone Quest",
    "Deshaan": "Deshaan - The Judgement of Veloth Zone Quest",
    "Shadowfen": "Shadowfen - The Dream of the Hist Zone Quest",
    "Eastmarch": "Eastmarch - Songs of Sovngarde Zone Quest",
    "The Rift": "The Rift - Stomping Sinmur Zone Quest",
    "Craglorn": "Craglorn - The Time-Lost Warrior Zone Quest",
    "Coldharbour": "Coldharbour - The Final Assault Zone Quest",
}

# Some final quests require access to another zone to complete
# Map of zone -> list of required zones for final quest
ZONE_FINAL_QUEST_REQUIREMENTS: Dict[str, List[str]] = {
    "Stros M'kai": ["Betnikh"],      # Tip of the Spearhead requires Betnikh Access
    "Bleakrock Isle": ["Bal Foyen"], # Escape from Bleakrock requires Bal Foyen Access
    "Betnikh": ["Stros M'kai", "Glenumbra"],  # On to Glenumbria requires Stros M'kai (zone quest continues from there) and Glenumbra to complete
    "Bal Foyen": ["Bleakrock Isle"], # Breaking The Tide requires Bleakrock Isle Access (zone quest continues from Bleakrock)
}

def is_final_quest_achievable(zone: str, selected_zones: Set[str]) -> bool:
    """Check if a zone's final quest is achievable with the selected zones."""
    required_zones = ZONE_FINAL_QUEST_REQUIREMENTS.get(zone)
    if required_zones is None:
        return True
    return all(req in selected_zones for req in required_zones)

# Zones required for main quest progression
MAIN_QUEST_REQUIRED_ZONES: Dict[int, List[str]] = {
    # Alliance -> list of zones needed for main quest
    0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan", "Coldharbour"],  # AD
    1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan", "Coldharbour"],  # DC
    2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven", "Coldharbour"],  # EP
}

# Main Quest location requirements by alliance
# Format: (location_name, required_zones_by_alliance, progressive_mq_count)
# required_zones_by_alliance: {alliance_id: [zone_names]}
MAIN_QUEST_LOCATIONS: List[tuple] = [
    # (Location name, {alliance: required_zones}, progressive_mq_needed)
    ("Main Quest - The Harborage", {0: ["Auridon"], 1: ["Glenumbra"], 2: ["Stonefalls"]}, 0),
    ("Main Quest - Daughter of Giants", {0: ["Auridon"], 1: ["Glenumbra"], 2: ["Stonefalls"]}, 1),
    ("Main Quest - Chasing Shadows", {0: ["Auridon"], 1: ["Glenumbra"], 2: ["Stonefalls"]}, 2),
    ("Main Quest - Castle of the Worm", {0: ["Auridon"], 1: ["Glenumbra"], 2: ["Stonefalls"]}, 3),
    ("Main Quest - The Tharn Speaks", {0: ["Auridon", "Grahtwood"], 1: ["Glenumbra", "Stormhaven"], 2: ["Stonefalls", "Deshaan"]}, 4),
    ("Main Quest - Halls of Torment", {0: ["Auridon", "Grahtwood"], 1: ["Glenumbra", "Stormhaven"], 2: ["Stonefalls", "Deshaan"]}, 5),
    ("Main Quest - Valley of Blades", {0: ["Auridon", "Grahtwood"], 1: ["Glenumbra", "Stormhaven"], 2: ["Stonefalls", "Deshaan"]}, 6),
    ("Main Quest - Shadow of Sancre Tor", {0: ["Auridon", "Grahtwood"], 1: ["Glenumbra", "Stormhaven"], 2: ["Stonefalls", "Deshaan"]}, 7),
    ("Main Quest - Council of the Five Companions", {0: ["Auridon", "Grahtwood"], 1: ["Glenumbra", "Stormhaven"], 2: ["Stonefalls", "Deshaan"]}, 8),
    ("Main Quest - Messages Across Tamriel", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven"]}, 9),
    ("Main Quest - The Weight of Three Crowns", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan", "Coldharbour"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan", "Coldharbour"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven", "Coldharbour"]}, 10),
    ("Main Quest - God of Schemes", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan", "Coldharbour"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan", "Coldharbour"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven", "Coldharbour"]}, 11),
]

def get_achievable_main_quest_locations(alliance: int, selected_zones: Set[str]) -> List[str]:
    """Returns list of Main Quest location names that are achievable with the selected zones."""
    achievable = []
    for loc_name, zone_reqs, _ in MAIN_QUEST_LOCATIONS:
        required_zones = zone_reqs.get(alliance, [])
        if all(zone in selected_zones for zone in required_zones):
            achievable.append(loc_name)
    return achievable

def get_max_progressive_main_quest(alliance: int, selected_zones: Set[str]) -> int:
    """Returns the maximum number of Progressive Main Quest items needed based on achievable locations."""
    max_needed = 0
    for loc_name, zone_reqs, prog_count in MAIN_QUEST_LOCATIONS:
        required_zones = zone_reqs.get(alliance, [])
        if all(zone in selected_zones for zone in required_zones):
            max_needed = max(max_needed, prog_count)
    return max_needed

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
        "exits": ["Glenumbra","Rivenspire","Bangkorai","Deshaan","Grahtwood","Alik'r Desert","Craglorn","Coldharbour"],
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
        "exits": ["Auridon","Deshaan","Greenshade","Stormhaven","Malabal Tor","Craglorn","Coldharbour"],
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
        "exits": ["Stonefalls","Shadowfen","Grahtwood","Stormhaven","Coldharbour"],
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
    "Coldharbour": {
        "locations": "Coldharbour",
        "exits": ["Main Quest"],
        "requires": "Coldharbour Access",
    },
    "Main Quest": {
        "locations": "Main Quest",
        "exits": ["Menu","Coldharbour"],
    },
}

def create_regions(world: "ESOWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player
    selected_zones: Set[str] = world.selected_zones

    # Special regions that are always included
    always_include = {"Menu", "Main Quest"}

    # Determine which regions to create
    regions_to_create: Set[str] = selected_zones | always_include

    print("=== SELECTED ZONES ===")
    print(f"Creating regions for: {sorted(regions_to_create)}")

    # Get achievable main quest locations
    achievable_main_quests = set(world.achievable_main_quests)

    # Build set of final quests that are NOT achievable (zone in pool but required zone isn't)
    unachievable_final_quests: Set[str] = set()
    for zone in selected_zones:
        if not is_final_quest_achievable(zone, selected_zones):
            final_quest = ZONE_FINAL_QUESTS.get(zone)
            if final_quest:
                unachievable_final_quests.add(final_quest)
                print(f"ESO: Filtering out {final_quest} (required zone not in pool)")

    # Create region objects only for selected zones
    for region_name, data in REGION_GRAPH.items():
        if region_name not in regions_to_create:
            continue

        region = Region(region_name, player, multiworld)

        # Add locations
        category = data.get("locations")
        if category:
            for loc_name in get_locations_by_category(category, world).keys():
                # Filter Main Quest locations to only achievable ones
                if category == "Main Quest" and loc_name not in achievable_main_quests:
                    continue

                # Filter out final quests that require zones not in the pool
                if loc_name in unachievable_final_quests:
                    continue

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

    # Create entrances and connect them (only to regions that exist)
    for region_name, data in REGION_GRAPH.items():
        if region_name not in regions_to_create:
            continue

        region = world.get_region(region_name)

        for exit_name in data.get("exits", []):
            # Only create entrance if the destination region exists
            if exit_name not in regions_to_create:
                continue

            entrance_name = f"{region_name} -> {exit_name}"
            entrance = Entrance(player, entrance_name, region)
            region.exits.append(entrance)
            entrance.connect(world.get_region(exit_name))

    print("=== REGION CONNECTIVITY CHECK ===")
    for region in world.multiworld.regions:
        if region.player == player:
            print(region.name, "exits:", [e.name for e in region.exits])

