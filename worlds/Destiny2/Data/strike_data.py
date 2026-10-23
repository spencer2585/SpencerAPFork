from dataclasses import dataclass
from .constants import Destinations

@dataclass
class StrikeData:
    destination: str
    id: int

STRIKE_DATA: dict[str, StrikeData] = {
    "Lake of Shadows": StrikeData(destination = Destinations.EDZ,id=1),
    "The Arms Dealer": StrikeData(destination = Destinations.EDZ,id=2),
    "The Devils' Lair": StrikeData(destination = Destinations.COSMODROME,id=3),
    "Fallen S.A.B.E.R": StrikeData(destination = Destinations.COSMODROME,id=4),
    "The Disgraced": StrikeData(destination = Destinations.COSMODROME,id=5),
    "The Inverted Spire": StrikeData(destination = Destinations.NESSUS,id=6),
    "The Insight Terminus": StrikeData(destination = Destinations.NESSUS,id=7),
    "Exodus Crash": StrikeData(destination = Destinations.NESSUS,id=8),
    "Proving Grounds": StrikeData(destination = Destinations.NESSUS,id=9),
    "Warden of Nothing": StrikeData(destination = Destinations.DREAMINGCITY,id=10),
    "The Corrupted": StrikeData(destination = Destinations.DREAMINGCITY,id=11),
    "Birthplace of the Vile": StrikeData(destination = Destinations.THRONEWORLD,id=12),
    "The Lightblade": StrikeData(destination = Destinations.THRONEWORLD,id=13),
    "The Scarlet Keep": StrikeData(destination = Destinations.MOON,id=14),
    "The Glassway": StrikeData(destination = Destinations.EUROPA,id=15),
    "Hypernet Current": StrikeData(destination = Destinations.NEPTUNE,id=16),
    "Liminality": StrikeData(destination = Destinations.PALEHEART,id=17),
}