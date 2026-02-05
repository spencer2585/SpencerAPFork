from .Regions import REGION_GRAPH, ZONE_FINAL_QUESTS

def set_rules(world):
    player = world.player
    alliance = world.options.alliance.value
    selected_zones = world.selected_zones

    if alliance == 0:
        allianceRegion="Auridon Access"
        allianceRegion2 = "Grahtwood Access"
        oppRegion1="Stormhaven Access"
        oppRegion2="Deshaan Access"
    elif alliance == 1:
        allianceRegion="Glenumbra Access"
        allianceRegion2 = "Stormhaven Access"
        oppRegion1 = "Grahtwood Access"
        oppRegion2 = "Deshaan Access"
    else:
        allianceRegion="Stonefalls Access"
        allianceRegion2 = "Deshaan Access"
        oppRegion1 = "Grahtwood Access"
        oppRegion2 = "Stormhaven Access"

    # Special regions always included
    always_include = {"Menu", "Main Quest"}
    regions_to_process = selected_zones | always_include

    for region_name, data in REGION_GRAPH.items():
        if region_name not in regions_to_process:
            continue

        for exit_name in data.get("exits", []):
            # Skip exits to regions that don't exist
            if exit_name not in regions_to_process:
                continue

            entrance_name = f"{region_name} -> {exit_name}"
            entrance = world.get_entrance(entrance_name)

            required_item = REGION_GRAPH[exit_name].get("requires")
            if region_name == "Menu":
                if exit_name == "Stros M'kai":
                    entrance.access_rule = (lambda state, a=alliance: a == 1)
                elif exit_name == "Khenarthi's Roost":
                    entrance.access_rule = (lambda state, a=alliance: a == 0)
                elif exit_name == "Bleakrock Isle":
                    entrance.access_rule = (lambda state, a=alliance: a == 2)
                continue

            if region_name == "Craglorn":
                if exit_name == "Grahtwood":
                    entrance.access_rule = (lambda state, a=alliance, ri=required_item: a == 0 and state.has(ri, player))
                elif exit_name == "Stormhaven":
                    entrance.access_rule = (lambda state, a=alliance, ri=required_item: a == 1 and state.has(ri, player))
                elif exit_name == "Stonefalls":
                    entrance.access_rule = (lambda state, a=alliance, ri=required_item: a == 2 and state.has(ri, player))
                continue

            if exit_name == "Coldharbour":
                entrance.access_rule = (lambda state, ri=required_item, ar=allianceRegion: state.has(ri, player) and state.has(ar, player) and state.has("Progressive Main Quest", player, 10))
                continue

            entrance.access_rule = (
                lambda state, item=required_item: state.has(item, player)
            )

    # Misc Mapping - only if those zones AND their required zones are included
    if "Stros M'kai" in selected_zones and "Betnikh" in selected_zones:
        world.get_location("Stros M'kai - Tip of the Spearhead Zone Quest").access_rule = lambda state: state.has("Betnikh Access", player)
    if "Bleakrock Isle" in selected_zones and "Bal Foyen" in selected_zones:
        world.get_location("Bleakrock Isle - Escape from Bleakrock Zone Quest").access_rule = lambda state: state.has("Bal Foyen Access", player)
    if "Betnikh" in selected_zones and "Stros M'kai" in selected_zones and "Glenumbra" in selected_zones:
        world.get_location("Betnikh - On to Glenumbria Zone Quest").access_rule = lambda state: state.has("Stros M'kai Access", player) and state.has("Glenumbra Access", player)
    if "Bal Foyen" in selected_zones and "Bleakrock Isle" in selected_zones:
        world.get_location("Bal Foyen - Breaking The Tide / Zeren in Peril Zone Quest").access_rule = lambda state: state.has("Bleakrock Isle Access", player)

    # Main Quest Mapping - only for achievable locations
    achievable_mq = set(world.achievable_main_quests)

    if "Main Quest - The Harborage" in achievable_mq:
        world.get_location("Main Quest - The Harborage").access_rule = lambda state: state.has(allianceRegion, player)
    if "Main Quest - Daughter of Giants" in achievable_mq:
        world.get_location("Main Quest - Daughter of Giants").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player)
    if "Main Quest - Chasing Shadows" in achievable_mq:
        world.get_location("Main Quest - Chasing Shadows").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player, 2)
    if "Main Quest - Castle of the Worm" in achievable_mq:
        world.get_location("Main Quest - Castle of the Worm").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player, 3)
    if "Main Quest - The Tharn Speaks" in achievable_mq:
        world.get_location("Main Quest - The Tharn Speaks").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 4)
    if "Main Quest - Halls of Torment" in achievable_mq:
        world.get_location("Main Quest - Halls of Torment").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 5)
    if "Main Quest - Valley of Blades" in achievable_mq:
        world.get_location("Main Quest - Valley of Blades").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 6)
    if "Main Quest - Shadow of Sancre Tor" in achievable_mq:
        world.get_location("Main Quest - Shadow of Sancre Tor").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 7)
    if "Main Quest - Council of the Five Companions" in achievable_mq:
        world.get_location("Main Quest - Council of the Five Companions").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 8)
    if "Main Quest - Messages Across Tamriel" in achievable_mq:
        world.get_location("Main Quest - Messages Across Tamriel").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 9) and state.has(oppRegion1, player) and state.has(oppRegion2, player)
    if "Main Quest - The Weight of Three Crowns" in achievable_mq:
        world.get_location("Main Quest - The Weight of Three Crowns").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest",player, 10) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player)
    if "Main Quest - God of Schemes" in achievable_mq:
        world.get_location("Main Quest - God of Schemes").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest",player, 11) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player)

    # Place Victory item based on goal option
    if world.options.goal.value == 0:  # main_quest
        final_loc = world.multiworld.get_location("Main Quest - God of Schemes", world.player)
    else:  # final_zone_quest
        goal_zone = world.goal_zone
        final_quest_name = ZONE_FINAL_QUESTS[goal_zone]
        final_loc = world.multiworld.get_location(final_quest_name, world.player)

    final_loc.place_locked_item(world.create_item("Victory"))



