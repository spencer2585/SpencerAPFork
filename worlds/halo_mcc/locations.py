from BaseClasses import ItemClassification, Location

from data.halo_ce_location_data import CE_LOCATION_DATA

class MCCLocation(Location):
    game = "Elder Scrolls Online"

def get_location_name_to_id():
    location_map = {
        **{f"{data.level} - {name}": data.id for name, data in CE_LOCATION_DATA.items()},
    }
    return location_map


def create_locations(world):
    for name, data in CE_LOCATION_DATA.items():
        region = world.getRegion(data.level)
        location = MCCLocation(world.player, f"{data.level} - {name}",data.id, region)
        region.append(location)