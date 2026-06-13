from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice


class SkullSanity(Choice):
    """
    Adds skull disabler items to the item pool. All included skulls are forced
    on at game start; receiving a "Disable X" item lets you toggle that skull off.

    WARNING: Until more location checks are added, enabling skullsanity will
    significantly slow early-game progress. No mission completions can be
    logically checked until enough disablers are in hand to make missions
    beatable. Consider this carefully before enabling.

    off:         No skull items or logic.
    non_scoring: Only 1.00x (non-scoring) skulls included. No logic requirements.
    hard:        All skulls. Logic requires Iron, Black Eye, Blind, Eye Patch,
                 Famine, Foreign, Mythic, Thunderstorm, and Recession disablers
                 before missions are logically beatable.
    harder:      All skulls. Logic requires Iron, Blind, Famine, Foreign, and
                 Mythic disablers before missions are logically beatable.
    laso:        All skulls. No logic requirements; missions are considered
                 beatable with all skulls active.
    """
    display_name = "Skull Sanity"
    option_off = 0
    option_non_scoring = 1
    option_hard = 2
    option_harder = 3
    option_laso = 4
    default = 0

#class Powerups(Toggle):
#    """Should Powerups be locations"""
#    display_name = "Enable Powerups"
#    default = True

class CeEnabled(Toggle):
    """Should CeEnabled be locations"""
    display_name = "Enable Halo CE"
    default = True

@dataclass
class MCCOptions(PerGameCommonOptions):
    skullsanity: SkullSanity
    #powerups: Powerups
    ce_enabled: CeEnabled