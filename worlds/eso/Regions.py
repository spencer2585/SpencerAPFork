from BaseClasses import MultiWorld, Region, Entrance

from .data.ZoneData import ZONE_DATA
from .data.DelveData import DELVE_DATA

def create_regions(world):
    #create Menu
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    #create zone regions
    for zone_name, zone_data in ZONE_DATA.items():
        if zone_name in world.selected_zones:
            region = Region(zone_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

    #create delve regions
    for delve_name, delve_data in DELVE_DATA.items():
        if delve_name in world.selected_delves:
            region = Region(delve_name, world.player, world.multiworld)
            world.multiworld.regions.append(region)

    #Connect Zones to each other
    for zone_name, zone_data in ZONE_DATA.items():
        if zone_name in world.selected_zones:
            region = world.multiworld.get_region(zone_name, world.player)
            for connection in zone_data.connections:
                if connection in world.selected_zones:
                    entrance_name = f"{zone_name} -> {connection}"
                    entrance = Entrance(world.player, entrance_name, region)
                    region.exits.append(entrance)
                    entrance.connect(world.get_region(connection))

    #connect delves to parent zone
    for delve_name, delve_data in DELVE_DATA.items():
        if delve_name in world.selected_delves:
            delve_region = world.multiworld.get_region(delve_name, world.player)
            parent_region = world.multiworld.get_region(delve_data.zone, world.player)
            entrance_name = f"{delve_data.zone} -> {delve_name}"
            entrance = Entrance(world.player, entrance_name, parent_region)
            parent_region.exits.append(entrance)
            entrance.connect(delve_region)

    #connect Menu to starting zone based on alliance
    starting_zone_name = get_starting_zone(world.options.alliance)
    entrance_name = f"Menu -> {starting_zone_name}"
    entrance = Entrance(world.player, entrance_name, menu_region)
    menu_region.exits.append(entrance)
    entrance.connect(world.get_region(starting_zone_name))

    #connect Menu to Main Quest and create main quest region
    if world.options.main_quests_enabled:
        main_quest = Region("Main Quest", world.player, world.multiworld)
        world.multiworld.regions.append(main_quest)
        entrance_name = "Menu -> Main Quest"
        entrance = Entrance(world.player, entrance_name, menu_region)
        menu_region.exits.append(entrance)
        entrance.connect(main_quest)

        #connect main quest to coldharbour
        if "Coldharbour" in world.selected_zones and world.max_main_quest == 10:
            entrance_name = "Main Quest -> Coldharbour"
            entrance = Entrance(world.player, entrance_name, main_quest)
            main_quest.exits.append(entrance)
            entrance.connect(world.get_region("Coldharbour"))

def get_starting_zone(alliance):
    if alliance == 0:
        return "Khenarthi's Roost"
    if alliance == 1:
        return "Stros M'kai"
    if alliance == 2:
        return "Bleakrock Isle"



