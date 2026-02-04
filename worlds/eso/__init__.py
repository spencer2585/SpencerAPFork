import worlds.LauncherComponents as LauncherComponents
from typing import List
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Type, components, launch_subprocess, icon_paths
from .Items import ESOItem, ESOItemData, get_items_by_category, item_table, get_starting_region_item_name
from .Locations import ESOLocation, location_table
from .eso_options import ESOOptions, Alliance
from .Regions import create_regions
from .Rules import set_rules
from .Goals import set_goals

from worlds.LauncherComponents import Component


def run_client(*args):
    print("Running ESO Client")
    print("run_client args:", args)
    from .client import launch
    launch_subprocess(launch, name="ESOClient", args=args)

components.append(
    Component("ESO Client", func=run_client, component_type=Type.CLIENT)
)

class ESOWeb(WebWorld):
    theme = 'stone'
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to set up ESO for AP",
        "English",
        "eso_en.md",
        "eso/en",
        ["Spencer2585"]
    )]

class ESOWorld(World):
    """
    Elder Scrolls Online is a MMORPG Set in the world of The elder Scrolls. Journey across the reagons of Tamriel while fighting
    against various enimys
    """
    game = "Elder Scrolls Online"
    options_dataclass = ESOOptions
    options: ESOOptions
    required_client_version = (0, 0, 1)
    web = ESOWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}

    def generate_location_name_to_id(self):
        locs = {}
        for name, data in location_table.items():
            # Quest toggle
            if data.loc_type == "zone quest" and not self.options.zone_quests_enabled:
                continue
            # Wayshrine toggle
            if data.loc_type == "wayshrine" and not self.options.wayshrine_checks_enabled:
                continue
            locs[name] = data.code
        return locs

    def create_items(self):
        item_pool: List[ESOItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Determine starting region item based on alliance (exclude from pool)
        alliance_value = self.options.alliance.value
        starting_item_name = get_starting_region_item_name(alliance_value)

        # Build normal item pool, skipping the starting region item
        for name, data in item_table.items():
            if name == starting_item_name:
                continue  # Don't add to pool, will be precollected
            quantity = data.max_quantity
            item_pool += [self.create_item(name) for _ in range(quantity)]

        # Add filler items
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        # Inject starting region item into starting inventory
        self.multiworld.push_precollected(self.create_item(starting_item_name))

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

    def create_item(self, name: str) -> ESOItem:
        data = item_table[name]
        return ESOItem(name, data.classification, data.code, self.player)

    def fill_slot_data(self) -> dict:
        return {
            "Alliance": self.options.alliance.value,
            "ZoneQuestsEnabled": self.options.zone_quests_enabled.value,
            "WayshrineChecksEnabled": self.options.wayshrine_checks_enabled.value,
#            "SkillRandomization": self.options.skill_randomization.value,
        }