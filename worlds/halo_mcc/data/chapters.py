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
"The Truth and Reconciliation": LevelData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 11), #103011
"Into the Belly of the Beast": LevelData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 12), #103012
"Shut Up and Get Behind me... Sir": LevelData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 13), #103013
"The Silent Cartographer": LevelData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 11), #104011
"Its Quiet...": LevelData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 12), #104012
"Shafted": LevelData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 13), #104012
"I Would Have Been Your Daddy...": LevelData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 11), #105011
"Rolling Thunder": LevelData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 11), #105012
"If I Had a Super Weapon...": LevelData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 13), #105013
"Well Enough Alone": LevelData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 11), #106011
"The Flood": LevelData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 12), #106012
"343 Guilty Spark": LevelData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 13), #106013
"The Library": LevelData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 11), #107011
"The Library": LevelData(game = "CE", level = "Wait, it Gets Worse!", offset = constants.LIBRARY_OFFSET + 12), #107012
"But I Don't Want to Ride the Elevator!": LevelData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 13), #107013
"Fourth Floor: Tools, Guns, Keys To Super Weapons": LevelData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 14), #107014
"The Gun Pointed at the Head of the Universe": LevelData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 11), #108011
"Breaking Stuff to look Tough": LevelData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 12), #108012
"The Tunnels Below": LevelData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 13), #108013
"Ginal Run": LevelData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 14), #108014
"Under New Management": LevelData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 11), #109011
"Upstairs, Downstairs": LevelData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 12), #109012
"The Captain": LevelData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 13), #109013
"...And the Horse You Rode in On": LevelData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 11), #110011
"Light Fuse, Run Away": LevelData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 12), #110012
"Warning: Hitchhikers May Be Escaping Convicts": LevelData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 13), #110013
}