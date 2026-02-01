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



