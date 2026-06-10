from dataclasses import dataclass, field
from typing import List, Dict

from .constants import CE_OFFSET, PILLER_OF_AUTUMN_OFFSET

@dataclass
class HaloCeData:
    type: str
    id: int
    level: str
    pass_to_client: bool = False


CE_LOCATION_DATA: Dict[str, HaloCeData] = {
}