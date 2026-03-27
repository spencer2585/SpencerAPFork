from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class WeaponFrameData:
    id: int

WEAPON_FRAME_DATA: Dict[str, WeaponFrameData] = {
    "Auto Rifle": WeaponFrameData(id = 6),
    "Hand Cannon": WeaponFrameData(id = 9),
    "Pulse Rifle": WeaponFrameData(id = 13),
    "Scout Rifle": WeaponFrameData(id = 14),
    "Fusion Rifle": WeaponFrameData(id = 11),
    "Sniper Rifle": WeaponFrameData(id = 12),
    "Shotgun": WeaponFrameData(id = 7),
    "Machine Gun": WeaponFrameData(id = 8),
    "Rocket Launcher": WeaponFrameData(id = 10),
    "Sidearm": WeaponFrameData(id = 17),
    "Sword": WeaponFrameData(id = 18),
    "Grenade Launcher": WeaponFrameData(id = 23),
    "Linear Fusion Rifle": WeaponFrameData(id = 22),
    "Trace Rifle": WeaponFrameData(id = 24),
    "Bow": WeaponFrameData(id = 31),
    "Glaive": WeaponFrameData(id = 33),
    "Submachine Gun": WeaponFrameData(id = 19),
}