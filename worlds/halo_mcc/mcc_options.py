from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice

class SkullSanity(Choice):
    """
    Adds skull disabler items to the item pool. All included skulls are forced
    on at game start; receiving a "Disable X" item lets you toggle that skull off.

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

class CeFinalMission(Choice):
    """What the goal mission for halo CE is"""
    display_name = "Final CE Mission"
    default = 10
    option_pillar_of_autumn = 1
    option_halo = 2
    option_truth_and_reconciliation = 3
    option_silent_cartographer = 4
    option_assault_on_the_control_room = 5
    option_343_guilty_spark = 6
    option_library = 7
    option_two_betrayals = 8
    option_keyes = 9
    option_the_maw = 10
    option_random_choice = 11

@dataclass
class MCCOptions(PerGameCommonOptions):
    skullsanity: SkullSanity
    #powerups: Powerups
    ce_enabled: CeEnabled
    ce_final_mission: CeFinalMission