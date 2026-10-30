from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle,Range, OptionSet

class PrimaryFrames(Range):
    """How many primary Weapon frames to start with"""
    display_name = "Primary Frames"
    range_start = 1
    range_end = 7
    default = 3

class SpecialFrames(Range):
    """How many Special Weapon frames to start with"""
    display_name = "Special Frames"
    range_start = 0
    range_end = 9
    default = 2

class PowerFrames(Range):
    """How many power Weapon frames to start with"""
    display_name = "Power Frames"
    range_start = 1
    range_end = 7
    default = 1


class IncludedRareSpecialFrames(OptionSet):
    """What rare Special Weapon frames to count as valid starting frames
    Valid Keys: Sidearm, Pulse Rifle, Hand Cannon, Trace Rifle"""
    display_name = "Include Rare Special Frames"
    valid_keys = frozenset(["Sidearm", "Pulse Rifle", "Hand Cannon", "Trace Rifle"])

class IncludedRarePowerFrames(OptionSet):
    """What rare power weapon frames to count as valid starting frames
    Valid Keys: Bow, Sniper Rifle
    """
    display_name = "Include Rare Power Frames"
    valid_keys = frozenset(["Bow", "Sniper Rifle"])

class PinnacleOps(Toggle):
    """If Pinnacle Ops missions should be included in the randomizer"""
    display_name = "Include Pinnacle Ops"
    default = False

class IncludedDLC(OptionSet):
    """What DLC to include
    valid keys: Forsaken, Shadowkeep, Beyond Light, 30th Anniversary, Lightfall, Final Shape, Edge of Fate, Renegades"""
    display_name = "Included DLC"
    valid_keys = frozenset(["Forsaken","Shadowkeep","Beyond Light","30th Anniversary","Lightfall","Final Shape","Edge of Fate","Renegades"])


@dataclass
class D2Options(PerGameCommonOptions):
    primary_frames: PrimaryFrames
    special_frames: SpecialFrames
    power_frames: PowerFrames
    rare_special_frames: IncludedRareSpecialFrames
    rare_power_frames: IncludedRarePowerFrames
    pinnacle_ops: PinnacleOps
    included_dlc: IncludedDLC