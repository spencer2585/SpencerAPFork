import worlds.LauncherComponents as LauncherComponents
import settings
from typing import List, Set, Dict, Optional, ClassVar
from collections import deque
from pathlib import Path
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Type, components, launch_subprocess, icon_paths
from .Items import ESOItem, ESOItemData, get_items_by_category, item_table, get_starting_region_item_name
from .Locations import ESOLocation, location_table
from .eso_options import (
    ESOOptions, Alliance, GOAL_ZONE_NAMES, Goal
)
from .Regions import (
    create_regions, REGION_GRAPH, ALL_ZONES, ALLIANCE_STARTING_ZONES,
    ZONE_FINAL_QUESTS, MAIN_QUEST_REQUIRED_ZONES, ZONE_FINAL_QUEST_REQUIREMENTS,
    get_achievable_main_quest_locations, get_max_progressive_main_quest,
    is_final_quest_achievable, MAIN_QUEST_DELVE_REQUIREMENTS, REQUIRED_DELVES_FOR_QUESTS
)
from .Rules import set_rules
from .Goals import set_goals
from Options import OptionError
from worlds.LauncherComponents import Component


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
    required_client_version = (0, 0, 1)
    web = ESOWeb()
    settings: ClassVar[EsoSettings]

    # Instance variables set in generate_early
    selected_zones: Set[str]
    goal_zone: Optional[str]
    achievable_main_quests: List[str]
    max_progressive_mq: int
    selected_delves: Set[str]

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}

    def generate_early(self):
        """Determine which zones to include and select goal zone."""
        alliance = self.options.alliance.value
        starting_zone = ALLIANCE_STARTING_ZONES[alliance]
        if self.options.goal == Goal.option_final_zone_quest and not self.options.zone_quests_enabled:
            raise OptionError(
                f"Goal is set to final zone quest but zone quests are disabled"
            )

        # Initial zone pool
        if self.options.included_zones.value:
            available_zones = set(self.options.included_zones.value)
        else:
            available_zones = set(ALL_ZONES)

        # Determine required zones based on goal
        required_zones: Set[str] = {starting_zone}

        if self.options.goal.value == 0:  # main_quest
            # Main quest requires specific zones + Coldharbour
            required_zones.update(MAIN_QUEST_REQUIRED_ZONES[alliance])
            required_zones.add("Coldharbour")
            self.goal_zone = None
        else:  # final_zone_quest
            # Determine goal zone
            if self.options.goal_zone.value == 0:  # any/random
                # Pick a random zone from available, exclude starting zone
                potential_goals = available_zones - {starting_zone}
                if not potential_goals:
                    raise Exception(
                        f"ESO: No valid goal zones available. The starting zone ({starting_zone}) "
                        f"cannot be the goal zone. Add more zones to your included zones."
                    )
                self.goal_zone = self.random.choice(list(potential_goals))
            else:
                self.goal_zone = GOAL_ZONE_NAMES[self.options.goal_zone.value]

                # Validate that goal zone is not the starting zone
                if self.goal_zone == starting_zone:
                    raise Exception(
                        f"ESO: Goal zone ({self.goal_zone}) cannot be the same as your starting zone. "
                        f"Choose a different goal zone or use 'any' for random selection."
                    )

            required_zones.add(self.goal_zone)

            # If the goal zone's final quest requires other zones, add those too
            extra_required = ZONE_FINAL_QUEST_REQUIREMENTS.get(self.goal_zone)
            if extra_required:
                for req_zone in extra_required:
                    required_zones.add(req_zone)
                    if req_zone not in available_zones:
                        raise Exception(
                            f"ESO: Goal zone {self.goal_zone}'s final quest requires {req_zone}, "
                            f"but it's not in your available zones. Add {req_zone} to included zones."
                        )

        # Validate that required zones are available
        missing_zones = required_zones - available_zones
        if missing_zones:
            raise Exception(
                f"ESO: Required zones are not in included zones: {missing_zones}. "
                f"Your starting zone ({starting_zone}) and goal zone must be available."
            )

        # Find path from starting zone to goal and ensure connectivity
        if self.options.goal.value == 0:  # main_quest
            # For main quest, Coldharbour is already in required_zones
            path = {starting_zone}
        else:  # final_zone_quest
            if self.goal_zone == "Coldharbour":
                # Coldharbour is accessed via Stirk, handled in validation
                path = {starting_zone}
            else:
                # Normal path finding for non-Coldharbour goals
                path = self._find_path(starting_zone, self.goal_zone, available_zones)
                if path is None:
                    raise Exception(
                        f"ESO: No valid path exists from {starting_zone} to {self.goal_zone} "
                        f"with your zone configuration. Check your included/excluded zones."
                    )
            required_zones.update(path)

        # Select zones based on zone_count
        zone_count = self.options.zone_count.value

        if zone_count == 0:
            # Include all available zones
            self.selected_zones = available_zones
        else:
            # Start with required zones
            self.selected_zones = set(required_zones)

            # Add more zones up to zone_count from available pool
            extra_zones = list(available_zones - self.selected_zones)
            self.random.shuffle(extra_zones)

            while len(self.selected_zones) < zone_count and extra_zones:
                self.selected_zones.add(extra_zones.pop())

            # Warn if we couldn't reach zone_count
            if len(self.selected_zones) < zone_count:
                print(f"ESO Warning: Could only select {len(self.selected_zones)} zones "
                      f"(requested {zone_count}). Check your included/excluded zones.")

        # Filter to only zones reachable from the starting zone
        # SPECIAL CASE: Don't filter out Coldharbour yet - validation will handle it
        zones_to_check = self.selected_zones - {"Coldharbour"}
        reachable_zones = self._get_reachable_zones(starting_zone, zones_to_check)

        # Add Coldharbour back if it was selected (validation will check accessibility)
        if "Coldharbour" in self.selected_zones:
            reachable_zones.add("Coldharbour")

        unreachable = self.selected_zones - reachable_zones
        if unreachable:
            print(f"ESO Warning: Removing unreachable zones: {unreachable}")
            self.selected_zones = reachable_zones

        # Do a preliminary delve selection for validation purposes
        # (Will be finalized after Coldharbour validation)
        self.selected_delves = self._select_delves()

        # Validate and fix Coldharbour accessibility
        self._validate_coldharbour_access()

        # NOW finalize delve selection (in case zones changed during validation)
        self.selected_delves = self._select_delves()
        print(f"ESO: Selected {len(self.selected_delves)} delves from {len(self.selected_zones)} zones")

        # Calculate achievable Main Quest locations based on selected zones and delves
        self.achievable_main_quests = get_achievable_main_quest_locations(alliance, self.selected_zones,
                                                                          self.selected_delves)
        self.max_progressive_mq = get_max_progressive_main_quest(alliance, self.selected_zones, self.selected_delves)

        print(f"ESO: Achievable Main Quest locations: {len(self.achievable_main_quests)}")
        print(f"ESO: Max Progressive Main Quest items: {self.max_progressive_mq}")

    def _find_path(self, start: str, end: str, available_zones: Set[str]) -> Optional[Set[str]]:
        # Find a path between two zones using BFS, returning all zones in the path.

        # Special case: Coldharbour is accessible via Stirk, not direct paths
        if end == "Coldharbour":
            # For Coldharbour, we don't need a traditional path
            # Just return {start, Coldharbour} to indicate it's been considered
            return {start, "Coldharbour"}

        if start == end:
            return {start}

        # BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()

            # Get exits from this zone
            zone_data = REGION_GRAPH.get(current, {})
            exits = zone_data.get("exits", [])

            for next_zone in exits:
                # Skip zones not in available set or already visited
                if next_zone not in available_zones or next_zone in visited:
                    continue
                # Skip special regions
                if next_zone in ["Menu", "Main Quest", "Stirk"]:
                    continue

                new_path = path + [next_zone]

                if next_zone == end:
                    return set(new_path)

                visited.add(next_zone)
                queue.append((next_zone, new_path))

        return None  # No path found

    def _select_delves(self) -> Set[str]:
        """Select which delves to include based on selected zones and options."""
        from .Regions import get_delves_for_zone

        delves_per_region = self.options.delves_per_region.value
        selected_delves = set()

        # If 0, delves are not randomized at all - return empty set
        if delves_per_region == 0:
            return selected_delves

        # Step 1: Force include delves required by goal
        required_delves = set()

        # Main Quest goal requires alliance-specific delve
        if self.options.goal.value == 0:  # main_quest
            alliance = self.options.alliance.value
            required_zone, required_delve = MAIN_QUEST_DELVE_REQUIREMENTS[alliance]
            if required_zone in self.selected_zones:
                required_delves.add(required_delve)
                print(f"ESO: Main Quest requires {required_delve} from {required_zone}")

        # Final Zone Quest goal may require specific delves
        elif self.options.goal.value == 1 and self.goal_zone:  # final_zone_quest
            zone_required = REQUIRED_DELVES_FOR_QUESTS.get(self.goal_zone, set())
            print(f"ESO DEBUG: Goal zone is {self.goal_zone}")
            print(f"ESO DEBUG: Required delves from REQUIRED_DELVES_FOR_QUESTS: {zone_required}")
            if zone_required:
                required_delves.update(zone_required)
                print(
                    f"ESO: Goal zone {self.goal_zone} requires delves, forcing them into randomization: {zone_required}")

        # Add all required delves to selection
        selected_delves.update(required_delves)

        # Step 2: For each zone, select delves up to delves_per_region
        for zone in self.selected_zones:
            available_delves = get_delves_for_zone(zone)
            print(f"ESO DEBUG: Required delves added to selected_delves: {selected_delves}")

            if not available_delves:
                continue

            # Separate into required and non-required for this zone
            zone_required = [d for d in available_delves if d in required_delves]
            zone_optional = [d for d in available_delves if d not in required_delves]

            # Count how many delves from this zone are already selected (required ones)
            already_selected = len([d for d in zone_required if d in selected_delves])

            # Calculate how many more we can add
            remaining_slots = delves_per_region - already_selected

            if remaining_slots > 0 and zone_optional:
                # Randomly select from optional delves
                self.random.shuffle(zone_optional)
                to_add = zone_optional[:remaining_slots]
                selected_delves.update(to_add)

        return selected_delves

    def _get_reachable_zones(self, start: str, available_zones: Set[str]) -> Set[str]:
        #Get all zones reachable from start within available_zones using BFS.
        reachable = {start}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            # Get exits from this zone
            zone_data = REGION_GRAPH.get(current, {})
            exits = zone_data.get("exits", [])

            for next_zone in exits:
                # Skip zones not in available set or already visited
                if next_zone not in available_zones or next_zone in reachable:
                    continue
                # Skip special regions
                if next_zone in ["Menu", "Main Quest"]:
                    continue

                reachable.add(next_zone)
                queue.append(next_zone)

        return reachable

    def _validate_coldharbour_access(self):
        """Validate that Coldharbour is accessible if required, or remove it if not."""

        # If Coldharbour is not in selected zones, nothing to validate
        if "Coldharbour" not in self.selected_zones:
            return

        alliance = self.options.alliance.value

        # Define the three final alliance zones that can access Stirk
        FINAL_ALLIANCE_ZONES = {
            0: "Reaper's March",  # Aldmeri Dominion
            1: "Bangkorai",  # Daggerfall Covenant
            2: "The Rift",  # Ebonheart Pact
        }

        # Check Path 1: Main Quest → Stirk → Coldharbour
        temp_achievable_mq = get_achievable_main_quest_locations(alliance, self.selected_zones, self.selected_delves)
        max_progressive_mq = get_max_progressive_main_quest(alliance, self.selected_zones, self.selected_delves)
        main_quest_path_viable = max_progressive_mq >= 8

        # Check Path 2: Final Alliance Zone → Stirk → Coldharbour
        final_alliance_zone = FINAL_ALLIANCE_ZONES[alliance]
        zone_quest_path_viable = final_alliance_zone in self.selected_zones

        # Determine if Coldharbour is accessible via ANY path
        coldharbour_accessible = main_quest_path_viable or zone_quest_path_viable

        # Check if Coldharbour is the goal zone
        if self.options.goal.value == 1:  # final_zone_quest
            # Check if Coldharbour is the goal zone
            potential_goal_zone = None
            if hasattr(self, 'goal_zone') and self.goal_zone:
                potential_goal_zone = self.goal_zone
            elif self.options.goal_zone and self.options.goal_zone.value != "random":
                potential_goal_zone = self.options.goal_zone.value

            is_coldharbour_goal = potential_goal_zone == "Coldharbour"
        else:
            is_coldharbour_goal = False

        # Handle based on goal type
        if self.options.goal.value == 0:  # main_quest goal
            # Main Quest REQUIRES Coldharbour - must be accessible
            if not coldharbour_accessible:
                # Try to fix it by adding the final alliance zone
                if not zone_quest_path_viable:
                    print(
                        f"ESO: Main Quest goal requires Coldharbour. Adding {final_alliance_zone} to ensure accessibility.")
                    self.selected_zones.add(final_alliance_zone)
                    coldharbour_accessible = True

                # If still not accessible, we have a problem with main quest progression
                if not coldharbour_accessible:
                    error_msg = f"ESO Player {self.player}: Main Quest goal requires Coldharbour, but it is not accessible!\n"
                    error_msg += f"  - Main Quest path requires 8 Progressive Main Quest items, but only {max_progressive_mq} are achievable.\n"
                    error_msg += f"    Missing zones or delves are preventing main quest progression.\n"
                    error_msg += "\nTo fix this, include all zones needed for main quest progression (check alliance requirements)\n"
                    raise Exception(error_msg)

            print(f"ESO: Main Quest goal validated - Coldharbour is accessible")

        elif is_coldharbour_goal:  # final_zone_quest goal with Coldharbour
            # Coldharbour as goal REQUIRES it to be accessible - FIX IT if not
            if not coldharbour_accessible:
                # Try to make it accessible by adding the final alliance zone
                if not zone_quest_path_viable:
                    print(
                        f"ESO: Coldharbour is goal zone but unreachable. Adding {final_alliance_zone} to ensure accessibility.")
                    self.selected_zones.add(final_alliance_zone)
                    coldharbour_accessible = True

                # If still not accessible after adding final zone, the main quest path is broken
                if not coldharbour_accessible:
                    error_msg = f"ESO Player {self.player}: Coldharbour is the goal zone, but cannot be made accessible!\n"
                    error_msg += f"  - Main Quest path requires 8 Progressive Main Quest items, but only {max_progressive_mq} are achievable.\n"
                    error_msg += f"  - Added {final_alliance_zone}, but more zones/delves may be needed for main quest progression.\n"
                    error_msg += "\nTo fix this, either:\n"
                    error_msg += f"  1. Include all zones needed for main quest progression, OR\n"
                    error_msg += f"  2. Choose a different goal zone\n"
                    raise Exception(error_msg)

            print(f"ESO: Coldharbour goal zone validated - accessible via {final_alliance_zone}")



        else:  # Coldharbour is just a selected zone, not the goal

            if not coldharbour_accessible:

                # Remove Coldharbour and try to replace it with another zone

                print(f"ESO Warning: Removing unreachable zones: {{'Coldharbour'}}")

                self.selected_zones.remove("Coldharbour")

                # CRITICAL FIX: If goal_zone was set to Coldharbour, we need to change it

                # This happens when goal_zone is randomly selected before validation runs

                if hasattr(self, 'goal_zone') and self.goal_zone == "Coldharbour":

                    # Pick a new random goal zone from remaining selected zones

                    if self.selected_zones:

                        self.goal_zone = self.random.choice(list(self.selected_zones))

                        print(f"ESO: Changed goal_zone from Coldharbour to {self.goal_zone}")

                    else:

                        # This should never happen, but handle it gracefully

                        raise Exception("ESO: No zones available after removing Coldharbour")

                # Try to add a replacement zone if zone_count was specified

                zone_count = self.options.zone_count.value

                if zone_count > 0 and len(self.selected_zones) < zone_count:

                    # Get available zones that aren't already selected

                    if self.options.included_zones.value:

                        available_zones = set(self.options.included_zones.value)

                    else:

                        available_zones = set(ALL_ZONES)

                    potential_replacements = available_zones - self.selected_zones

                    # Filter to only reachable zones

                    starting_zone = ALLIANCE_STARTING_ZONES[alliance]

                    reachable_replacements = []

                    for zone in potential_replacements:

                        # Check if this zone is reachable from starting zone

                        test_zones = self.selected_zones | {zone}

                        if zone in self._get_reachable_zones(starting_zone, test_zones):
                            reachable_replacements.append(zone)

                    if reachable_replacements:

                        replacement = self.random.choice(reachable_replacements)

                        self.selected_zones.add(replacement)

                        print(f"ESO: Added {replacement} to replace Coldharbour")

                    else:

                        print(f"ESO: No suitable replacement zone found for Coldharbour")

            else:

                # Coldharbour is accessible and in selected zones - all good!

                paths = []

                if main_quest_path_viable:
                    paths.append("main quest")

                if zone_quest_path_viable:
                    paths.append(f"{final_alliance_zone} zone quest")

                print(f"ESO: Coldharbour is accessible via: {', '.join(paths)}")

    def generate_location_name_to_id(self):
        locs = {}
        for name, data in location_table.items():
            # Quest toggle
            if data.loc_type == "zone quest" and not self.options.zone_quests_enabled:
                continue
            locs[name] = data.code
        return locs

    def create_items(self):
        item_pool: List[ESOItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Determine starting region item based on alliance (exclude from pool)
        alliance_value = self.options.alliance.value
        starting_item_name = get_starting_region_item_name(alliance_value)

        # Build normal item pool
        for name, data in item_table.items():
            if name == starting_item_name:
                continue  # Don't add to pool, will be precollected

            # Skip items associated with zones not in selected_zones
            if data.zone is not None and data.zone not in self.selected_zones:
                continue

            if data.category == "Delve Access":
                if self.options.delves_per_region == 0:
                    continue

                delve_name = name.replace(" Access","")
                if delve_name not in self.selected_delves:
                    continue

            # Limit Progressive Main Quest items to what's achievable
            if name == "Progressive Main Quest":
                quantity = self.max_progressive_mq
            else:
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
            "Goal": self.options.goal.value,
            "GoalZone": self.goal_zone,
            "SelectedZones": list(self.selected_zones),
            "ZoneQuestsEnabled": self.options.zone_quests_enabled.value,
            "WayshrineChecksEnabled": self.options.wayshrine_checks_enabled.value,
            "DelvesNum": self.options.delves_per_region.value,
        }