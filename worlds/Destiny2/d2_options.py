from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle


class dummy(Toggle):
    """dummy option"""
    display_name = "dummy"
    default = False


@dataclass
class D2Options(PerGameCommonOptions):
    Dummy:dummy