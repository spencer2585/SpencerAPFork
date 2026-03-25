from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ZoneData:
    zone_id: int
    connections: List[str] = field(default_factory=list)

ZONE_DATA: Dict[str, ZoneData] = {
    "Glenumbra": ZoneData(zone_id=3, connections=["Betnikh","Stros M'kai","Stormhaven","Bangkorai","Stonefalls","Auridon"]),
    "Stormhaven": ZoneData(zone_id=19, connections=["Glenumbra","Rivenspire","Bangkorai","Deshaan","Grahtwood","Alik'r Desert"]),
    "Rivenspire": ZoneData(zone_id=20, connections=["Stormhaven","Alik'r Desert","Greenshade","Shadowfen"]),
    "Stonefalls": ZoneData(zone_id=41, connections=["Bal Foyen","The Rift","Deshaan","Glenumbra","Bleakrock Isle","Auridon"]),
    "Deshaan": ZoneData(zone_id=57, connections=["Stonefalls","Shadowfen","Grahtwood","Stormhaven"]),
    "Malabal Tor": ZoneData(zone_id=58, connections=["Grahtwood","Reaper's March","Greenshade","Alik'r Desert","Eastmarch"]),
    "Bangkorai": ZoneData(zone_id=92, connections=["Stormhaven","Craglorn","The Rift","Reaper's March"]),
    "Eastmarch": ZoneData(zone_id=101, connections=["The Rift","Alik'r Desert","Malabal Tor","Shadowfen","Auridon"]),
    "The Rift": ZoneData(zone_id=103, connections=["Eastmarch","Stonefalls"]),
    "Alik'r Desert": ZoneData(zone_id=104, connections=["Bangkorai","Eastmarch","Malabal Tor","Rivenspire","Stormhaven"]),
    "Greenshade": ZoneData(zone_id=108, connections=["Grahtwood","Malabal Tor","Rivenspire","Shadowfen"]),
    "Shadowfen": ZoneData(zone_id=117, connections=["Deshaan","Eastmarch","Greenshade","Rivenspire"]),
    "Bleakrock Isle": ZoneData(zone_id=280, connections=["Bal Foyen","Stonefalls"]),
    "Bal Foyen": ZoneData(zone_id=281, connections=["Stonefalls","Bleakrock Isle"]),
    "Coldharbour": ZoneData(zone_id=347, connections=[]),
    "Auridon": ZoneData(zone_id=381, connections=["Khenarthi's Roost","Glenumbra","Grahtwood","Reaper's March","Stonefalls"]),
    "Reaper's March": ZoneData(zone_id=382, connections=["Malabal Tor","Auridon","Bangkorai","The Rift"]),
    "Grahtwood": ZoneData(zone_id=383, connections=["Auridon","Deshaan","Greenshade","Stormhaven","Malabal Tor"]),
    "Stros M'kai": ZoneData(zone_id=534, connections=["Betnikh","Glenumbra"]),
    "Betnikh": ZoneData(zone_id=535, connections=["Stros M'kai","Glenumbra"]),
    "Khenarthi's Roost": ZoneData(zone_id=537, connections=["Auridon"]),
    "Craglorn": ZoneData(zone_id=888, connections=["Bangkorai"]),
}