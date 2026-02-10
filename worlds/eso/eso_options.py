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
    default = 0

class ZoneCount(Range):
    """Number of zones to include in the randomizer.
    Set to 0 to include all available zones.
    The generator will ensure connectivity from your starting zone to the goal.
    (Note at least 5 are required for main quest goal)"""
    display_name = "Zone Count"
    range_start = 0
    range_end = 22
    default = 7

class IncludedZones(OptionSet):
    """Zones to include in the randomizer pool.
    Leave empty to include all zones (minus any in Excluded Zones).
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
        "Shadowfen", "Eastmarch", "The Rift", "Craglorn", "Coldharbour"
    ])

class ExcludedZones(OptionSet):
    """Zones to exclude from the randomizer pool.
    These zones will not be included even if listed in Included Zones."""
    display_name = "Excluded Zones"
    valid_keys = frozenset([
        "Stros M'kai", "Betnikh", "Glenumbra", "Stormhaven", "Rivenspire",
        "Bangkorai", "Alik'r Desert", "Khenarthi's Roost", "Auridon",
        "Grahtwood", "Greenshade", "Malabal Tor", "Reaper's March",
        "Bleakrock Isle", "Bal Foyen", "Stonefalls", "Deshaan",
        "Shadowfen", "Eastmarch", "The Rift", "Craglorn", "Coldharbour"
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

class WayshrineChecksEnabled(Toggle):
    """Enable or disable checks for finding Wayshrine"""
    display_name = "Enable Wayshrine Checks"
    default = True

class ZoneWayshrinesEnabled(Toggle):
    """Enable or disable zone wayshrine unlock items.
    When enabled, receiving a zone's wayshrine item unlocks all wayshrines in that zone."""
    display_name = "Enable Zone Wayshrine Unlocks"
    default = False

#class DelveChecksEnabled(Toggle):
#    """Enable or disable checks for completing Delves"""
#    display_name = "Enable Delve Checks"
#    default = True

#class DungeonChecksEnabled(Toggle):
#    """Enable or disable checks for completing Dungeons"""
#    display_name = "Enable Dungeon Checks"
#    default = True


@dataclass
class ESOOptions(PerGameCommonOptions):
    alliance: Alliance
    goal: Goal
    zone_count: ZoneCount
    included_zones: IncludedZones
    excluded_zones: ExcludedZones
    goal_zone: GoalZone
    zone_quests_enabled: ZoneQuestsEnabled
    wayshrine_checks_enabled: WayshrineChecksEnabled
    zone_wayshrines_enabled: ZoneWayshrinesEnabled
#    delve_checks_enabled:DelveChecksEnabled
#    dungeon_checks_enabled:DungeonChecksEnabled
