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
            if required_item:
                entrance.access_rule = (
                    lambda state, item=required_item: state.has(item, player)
                )



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

            if "Mountains - Tournament Race" in loc_name:
                location.access_rule = lambda state: state.has("Mountains Tournament Ticket", player) and skill_rule(state)
            elif "Swamp - Tournament Race" in loc_name:
                location.access_rule = lambda state: state.has("Swamp Tournament Ticket", player) and skill_rule(state)
            elif "Grasslands - Tournament Race" in loc_name:
                location.access_rule = lambda state: state.has("Grasslands Tournament Ticket", player) and skill_rule(state)
            elif "Glacier - Tournament Race" in loc_name:
                location.access_rule = lambda state: state.has("Glacier Tournament Ticket", player) and skill_rule(state)
            elif "City - Tournament Race" in loc_name:
                location.access_rule = lambda state: state.has("City Tournament Ticket", player) and skill_rule(state)
            elif loc_name == "Volcano - Fire Duck Race Won" in loc_name:
                location.access_rule = lambda state: state.has("Red Key", player) and state.has("Orange Key", player) and state.has("Green Key", player) and skill_rule(state)
            else:
                location.access_rule = skill_rule

    world.get_location("Volcano - Fire Duck Race Won").place_locked_item(world.create_item("Victory"))

