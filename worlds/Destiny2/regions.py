from BaseClasses import Region, Entrance
from .Data.destination_data import DESTINATION_DATA


def create_regions(world):
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    orbit = Region("Orbit", world.player, world.multiworld)
    world.multiworld.regions.append(orbit)
    orbit_e = Entrance(world.player, "Menu -> Orbit", menu)
    menu.exits.append(orbit_e)
    orbit_e.connect(orbit)

    for destination, data in DESTINATION_DATA.items():
        region = Region(destination, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        entrance = Entrance(world.player, f"Orbit -> {destination}", orbit)
        orbit.exits.append(entrance)
        entrance.connect(region)

        if data.endgame_content:
            for content in data.endgame_content:
                c_region = Region(content, world.player, world.multiworld)
                world.multiworld.regions.append(c_region)
                c_entrance = Entrance(world.player, f"{destination} -> {content}", c_region)
                region.exits.append(c_entrance)
                c_entrance.connect(c_region)