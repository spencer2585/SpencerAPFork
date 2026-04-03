from dataclasses import dataclass, field
from typing import List, Dict

from constants import CE_OFFSET, PILLER_OF_AUTUMN_OFFSET

@dataclass
class HaloCeData:
    type: str
    id: int = CE_OFFSET
    level: str
    pass_to_client: bool = False


CE_LOCATION_DATA: Dict[str, HaloCeData] = {
    "Overshield 1": HaloCeData(type = "powerup", id = PILLER_OF_AUTUMN_OFFSET + 1, level = "The Piller of Autumn", pass_to_client = True),
    "Overshield 2": HaloCeData(type = "powerup", id = PILLER_OF_AUTUMN_OFFSET + 2, level = "The Piller of Autumn", pass_to_client = True),
    "Overshield 3": HaloCeData(type = "powerup", id = PILLER_OF_AUTUMN_OFFSET + 3, level = "The Piller of Autumn", pass_to_client = True),
    "Overshield 4": HaloCeData(type = "powerup", id = PILLER_OF_AUTUMN_OFFSET + 4, level = "The Piller of Autumn", pass_to_client = True),
    "Iron Skull": HaloCeData(type = "skull", id = PILLER_OF_AUTUMN_OFFSET + 5, level = "The Piller of Autumn", pass_to_client = True),
}