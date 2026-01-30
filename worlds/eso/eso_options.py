from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle

class Alliance(Choice):
    """Which alliance your character belongs to."""
    display_name = "alliance"
    option_aldmeri_dominion = 0
    option_daggerfall_covenant = 1
    option_ebonheart_pact = 2
    default = 0

class ZoneQuestsEnabled(Toggle):
    """Enable or disable checks for completing zone quests"""
    display_name = "Enable Zone Quests"
    default = True

class WayshrineChecksEnabled(Toggle):
    """Enable or disable checks for finding Wayshrine"""
    display_name = "Enable Wayshrine Checks"
    default = True

#class DelveChecksEnabled(Toggle):
#    """Enable or disable checks for completing Delves"""
#    display_name = "Enable Delve Checks"
#    default = True

#class DungeonChecksEnabled(Toggle):
#    """Enable or disable checks for completing Dungeons"""
#    display_name = "Enable Dungeon Checks"
#    default = True

#class SkillRandomization(Choice):
#    """How you want skills to be randomized
#    None: Skills are not randomized
#    Skyshards: you must receive 3 skyshards to be able to use 1 skill point
#    items: each skill has a corresponding item that must be received before unlocking
#    Both: you must recive 3 skyshards and the corresponding item before unlocking the skill"""
#    display_name = "Skill Randomization"
#    option_none = 0
#    option_skyshards = 1
#    option_items = 2
#    option_both - 3
#    default = 1

#class CharacterClass(Choice):
#    """What class you want your character to be (only used for skill randomization)"""
#    display_name = "Character Class"
#    option_Dragonknight = 1
#    option_Sorcerer = 2
#    option_Nightblade = 3
#    option_Warden = 4
#    option_Necromancer = 5
#    option_Templar = 6
#    option_Arcanist = 7
#    default = 1


@dataclass
class ESOOptions(PerGameCommonOptions):
    alliance: Alliance
    zone_quests_enabled: ZoneQuestsEnabled
    wayshrine_checks_enabled: WayshrineChecksEnabled
#    delve_checks_enabled:DelveChecksEnabled
#    dungeon_checks_enabled:DungeonChecksEnabled
#    skill_randomization: SkillRandomization
#    character_class: CharacterClass
