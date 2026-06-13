from worlds.AutoWorld import World
from .webWorld import MCCWeb
from .mcc_options import MCCOptions
from . import regions, locations, items, rules, goal


class MCCWorld(World):
    """
    yipee
    """

    game = "Halo The Master Chief Collection"
    options_dataclass = MCCOptions
    options: MCCOptions
    required_client_version = (0, 0, 1)
    web = MCCWeb()

    #connects item names to their ID
    item_name_to_id = items.get_item_name_to_id()
    ##same thing as items but for locations
    location_name_to_id = locations.get_location_name_to_id()

    #creates all logic for locations, entrances, and goal      
    def set_rules(self):
        rules.set_rules(self)
        goal.set_goal(self)

    #create regions and place locations inside the regions
    def create_regions(self):
        regions.create_regions(self)
        locations.create_locations(self)

    #creates all items
    def create_items(self):
        items.create_items(self)

    #creates one item with needed information
    def create_item(self, name):
        return items.create_item_with_data(self, name)

    #get the name of a filler item, used to fill unfilled locations
    def get_filler_item_name(self):
        return items.get_filler_item_name(self)

    #fill slot data from yaml options
    def fill_slot_data(self) -> dict:
        return {
            "skullsanity": self.options.skullsanity.value,
        }
