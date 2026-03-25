from BaseClasses import ItemClassification, Location

from . import constants

from .data.DelveData import DELVE_DATA
from .data.WayshrineData import WAYSHRINE_DATA
from .data.MainQuestData import MAIN_QUEST_DATA
from .data.ZoneQuestData import ZONE_QUEST_DATA

class ESOLocation(Location):
    game = "Elder Scrolls Online"


def get_location_name_to_id():
    location_map = {
        **{f"{wayshrine_data.zone} - {wayshrine_name} Wayshrine": constants.WAYSHRINE_OFFSET + wayshrine_data.node_id for wayshrine_name, wayshrine_data in WAYSHRINE_DATA.items()},
        **{f"Main Quest - {mainquest_name}": mainquest_data.quest_id + constants.QUEST_OFFSET for mainquest_name, mainquest_data in MAIN_QUEST_DATA.items()},
        **{f"{delve_data.zone} - {delve_name} Delve Complete": constants.DELVE_LOCATION_OFFSET + delve_data.delve_id for delve_name, delve_data in DELVE_DATA.items()},
        **{f"{zone_quest_data.zone} - {zone_quest_name} Zone Quest": constants.QUEST_OFFSET + zone_quest_data.quest_id for zone_quest_name, zone_quest_data in ZONE_QUEST_DATA.items()},
    }
    return location_map


def create_locations(world):
    #create Wayshrine locations
    if world.options.wayshrine_checks_enabled:
        for wayshrine_name, wayshrine_data in WAYSHRINE_DATA.items():
            if wayshrine_data.zone in world.selected_zones:
                region = world.get_region(wayshrine_data.zone)
                location = ESOLocation(world.player, f"{wayshrine_data.zone} - {wayshrine_name} Wayshrine", (constants.WAYSHRINE_OFFSET + wayshrine_data.node_id), region)
                region.locations.append(location)

    #Create Main Quest Locations
    if world.options.main_quests_enabled:
        for mainquest_name, mainquest_data in MAIN_QUEST_DATA.items():
            if mainquest_data.quest_step <= world.max_main_quest:
                region = world.get_region("Main Quest")
                location = ESOLocation(world.player, f"Main Quest - {mainquest_name}", (constants.QUEST_OFFSET + mainquest_data.quest_id), region)
                region.locations.append(location)

    #Create Delve Completion Locations
    if world.options.delves_per_region > 0:
        for delve_name, delve_data in DELVE_DATA.items():
            if delve_name in world.selected_delves:
                region = world.get_region(delve_name)
                location = ESOLocation(world.player, f"{delve_data.zone} - {delve_name} Delve Complete", (constants.DELVE_LOCATION_OFFSET + delve_data.delve_id), region)
                region.locations.append(location)

    #create Zone Quest Locations
    if world.options.zone_quests_enabled:
        for zone_quest_name, zone_quest_data in ZONE_QUEST_DATA.items():
            if zone_quest_data.zone in world.selected_zones:
                if not zone_quest_data.required_delves or all(delve_name in world.selected_delves for delve_name in zone_quest_data.required_delves):
                    region = world.get_region(zone_quest_data.zone)
                    location = ESOLocation(world.player, f"{zone_quest_data.zone} - {zone_quest_name} Zone Quest",(constants.QUEST_OFFSET + zone_quest_data.quest_id), region)
                    region.locations.append(location)