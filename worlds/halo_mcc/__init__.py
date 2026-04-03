from worlds.AutoWorld import World
from .webWorld import webWorld as MCCWeb
from .mcc_options import MCCOptions

from . import locations


class MCCWorld(World):
    """
    yipee
    """

    game = "Halo The Master Chief Collection"
    options_dataclass = MCCOptions
    options: MCCOptions
    required_client_version = (0, 0, 1)
    web = MCCWeb()

    item_name_to_id = items.get_item_name_to_id()
    location_name_to_id = locations.get_location_name_to_id()

    def set_rules(self):


    def create_regions(self):


    def create_items(self):


    def create_item(self, name: str):


    def get_filler_item_name(self):