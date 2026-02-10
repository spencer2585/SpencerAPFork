from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Toggle, NamedRange, Range


class XpModifier(NamedRange):
    """Experience modifier for skill leveling"""
    display_name = "Xp Modifier"
    default = 1
    range_start = 16
    range_end = 255
    special_range_names = {
        "normal": default,
        "double": default * 2,
        "Quadruple": default * 4,
    }

class SkillSize(Range):
    """How many skill levels are sent by a skill level item and how many level you have to do to send an item"""
    display_name = "Skill Size"
    default = 5
    range_start = 1
    range_end = 150

@dataclass
class DL4Options(PerGameCommonOptions):
    xp_modifier: XpModifier
    skill_size: SkillSize