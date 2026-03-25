from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from typing import ClassVar

class D2Web(WebWorld):
    theme = 'stone'
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to set up ESO for AP",
        "English",
        "eso_en.md",
        "eso/en",
        ["Spencer2585"]
    )]

class D2World(World):
    """
    Elder Scrolls Online is a MMORPG Set in the world of The elder Scrolls. Journey across the regions of Tamriel while fighting
    against various enemies
    """

    game = "Destiny 2"
    options_dataclass = D2Options
    options: D2Options
    required_client_version = (0, 3, 0)
    web = D2Web()
    settings: ClassVar[D2Settings]
