from dataclasses import dataclass
from .constants import Destinations

class OpsTypes:
    FIRETEAM = "fireteam"
    PINNACLE = "pinnacle"
    ARENA = "arena"
    SOLO = "solo"

@dataclass
class OpsData:
    destination: str
    type: str
    hash: str

OPS_DATA = dict[str, OpsData] = {
    "The Lightblade": OpsData(destination = Destinations.THRONEWORLD, type = OpsTypes.FIRETEAM,),
    "Heist Battleground: Mars": OpsData(destination = Destinations.MARS, type = OpsTypes.FIRETEAM,),
    "Savathun's Spire": OpsData(destination = Destinations.THRONEWORLD, type = OpsTypes.FIRETEAM,),
    "Lake of Shadows": OpsData(destination = Destinations.EDZ, type = OpsTypes.FIRETEAM,),
    "The Scarlet Keep": OpsData(destination = Destinations.MOON, type = OpsTypes.FIRETEAM,),
    "The Disgraced": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.FIRETEAM,),
    "The Sunless Cell": OpsData(destination = Destinations.DREADNAUGHT, type = OpsTypes.FIRETEAM,),
    "Exodus Crash": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "The Arms Dealer": OpsData(destination = Destinations.EDZ, type = OpsTypes.FIRETEAM,),
    "Warden of Nothing": OpsData(destination = Destinations.DREAMINGCITY, type = OpsTypes.FIRETEAM,),
    "Birthplace of the Vile": OpsData(destination = Destinations.THRONEWORLD, type = OpsTypes.FIRETEAM,),
    "Defiant Battleground: EDZ": OpsData(destination = Destinations.EDZ, type = OpsTypes.FIRETEAM,),
    "Heist Battleground: Moon": OpsData(destination = Destinations.MOON, type = OpsTypes.FIRETEAM,),
    "Fallen S.A.B.E.R.": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.FIRETEAM,),
    "Hypernet Current": OpsData(destination = Destinations.NEPTUNE, type = OpsTypes.FIRETEAM,),
    "The Insight Terminus": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Battleground: Core": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Battleground: Delve": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Battleground: Conduit": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Expedition: Europa": OpsData(destination = Destinations.EUROPA, type = OpsTypes.FIRETEAM,),
    "Fallen Bunker": OpsData(destination = Destinations.EDZ, type = OpsTypes.FIRETEAM,),
    "Battleground: Behemoth": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Battleground: Foothold": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.FIRETEAM,),
    "Battleground: Oracle": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "The Warrior": OpsData(destination = Destinations.EUROPA, type = OpsTypes.FIRETEAM,),
    "The Technocrat": OpsData(destination = Destinations.EUROPA, type = OpsTypes.FIRETEAM,),
    "The Dark Priestess": OpsData(destination = Destinations.EUROPA, type = OpsTypes.FIRETEAM,),
    "The Devils' Lair": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.FIRETEAM,),
    "The Glassway": OpsData(destination = Destinations.Europa, type = OpsTypes.FIRETEAM,),
    "The Inverted Spire": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
    "Liminality": OpsData(destination = Destinations.PALEHEART, type = OpsTypes.FIRETEAM,),
    "Proving Grounds": OpsData(destination = Destinations.NESSUS, type = OpsTypes.FIRETEAM,),
}