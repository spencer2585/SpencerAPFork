from dataclasses import dataclass, field
from typing import List, Dict
from . import constants

@dataclass
class ChapterData:
    game:str
    level:str
    offset:int


CHAPTER_DATA: Dict[str, ChapterData] = {
    "Reveillie": ChapterData(game = "CE", level = "The Pillar of Autumn", offset = constants.PILLER_OF_AUTUMN_OFFSET + 11), #101011
    "AI Constructs and Cyborgs First!": ChapterData(game = "CE", level = "The Pillar of Autumn", offset = constants.PILLER_OF_AUTUMN_OFFSET + 12), #101012
    "Flawless Cowboy": ChapterData(game = "CE", level = "Halo (CE)", offset = constants.HALO_CE_MISSION_OFFSET + 11), #102011
    "Reunion Tour": ChapterData(game = "CE", level = "Halo (CE)", offset = constants.HALO_CE_MISSION_OFFSET + 12), #102012
    "The Truth and Reconciliation": ChapterData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 11), #103011
    "Into the Belly of the Beast": ChapterData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 12), #103012
    "Shut Up and Get Behind me... Sir": ChapterData(game = "CE", level = "The Truth and Reconciliation", offset = constants.TRUTH_AND_RECONCILIATION_OFFSET + 13), #103013
    "The Silent Cartographer": ChapterData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 11), #104011
    "Its Quiet...": ChapterData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 12), #104012
    "Shafted": ChapterData(game = "CE", level = "The Silent Cartographer", offset = constants.SILENT_CARTOGRAPHER_OFFSET + 13), #104012
    "I Would Have Been Your Daddy...": ChapterData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 11), #105011
    "Rolling Thunder": ChapterData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 11), #105012
    "If I Had a Super Weapon...": ChapterData(game = "CE", level = "Assault on the Control Room", offset = constants.ASSAULT_CONTROL_ROOM_OFFSET + 13), #105013
    "Well Enough Alone": ChapterData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 11), #106011
    "The Flood": ChapterData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 12), #106012
    "343 Guilty Spark": ChapterData(game = "CE", level = "343 Guilty Spark", offset = constants.GUILTY_SPARK_OFFSET + 13), #106013
    "The Library": ChapterData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 11), #107011
    "Wait, it Gets Worse!": ChapterData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 12), #107012
    "But I Don't Want to Ride the Elevator!": ChapterData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 13), #107013
    "Fourth Floor: Tools, Guns, Keys To Super Weapons": ChapterData(game = "CE", level = "The Library", offset = constants.LIBRARY_OFFSET + 14), #107014
    "The Gun Pointed at the Head of the Universe": ChapterData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 11), #108011
    "Breaking Stuff to look Tough": ChapterData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 12), #108012
    "The Tunnels Below": ChapterData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 13), #108013
    "Ginal Run": ChapterData(game = "CE", level = "Two Betrayals", offset = constants.TWO_BETRAYALS_OFFSET + 14), #108014
    "Under New Management": ChapterData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 11), #109011
    "Upstairs, Downstairs": ChapterData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 12), #109012
    "The Captain": ChapterData(game = "CE", level = "Keyes", offset = constants.KEYES_OFFSET + 13), #109013
    "...And the Horse You Rode in On": ChapterData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 11), #110011
    "Light Fuse, Run Away": ChapterData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 12), #110012
    "Warning: Hitchhikers May Be Escaping Convicts": ChapterData(game = "CE", level = "The Maw", offset = constants.MAW_OFFSET + 13), #110013
}