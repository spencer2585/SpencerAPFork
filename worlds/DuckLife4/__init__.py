import worlds.LauncherComponents as LauncherComponents
from typing import List
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import DL4Item, DL4ItemData, get_items_by_category, item_table
from .Locations import DL4Location, location_table
from .dl4_options import DL4Options
from .Regions import create_regions
from .Rules import set_rules
from .Goals import set_goals

from worlds.LauncherComponents import Component

class DL4Web(WebWorld):
    theme = 'stone'
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to set up Duck Life 4 for AP",
        "English",
        "dl4_en.md",
        "dl4/en",
        ["Spencer2585"]
    )]

class dl4World(World):
    """
    Duck Life 4 is the fourth installment in the popular Duck Life series. Train and race your duck around the globe and become the champion!
    """
    game = "Duck Life 4"
    options_dataclass = DL4Options
    options: DL4Options
    required_client_version = (0, 0, 1)
    web = DL4Web()

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}

    def generate_location_name_to_id(self):
        locs = {}
        for name, data in location_table.items():
            locs[name] = data.code
        return locs

    def create_items(self):
        item_pool: List[DL4Item] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Build normal item pool
        for name, data in item_table.items():
            quantity = data.max_quantity
            item_pool += [self.create_item(name) for _ in range(quantity)]  # Fixed range(0, quantity) → range(quantity)

        # Add filler items
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        # Inject starting region item based on alliance
        self.victory_item = self.create_item("Victory")

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.random.choices(list(fillers.keys()), weights, k=1)[0]

    def set_rules(self):
        set_rules(self)
        set_goals(self)

    def create_regions(self):
        create_regions(self)

    def create_item(self, name: str) -> DL4Item:
        data = item_table[name]
        return DL4Item(name, data.classification, data.code, self.player)

    def fill_slot_data(self) -> dict:
        return {
        }