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
        delve = "Wormroot Depths Access"
    elif alliance == 1:
        allianceRegion="Glenumbra Access"
        allianceRegion2 = "Stormhaven Access"
        oppRegion1 = "Grahtwood Access"
        oppRegion2 = "Deshaan Access"
        delve = "Norvulk Ruins Access"
    else:
        allianceRegion="Stonefalls Access"
        allianceRegion2 = "Deshaan Access"
        oppRegion1 = "Grahtwood Access"
        oppRegion2 = "Stormhaven Access"
        delve = "Knife Ear Grotto Access"

    # Special regions always included
    always_include = {"Menu", "Main Quest"}
    regions_to_process = selected_zones | always_include
    if "Coldharbour" in regions_to_process:
        regions_to_process.add("Stirk")

    print(f"ESO DEBUG: Processing entrances for regions: {regions_to_process}")
    print(f"ESO DEBUG: Stirk in regions? {'Stirk' in regions_to_process}")
    print(f"ESO DEBUG: Coldharbour in regions? {'Coldharbour' in regions_to_process}")

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

            if exit_name == "Stirk":
                print(f"ESO DEBUG: Setting entrance {region_name} -> Stirk")
                if region_name == "Bangkorai":
                    entrance.access_rule = (lambda state: state.has(allianceRegion2, player) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player))
                elif region_name == "Reaper's March":
                    entrance.access_rule = (lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player))
                elif region_name == "The Rift":
                    entrance.access_rule = (lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player))
                elif region_name == "Coldharbour":
                    entrance.access_rule = (lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player))
                elif region_name == "Main Quest":
                    if world.options.delves_per_region > 0:
                        entrance.access_rule = (lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2,player) and state.has(oppRegion1,player) and state.has(oppRegion2, player) and state.has("Coldharbour Access", player) and state.has("Progressive Main Quest",player,8)and state.has (delve,player))
                    else:
                        entrance.access_rule = (lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2,player) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access", player) and state.has("Progressive Main Quest", player,8))
                print(f"ESO DEBUG: Entrance rule set for {region_name} -> Stirk")
                continue

            entrance.access_rule = (
                lambda state, item=required_item: state.has(item, player)
            )

    # Misc Mapping - only if those zones AND their required zones are included
    if world.options.zone_quests_enabled:
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

    if world.options.delves_per_region > 0:
        if "Main Quest - The Tharn Speaks" in achievable_mq:
            world.get_location("Main Quest - The Tharn Speaks").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 4) and state.has(delve,player)
        if "Main Quest - Halls of Torment" in achievable_mq:
            world.get_location("Main Quest - Halls of Torment").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 5) and state.has(delve,player)
        if "Main Quest - Valley of Blades" in achievable_mq:
            world.get_location("Main Quest - Valley of Blades").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 6) and state.has(delve,player)
        if "Main Quest - Shadow of Sancre Tor" in achievable_mq:
            world.get_location("Main Quest - Shadow of Sancre Tor").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 7) and state.has(delve,player)
        if "Main Quest - Council of the Five Companions" in achievable_mq:
            world.get_location("Main Quest - Council of the Five Companions").access_rule = lambda state: state.has(allianceRegion, player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest", player, 8) and state.has(delve,player)
        if "Main Quest - God of Schemes" in achievable_mq:
            world.get_location("Main Quest - God of Schemes").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest",player, 9) and state.has(oppRegion1, player) and state.has(oppRegion2, player) and state.has("Coldharbour Access",player) and state.has(delve,player)
    else:
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
        if "Main Quest - God of Schemes" in achievable_mq:
            world.get_location("Main Quest - God of Schemes").access_rule = lambda state: state.has(allianceRegion,player) and state.has(allianceRegion2, player) and state.has("Progressive Main Quest",player, 9)

    if world.options.zone_quests_enabled and world.options.delves_per_region > 0:
        craglorn_quests = {loc.name for loc in world.multiworld.get_locations(player) if "Craglorn" in loc.name and "Zone Quest" in loc.name}
        if "Craglorn - The Warrior's Call Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - The Warrior's Call Zone Quest").access_rule = lambda state: state.has("Buried Sands Access",player) and state.has("Tombs of the Na-Totambu Access",player)
        if "Craglorn - Elemental Army Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - Elemental Army Zone Quest").access_rule = lambda state: state.has("Haddock's Market Access",player) and state.has("Molavar Access",player) and state.has("Balamath Access",player)
        if "Craglorn - The Missing Guardian Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - The Missing Guardian Zone Quest").access_rule = lambda state: state.has("Haddock's Market Access", player) and state.has("Molavar Access",player) and state.has("Balamath Access",player) and state.has("Buried Sands Access",player) and state.has("Tombs of the Na-Totambu Access",player)
        if "Craglorn - Slithering Brood Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - Slithering Brood Zone Quest").access_rule = lambda state: state.has("Fearfangs Cavern Access", player) and state.has("Serpent's Nest Access",player)
        if "Craglorn - The Serpent's Fang Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - The Serpent's Fang Zone Quest").access_rule = lambda state: state.has("Ilthag's Undertower Access", player) and state.has("Exarch's Stronghold Access",player)
        if "Craglorn - Dawn of the Exalted Viper Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - Dawn of the Exalted Viper Zone Quest").access_rule = lambda state: state.has("Buried Sands Access",player) and state.has("Tombs of the Na-Totambu Access",player) and state.has("Haddock's Market Access",player) and state.has("Molavar Access",player) and state.has("Balamath Access",player) and state.has("Fearfangs Cavern Access", player) and state.has("Serpent's Nest Access",player) and state.has("Ilthag's Undertower Access", player) and state.has("Exarch's Stronghold Access",player) and state.has("The Howling Sepulchers Access",player) and state.has("Loth'Na Caverns Access",player)
        if "Craglorn - The Time-Lost Warrior Zone Quest" in craglorn_quests:
            world.get_location("Craglorn - The Time-Lost Warrior Zone Quest").access_rule = lambda state: state.has("Buried Sands Access",player) and state.has("Tombs of the Na-Totambu Access",player) and state.has("Haddock's Market Access",player) and state.has("Molavar Access",player) and state.has("Balamath Access",player) and state.has("Fearfangs Cavern Access", player) and state.has("Serpent's Nest Access",player) and state.has("Ilthag's Undertower Access", player) and state.has("Exarch's Stronghold Access",player) and state.has("The Howling Sepulchers Access",player) and state.has("Loth'Na Caverns Access",player)


    # Place Victory item based on goal option
    if world.options.goal.value == 0:  # main_quest
        final_loc = world.multiworld.get_location("Main Quest - God of Schemes", world.player)
    else:  # final_zone_quest
        goal_zone = world.goal_zone
        final_quest_name = ZONE_FINAL_QUESTS[goal_zone]
        final_loc = world.multiworld.get_location(final_quest_name, world.player)

    final_loc.place_locked_item(world.create_item("Victory"))



