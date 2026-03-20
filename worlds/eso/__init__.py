import settings
from typing import ClassVar, Optional, Set
from BaseClasses import Tutorial
from pathlib import Path
from worlds.LauncherComponents import Type, components, launch_subprocess, Component
from worlds.AutoWorld import WebWorld, World
from .eso_options import (
    ESOOptions, Alliance, GOAL_ZONE_NAMES, Goal
)
from . import regions, locations, items, rules, earlyGeneration, goals


def run_client(*args):
    from .client import launch
    launch_subprocess(launch, name="ESOClient", args=args)

components.append(
    Component("ESO Client", func=run_client, component_type=Type.CLIENT)
)

class EsoSettings(settings.Group):
    class ModsFolder(settings.UserFolderPath):
        description = "Path to the Elder Scrolls Online mods folder (note point to live folder not addons)"

    mods_folder: ModsFolder = ModsFolder(Path.home() / "Documents" / "Elder Scrolls Online")

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
    Elder Scrolls Online is a MMORPG Set in the world of The elder Scrolls. Journey across the regions of Tamriel while fighting
    against various enemies
    """

    game = "Elder Scrolls Online"
    options_dataclass = ESOOptions
    options: ESOOptions
    required_client_version = (0, 3, 0)
    web = ESOWeb()
    settings: ClassVar[EsoSettings]


    item_name_to_id = items.get_item_name_to_id()
    location_name_to_id = locations.get_location_name_to_id()

    selected_zones: Set[str]
    goal_zone: Optional[str]
    selected_delves: Set[str]
    max_main_quest: int

    def generate_early(self):
        earlyGeneration.generate_early(self)

    def set_rules(self):
        rules.create_rules(self)
        goals.set_goal(self)

    def create_regions(self):
        regions.create_regions(self)
        locations.create_locations(self)

    def create_items(self):
        items.create_items(self)

    def create_item(self, name: str):
        return items.create_item_with_data(self, name)

    def get_filler_item_name(self):
        return items.get_filler_item_name(self)

    def fill_slot_data(self):
        return{
            "seed": str(self.multiworld.seed),
            "Alliance": self.options.alliance.value,
            "Goal": self.options.goal.value,
            "GoalZone": self.goal_zone,
            "SelectedZones": self.selected_zones,
            "SelectedDelves": self.selected_delves,
            "MainQuestsEnabled": self.options.main_quests_enabled.value,
            "ZoneQuestsEnabled": self.options.zone_quests_enabled.value,
            "WayshrineChecksEnabled": self.options.wayshrine_checks_enabled.value,
            "DelvesNum": self.options.delves_per_region.value,
            "GoldCap": self.options.gold_cap.value,
            "MaxMainQuests": self.max_main_quest,
        }