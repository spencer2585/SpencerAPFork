from dataclasses import dataclass
from typing import FrozenSet

from Options import PerGameCommonOptions, Choice, Toggle, Range, OptionSet

class Alliance(Choice):
    """Which alliance your character belongs to."""
    display_name = "Alliance"
    option_aldmeri_dominion = 0
    option_daggerfall_covenant = 1
    option_ebonheart_pact = 2
    default = 0

class Goal(Choice):
    """What is required to complete the game.
    Main Quest: Complete the base game's main questline (God of Schemes).
    Final Zone Quest: Complete the final quest in the goal zone."""
    display_name = "Goal"
    option_main_quest = 0
    option_final_zone_quest = 1
    option_dungeon_delver = 2
    default = 0

class ZoneCount(Range):
    """Number of zones to include in the randomizer.
    Set to 0 to include all available zones.
    The generator will ensure connectivity from your starting zone to the goal.
    (Note at least 4 are required for main quest goal)"""
    display_name = "Zone Count"
    range_start = 3
    range_end = 22
    default = 7

class IncludedZones(OptionSet):
    """Zones to include in the randomizer pool.
    Leave empty to include all zones.
    Coldharbour is automatically included when required by your goal.
    Valid zones: Stros M'kai, Betnikh, Glenumbra, Stormhaven, Rivenspire, Bangkorai,
    Alik'r Desert, Khenarthi's Roost, Auridon, Grahtwood, Greenshade, Malabal Tor,
    Reaper's March, Bleakrock Isle, Bal Foyen, Stonefalls, Deshaan, Shadowfen,
    Eastmarch, The Rift, Craglorn, Coldharbour"""
    display_name = "Included Zones"
    valid_keys = frozenset([
        "Stros M'kai", "Betnikh", "Glenumbra", "Stormhaven", "Rivenspire",
        "Bangkorai", "Alik'r Desert", "Khenarthi's Roost", "Auridon",
        "Grahtwood", "Greenshade", "Malabal Tor", "Reaper's March",
        "Bleakrock Isle", "Bal Foyen", "Stonefalls", "Deshaan",
        "Shadowfen", "Eastmarch", "The Rift", "Craglorn"
    ])

class GoalZone(Choice):
    """Which zone's final quest is the goal (only used when Goal is set to Final Zone Quest).
    Any: The generator will pick a zone from your included zones.
    Or select a specific zone."""
    display_name = "Goal Zone"
    option_any = 0
    option_betnikh = 1
    option_glenumbra = 2
    option_stormhaven = 3
    option_rivenspire = 4
    option_bangkorai = 5
    option_alikr_desert = 6
    option_auridon = 7
    option_grahtwood = 8
    option_greenshade = 9
    option_malabal_tor = 10
    option_reapers_march = 11
    option_bal_foyen = 12
    option_stonefalls = 13
    option_deshaan = 14
    option_shadowfen = 15
    option_eastmarch = 16
    option_the_rift = 17
    option_craglorn = 18
    option_coldharbour = 19
    default = 0

# Mapping from GoalZone option value to actual zone name
GOAL_ZONE_NAMES = {
    1: "Betnikh",
    2: "Glenumbra",
    3: "Stormhaven",
    4: "Rivenspire",
    5: "Bangkorai",
    6: "Alik'r Desert",
    7: "Auridon",
    8: "Grahtwood",
    9: "Greenshade",
    10: "Malabal Tor",
    11: "Reaper's March",
    12: "Bal Foyen",
    13: "Stonefalls",
    14: "Deshaan",
    15: "Shadowfen",
    16: "Eastmarch",
    17: "The Rift",
    18: "Craglorn",
    19: "Coldharbour",
}

class ZoneQuestsEnabled(Toggle):
    """Enable or disable checks for completing zone quests"""
    display_name = "Enable Zone Quests"
    default = True

class MainQuestsEnabled(Toggle):
    """Enable or disable checks for completing main quests"""
    display_name = "Enable Main Quests"
    default = True

class WayshrineChecksEnabled(Toggle):
    """Enable or disable checks for finding Wayshrine"""
    display_name = "Enable Wayshrine Checks"
    default = True

class DelvesPerRegion(Range):
    """Maximum number of dungeons selected from each unlocked region"""
    display_name = "dungeons_per_region"
    range_start = 0
    range_end = 18
    default = 6

#class DungeonChecksEnabled(Toggle):
#    """Enable or disable checks for completing Dungeons"""
#    display_name = "Enable Dungeon Checks"
#    default = True

class BaseGoldCap(Range):
    """What you want your starting gold cap to be without any items, set to 0 to turn off gold limiting"""
    display_name = "Gold Cap"
    range_start = 0
    range_end = 100000
    default = 1000


@dataclass
class ESOOptions(PerGameCommonOptions):
    alliance: Alliance
    goal: Goal
    zone_count: ZoneCount
    included_zones: IncludedZones
    goal_zone: GoalZone
    main_quests_enabled: MainQuestsEnabled
    zone_quests_enabled: ZoneQuestsEnabled
    wayshrine_checks_enabled: WayshrineChecksEnabled
    delves_per_region:DelvesPerRegion
    gold_cap: BaseGoldCap
#    dungeon_checks_enabled:DungeonChecksEnabled
