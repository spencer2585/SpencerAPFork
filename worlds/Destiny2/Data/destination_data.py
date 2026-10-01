from dataclasses import dataclass, field
from typing import List, Dict
from .constants import Destinations


@dataclass
class DestinationData:
    endgame_content:list[str] = field(default_factory=list)
    primary:bool = False
    subconnections:list[str] = field(default_factory=list)
    social:bool = False



DESTINATION_DATA: Dict[str, DestinationData] = {
    Destinations.EDZ: DestinationData(endgame_content=["Warlord's Ruin"], primary=True),
    Destinations.COSMODROME: DestinationData(endgame_content=["Grasp of Avarice"], primary=True),
    Destinations.NESSUS: DestinationData(primary=True),
    Destinations.ETERNITY: DestinationData(primary=True),
    Destinations.DREAMINGCITY: DestinationData(endgame_content=["The Shattered Throne", "Last Wish"], primary=True),
    Destinations.THRONEWORLD: DestinationData(endgame_content=["Sundered Doctrine","Vow of the Disciple"], primary=True),
    Destinations.MOON: DestinationData(endgame_content=["Pit of Heresy","Duality", "Garden of Salvation","Crota's End"], primary=True),
    Destinations.EUROPA: DestinationData(endgame_content=["Vesper's Host","Deep Stone Crypt"], primary=True),
    Destinations.NEPTUNE: DestinationData(endgame_content=["Root of Nightmares"] , primary=True),
    Destinations.PALEHEART: DestinationData(endgame_content=["Salvation's Edge"], primary=True),
    Destinations.KEPLER: DestinationData(endgame_content=["The Desert Perpetual"], primary=True),
    Destinations.MARS: DestinationData(endgame_content=["Spire of the Watcher"], subconnections=["Tharsis Outpost", "The Enclave"]),
    Destinations.TITAN: DestinationData(endgame_content=["Ghosts of the Deep"]),
    Destinations.VENUS: DestinationData(endgame_content=["Equilibrium","Vault of Glass"]),
    Destinations.DREADNAUGHT: DestinationData(endgame_content=["King's Fall"]),
    Destinations.LASTCITY: DestinationData(social = True),
    Destinations.THARSISOUTPOST: DestinationData(social = True),
    Destinations.ENCLAVE: DestinationData(social = True),
}