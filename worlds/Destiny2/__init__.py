from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from typing import ClassVar
from .d2_options import D2Options
from . import rules, items, locations, regions

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
    required_client_version = (0, 0, 1)
    web = D2Web()

    item_name_to_id = items.get_item_name_to_id()
    location_name_to_id = locations.get_location_name_to_id()

    #def set_rules(self):
        #rules.set_rules(self)

    #def create_regions(self):
        #regions.create_regions(self)
        #locations.create_locations(self)

    #def create_items(self):
        #items.create_items(self)
