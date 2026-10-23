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
    id: int


OPS_DATA = {
    "The Lightblade": OpsData(destination=Destinations.THRONEWORLD, type=OpsTypes.FIRETEAM, id=1),
    "Heist Battleground: Mars": OpsData(destination=Destinations.MARS, type=OpsTypes.FIRETEAM, id=2),
    "Savathun's Spire": OpsData(destination=Destinations.THRONEWORLD, type=OpsTypes.FIRETEAM, id=3),
    "Lake of Shadows": OpsData(destination=Destinations.EDZ, type=OpsTypes.FIRETEAM, id=4),
    "The Scarlet Keep": OpsData(destination=Destinations.MOON, type=OpsTypes.FIRETEAM, id=5),
    "The Disgraced": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.FIRETEAM, id=6),
    "The Sunless Cell": OpsData(destination=Destinations.DREADNAUGHT, type=OpsTypes.FIRETEAM, id=7),
    "Exodus Crash": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=8),
    "The Arms Dealer": OpsData(destination=Destinations.EDZ, type=OpsTypes.FIRETEAM, id=9),
    "Warden of Nothing": OpsData(destination=Destinations.DREAMINGCITY, type=OpsTypes.FIRETEAM, id=10),
    "Birthplace of the Vile": OpsData(destination=Destinations.THRONEWORLD, type=OpsTypes.FIRETEAM, id=11),
    "Defiant Battleground: EDZ": OpsData(destination=Destinations.EDZ, type=OpsTypes.FIRETEAM, id=12),
    "Heist Battleground: Moon": OpsData(destination=Destinations.MOON, type=OpsTypes.FIRETEAM, id=13),
    "Fallen S.A.B.E.R.": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.FIRETEAM, id=14),
    "Hypernet Current": OpsData(destination=Destinations.NEPTUNE, type=OpsTypes.FIRETEAM, id=15),
    "The Insight Terminus": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=16),
    "Battleground: Core": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=17),
    "Battleground: Delve": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=18),
    "Battleground: Conduit": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=19),
    "Expedition: Europa": OpsData(destination=Destinations.EUROPA, type=OpsTypes.FIRETEAM, id=20),
    "Fallen Bunker": OpsData(destination=Destinations.EDZ, type=OpsTypes.FIRETEAM, id=21),
    "Battleground: Behemoth": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=22),
    "Battleground: Foothold": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.FIRETEAM, id=23),
    "Battleground: Oracle": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=24),
    "The Warrior": OpsData(destination=Destinations.EUROPA, type=OpsTypes.FIRETEAM, id=25),
    "The Technocrat": OpsData(destination=Destinations.EUROPA, type=OpsTypes.FIRETEAM, id=26),
    "The Dark Priestess": OpsData(destination=Destinations.EUROPA, type=OpsTypes.FIRETEAM, id=27),
    "The Devils' Lair": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.FIRETEAM, id=28),
    "The Glassway": OpsData(destination=Destinations.EUROPA, type=OpsTypes.FIRETEAM, id=29),
    "The Inverted Spire": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=30),
    "Liminality": OpsData(destination=Destinations.PALEHEART, type=OpsTypes.FIRETEAM, id=31),
    "Proving Grounds": OpsData(destination=Destinations.NESSUS, type=OpsTypes.FIRETEAM, id=32),
    "The Coil": OpsData(destination=Destinations.DREAMINGCITY, type=OpsTypes.PINNACLE, id=33),
    "Midtown": OpsData(destination=Destinations.EDZ, type=OpsTypes.PINNACLE, id=34),
    "Heliostat": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.PINNACLE, id=35),
    "Derealize": OpsData(destination=Destinations.DREADNAUGHT, type=OpsTypes.PINNACLE, id=36),
    "Kell's Fall": OpsData(destination=Destinations.TANGLEDSHORE, type=OpsTypes.PINNACLE, id=37),
    "Encore": OpsData(destination=Destinations.NESSUS, type=OpsTypes.PINNACLE, id=38),
    "Starcrossed": OpsData(destination=Destinations.MOON, type=OpsTypes.PINNACLE, id=39),
    "//node.ovrd.AVALON//": OpsData(destination=Destinations.EDZ, type=OpsTypes.PINNACLE, id=40),
    "Operation: Seraph's Shield": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.PINNACLE, id=41),
    "Vox Obscura": OpsData(destination=Destinations.MARS, type=OpsTypes.PINNACLE, id=42),
    "Presage": OpsData(destination=Destinations.LASTCITY, type=OpsTypes.PINNACLE, id=43),
    "Zero Hour": OpsData(destination=Destinations.LASTCITY, type=OpsTypes.PINNACLE, id=44),
    "The Whisper": OpsData(destination=Destinations.IO, type=OpsTypes.PINNACLE, id=45),
    "Contest of Elders": OpsData(destination=Destinations.TANGLEDSHORE, type=OpsTypes.PINNACLE, id=46),
    "Katchcrash": OpsData(destination=Destinations.LASTCITY, type=OpsTypes.ARENA, id=47),
    "Astral Alignment": OpsData(destination=Destinations.DREAMINGCITY, type=OpsTypes.ARENA, id=48),
    "Nightmare Containment": OpsData(destination=Destinations.MOON, type=OpsTypes.ARENA, id=49),
    "Override: The Moon": OpsData(destination=Destinations.MOON, type=OpsTypes.ARENA, id=50),
    "Caldera": OpsData(destination=Destinations.KEPLER, type=OpsTypes.SOLO, id=51),
    "Typhon Imperator": OpsData(destination=Destinations.NEPTUNE, type=OpsTypes.SOLO, id=52),
    "The Salt Mines": OpsData(destination=Destinations.EDZ, type=OpsTypes.SOLO, id=53),
    "The Conflux": OpsData(destination=Destinations.NESSUS, type=OpsTypes.SOLO, id=54),
    "Creation": OpsData(destination=Destinations.EUROPA, type=OpsTypes.SOLO, id=55),
    "K1 Logistics": OpsData(destination=Destinations.MOON, type=OpsTypes.SOLO, id=56),
    "Skywatch": OpsData(destination=Destinations.COSMODROME, type=OpsTypes.SOLO, id=57),
}
