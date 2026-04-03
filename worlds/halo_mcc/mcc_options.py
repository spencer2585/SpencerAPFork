from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle

class Skulls(Toggle):
    """Should Skulls be locations"""
    display_name = "Enable Skulls"
    default = True

class Powerups(Toggle):
    """Should Powerups be locations"""
    display_name = "Enable Powerups"
    default = True

@dataclass
class MCCOptions(PerGameCommonOptions):
    skulls: Skulls
    powerups: Powerups