import math

from .Locations import location_table
from .Regions import REGION_GRAPH

def set_rules(world):
    player = world.player

    for region_name, data in REGION_GRAPH.items():
        # Apply rule to each exit (entrance) from this region
        for exit_name in data.get("exits", []):
            entrance_name = f"{region_name} -> {exit_name}"
            entrance = world.get_entrance(entrance_name)

            required_item = REGION_GRAPH[exit_name].get("requires")
            entrance.access_rule = (
                lambda state, item=required_item: state.has(item, player)
            )


    #create rules for tournament checks
    world.get_location("Grasslands - Tournament Race 1 Won").access_rule = lambda state: state.has("Grasslands Tournament Ticket", player)
    world.get_location("Grasslands - Tournament Race 2 Won").access_rule = lambda state: state.has("Grasslands Tournament Ticket", player)
    world.get_location("Grasslands - Tournament Race 3 Won").access_rule = lambda state: state.has("Grasslands Tournament Ticket", player)
    world.get_location("Grasslands - Tournament Won").access_rule = lambda state: state.has("Grasslands Tournament Ticket", player)
    world.get_location("Swamp - Tournament Race 1 Won").access_rule = lambda state: state.has("Swamp Tournament Ticket", player)
    world.get_location("Swamp - Tournament Race 2 Won").access_rule = lambda state: state.has("Swamp Tournament Ticket", player)
    world.get_location("Swamp - Tournament Race 3 Won").access_rule = lambda state: state.has("Swamp Tournament Ticket", player)
    world.get_location("Swamp - Tournament Won").access_rule = lambda state: state.has("Swamp Tournament Ticket", player)
    world.get_location("Mountains - Tournament Race 1 Won").access_rule = lambda state: state.has("Mountains Tournament Ticket", player)
    world.get_location("Mountains - Tournament Race 2 Won").access_rule = lambda state: state.has("Mountains Tournament Ticket", player)
    world.get_location("Mountains - Tournament Race 3 Won").access_rule = lambda state: state.has("Mountains Tournament Ticket", player)
    world.get_location("Mountains - Tournament Won").access_rule = lambda state: state.has("Mountains Tournament Ticket", player)
    world.get_location("Glacier - Tournament Race 1 Won").access_rule = lambda state: state.has("Glacier Tournament Ticket", player)
    world.get_location("Glacier - Tournament Race 2 Won").access_rule = lambda state: state.has("Glacier Tournament Ticket", player)
    world.get_location("Glacier - Tournament Race 3 Won").access_rule = lambda state: state.has("Glacier Tournament Ticket", player)
    world.get_location("Glacier - Tournament Won").access_rule = lambda state: state.has("Glacier Tournament Ticket", player)
    world.get_location("City - Tournament Race 1 Won").access_rule = lambda state: state.has("City Tournament Ticket", player)
    world.get_location("City - Tournament Race 2 Won").access_rule = lambda state: state.has("City Tournament Ticket", player)
    world.get_location("City - Tournament Race 3 Won").access_rule = lambda state: state.has("City Tournament Ticket", player)
    world.get_location("City - Tournament Won").access_rule = lambda state: state.has("City Tournament Ticket", player)
    world.get_location("Volcano - Fire Duck Race Won").access_rule = lambda state: state.has("Red Key", player) and state.has("Orange Key", player) and state.has("Green Key", player)


    chunk = world.options.skill_size.value

    for loc_name, loc_data in location_table.items():
        if loc_data.required_skills:
            location= world.get_location(loc_name)

            def skill_rule(state, loc_data=loc_data):
                for skill, required_level in loc_data.required_skills.items():
                    items_needed = math.ceil(required_level/chunk)
                    if not state.has(f"{skill} Level", player, items_needed):
                        return False
                return True

            location.access_rule = skill_rule


