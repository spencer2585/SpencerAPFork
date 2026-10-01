from dataclasses import dataclass
from .constants import Destinations

@dataclass
class StrikeData:
    destination: str
    hash: int

STRIKE_DATA: dict[str, StrikeData] = {
    "Lake of Shadows": StrikeData(destination = Destinations.EDZ,),
    "The Arms Dealer": StrikeData(destination = Destinations.EDZ,),
    "The Devils' Lair": StrikeData(destination = Destinations.COSMODROME,),
    "Fallen S.A.B.E.R": StrikeData(destination = Destinations.COSMODROME,),
    "The Disgraced": StrikeData(destination = Destinations.COSMODROME,),
    "The Inverted Spire": StrikeData(destination = Destinations.NESSUS,),
    "The Insight Terminus": StrikeData(destination = Destinations.NESSUS,),
    "Exodus Crash": StrikeData(destination = Destinations.NESSUS,),
    "Proving Grounds": StrikeData(destination = Destinations.NESSUS,),
    "Warden of Nothing": StrikeData(destination = Destinations.DREAMINGCITY,),
    "The Corrupted": StrikeData(destination = Destinations.DREAMINGCITY,),
    "Birthplace of the Vile": StrikeData(destination = Destinations.THRONEWORLD,),
    "The Lightblade": StrikeData(destination = Destinations.THRONEWORLD,),
    "The Scarlet Keep": StrikeData(destination = Destinations.MOON,),
    "The Glassway": StrikeData(destination = Destinations.EUROPA,),
    "Hypernet Current": StrikeData(destination = Destinations.NEPTUNE,),
    "Liminality": StrikeData(destination = Destinations.PALEHEART,),
}