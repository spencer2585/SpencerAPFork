import worlds.LauncherComponents as LauncherComponents
from typing import List, Set, Dict, Optional
from collections import deque
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Type, components, launch_subprocess, icon_paths
from .Items import ESOItem, ESOItemData, get_items_by_category, item_table, get_starting_region_item_name
from .Locations import ESOLocation, location_table
from .eso_options import (
    ESOOptions, Alliance, GOAL_ZONE_NAMES
)
from .Regions import (
    create_regions, REGION_GRAPH, ALL_ZONES, ALLIANCE_STARTING_ZONES,
    ZONE_FINAL_QUESTS, MAIN_QUEST_REQUIRED_ZONES, ZONE_FINAL_QUEST_REQUIREMENTS,
    get_achievable_main_quest_locations, get_max_progressive_main_quest,
    is_final_quest_achievable
)
from .Rules import set_rules
from .Goals import set_goals

from worlds.LauncherComponents import Component


def run_client(*args):
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
    against various enemys
    """
    game = "Elder Scrolls Online"
    options_dataclass = ESOOptions
    options: ESOOptions
    required_client_version = (0, 0, 1)
    web = ESOWeb()

    # Instance variables set in generate_early
    selected_zones: Set[str]
    goal_zone: Optional[str]
    achievable_main_quests: List[str]
    max_progressive_mq: int

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}

    def generate_early(self):
        """Determine which zones to include and select goal zone."""
        alliance = self.options.alliance.value
        starting_zone = ALLIANCE_STARTING_ZONES[alliance]

        #initial zone pool
        if self.options.included_zones.value:
            available_zones = set(self.options.included_zones.value)
        else:
            available_zones = set(ALL_ZONES)

        #Determine required zones based on goal
        required_zones: Set[str] = {starting_zone}

        if self.options.goal.value == 0:  # main_quest
            # Main quest requires specific zones
            required_zones.update(MAIN_QUEST_REQUIRED_ZONES[alliance])
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

        #Validate that required zones are available
        missing_zones = required_zones - available_zones
        if missing_zones:
            raise Exception(
                f"ESO: Required zones are not in included zones: {missing_zones}. "
                f"Your starting zone ({starting_zone}) and goal zone must be available."
            )

        #Find path from starting zone to goal and ensure connectivity
        if self.options.goal.value == 0:  # main_quest
            # For main quest, ensure path exists to Coldharbour (the final zone)
            path = self._find_path(starting_zone, "Coldharbour", available_zones)
            if path is None:
                raise Exception(
                    f"ESO: No valid path exists from {starting_zone} to Coldharbour "
                    f"with your zone configuration. Main Quest requires reaching Coldharbour."
                )
            required_zones.update(path)
        else:  # final_zone_quest
            path = self._find_path(starting_zone, self.goal_zone, available_zones)
            if path is None:
                raise Exception(
                    f"ESO: No valid path exists from {starting_zone} to {self.goal_zone} "
                    f"with your zone configuration. Check your included/excluded zones."
                )
            required_zones.update(path)

        #Select zones based on zone_count
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

        #Filter to only zones reachable from the starting zone
        reachable_zones = self._get_reachable_zones(starting_zone, self.selected_zones)
        unreachable = self.selected_zones - reachable_zones
        if unreachable:
            print(f"ESO Warning: Removing unreachable zones: {unreachable}")
            self.selected_zones = reachable_zones

        #ensure goal is still reachable
        if self.options.goal.value == 0:  # main_quest
            if "Coldharbour" not in self.selected_zones:
                raise Exception(
                    f"ESO: Coldharbour is not reachable from {starting_zone} with the selected zones. "
                    f"Main Quest goal requires Coldharbour to be accessible."
                )
        elif self.goal_zone and self.goal_zone not in self.selected_zones:
            raise Exception(
                f"ESO: Goal zone {self.goal_zone} is not reachable from {starting_zone}. "
                f"Check your zone configuration."
            )

        #Calculate achievable Main Quest locations based on selected zones
        self.achievable_main_quests = get_achievable_main_quest_locations(alliance, self.selected_zones)
        self.max_progressive_mq = get_max_progressive_main_quest(alliance, self.selected_zones)

        print(f"ESO: Achievable Main Quest locations: {len(self.achievable_main_quests)}")
        print(f"ESO: Max Progressive Main Quest items: {self.max_progressive_mq}")

    def _find_path(self, start: str, end: str, available_zones: Set[str]) -> Optional[Set[str]]:
        #Find a path between two zones using BFS, returning all zones in the path.
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
                if next_zone in ["Menu", "Main Quest"]:
                    continue

                new_path = path + [next_zone]

                if next_zone == end:
                    return set(new_path)

                visited.add(next_zone)
                queue.append((next_zone, new_path))

        return None  # No path found

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

            # Skip zone wayshrine items if option is disabled
            if data.category == "Zone Wayshrines Access" and not self.options.zone_wayshrines_enabled:
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
        }