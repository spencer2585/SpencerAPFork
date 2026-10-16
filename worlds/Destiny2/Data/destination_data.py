from dataclasses import dataclass, field
from typing import List, Dict
from .constants import Destinations


@dataclass
class DestinationData:
    id: int
    endgame_content:list[str] = field(default_factory=list)
    primary:bool = False
    subconnections:list[str] = field(default_factory=list)
    social:bool = False



DESTINATION_DATA: Dict[str, DestinationData] = {
    Destinations.EDZ: DestinationData(id = 1, endgame_content=["Warlord's Ruin"], primary=True),
    Destinations.COSMODROME: DestinationData(id = 2,endgame_content=["Grasp of Avarice"], primary=True),
    Destinations.NESSUS: DestinationData(id = 3,primary=True),
    Destinations.ETERNITY: DestinationData(id = 4,primary=True),
    Destinations.DREAMINGCITY: DestinationData(id = 5,endgame_content=["The Shattered Throne", "Last Wish"], primary=True),
    Destinations.THRONEWORLD: DestinationData(id = 6,endgame_content=["Sundered Doctrine","Vow of the Disciple"], primary=True),
    Destinations.MOON: DestinationData(id = 7,endgame_content=["Pit of Heresy","Duality", "Garden of Salvation","Crota's End"], primary=True),
    Destinations.EUROPA: DestinationData(id = 8,endgame_content=["Vesper's Host","Deep Stone Crypt"], primary=True),
    Destinations.NEPTUNE: DestinationData(id = 9,endgame_content=["Root of Nightmares"] , primary=True),
    Destinations.PALEHEART: DestinationData(id = 10,endgame_content=["Salvation's Edge"], primary=True),
    Destinations.KEPLER: DestinationData(id = 11,endgame_content=["The Desert Perpetual"], primary=True),
    Destinations.MARS: DestinationData(id = 12,endgame_content=["Spire of the Watcher"], subconnections=["Tharsis Outpost", "The Enclave"]),
    Destinations.TITAN: DestinationData(id = 13,endgame_content=["Ghosts of the Deep"]),
    Destinations.VENUS: DestinationData(id = 14,endgame_content=["Equilibrium","Vault of Glass"]),
    Destinations.DREADNAUGHT: DestinationData(id = 15,endgame_content=["King's Fall"]),
    Destinations.LASTCITY: DestinationData(id = 16,social = True),
    Destinations.THARSISOUTPOST: DestinationData(id = 17,social = True),
    Destinations.ENCLAVE: DestinationData(id = 18,social = True),
    Destinations.IO: DestinationData(id = 19),
    Destinations.TANGLEDSHORE: DestinationData(id = 20),
}