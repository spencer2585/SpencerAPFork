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
    id: str

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
    "The Coil": OpsData(destination = Destinations.DREAMINGCITY, type = OpsTypes.PINNACLE),
    "Midtown": OpsData(destination = Destinations.EDZ, type = OpsTypes.PINNACLE),
    "Heliostat": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.PINNACLE),
    "Derealize": OpsData(destination = Destinations.DREADNAUGHT, type = OpsTypes.PINNACLE),
    "Kell's Fall": OpsData(destination = Destinations.TANGLEDSHORE, type = OpsTypes.PINNACLE),
    "Encore": OpsData(destination = Destinations.NESSUS, type = OpsTypes.PINNACLE),
    "Starcrossed": OpsData(destination = Destinations.MOON, type = OpsTypes.PINNACLE),
    "//node.ovrd.AVALON//": OpsData(destination = Destinations.EDZ, type = OpsTypes.PINNACLE),
    "Operation: Seraph's Shield": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.PINNACLE),
    "Vox Obscura": OpsData(destination = Destinations.MARS, type = OpsTypes.PINNACLE),
    "Presage": OpsData(destination = Destinations.LASTCITY, type = OpsTypes.PINNACLE),
    "Zero Hour": OpsData(destination = Destinations.LASTCITY, type = OpsTypes.PINNACLE),
    "The Whisper": OpsData(destination = Destinations.IO, type = OpsTypes.PINNACLE),
    "Contest of Elders": OpsData(destination = Destinations.TANGLEDSHORE, type = OpsTypes.PINNACLE),
    "Katchcrash": OpsData(destination = Destinations.LASTCITY, type = OpsTypes.ARENA),
    "Astral Alignment": OpsData(destination = Destinations.DREAMINGCITY, type = OpsTypes.ARENA),
    "Nightmare Containment": OpsData(destination = Destinations.MOON, type = OpsTypes.ARENA),
    "Override: The Moon": OpsData(destination = Destinations.MOON, type = OpsTypes.ARENA),
    "Caldera": OpsData(destination = Destinations.KEPLER, type = OpsTypes.SOLO),
    "Typhon Imperator": OpsData(destination = Destinations.NEPTUNE, type = OpsTypes.SOLO),
    "The Salt Mines": OpsData(destination = Destinations.EDZ, type = OpsTypes.SOLO),
    "The Conflux": OpsData(destination = Destinations.NESSUS, type = OpsTypes.SOLO),
    "Creation": OpsData(destination = Destinations.EUROPA, type = OpsTypes.SOLO),
    "K1 Logistics": OpsData(destination = Destinations.MOON, type = OpsTypes.SOLO),
    "Skywatch": OpsData(destination = Destinations.COSMODROME, type = OpsTypes.SOLO),
}