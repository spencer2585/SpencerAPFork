from dataclasses import dataclass, field
from typing import List, Dict



@dataclass
class DestinationData:
    endgame_content:list[str] = field(default_factory=list)
    primary:bool = False
    subconnections:list[str] = field(default_factory=list)
    social:bool = False



DESTINATION_DATA: Dict[str, DestinationData] = {
    "EDZ": DestinationData(endgame_content=["Warlord's Ruin"], primary=True),
    "Cosmodrome": DestinationData(endgame_content=["Grasp of Avarice"], primary=True),
    "Nessus": DestinationData(primary=True),
    "Eternity": DestinationData(primary=True),
    "Dreaming City": DestinationData(endgame_content=["The Shattered Throne", "Last Wish"], primary=True),
    "Savathun's Throne World": DestinationData(endgame_content=["Sundered Doctrine","Vow of the Disciple"], primary=True),
    "Moon": DestinationData(endgame_content=["Pit of Heresy","Duality", "Garden of Salvation","Crota's End"], primary=True),
    "Europa": DestinationData(endgame_content=["Vesper's Host","Deep Stone Crypt"], primary=True),
    "Neptune": DestinationData(endgame_content=["Root of Nightmares"] , primary=True),
    "The Pale Heart": DestinationData(endgame_content=["Salvation's Edge"], primary=True),
    "Kepler": DestinationData(endgame_content=["The Desert Perpetual"], primary=True),
    "Mars": DestinationData(endgame_content=["Spire of the Watcher"], subconnections=["Tharsis Outpost", "The Enclave"]),
    "Titan": DestinationData(endgame_content=["Ghosts of the Deep"]),
    "Venus": DestinationData(endgame_content=["Equilibrium","Vault of Glass"]),
    "Dreadnaught": DestinationData(endgame_content=["King's Fall"]),
    "The Last City": DestinationData(social = True),
    "Tharsis Outpost": DestinationData(social = True),
    "The Enclave": DestinationData(social = True),
}