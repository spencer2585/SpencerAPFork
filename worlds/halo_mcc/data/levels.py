from dataclasses import dataclass, field
from typing import List, Dict
from . import constants

@dataclass
class LevelData:
    game:str
    offset:int

#the base level offset is used for the level completion location and the location access item

LEVEL_DATA: Dict[str, LevelData] = {
    "The Pillar of Autumn": LevelData(game = "CE", offset = constants.PILLER_OF_AUTUMN_OFFSET),
    "Halo (CE)": LevelData(game = "CE", offset = constants.HALO_CE_MISSION_OFFSET),
    "The Truth and Reconciliation": LevelData(game = "CE", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET),
    "The Silent Cartographer": LevelData(game = "CE", offset = constants.SILENT_CARTOGRAPHER_OFFSET),
    "Assault on the Control Room": LevelData(game = "CE", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET),
    "343 Guilty Spark": LevelData(game = "CE", offset= constants.GUILTY_SPARK_OFFSET),
    "The Library": LevelData(game = "CE", offset = constants.LIBRARY_OFFSET),
    "Two Betrayals": LevelData(game = "CE", offset = constants.TWO_BETRAYALS_OFFSET),
    "Keyes": LevelData(game = "CE", offset = constants.KEYS_OFFSET),
    "The Maw": LevelData(game = "CE", offset = constants.MAW_OFFSET),
}