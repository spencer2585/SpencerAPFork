from .Regions import REGION_GRAPH

def set_rules(world):
    player = world.player
    alliance = world.options.alliance
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

    for region_name, data in REGION_GRAPH.items():
        # Apply rule to each exit (entrance) from this region
        for exit_name in data.get("exits", []):
            entrance_name = f"{region_name} -> {exit_name}"
            entrance = world.get_entrance(entrance_name)

            required_item = REGION_GRAPH[exit_name].get("requires")
            if region_name == "Menu":
                if exit_name == "Stros M'kai":
                    entrance.access_rule = (lambda state: alliance == 1)
                elif exit_name == "Khenarthi's Roost":
                    entrance.access_rule = (lambda state: alliance == 0)
                elif exit_name == "Bleakrock Isle":
                    entrance.access_rule = (lambda state: alliance == 2)
                continue

            if region_name == "Craglorn":
                if exit_name == "Grahtwood":
                    entrance.access_rule = (lambda state: alliance == 0 and state.has(required_item, player))
                elif exit_name == "Stormhaven":
                    entrance.access_rule = (lambda state: alliance == 1 and state.has(required_item, player))
                elif exit_name == "Stonefalls":
                    entrance.access_rule = (lambda state: alliance == 2 and state.has(required_item, player))
                continue

            if exit_name == "Coldharbor":
                entrance.access_rule = (lambda state: state.has(required_item, player) and state.has(allianceRegion,player) and state.has("Progressive Main Quest",player, 10))
                continue
            # Use access_rule (old API)
            entrance.access_rule = (
                lambda state, item=required_item: state.has(item, player)
            )
    #Misc Mapping
    world.get_location("Stros M'kai - Tip of the Spearhead Zone Quest").access_rule = lambda state: state.has("Betnikh Access", player)
    world.get_location("Bleakrock Isle - Escape from Bleakrock Zone Quest").access_rule = lambda state: state.has("Bal Foyen Access", player)

    #Main Quest Mapping

    world.get_location("Main Quest - The Harborage").access_rule = lambda state: state.has(allianceRegion, player)
    world.get_location("Main Quest - Daughter of Giants").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player)
    world.get_location("Main Quest - Chasing Shadows").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player, 2)
    world.get_location("Main Quest - Castle of the Worm").access_rule = lambda state: state.has(allianceRegion, player) and state.has("Progressive Main Quest", player, 3)
    world.get_location("Main Quest - The Tharn Speaks").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 4,)
    world.get_location("Main Quest - Halls of Torment").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 5)
    world.get_location("Main Quest - Valley of Blades").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 6)
    world.get_location("Main Quest - Shadow of Sancre Tor").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 7)
    world.get_location("Main Quest - Council of the Five Companions")   .access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 8)
    world.get_location("Main Quest - Message Across Tamriel").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 9) and state.has(oppRegion1, player) and state.has(oppRegion2, player)
    world.get_location("Main Quest - The Weight of Three Crowns").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has( "Progressive Main Quest",player, 10) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbor Access",player)
    world.get_location("Main Quest - God of Schemes").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has( "Progressive Main Quest",player, 11) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbor Access",player)

    final_loc = world.multiworld.get_location("Main Quest - God of Schemes", world.player)
    final_loc.place_locked_item(world.victory_item)



