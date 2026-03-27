from .data.ZoneData import ZONE_DATA
from .data.DelveData import DELVE_DATA
from .data.ZoneQuestData import ZONE_QUEST_DATA
from .data.MainQuestData import MAIN_QUEST_DATA

def create_rules(world):
    player = world.player

    #zone entrance Rules
    for zone_name, zone_data in ZONE_DATA.items():
        if zone_name in world.selected_zones:
            for connection in zone_data.connections:
                if connection in world.selected_zones:
                    entrance_name = f"{zone_name} -> {connection}"
                    entrance = world.multiworld.get_entrance(entrance_name,player)
                    required_item = f"{connection} Access"
                    entrance.access_rule = lambda state, item = required_item, p = player: state.has(item, p)

    #Delve Entrance Rules
    if world.options.delves_per_region > 0:
        for delve_name, delve_data in DELVE_DATA.items():
            if delve_name in world.selected_delves:
                entrance_name = f"{delve_data.zone} -> {delve_name}"
                entrance = world.multiworld.get_entrance(entrance_name,player)
                required_item = f"{delve_name} Access"
                entrance.access_rule = lambda state, item = required_item, p = player: state.has(item, p)

    #Zone Quest Rules
    if world.options.zone_quests_enabled:
        for quest_name, quest_data in ZONE_QUEST_DATA.items():
            if quest_name == "Escape from Bleakrock" and "Bal Foyen" not in world.selected_zones:
                continue
            elif quest_name == "Escape from Bleakrock":
                location = world.multiworld.get_location(f"{quest_data.zone} - {quest_name} Zone Quest", player)
                location.access_rule = lambda state, item = "Bal Foyen Access", p = player: state.has(item, p)

            if quest_name == "Tip of the Spearhead" and "Betnikh" not in world.selected_zones:
                continue
            elif quest_name == "Tip of the Spearhead":
                location = world.multiworld.get_location(f"{quest_data.zone} - {quest_name} Zone Quest", player)
                location.access_rule = lambda state, item="Betnikh Access", p=player: state.has(item, p)

            if quest_data.zone in world.selected_zones:
                if quest_data.required_delves and all(delve_name in world.selected_delves for delve_name in quest_data.required_delves):
                    location = world.multiworld.get_location(f"{quest_data.zone} - {quest_name} Zone Quest", player)
                    location.access_rule = lambda state, q=quest_data: all(state.has(f"{delve} Access", world.player) for delve in q.required_delves)

    if "Coldharbour" in world.selected_zones:
        entrance_name = "Main Quest -> Coldharbour"
        required_item = "Coldharbour Access"
        entrance = world.multiworld.get_entrance(entrance_name,player)
        entrance.access_rule = lambda state, item = required_item, p = player: state.has(item, p)

    #Main Quest Rules
    if world.options.main_quests_enabled:
        zone1, zone2, delve = get_alliance_data(world.options.alliance)
        for quest_name, quest_data in MAIN_QUEST_DATA.items():
            if quest_data.quest_step <= world.max_main_quest:
                location = world.multiworld.get_location(f"Main Quest - {quest_name}", world.player)
                if quest_data.quest_step == 1:
                    location.access_rule = lambda state, z1 = zone1: state.has(f"{z1} Access", player)
                elif quest_data.quest_step <= 4:
                    location.access_rule = lambda state, q=quest_data, z1 = zone1: state.has(f"{z1} Access", world.player) and state.has("Progressive Main Quest", world.player, q.quest_step - 1)
                elif quest_data.quest_step <= 9:
                    location.access_rule = lambda state, q=quest_data, z1 = zone1, z2 = zone2, d = delve: state.has(f"{z1} Access", world.player) and state.has("Progressive Main Quest", world.player, q.quest_step - 1) and state.has(f"{z2} Access", world.player) and ( state.has(f"{d} Access", player)if world.options.delves_per_region > 0 else True)
                elif quest_data.quest_step == 10:
                    location.access_rule = lambda state, q=quest_data, z1 = zone1, z2 = zone2, d = delve: state.has(f"{z1} Access", world.player) and state.has("Progressive Main Quest", world.player, q.quest_step - 1) and state.has(f"{z2} Access", world.player) and state.has("Coldharbour Access", world.player) and (state.has(f"{d} Access", player) if world.options.delves_per_region > 0 else True)




def get_alliance_data(alliance):
    if alliance == 0:
        zone1 = "Auridon"
        zone2 = "Grahtwood"
        delve = "Wormroot Depths"
    elif alliance == 1:
        zone1 = "Glenumbra"
        zone2 = "Stormhaven"
        delve = "Norvulk Ruins"
    else:
        zone1 = "Stonefalls"
        zone2 = "Deshaan"
        delve = "Knife Ear Grotto"
    return zone1, zone2, delve