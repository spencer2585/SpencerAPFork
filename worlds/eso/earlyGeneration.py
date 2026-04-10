from . import regions, eso_options
from .data.ZoneData import ZONE_DATA
from .data.DelveData import DELVE_DATA

MAIN_QUEST_ZONES = {
    0: ["Auridon", "Grahtwood"],
    1: ["Glenumbra", "Stormhaven"],
    2: ["Stonefalls", "Deshaan"],
}

MAIN_QUEST_DELVES = {
    0: "Wormroot Depths",
    1: "Norvulk Ruins",
    2: "Knife Ear Grotto",
}

CRAGLORN_REQUIRED_DELVE_COUNT = 11
CRAGLORN_REQUIRED_DELVES = ["Buried Sands", "Tombs of the Na-Totambu", "Haddock's Market", "Molavar", "Balamath", "Fearfangs Cavern","Serpent's Nest","Ilthag's Undertower","Exarch's Stronghold","The Howling Sepulchers","Loth'Na Caverns"]

def find_path(start, goal, valid_zones):
    if start == goal:
        return [start]

    traversable = set(valid_zones) | {start, goal}
    visited = {start}
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        current = path[-1]

        for neighbor in ZONE_DATA[current].connections:
            if neighbor not in traversable:
                continue
            if neighbor == goal:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None

def get_max_main_quest(world, alliance):
    max_main_quest = 0
    if alliance == 0:
        if "Auridon" in world.selected_zones:
            max_main_quest = 4
            if "Grahtwood" in world.selected_zones:
                if world.options.delves_per_region == 0 or "Wormroot Depths" in world.selected_delves:
                    max_main_quest = 8
                    if "Coldharbour" in world.selected_zones:
                        max_main_quest = 10
    elif alliance == 1:
        if "Glenumbra" in world.selected_zones:
            max_main_quest = 4
            if "Stormhaven" in world.selected_zones:
                if world.options.delves_per_region == 0 or "Norvulk Ruins" in world.selected_delves:
                    max_main_quest = 8
                    if "Coldharbour" in world.selected_zones:
                        max_main_quest = 10
    else:
        if "Stonefalls" in world.selected_zones:
            max_main_quest = 4
            if "Deshaan" in world.selected_zones:
                if world.options.delves_per_region == 0 or "Knife Ear Grotto" in world.selected_delves:
                    max_main_quest = 8
                    if "Coldharbour" in world.selected_zones:
                        max_main_quest = 10
    world.max_main_quest = max_main_quest

def generate_early(world):
    #get all needed information from the world for early generation
    player = world.player
    alliance = world.options.alliance
    starting_zone = regions.get_starting_zone(alliance)
    goal_zone = world.options.goal_zone
    num_zones = world.options.zone_count
    goal = world.options.goal
    delve_count = world.options.delves_per_region
    included_zones = world.options.included_zones
    zone_quests_enabled = world.options.zone_quests_enabled
    main_quests_enabled = world.options.main_quests_enabled
    valid_zones = list(included_zones) if included_zones else list(ZONE_DATA.keys())
    selected_zones_count = 0

    #Error if invalid settings
    if not main_quests_enabled and goal == 0:
        raise Exception(
            "Cannot set goal to Main Quest completion and disable Main Quest locations at the same time"
        )

    if not zone_quests_enabled and goal == 1:
        raise Exception(
            "Cannot set goal to Zone Quest Completion and disable Zone Quest locations at the same time"
        )

    if goal == 2 and delve_count == 0:
        raise Exception(
            "Cannot set goal to Dungeon Delver and disable Delve locations at the same time"
        )

    if goal == 1 and goal_zone == 19 and not main_quests_enabled:
        raise Exception(
            "Cannot set Coldharbour as goal zone and have main quests disabled at the same time"
        )

    if goal == 1 and goal_zone == 18 and delve_count != 0 and delve_count < 11 :
        raise Exception(
            "Craglorn cannot be set as goal zone with delves per zone set lower than 11"
        )

    #remove coldharbour from valid zones if settings arnt right
    if not main_quests_enabled:
        valid_zones.remove("Coldharbour")
    elif goal != 0 and goal_zone != 19:
        valid_zones.remove("Coldharbour")

    zone_list = [starting_zone]
    selected_zones_count += 1
    valid_zones.remove(starting_zone)

    # Select goal zone
    if goal_zone == 0:
        if delve_count < 11:
            random_candidates = [z for z in valid_zones if z != "Craglorn"]
        else:
            random_candidates = valid_zones
        # remove starter zones from valid zone pool
        random_candidates = [z for z in random_candidates if z not in ["Bleakrock Isle", "Stros M'kai", "Khenarthi's Roost"]]
        # filter zones to those accessible with chosen zone count
        random_candidates = [z for z in random_candidates if(p := find_path(starting_zone, z, valid_zones)) and len(p) <= num_zones]
        if not random_candidates:
            raise Exception(
                "No valid zones to choose as goal zone, Increase your zone count"
            )
        world.goal_zone = world.random.choice(random_candidates)
    else:
        world.goal_zone = eso_options.GOAL_ZONE_NAMES[goal_zone]

    #Create List of zones to include
    if goal == 1:
        zone_list.append(world.goal_zone)
        valid_zones.remove(world.goal_zone)
        selected_zones_count += 1

    #Add zones required for main quest
    if goal == 0:
        for zone in MAIN_QUEST_ZONES[alliance]:
            if zone not in zone_list:
                zone_list.append(zone)
                valid_zones.remove(zone)
                selected_zones_count += 1
        if "Coldharbour" not in zone_list:
            zone_list.append("Coldharbour")
            valid_zones.remove("Coldharbour")
            selected_zones_count += 1

    if goal == 1:
        path = find_path(starting_zone, world.goal_zone, valid_zones)
        if path is None:
            raise Exception(
                "No valid path from starting zone to goal zone found. Add more zones to included zones so that a path can be found"
            )
        for zone in path:
            if zone not in zone_list:
                zone_list.append(zone)
                valid_zones.remove(zone)
                selected_zones_count += 1

    if selected_zones_count > num_zones:
        raise Exception(
            f"No path leading from starting zone {starting_zone} to goal zone {goal_zone} in {num_zones} zones with included zones, minimum length is {selected_zones_count} zones"
        )

    while selected_zones_count < num_zones:
        candidates = [
            zone for zone in valid_zones if any(zone in ZONE_DATA[z].connections for z in zone_list)
        ]

        if not candidates:
            #no reachable zones left
            print(f"No more valid zones left to reach player chosen zones. Generating with {selected_zones_count} zones")
            break

        zone = world.random.choice(candidates)
        zone_list.append(zone)
        valid_zones.remove(zone)
        selected_zones_count += 1

    world.selected_zones = zone_list

    #Select Delves to include

    if delve_count == 0:
        world.selected_delves = []

    else:
        selected_delves = []

        #force main quest delve in
        if goal == 0:
            selected_delves.append(MAIN_QUEST_DELVES[alliance])

        if goal == 2 and world.goal_zone == "Craglorn":
            selected_delves.extend(CRAGLORN_REQUIRED_DELVES)

        for zone in world.selected_zones:
            zone_delves = [d for d, data in DELVE_DATA.items() if data.zone == zone and d not in selected_delves]
            target = min(delve_count, len(zone_delves)+ len([d for d in selected_delves if DELVE_DATA[d].zone == zone]))
            while len([d for d in selected_delves if DELVE_DATA[d].zone == zone]) < target and zone_delves:
                chosen = world.random.choice(zone_delves)
                selected_delves.append(chosen)
                zone_delves.remove(chosen)

        world.selected_delves = selected_delves
        get_max_main_quest(world, alliance)

        world.multiworld.push_precollected(world.create_item(f"{starting_zone} Access"))






