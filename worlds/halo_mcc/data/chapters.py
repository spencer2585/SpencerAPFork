from dataclasses import dataclass, field
from typing import List, Dict
from . import constants

@dataclass
class LevelData:
    game:str
    level:str
    offset:int


LEVEL_DATA: Dict[str, LevelData] = {
    "Reveillie": LevelData(game = "CE", level = "The Pillar of Autumn", offset = constants.PILLER_OF_AUTUMN_OFFSET + 11), #101011
    "AI Constructs and Cyborgs First!": LevelData(game = "CE", level = "The Pillar of Autumn", offset = constants.PILLER_OF_AUTUMN_OFFSET + 12), #101012
"Flawless Cowboy": LevelData(game = "CE", level = "Halo (CE)", offset = constants.HALO_CE_MISSION_OFFSET + 11), #102011
"Reunion Tour": LevelData(game = "CE", level = "Halo (CE)", offset = constants.HALO_CE_MISSION_OFFSET + 12), #102012
}