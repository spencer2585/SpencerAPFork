import worlds.LauncherComponents as LauncherComponents
from typing import List, Set, Dict, Optional
from collections import deque
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Type, components, launch_subprocess, icon_paths
from .Items import ESOItem, ESOItemData, get_items_by_category, item_table, get_starting_region_item_name
from .Locations import ESOLocation, location_table
from .eso_options import (
    ESOOptions, Alliance, GOAL_ZONE_NAMES, CLASS_NAMES, CLASS_SKILL_LINES,
    RACE_NAMES, ALL_RACES, ALLIANCE_RACES,
    ALL_WEAPON_SKILL_LINES, ALL_ARMOR_SKILL_LINES, ALL_RACIAL_SKILL_LINES, ALL_MISC_SKILL_LINES
)

# Mapping from option skill line names to item category names
# Most follow the pattern "{name} Skills" but some are different
SKILL_LINE_TO_CATEGORY = {
    # Dragonknight skill lines
    "Ardent Flame": "Ardent Flame Skills",
    "Draconic Power": "Draconic Power Skills",
    "Earthen Heart": "Earthen Heart Skills",
    # Sorcerer skill lines
    "Dark Magic": "Dark Magic Skills",
    "Daedric Summoning": "Daedric Summoning Skills",
    "Storm Calling": "Storm Calling Skills",
    # Nightblade skill lines
    "Assassination": "Assassination Skills",
    "Shadow": "Shadow Skills",
    "Siphoning": "Siphoning Skills",
    # Templar skill lines
    "Aedric Spear": "Aedric Spear Skills",
    "Dawn's Wrath": "Dawn's Wrath Skills",
    "Restoring Light": "Restoring Light Skills",
    # Warden skill lines
    "Winter's Embrace": "Winter's Embrace Skills",
    "Green Balance": "Green Balance Skills",
    "Animal Companions": "Animal Companions Skills",
    # Necromancer skill lines
    "Grave Lord": "Grave Lord Skills",
    "Bone Tyrant": "Bone Tyrant Skills",
    "Living Death": "Living Death Skills",
    # Arcanist skill lines
    "Herald of the Tome": "Herald of the Tome Skills",
    "Soldier of Apocrypha": "Soldier of Apocrypha Skills",
    "Curative Runeforms": "Curative Runeforms Skills",
    # Weapon skill lines
    "Two Handed": "Two Handed Skills",
    "One Hand and Shield": "One Hand Shield Skills",
    "Dual Wield": "Dual Wield Skills",
    "Bow": "Bow Skills",
    "Destruction Staff": "Destruction Staff Skills",
    "Restoration Staff": "Restoration Staff Skills",
    # Armor skill lines
    "Light Armor": "Light Armor Skills",
    "Medium Armor": "Medium Armor Skills",
    "Heavy Armor": "Heavy Armor Skills",
    # Guild skill lines
    "Fighters Guild": "Fighters Guild Skills",
    "Mages Guild": "Mages Guild Skills",
    # World skill lines (note: these use singular "Skill")
    "Soul Magic": "Soul Magic Skill",
    "Legerdemain": "Legerdemain Skill",
    "Vampirism": "Vampirism Skill",
    "Lycanthropy": "Lycanthropy Skill",
    #Crafting Skills
    "Alchemy": "Alchemy Skills",
    "Blacksmithing": "Blacksmithing Skills",
    "Clothing": "Clothing Skills",
    "Enchanting": "Enchanting Skills",
    "Provisioning": "Provisioning Skills",
    "Woodworking": "Woodworking Skills",
    # Racial skill lines
    "Argonian": "Argonian Skills",
    "Breton": "Breton Skills",
    "Dark Elf": "Dark Elf Skills",
    "High Elf": "High Elf Skills",
    "Imperial": "Imperial Skills",
    "Khajiit": "Khajiit Skill",
    "Nord": "Nord Skill",
    "Orc": "Orc Skill",
    "Redguard": "Redguard Skill",
    "Wood Elf": "Wood Elf Skill",
}

# All skill categories for checking if an item is a skill
ALL_SKILL_CATEGORIES = set(SKILL_LINE_TO_CATEGORY.values())
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

    # Instance variables set in create_items (for skill randomization)
    player_class: str
    player_race: str
    enabled_skill_lines: Set[str]

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

        #Remove excluded zones
        available_zones -= set(self.options.excluded_zones.value)

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
                f"ESO: Required zones are excluded or not in included zones: {missing_zones}. "
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

        # Build set of enabled skill categories based on options
        skill_mode = self.options.skill_randomization.value
        enabled_skill_categories: Set[str] = set()
        enabled_skill_lines: Set[str] = set()  # Track skill line names for slot_data

        # Initialize instance variables with defaults
        self.player_class = ""
        self.player_race = ""
        self.enabled_skill_lines = set()

        if skill_mode in [2, 3]:  # items or both
            # Always include player's class skill lines (all 3)
            player_class = CLASS_NAMES[self.options.character_class.value]
            self.player_class = player_class
            for skill_line in CLASS_SKILL_LINES[player_class]:
                enabled_skill_lines.add(skill_line)
                if skill_line in SKILL_LINE_TO_CATEGORY:
                    enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[skill_line])

            # Determine player's race for racial skills
            race_option = self.options.character_race.value
            if race_option == 0:  # any_race
                player_race = self.random.choice(ALL_RACES)
            elif race_option == 1:  # any_alliance_race
                alliance_races = ALLIANCE_RACES.get(alliance_value, [])
                if alliance_races:
                    player_race = self.random.choice(alliance_races)
                else:
                    # Fallback to any random race if alliance races not configured
                    player_race = self.random.choice(ALL_RACES)
            else:  # specific race selected
                player_race = RACE_NAMES.get(race_option, self.random.choice(ALL_RACES))

            self.player_race = player_race

            # Include player's racial skills
            enabled_skill_lines.add(player_race)
            if player_race in SKILL_LINE_TO_CATEGORY:
                enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[player_race])

            # Handle weapon skill lines
            weapon_selection = self.options.weapon_selection.value
            if weapon_selection == 2:  # all
                for weapon in ALL_WEAPON_SKILL_LINES:
                    enabled_skill_lines.add(weapon)
                    if weapon in SKILL_LINE_TO_CATEGORY:
                        enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[weapon])
            elif weapon_selection == 1:  # random - pick 2
                weapons = list(ALL_WEAPON_SKILL_LINES)
                selected_weapons = self.random.sample(weapons, min(2, len(weapons)))
                for weapon in selected_weapons:
                    enabled_skill_lines.add(weapon)
                    if weapon in SKILL_LINE_TO_CATEGORY:
                        enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[weapon])
            else:  # manual
                for weapon in self.options.weapon_skill_lines.value:
                    enabled_skill_lines.add(weapon)
                    if weapon in SKILL_LINE_TO_CATEGORY:
                        enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[weapon])

            # Handle armor skill lines
            armor_selection = self.options.armor_selection.value
            if armor_selection == 1:  # all
                for armor in ALL_ARMOR_SKILL_LINES:
                    enabled_skill_lines.add(armor)
                    if armor in SKILL_LINE_TO_CATEGORY:
                        enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[armor])
            else:  # manual
                for armor in self.options.armor_skill_lines.value:
                    enabled_skill_lines.add(armor)
                    if armor in SKILL_LINE_TO_CATEGORY:
                        enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[armor])

            # Include misc skill lines (guilds, world skills)
            for skill_line in self.options.misc_skill_lines.value:
                enabled_skill_lines.add(skill_line)
                if skill_line in SKILL_LINE_TO_CATEGORY:
                    enabled_skill_categories.add(SKILL_LINE_TO_CATEGORY[skill_line])

            # Store for slot_data
            self.enabled_skill_lines = enabled_skill_lines

        # Build normal item pool, skipping items we don't need
        skill_items: List[ESOItem] = []

        for name, data in item_table.items():
            if name == starting_item_name:
                continue  # Don't add to pool, will be precollected

            # Skip items associated with zones not in selected_zones
            if data.zone is not None and data.zone not in self.selected_zones:
                continue

            # Skip zone wayshrine items if option is disabled
            if data.category == "Zone Wayshrines Access" and not self.options.zone_wayshrines_enabled:
                continue

            # Handle skill items based on skill randomization mode
            if data.category in ALL_SKILL_CATEGORIES:
                if skill_mode == 0:  # none - skip all skill items
                    continue
                if skill_mode == 1:  # skyshards only - skip skill items
                    continue
                if skill_mode in [2, 3]:  # items or both
                    if data.category not in enabled_skill_categories:
                        continue
                    # Collect skill items separately for "both" mode handling
                    quantity = data.max_quantity
                    for _ in range(quantity):
                        skill_items.append(self.create_item(name))
                    continue

            # Limit Progressive Main Quest items to what's achievable
            if name == "Progressive Main Quest":
                quantity = self.max_progressive_mq
            else:
                quantity = data.max_quantity

            item_pool += [self.create_item(name) for _ in range(quantity)]

        # Handle "both" mode - ensure 3 skyshards per skill, remove skills if needed
        if skill_mode == 3:  # both
            num_skills = len(skill_items)
            skyshards_needed = num_skills * 3
            available_space = total_locations - len(item_pool)

            if skyshards_needed + num_skills > available_space:
                # Need to remove some skills to make room
                # Weight removal: higher chance to remove non-class skills
                player_class = CLASS_NAMES[self.options.character_class.value]
                player_class_categories = {
                    SKILL_LINE_TO_CATEGORY[skill_line]
                    for skill_line in CLASS_SKILL_LINES[player_class]
                    if skill_line in SKILL_LINE_TO_CATEGORY
                }

                # Sort skills by removal priority (class skills last)
                def removal_weight(item: ESOItem) -> float:
                    item_data = item_table.get(item.name)
                    if item_data and item_data.category in player_class_categories:
                        return 0.2  # Low chance to remove class skills
                    return 1.0  # Higher chance to remove other skills

                # Calculate how many skills to remove
                items_to_fit = available_space // 4  # Each skill needs 1 item + 3 skyshards
                skills_to_remove = num_skills - items_to_fit

                if skills_to_remove > 0:
                    # Weighted random removal
                    weights = [removal_weight(item) for item in skill_items]
                    for _ in range(min(skills_to_remove, len(skill_items))):
                        if not skill_items:
                            break
                        # Recalculate weights
                        weights = [removal_weight(item) for item in skill_items]
                        total_weight = sum(weights)
                        if total_weight == 0:
                            break
                        # Pick a random skill to remove
                        r = self.random.random() * total_weight
                        cumulative = 0
                        for i, w in enumerate(weights):
                            cumulative += w
                            if r <= cumulative:
                                skill_items.pop(i)
                                break

            # Add skill items and corresponding skyshards
            item_pool.extend(skill_items)
            for _ in range(len(skill_items) * 3):
                item_pool.append(self.create_item("Skyshard"))
        elif skill_mode == 2:  # items only
            item_pool.extend(skill_items)
        elif skill_mode == 1:  # skyshards only
            # Add skyshards based on some calculation (e.g., a fixed number or based on locations)
            # For now, just fill with skyshards as filler
            pass

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
        # Build enabled skill categories dict for the game mod
        enabled_categories = {}
        for skill_line in self.enabled_skill_lines:
            enabled_categories[skill_line] = True

        return {
            "Alliance": self.options.alliance.value,
            "Goal": self.options.goal.value,
            "GoalZone": self.goal_zone,
            "SelectedZones": list(self.selected_zones),
            "ZoneQuestsEnabled": self.options.zone_quests_enabled.value,
            "WayshrineChecksEnabled": self.options.wayshrine_checks_enabled.value,
            "SkillRandomization": self.options.skill_randomization.value,
            "CharacterClass": self.player_class,
            "CharacterRace": self.player_race,
            "EnabledSkillCategories": enabled_categories,
        }