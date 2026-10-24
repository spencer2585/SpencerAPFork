from dataclasses import dataclass
from BaseClasses import Region, Location
from worlds.Destiny2.Data.ops_data import OpsTypes, OPS_DATA
from worlds.Destiny2.Data.strike_data import STRIKE_DATA
from .Data.constants import BASE_ID


class LocationTypes:
    STRIKE = "strike"
    SOLO_OPS = OpsTypes.SOLO
    FIRETEAM_OPS = OpsTypes.FIRETEAM
    PINNICLE_OPS = OpsTypes.PINNACLE
    ARENA_OPS = OpsTypes.ARENA

class LocationIds:
    STRIKE_ID = BASE_ID
    OPS_ID = BASE_ID + 1000

class D2Location(Location):
    game = "Destiny 2"

@dataclass
class LocationData:
    type: str
    id: int
    region: str

locations_dict = {
    **{f"{strike} {i+1}": LocationData(type = LocationTypes.STRIKE, id = LocationIds.STRIKE_ID + (data.id*10)+i, region = data.destination) for strike, data in STRIKE_DATA.items() for i in range(10)},
    **{ops: LocationData(type = data.type, id = LocationIds.OPS_ID + data.id, region = data.destination) for ops, data in OPS_DATA.items()},
}

def get_location_name_to_id():
    return {**{location: data.id for location, data in locations_dict.items()},}

def create_locations(world):
    for location, data in locations_dict.items():
        if data.type == LocationTypes.PINNICLE_OPS:
            #if pinnacle ops enabled (option not implemented yet)
            region = world.get_region(data.region)
            region.locations.append(D2Location(world.player, location, data.id, region))
        else:
            region = world.get_region(data.region)
            region.locations.append(D2Location(world.player, location, data.id, region))