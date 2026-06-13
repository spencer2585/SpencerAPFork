from dataclasses import dataclass, field
from typing import List, Dict

from .constants import CE_OFFSET, PILLER_OF_AUTUMN_OFFSET, CE_CHECKPOINT_OFFSET, CE_SKULL_OFFSET


@dataclass
class HaloCeData:
    type: str
    id: int
    level: str
    pass_to_client: bool = False

# Collectible skull locations - one per physically findable skull in CEA/MCC.
# Level names must match LEVEL_DATA keys exactly.
CE_SKULL_DATA: Dict[str, HaloCeData] = {
    "Pillar of Autumn - Iron Skull":                    HaloCeData(type="skull", id=CE_SKULL_OFFSET + 1,  level="The Piller of Autumn",         pass_to_client=True),
    "Halo (CE) - Mythic Skull":                         HaloCeData(type="skull", id=CE_SKULL_OFFSET + 2,  level="Halo (CE)",                    pass_to_client=True),
    "Halo (CE) - Boom Skull":                           HaloCeData(type="skull", id=CE_SKULL_OFFSET + 3,  level="Halo (CE)",                    pass_to_client=True),
    "Truth and Reconciliation - Foreign Skull":         HaloCeData(type="skull", id=CE_SKULL_OFFSET + 4,  level="The Truth and Reconciliation", pass_to_client=True),
    "Silent Cartographer - Famine Skull":               HaloCeData(type="skull", id=CE_SKULL_OFFSET + 5,  level="The Silent Cartographer",      pass_to_client=True),
    "Silent Cartographer - Bandana Skull":              HaloCeData(type="skull", id=CE_SKULL_OFFSET + 6,  level="The Silent Cartographer",      pass_to_client=True),
    "Assault on the Control Room - Fog Skull":          HaloCeData(type="skull", id=CE_SKULL_OFFSET + 7,  level="Assault on the Control Room",  pass_to_client=True),
    "Assault on the Control Room - Malfunction Skull":  HaloCeData(type="skull", id=CE_SKULL_OFFSET + 8,  level="Assault on the Control Room",  pass_to_client=True),
    "343 Guilty Spark - Recession Skull":               HaloCeData(type="skull", id=CE_SKULL_OFFSET + 9,  level="343 Guilty Spark",             pass_to_client=True),
    "Library - Black Eye Skull":                        HaloCeData(type="skull", id=CE_SKULL_OFFSET + 10, level="The Library",                  pass_to_client=True),
    "Library - Eye Patch Skull":                        HaloCeData(type="skull", id=CE_SKULL_OFFSET + 11, level="The Library",                  pass_to_client=True),
    "Two Betrayals - Pinata Skull":                     HaloCeData(type="skull", id=CE_SKULL_OFFSET + 12, level="Two Betrayals",                pass_to_client=True),
    "Maw - Grunt Birthday Party Skull":                 HaloCeData(type="skull", id=CE_SKULL_OFFSET + 13, level="The Maw",                      pass_to_client=True),
}
