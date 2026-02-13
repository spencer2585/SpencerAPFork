"""
Myst APWorld - Minimal test version for connection testing
"""
from typing import Dict, Any
from BaseClasses import Region, Entrance, Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld


class MystWeb(WebWorld):
    """Web configuration for Myst"""
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Myst for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["YourName"]
    )]


class MystItem(Item):
    game: str = "Myst"


class MystWorld(World):
    """
    Myst (2021) is a puzzle adventure game where you explore mysterious Ages.
    """
    game = "Myst"
    web = MystWeb()

    # Game metadata
    topology_present = True

    # Item/Location tables (minimal for testing)
    item_name_to_id = {
        "Test Item": 8675309000,
    }

    location_name_to_id = {
        "Test Location": 8675309000,
    }

    def create_item(self, name: str) -> Item:
        """Create an item"""
        item_id = self.item_name_to_id.get(name, None)
        return MystItem(name, ItemClassification.filler, item_id, self.player)

    def create_regions(self) -> None:
        """Create regions"""
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Create a simple test region
        test_region = Region("Test Region", self.player, self.multiworld)
        self.multiworld.regions.append(test_region)

        # Connect menu to test region
        menu.connect(test_region)

        # Add test location
        test_region.locations.append(
            self.create_location("Test Location", test_region)
        )

    def create_location(self, name: str, region: Region):
        """Helper to create a location"""
        from BaseClasses import Location

        class MystLocation(Location):
            game: str = "Myst"

        location_id = self.location_name_to_id.get(name, None)
        return MystLocation(self.player, name, location_id, region)

    def create_items(self) -> None:
        """Create items for the item pool"""
        # Add the test item to the pool
        self.multiworld.itempool.append(self.create_item("Test Item"))

    def set_rules(self) -> None:
        """Set access rules"""
        # No rules for testing
        pass

    def fill_slot_data(self) -> Dict[str, Any]:
        """Data to send to the client"""
        return {
            "death_link": False,
        }