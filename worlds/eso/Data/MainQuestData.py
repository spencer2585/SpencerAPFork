from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MainQuestData:
    quest_id: int
    quest_step: int

MAIN_QUEST_DATA: Dict[str, MainQuestData] = {
    "The Harborage": MainQuestData(quest_step=1, quest_id= 4831),
    "Daughter of Giants": MainQuestData(quest_step=2, quest_id=4474),
    "Chasing Shadows": MainQuestData(quest_step=3, quest_id=4552),
    "Castle of the Worm": MainQuestData(quest_step=4, quest_id=4607),
    "The Tharn Speaks": MainQuestData(quest_step=5, quest_id=4764),
    "Halls of Torment": MainQuestData(quest_step=6, quest_id=4836),
    "Valley of Blades": MainQuestData(quest_step=7, quest_id=4837),
    "Shadow of Sancre Tor": MainQuestData(quest_step=8, quest_id=4867),
    "Council of the Five Companions": MainQuestData(quest_step=9, quest_id=4832),
    "God of Schemes": MainQuestData(quest_step=10, quest_id=4847),
}