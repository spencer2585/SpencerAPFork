from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice

#class Skulls(Toggle):
#    """Should Skulls be locations"""
#    display_name = "Enable Skulls"
#    default = True

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
    option_piller_of_autumn = 1
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
    #skulls: Skulls
    #powerups: Powerups
    ce_enabled: CeEnabled
    ce_final_mission: CeFinalMission