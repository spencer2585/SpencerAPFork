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

class SkillRandomization(Choice):
    """How you want skills to be randomized.
    None: Skills are not randomized.
    Skyshards: You must receive 3 skyshards to be able to use 1 skill point.
    Items: Each skill has a corresponding item that must be received before unlocking.
    Both: You must receive 3 skyshards AND the corresponding item before unlocking the skill."""
    display_name = "Skill Randomization"
    option_none = 0
    option_skyshards = 1
    option_items = 2
    option_both = 3
    default = 1

class CharacterClass(Choice):
    """What class your character is (used for skill randomization).
    Your class's skill lines are always included when using item-based skill randomization."""
    display_name = "Character Class"
    option_dragonknight = 0
    option_sorcerer = 1
    option_nightblade = 2
    option_templar = 3
    option_warden = 4
    option_necromancer = 5
    option_arcanist = 6
    default = 0

# Mapping from CharacterClass option value to class name
CLASS_NAMES = {
    0: "Dragonknight",
    1: "Sorcerer",
    2: "Nightblade",
    3: "Templar",
    4: "Warden",
    5: "Necromancer",
    6: "Arcanist",
}

# Mapping from class name to its skill line names
CLASS_SKILL_LINES = {
    "Dragonknight": ["Ardent Flame", "Draconic Power", "Earthen Heart"],
    "Sorcerer": ["Dark Magic", "Daedric Summoning", "Storm Calling"],
    "Nightblade": ["Assassination", "Shadow", "Siphoning"],
    "Templar": ["Aedric Spear", "Dawn's Wrath", "Restoring Light"],
    "Warden": ["Winter's Embrace", "Green Balance", "Animal Companions"],
    "Necromancer": ["Grave Lord", "Bone Tyrant", "Living Death"],
    "Arcanist": ["Herald of the Tome", "Soldier of Apocrypha", "Curative Runeforms"],
}

# All individual class skill lines (21 total - 7 classes x 3 skill lines each)
ALL_CLASS_SKILL_LINES = frozenset([
    skill_line for skill_lines in CLASS_SKILL_LINES.values() for skill_line in skill_lines
])

class CharacterRace(Choice):
    """What race your character is (used for skill randomization).
    Any Race: Picks any race randomly.
    Any Alliance Race: Picks a random race from your chosen alliance."""
    display_name = "Character Race"
    option_any_race = 0
    option_any_alliance_race = 1
    option_argonian = 2
    option_breton = 3
    option_dark_elf = 4
    option_high_elf = 5
    option_imperial = 6
    option_khajiit = 7
    option_nord = 8
    option_orc = 9
    option_redguard = 10
    option_wood_elf = 11
    default = 0

# Mapping from CharacterRace option value to race name
RACE_NAMES = {
    2: "Argonian",
    3: "Breton",
    4: "Dark Elf",
    5: "High Elf",
    6: "Imperial",
    7: "Khajiit",
    8: "Nord",
    9: "Orc",
    10: "Redguard",
    11: "Wood Elf",
}

# All races list for random selection
ALL_RACES = list(RACE_NAMES.values())

# Alliance values: 0 = Aldmeri Dominion, 1 = Daggerfall Covenant, 2 = Ebonheart Pact
ALLIANCE_RACES = {
    0: ["High Elf", "Wood Elf", "Khajiit"],  # Aldmeri Dominion races
    1: ["Breton", "Redguard", "Orc"],  # Daggerfall Covenant races
    2: ["Nord", "Dark Elf", "Argonian"],  # Ebonheart Pact races
}

# All weapon skill lines
ALL_WEAPON_SKILL_LINES = frozenset([
    "Two Handed", "One Hand and Shield", "Dual Wield", "Bow",
    "Destruction Staff", "Restoration Staff"
])

class WeaponSkillLines(OptionSet):
    """Weapon skill lines to include in randomization.
    Leave empty and set weapon_selection to 'random two' for 2 random weapons, or 'all' for all weapons.
    Or select specific weapons to include."""
    display_name = "Weapon Skill Lines"
    valid_keys = ALL_WEAPON_SKILL_LINES

class WeaponSelection(Choice):
    """How to select weapon skill lines.
    Manual: Use the weapons specified in Weapon Skill Lines option.
    Random Two: Randomly select 2 weapon skill lines.
    All: Include all weapon skill lines."""
    display_name = "Weapon Selection"
    option_manual = 0
    option_random_two = 1
    option_all = 2
    default = 1

# All armor skill lines
ALL_ARMOR_SKILL_LINES = frozenset([
    "Light Armor", "Medium Armor", "Heavy Armor"
])

class ArmorSkillLines(OptionSet):
    """Armor skill lines to include in randomization.
    Leave empty and set armor_selection to 'all' for all armor types.
    Or select specific armor types to include."""
    display_name = "Armor Skill Lines"
    valid_keys = ALL_ARMOR_SKILL_LINES

class ArmorSelection(Choice):
    """How to select armor skill lines.
    Manual: Use the armor types specified in Armor Skill Lines option.
    All: Include all armor skill lines."""
    display_name = "Armor Selection"
    option_manual = 0
    option_all = 1
    default = 1

# All racial skill lines
ALL_RACIAL_SKILL_LINES = frozenset([
    "Argonian", "Breton", "Dark Elf", "High Elf", "Imperial",
    "Khajiit", "Nord", "Orc", "Redguard", "Wood Elf"
])

# Misc skill lines (guilds, world skills - NOT weapons, armor, or racial)
ALL_MISC_SKILL_LINES = frozenset([
    # Guild skills
    "Fighters Guild", "Mages Guild",
    # World skills
    "Soul Magic", "Legerdemain", "Vampirism", "Lycanthropy",
    #Cafting Skills
    "Alchemy", "Blacksmithing", "Clothing", "Enchanting", "Provisioning", "Woodworking",
])

class MiscSkillLines(OptionSet):
    """Miscellaneous skill lines to include (guilds, world skills).
    By default all are included. Remove skill lines you don't want in the randomizer."""
    display_name = "Misc Skill Lines"
    valid_keys = ALL_MISC_SKILL_LINES
    default = ALL_MISC_SKILL_LINES


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
    skill_randomization: SkillRandomization
    character_class: CharacterClass
    character_race: CharacterRace
    weapon_skill_lines: WeaponSkillLines
    weapon_selection: WeaponSelection
    armor_skill_lines: ArmorSkillLines
    armor_selection: ArmorSelection
    misc_skill_lines: MiscSkillLines
#    delve_checks_enabled:DelveChecksEnabled
#    dungeon_checks_enabled:DungeonChecksEnabled
