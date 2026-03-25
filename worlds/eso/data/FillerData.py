from dataclasses import dataclass
from typing import List, Dict

@dataclass
class FillerData:
    id: int

FILLER_DATA: Dict[str, FillerData] = {
    "Skyshard": FillerData(id = 149995),
    "Wallet Capacity Upgrade": FillerData(id = 149994),
}