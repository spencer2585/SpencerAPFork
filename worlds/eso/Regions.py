from typing import Dict, List, Set, TYPE_CHECKING

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import ESOLocation, location_table, get_locations_by_category

if TYPE_CHECKING:
    from . import ESOWorld

# All playable main zones (excluding Menu, Main Quest, and delves)
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

MAIN_QUEST_DELVE_REQUIREMENTS: Dict[int, tuple[str, str]] = {
    0: ("Grahtwood", "Wormroot Depths"),      # AD
    1: ("Stormhaven", "Norvulk Ruins"),       # DC
    2: ("Deshaan", "Knife Ear Grotto"),       # EP
}

REQUIRED_DELVES_FOR_QUESTS: Dict[str, Set[str]] = {
    "Craglorn": {"Buried Sands","Tombs of the Na-Totambu","Haddock's Market","Molavar","Balamath","Fearfangs Cavern","Serpent's Nest","Ilthag's Undertower","Exarch's Stronghold","The Howling Sepulchers","Loth'Na Caverns"}
}

ZONE_QUEST_REQUIRED_DELVES: Dict[str, Dict[str, Set[str]]] = {
    # Zone name -> {quest location name: required delve name}
    # Example for future use:
     "Craglorn": {
         "Craglorn - The Warrior's Call Zone Quest": {"Buried Sands", "Tombs of the Na-Totambu"},
         "Craglorn - Elemental Army Zone Quest": {"Haddock's Market","Molavar","Balamath"},
         "Craglorn - The Missing Guardian Zone Quest": {"Buried Sands", "Tombs of the Na-Totambu","Haddock's Market","Molavar","Balamath"},
         "Craglorn - Slithering Brood Zone Quest": {"Fearfangs Cavern","Serpent's Nest"},
         "Craglorn - The Serpent's Fang Zone Quest": {"Ilthag's Undertower","Exarch's Stronghold"},
         "Craglorn - Dawn of the Exalted Viper Zone Quest": {"Buried Sands", "Tombs of the Na-Totambu","Haddock's Market","Molavar","Balamath","Fearfangs Cavern","Serpent's Nest","Ilthag's Undertower","Exarch's Stronghold","The Howling Sepulchers","Loth'Na Caverns"},
         "Craglorn - The Time-Lost Warrior Zone Quest": {"Buried Sands", "Tombs of the Na-Totambu","Haddock's Market","Molavar","Balamath","Fearfangs Cavern","Serpent's Nest","Ilthag's Undertower","Exarch's Stronghold","The Howling Sepulchers","Loth'Na Caverns"},
    }
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
    #("Main Quest - Messages Across Tamriel", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven"]}, 9),
    #("Main Quest - The Weight of Three Crowns", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan", "Coldharbour"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan", "Coldharbour"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven", "Coldharbour"]}, 10),
    ("Main Quest - God of Schemes", {0: ["Auridon", "Grahtwood", "Stormhaven", "Deshaan", "Coldharbour"], 1: ["Glenumbra", "Stormhaven", "Grahtwood", "Deshaan", "Coldharbour"], 2: ["Stonefalls", "Deshaan", "Grahtwood", "Stormhaven", "Coldharbour"]}, 9),
]


def get_achievable_main_quest_locations(alliance: int, selected_zones: Set[str], selected_delves: Set[str] = None) -> \
List[str]:
    """Returns list of Main Quest location names that are achievable with the selected zones and delves."""
    achievable = []

    # Check if the required delve is selected (needed for quests 5+)
    required_zone, required_delve = MAIN_QUEST_DELVE_REQUIREMENTS[alliance]
    has_required_delve = selected_delves is not None and required_delve in selected_delves

    # If selected_delves is empty (not None, but empty set), delves are disabled entirely
    delves_disabled = selected_delves is not None and len(selected_delves) == 0

    for loc_name, zone_reqs, prog_count in MAIN_QUEST_LOCATIONS:
        required_zones = zone_reqs.get(alliance, [])

        # Check zone requirements
        if not all(zone in selected_zones for zone in required_zones):
            continue

        # If this quest requires the delve (prog_count >= 5) and we don't have it, skip
        # BUT if delves are completely disabled, skip this check
        if not delves_disabled and prog_count >= 4 and not has_required_delve:
            continue

        achievable.append(loc_name)
    return achievable


def get_max_progressive_main_quest(alliance: int, selected_zones: Set[str], selected_delves: Set[str] = None) -> int:
    """Returns the maximum number of Progressive Main Quest items needed based on achievable locations."""
    max_needed = 0

    # Check if the required delve is selected
    required_zone, required_delve = MAIN_QUEST_DELVE_REQUIREMENTS[alliance]
    has_required_delve = selected_delves is not None and required_delve in selected_delves

    # If selected_delves is empty, delves are disabled entirely
    delves_disabled = selected_delves is not None and len(selected_delves) == 0

    for loc_name, zone_reqs, prog_count in MAIN_QUEST_LOCATIONS:
        required_zones = zone_reqs.get(alliance, [])

        # Check zone requirements
        if not all(zone in selected_zones for zone in required_zones):
            continue

        # If this quest requires the delve (prog_count >= 4) and we don't have it, skip
        # BUT if delves are completely disabled, skip this check
        if not delves_disabled and prog_count >= 4 and not has_required_delve:
            continue

        max_needed = max(max_needed, prog_count)
    return max_needed

REGION_GRAPH: Dict[str, Dict[str, object]] = {
    "Menu": {
        "locations": "Menu",
        "exits": ["Stros M'kai", "Bleakrock Isle", "Khenarthi's Roost", "Main Quest"],
    },
    #Zones
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
        "exits": ["Betnikh","Stros M'kai","Stormhaven","Bangkorai","Stonefalls","Auridon","Ilessan Tower","Silumm","The Mines of Khuras","Enduum","Ebon Crypt","Cryptwatch Fort"],
        "requires": "Glenumbra Access",
    },
    "Stormhaven": {
        "locations": "Stormhaven",
        "exits": ["Glenumbra","Rivenspire","Bangkorai","Deshaan","Grahtwood","Alik'r Desert","Bearclaw Mine","Norvulk Ruins","Pariah Catacombs","Farangel's Delve","Portdun Watch","Koeglin Mine"],
        "requires": "Stormhaven Access",
    },
    "Rivenspire": {
        "locations": "Rivenspire",
        "exits": ["Stormhaven","Alik'r Desert","Greenshade","Shadowfen","Hildune's Secret Refuge","Orc's Finger Ruins","Erokii Ruins","Crestshade Mines","Flyleaf Catacombs","Tribulation Crypt"],
        "requires": "Rivenspire Access",
    },
    "Bangkorai": {
        "locations": "Bangkorai",
        "exits": ["Stormhaven","Craglorn","The Rift","Troll's Toothpick","Torog's Spite","Viridian Watch","Crypt of the Exiles","Rubble Butte","Klathzgar","Stirk"],
        "requires": "Bangkorai Access",
    },
    "Alik'r Desert": {
        "locations": "Alik'r Desert",
        "exits": ["Bangkorai","Eastmarch","Malabal Tor","Rivenspire","Stormhaven","Santaki","Divad's Chagrin Mine","Aldunz","Sandblown Mine","Yldzuun","Coldrock Digging"],
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
        "exits": ["Khenarthi's Roost","Glenumbra","Grahtwood","Reaper's March","Stonefalls","Mehrunes' Spite","Wansalen","Bewan","Entila's Folly","Ondil","Del's Claim"],
        "requires": "Auridon Access",
    },
    "Grahtwood": {
        "locations": "Grahtwood",
        "exits": ["Auridon","Deshaan","Greenshade","Stormhaven","Malabal Tor","Wormroot Depths","Vinedeath Cave","Burroot Kwama Mine","The Scuttle Pit","Mobar Mine","Ne Salas"],
        "requires": "Grahtwood Access",
    },
    "Greenshade": {
        "locations": "Greenshade",
        "exits": ["Grahtwood","Malabal Tor","Rivenspire","Shadowfen","Barrow Trench","The Underroot","Harridan's Lair","Gurzag's Mine","Naril Nagaia","Carac Dena"],
        "requires": "Greenshade Access",
    },
    "Malabal Tor": {
        "locations": "Malabal Tor",
        "exits": ["Grahtwood","Reaper's March","Greenshade","Alik'r Desert","Eastmarch","Black Vine Ruins","Roots of Silvenar","Shael Ruins","Tomb of the Apostates","Hoarvor Pit","Dead Man's Drop"],
        "requires": "Malabal Tor Access",
    },
    "Reaper's March": {
        "locations": "Reaper's March",
        "exits": ["Malabal Tor","Auridon","Bangkorai","The Rift","Fardir's Folly","Kuna's Delve","Jode's Light","Thibaut's Cairn","Claw's Strike","Weeping Wind Cave","Stirk"],
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
        "exits": ["Bal Foyen","The Rift","Deshaan","Glenumbra","Bleakrock Isle","Auridon","Inner Sea Armature","Emberflint Mine","Mephala's Nest","Hightide Hollow","Softloam Cavern","Sheogorath's Tongue"],
        "requires": "Stonefalls Access",
    },
    "Deshaan": {
        "locations": "Deshaan",
        "exits": ["Stonefalls","Shadowfen","Grahtwood","Stormhaven","Knife Ear Grotto","The Corpse Garden","Triple Circle Mine","Taleon's Crag","Lady Llarel's Shelter","Lower Bthanual"],
        "requires": "Deshaan Access",
    },
    "Shadowfen": {
        "locations": "Shadowfen",
        "exits": ["Deshaan","Eastmarch","Greenshade","Rivenspire","Shrine of the Black Maw","Broken Tusk","Grandranen Ruins","Atanaz Ruins","Onkobra Kwama Mine","Chid-Moska Ruins"],
        "requires": "Shadowfen Access",
    },
    "Eastmarch": {
        "locations": "Eastmarch",
        "exits": ["The Rift","Alik'r Desert","Malabal Tor","Shadowfen","Auridon","The Chill Hollow","Icehammer's Vault","The Bastard's Tomb","Stormcrag Crypt","Old Sord's Cave","The Frigid Grotto"],
        "requires": "Eastmarch Access",
    },
    "The Rift": {
        "locations": "The Rift",
        "exits": ["Eastmarch","Stonefalls","Broken Helm Hollow","Fort Greenwall","Faldar's Tooth","Avanchnzel","Snapleg Cave","Shroud Hearth Barrow","Stirk"],
        "requires": "The Rift Access",
    },
    #Misc
    "Stirk": {
        "locations": "Stirk",
        "exits": ["Coldharbour","The Rift","Reaper's March","Bangkorai","Main Quest"],
    },
    "Craglorn": {
        "locations": "Craglorn",
        "exits": ["Bangkorai","Fearfangs Cavern","Buried Sands","Mtharnaz","Serpent's Nest","Ruins of Kardala","Tombs of the Na-Totambu","Loth'Na Caverns","Rkhardahrk","Zalgaz's Den","Exarch's Stronghold","The Howling Sepulchers","Ilthag's Undertower","Hircine's Haunt","Chiselshriek Mine","Rkundzelft","Haddock's Market","Balamath","Molavar"],
        "requires": "Craglorn Access",
    },
    "Coldharbour": {
        "locations": "Coldharbour",
        "exits": ["Stirk"],
        "requires": "Coldharbour Access",
    },
    #Delves
    #Glenumbra
    "Ilessan Tower": {
        "locations": "Ilessan Tower",
        "exits": ["Glenumbra"],
        "requires": "Ilessan Tower Access",
    },
    "Silumm": {
        "locations": "Silumm",
        "exits": ["Glenumbra"],
        "requires": "Silumm Access",
    },
    "The Mines of Khuras": {
        "locations": "The Mines of Khuras",
        "exits": ["Glenumbra"],
        "requires": "The Mines of Khuras Access",
    },
    "Enduum": {
        "locations": "Enduum",
        "exits": ["Glenumbra"],
        "requires": "Enduum Access",
    },
    "Ebon Crypt": {
        "locations": "Ebon Crypt",
        "exits": ["Glenumbra"],
        "requires": "Ebon Crypt Access",
    },
    "Cryptwatch": {
        "locations": "Cryptwatch",
        "exits": ["Glenumbra"],
        "requires": "Cryptwatch Access",
    },
    #Rivenspire
    "Hildune's Secret Refuge": {
        "locations": "Hildune's Secret Refuge",
        "exits": ["Rivenspire"],
        "requires": "Hildune's Secret Refuge Access",
    },
    "Orc's Finger Ruins": {
        "locations": "Orc's Finger Ruins",
        "exits": ["Rivenspire"],
        "requires": "Orc's Finger Ruins Access",
    },
    "Erokii Ruins": {
        "locations": "Erokii Ruins",
        "exits": ["Rivenspire"],
        "requires": "Erokii Ruins Access",
    },
    "Crestshade Mines": {
        "locations": "Crestshade Mines",
        "exits": ["Rivenspire"],
        "requires": "Crestshade Mines Access",
    },
    "Flyleaf Catacombs": {
        "locations": "Flyleaf Catacombs",
        "exits": ["Rivenspire"],
        "requires": "Flyleaf Catacombs Access",
    },
    "Tribulation Crypt": {
        "locations": "Tribulation Crypt",
        "exits": ["Rivenspire"],
        "requires": "Tribulation Crypt Access",
    },
    #Stormhaven
    "Bearclaw Mine": {
        "locations": "Bearclaw Mine",
        "exits": ["Stormhaven"],
        "requires": "Bearclaw Mine Access",
    },
    "Norvulk Ruins": {
        "locations": "Norvulk Ruins",
        "exits": ["Stormhaven"],
        "requires": "Norvulk Ruins Access",
    },
    "Pariah Catacombs": {
        "locations": "Pariah Catacombs",
        "exits": ["Stormhaven"],
        "requires": "Pariah Catacombs Access",
    },
    "Farangel's Delve": {
        "locations": "Farangel's Delve",
        "exits": ["Stormhaven"],
        "requires": "Farangel's Delve Access",
    },
    "Portdun Watch": {
        "locations": "Portdun Watch",
        "exits": ["Stormhaven"],
        "requires": "Portdun Watch Access",
    },
    "Koeglin Mine": {
        "locations": "Koeglin Mine",
        "exits": ["Stormhaven"],
        "requires": "Koeglin Mine Access",
    },
    #Bankorai
    "Troll's Toothpick": {
        "locations": "Troll's Toothpick",
        "exits": ["Bankorai"],
        "requires": "Troll's Toothpick Access",
    },
    "Torog's Spite": {
        "locations": "Torog's Spite",
        "exits": ["Bankorai"],
        "requires": "Torog's Spite Access",
    },
    "Viridian Watch": {
        "locations": "Viridian Watch",
        "exits": ["Bankorai"],
        "requires": "Viridian Watch Access",
    },
    "Crypt of the Exiles": {
        "locations": "Crypt of the Exiles",
        "exits": ["Bankorai"],
        "requires": "Crypt of the Exiles Access",
    },
    "Rubble Butte": {
        "locations": "Rubble Butte",
        "exits": ["Bankorai"],
        "requires": "Rubble Butte Access",
    },
    "Klathzgar": {
        "locations": "Klathzgar",
        "exits": ["Bankorai"],
        "requires": "Klathzgar Access",
    },
    #Alik'r Desert
    "Santaki": {
        "locations": "Santaki",
        "exits": ["Alik'r Desert"],
        "requires": "Santaki Access",
    },
    "Divad's Chagrin Mine": {
        "locations": "Divad's Chagrin Mine",
        "exits": ["Alik'r Desert"],
        "requires": "Divad's Chagrin Mine Access",
    },
    "Aldunz": {
        "locations": "Aldunz",
        "exits": ["Alik'r Desert"],
        "requires": "Aldunz Access",
    },
    "Sandblown Mine": {
        "locations": "Sandblown Mine",
        "exits": ["Alik'r Desert"],
        "requires": "Sandblown Mine Access",
    },
    "Yldzuun": {
        "locations": "Yldzuun",
        "exits": ["Alik'r Desert"],
        "requires": "Yldzuun Access",
    },
    "Coldrock Digging": {
        "locations": "Coldrock Digging",
        "exits": ["Alik'r Desert"],
        "requires": "Coldrock Digging Access",
    },
    #Auridon
    "Mehrunes' Spite": {
        "locations": "Mehrunes' Spite",
        "exits": ["Auridon"],
        "requires": "Mehrunes' Spite Access",
    },
    "Wansalen": {
        "locations": "Wansalen",
        "exits": ["Auridon"],
        "requires": "Wansalen Access",
    },
    "Bewan": {
        "locations": "Bewan",
        "exits": ["Auridon"],
        "requires": "Bewan Access",
    },
    "Entila's Folly": {
        "locations": "Entila's Folly",
        "exits": ["Auridon"],
        "requires": "Entila's Folly Access",
    },
    "Ondil": {
        "locations": "Ondil",
        "exits": ["Auridon"],
        "requires": "Ondil Access",
    },
    "Del's Claim": {
        "locations": "Del's Claim",
        "exits": ["Auridon"],
        "requires": "Del;s Claim Access",
    },
    #Grahtwood
    "Wormroot Depths": {
        "locations": "Wormroot Depths",
        "exits": ["Grahtwood"],
        "requires": "Wormroot Depths Access",
    },
    "Vinedeath Cave": {
        "locations": "",
        "exits": ["Grahtwood"],
        "requires": " Access",
    },
    "Burroot Kwama Mine": {
        "locations": "Burroot Kwama Mine",
        "exits": ["Grahtwood"],
        "requires": "Burroot Kwama Mine Access",
    },
    "The Scuttle Pit": {
        "locations": "The Scuttle Pit",
        "exits": ["Grahtwood"],
        "requires": "The Scuttle Pit Access",
    },
    "Mobar Mine": {
        "locations": "Mobar Mine",
        "exits": ["Grahtwood"],
        "requires": "Mobar Mine Access",
    },
    "Ne Salas": {
        "locations": "Ne Salas",
        "exits": ["Grahtwood"],
        "requires": "Ne Salas Access",
    },
    #Greenshade
    "Barrow Trench": {
        "locations": "Barrow Trench",
        "exits": ["Greenshade"],
        "requires": "Barrow Trench Access",
    },
    "The Underroot": {
        "locations": "The Underroot",
        "exits": ["Greenshade"],
        "requires": "The Underroot Access",
    },
    "Harridan's Lair": {
        "locations": "Harridan's Lair",
        "exits": ["Greenshade"],
        "requires": "Harridan's Lair Access",
    },
    "Gurzag's Mine": {
        "locations": "Gurzag's Mine",
        "exits": ["Greenshade"],
        "requires": "Gurzag's Mine Access",
    },
    "Naril Nagaia": {
        "locations": "Naril Nagaia",
        "exits": ["Greenshade"],
        "requires": "Naril Nagaia Access",
    },
    "Carac Dena": {
        "locations": "Carac Dena",
        "exits": ["Greenshade"],
        "requires": "Carac Dena Access",
    },
    #Malabal Tor
    "Black Vine Ruins": {
        "locations": "Black Vine Ruins",
        "exits": ["Malabal Tor"],
        "requires": "Black Vine Ruins Access",
    },
    "Roots of Silvenar": {
        "locations": "Roots of Silvenar",
        "exits": ["Malabal Tor"],
        "requires": "Roots of Silvenar Access",
    },
    "Shael Ruins": {
        "locations": "Shael Ruins",
        "exits": ["Malabal Tor"],
        "requires": "Shael Ruins Access",
    },
    "Tomb of the Apostates": {
        "locations": "Tomb of the Apostates",
        "exits": ["Malabal Tor"],
        "requires": "Tomb of the Apostates Access",
    },
    "Hoarvor Pit": {
        "locations": "Hoarvor Pit",
        "exits": ["Malabal Tor"],
        "requires": "Hoarvor Pit Access",
    },
    "Dead Man's Drop": {
        "locations": "Dead Man's Drop",
        "exits": ["Malabal Tor"],
        "requires": "Dead Man's Drop Access",
    },
    #Reaper's March
    "Fardir's Folly": {
        "locations": "Fardir's Folly",
        "exits": ["Reaper's March"],
        "requires": "Fardir's Folly Access",
    },
    "Kuna's Delve": {
        "locations": "Kuna's Delve",
        "exits": ["Reaper's March"],
        "requires": "Kuna's Delve Access",
    },
    "Jode's Light": {
        "locations": "Jode's Light",
        "exits": ["Reaper's March"],
        "requires": "Jode's Light Access",
    },
    "Thibaut's Cairn": {
        "locations": "Thibaut's Cairn",
        "exits": ["Reaper's March"],
        "requires": "Thibaut's Cairn Access",
    },
    "Claw's Strike": {
        "locations": "Claw's Strike",
        "exits": ["Reaper's March"],
        "requires": "Claw's Strike Access",
    },
    "Weeping Wind Cave": {
        "locations": "Weeping Wind Cave",
        "exits": ["Reaper's March"],
        "requires": "Weeping Wind Cave Access",
    },
    #Stonefalls
    "Inner Sea Armature": {
        "locations": "Inner Sea Armature",
        "exits": ["Stonefalls"],
        "requires": "Inner Sea Armature Access",
    },
    "Emberflint Mine": {
        "locations": "Emberflint Mine",
        "exits": ["Stonefalls"],
        "requires": "Emberflint Mine Access",
    },
    "Mephala's Nest": {
        "locations": "Mephala's Nest",
        "exits": ["Stonefalls"],
        "requires": "Mephala's Nest Access",
    },
    "Hightide Hollow": {
        "locations": "Hightide Hollow",
        "exits": ["Stonefalls"],
        "requires": "Hightide Hollow Access",
    },
    "Softloam Cavern": {
        "locations": "Softloam Cavern",
        "exits": ["Stonefalls"],
        "requires": "Softloam Cavern Access",
    },
    "Sheogorath's Tongue": {
        "locations": "Sheogorath's Tongue",
        "exits": ["Stonefalls"],
        "requires": "Sheogorath's Tongue Access",
    },
    #Deshaan
    "Knife Ear Grotto": {
        "locations": "Knife Ear Grotto",
        "exits": ["Deshaan"],
        "requires": "Knife Ear Grotto Access",
    },
    "The Corpse Garden": {
        "locations": "The Corpse Garden",
        "exits": ["Deshaan"],
        "requires": "The Corpse Garden Access",
    },
    "Triple Circle Mine": {
        "locations": "Triple Circle Mine",
        "exits": ["Deshaan"],
        "requires": "Triple Circle Mine Access",
    },
    "Taleon's Crag": {
        "locations": "Taleon's Crag",
        "exits": ["Deshaan"],
        "requires": "Taleon's Crag Access",
    },
    "Lady Llarel's Shelter": {
        "locations": "Lady Llarel's Shelter",
        "exits": ["Deshaan"],
        "requires": "Lady Llarel's Shelter Access",
    },
    "Lower Bthanual": {
        "locations": "Lower Bthanual",
        "exits": ["Deshaan"],
        "requires": "Lower Bthanual Access",
    },
    #Shadowfen
    "Shrine of the Black Maw": {
        "locations": "Shrine of the Black Maw",
        "exits": ["Shadowfen"],
        "requires": "Shrine of the Black Maw Access",
    },
    "Broken Tusk": {
        "locations": "Broken Tusk",
        "exits": ["Shadowfen"],
        "requires": "Broken Tusk Access",
    },
    "Grandranen Ruins": {
        "locations": "Grandranen Ruins",
        "exits": ["Shadowfen"],
        "requires": "Grandranen Ruins Access",
    },
    "Atanaz Ruins": {
        "locations": "Atanaz Ruins",
        "exits": ["Shadowfen"],
        "requires": "Atanaz Ruins Access",
    },
    "Onkobra Kwama Mine": {
        "locations": "Onkobra Kwama Mine",
        "exits": ["Shadowfen"],
        "requires": "Onkobra Kwama Mine Access",
    },
    "Chid-Moska Ruins": {
        "locations": "Chid-Moska Ruins",
        "exits": ["Shadowfen"],
        "requires": "Chid-Moska Ruins Access",
    },
    #Eastmarch
    "The Chill Hollow": {
        "locations": "The Chill Hollow",
        "exits": ["Eastmarch"],
        "requires": "The Chill Hollow Access",
    },
    "Icehammer's Vault": {
        "locations": "IceHammer's Vault",
        "exits": ["Eastmarch"],
        "requires": "Icehammer's Vault Access",
    },
    "The Bastard's Tomb": {
        "locations": "The Bastard's Tomb",
        "exits": ["Eastmarch"],
        "requires": "The Bastard's Tomb Access",
    },
    "Stormcrag Crypt": {
        "locations": "Stormcrag Crypt",
        "exits": ["Eastmarch"],
        "requires": "Stormcrag Crypt Access",
    },
    "Old Sord's Cave": {
        "locations": "Old Sord's Cave",
        "exits": ["Eastmarch"],
        "requires": "Old Sord's Cave Access",
    },
    "The Frigid Grotto": {
        "locations": "The Frigid Grotto",
        "exits": ["Eastmarch"],
        "requires": "The Frigid Grotto Access",
    },
    #The Rift
    "Broken Helm Hollow": {
        "locations": "Broken Helm Hollow",
        "exits": ["The Rift"],
        "requires": "Broken Helm Hollow Access",
    },
    "Fort Greenwall": {
        "locations": "Fort Greenwall",
        "exits": ["The Rift"],
        "requires": "Fort Greenwall Access",
    },
    "Faldar's Tooth": {
        "locations": "Faldar's Tooth",
        "exits": ["The Rift"],
        "requires": "Faldar's Tooth Access",
    },
    "Avanchnzel": {
        "locations": "Avanchnzel",
        "exits": ["The Rift"],
        "requires": "Avanchnzel Access",
    },
    "Snapleg Cave": {
        "locations": "Snapleg Cave",
        "exits": ["The Rift"],
        "requires": "Snapleg Cave Access",
    },
    "Shroud Hearth Barrow": {
        "locations": "Shroud Hearth Barrow",
        "exits": ["The Rift"],
        "requires": "Shroud Hearth Barrow Access",
    },
    #Craglorn
    "Fearfangs Cavern": {
        "locations": "Fearfangs Cavern",
        "exits": ["Craglorn"],
        "requires": "Fearfangs Cavern Access",
    },
    "Buried Sands": {
        "locations": "Buried Sands",
        "exits": ["Craglorn"],
        "requires": "Buried Sands Access",
    },
    "Mtharnaz": {
        "locations": "Mtharnaz",
        "exits": ["Craglorn"],
        "requires": "Mtharnaz Access",
    },
    "Serpent's Nest": {
        "locations": "Serpent's Nest",
        "exits": ["Craglorn"],
        "requires": "Serpent's Nest Access",
    },
    "Ruins of Kardala": {
        "locations": "Ruins of Kardala",
        "exits": ["Craglorn"],
        "requires": "Ruins of Kardala Access",
    },
    "Tombs of the Na-Totambu": {
        "locations": "Tombs of the Na-Totambu",
        "exits": ["Craglorn"],
        "requires": "Tombs of the Na-Totambu Access",
    },
    "Loth'Na Caverns": {
        "locations": "Loth'Na Caverns",
        "exits": ["Craglorn"],
        "requires": "Loth'Na Caverns Access",
    },
    "Rkhardahrk": {
        "locations": "Rkhardahrk",
        "exits": ["Craglorn"],
        "requires": "Rkhardahrk Access",
    },
    "Zalgaz's Den": {
        "locations": "Zalgaz's Den",
        "exits": ["Craglorn"],
        "requires": "Zalgaz's Den Access",
    },
    "Exarch's Stronghold": {
        "locations": "Exarch's Stronghold",
        "exits": ["Craglorn"],
        "requires": "Exarch's Stronghold Access",
    },
    "The Howling Sepulchers": {
        "locations": "The Howling Sepulchers",
        "exits": ["Craglorn"],
        "requires": "The Howling Sepulchers Access",
    },
    "Ilthag's Undertower": {
        "locations": "Ilthag's Undertower",
        "exits": ["Craglorn"],
        "requires": "Ilthag's Undertower Access",
    },
    "Hircine's Haunt": {
        "locations": "Hircine's Haunt",
        "exits": ["Craglorn"],
        "requires": "Hircine's Haunt Access",
    },
    "Chiselshriek Mine": {
        "locations": "Chiselshriek Mine",
        "exits": ["Craglorn"],
        "requires": "Chiselshriek Mine Access",
    },
    "Rkundzelft": {
        "locations": "Rkundzelft",
        "exits": ["Craglorn"],
        "requires": "Rkundzelft Access",
    },
    "Haddock's Market": {
        "locations": "Haddock's Market",
        "exits": ["Craglorn"],
        "requires": "Haddock's Market Access",
    },
    "Balamath": {
        "locations": "Balamath",
        "exits": ["Craglorn"],
        "requires": "Balamath Access",
    },
    "Molavar": {
        "locations": "Molavar",
        "exits": ["Craglorn"],
        "requires": "Molavar Access",
    },
    #Non Zone
    "Main Quest": {
        "locations": "Main Quest",
        "exits": ["Menu","Stirk"],
    },
}


def get_delves_for_zone(zone: str) -> List[str]:
    """Get all delves in a zone by checking region exits."""
    delves = []

    zone_data = REGION_GRAPH.get(zone, {})
    exits = zone_data.get("exits", [])

    for exit_region in exits:
        # Skip if it's a main zone
        if exit_region in ALL_ZONES:
            continue

        # Check if this exit is a delve (has exactly one exit back to parent)
        exit_data = REGION_GRAPH.get(exit_region, {})
        exit_exits = exit_data.get("exits", [])

        # Delves have exactly 1 exit (back to parent zone)
        if len(exit_exits) == 1 and exit_exits[0] == zone:
            delves.append(exit_region)

    return delves


def get_required_delves_for_zone(zone: str) -> Set[str]:
    """Get delves required for quests in this zone."""
    return REQUIRED_DELVES_FOR_QUESTS.get(zone, set())

def create_regions(world: "ESOWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player
    selected_zones: Set[str] = world.selected_zones

    # Special regions that are always included
    always_include = {"Menu", "Main Quest"}

    if "Coldharbour" in selected_zones:
        always_include.add("Stirk")

    # Determine which regions to create
    regions_to_create: Set[str] = selected_zones | always_include | world.selected_delves

    print("=== SELECTED ZONES ===")
    print(f"Creating regions for: {sorted(regions_to_create)}")
    print(f"Including {len(world.selected_delves)} delves")  # Optional debug line

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

                if world.options.zone_quests_enabled:
                    skip_location = False
                    # Only check delve requirements if delves are randomized
                    if world.options.delves_per_region.value > 0:
                        # Check all zones for quest-delve requirements
                        for zone_name, quest_delve_map in ZONE_QUEST_REQUIRED_DELVES.items():
                            if loc_name in quest_delve_map:
                                required_delves = quest_delve_map[loc_name]  # Set[str]
                                # Check if ALL required delves are in selected_delves
                                if not required_delves.issubset(world.selected_delves):
                                    skip_location = True
                                    break
                    if skip_location:
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

