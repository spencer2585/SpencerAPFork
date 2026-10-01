from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DungeonData:
    dungeon_name: str
    hash: int

DUNGEON_DATA: Dict[str, DungeonData] = {
    "": DungeonData(dungeon_name="Shattered Throne", hash = 1),
}
