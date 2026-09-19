"""
Skull catalog for Halo MCC Archipelago.

SKULL_BITS  - global MCC bitmap bit per skull (shared pointer chain, all games).
              None = not yet scanned for that skull's game.
GAME_SKULLS - skulls per game; drives apworld item pool generation.

Multipliers:
  0.00x -> PERM_DISABLED: always forced off, never in item pool
  1.00x -> NON_SCORING:   in item pool, no score effect
  >1.00x -> scoring:      standard skullsanity skulls
"""

from __future__ import annotations
from dataclasses import dataclass
from constants import SKULL_OFFSET

_CE: list[str] = [
    "Anger",
    "Black Eye",
    "Blind",
    "Catch",
    "Eye Patch",
    "Famine",
    "Fog",
    "Foreign",
    "Iron",
    "Mythic",
    "Recession",
    "That's Just... Wrong",
    "Thunderstorm",
    "Tough Luck",
]

_H2A: list[str] = [
    "Acrophobia",
    "Anger",
    "Assassins",
    "Bandana",
    "Black Eye",
    "Blind",
    "Bonded Pair",
    "Boom",
    "Catch",
    "Envy",
    "Eye Patch",
    "Famine",
    "Feather",
    "Fog",
    "Ghost",
    "Grunt Birthday Party",
    "Grunt Funeral",
    "Iron",
    "IWHBYD",
    "Jacked",
    "Malfunction",
    "Masterblaster",
    "Mythic",
    "Pinata",
    "Prophet Birthday Party",
    "Recession",
    "Scarab",
    "SO...ANGRY...",
    "Sputnik",
    "Streaking",
    "Swarm",
    "That's Just... Wrong",
    "They Come Back",
    "Thunderstorm",
]

_H3: list[str] = [
    "Acrophobia",
    "Anger",
    "Bandana",
    "Black Eye",
    "Blind",
    "Bonded Pair",
    "Boom",
    "Catch",
    "Cowbell",
    "Eye Patch",
    "Famine",
    "Fog",
    "Foreign",
    "Ghost",
    "Grunt Birthday Party",
    "Iron",
    "IWHBYD",
    "Jacked",
    "Malfunction",
    "Masterblaster",
    "Mythic",
    "Pinata",
    "Recession",
    "SO...ANGRY...",
    "Swarm",
    "That's Just... Wrong",
    "They Come Back",
    "Thunderstorm",
    "Tilt",
    "Tough Luck",
]

_ODST: list[str] = [
    "Acrophobia",
    "Anger",
    "Bandana",
    "Black Eye",
    "Blind",
    "Bonded Pair",
    "Boom",
    "Catch",
    "Cowbell",
    "Eye Patch",
    "Famine",
    "Foreign",
    "Ghost",
    "Grunt Birthday Party",
    "Iron",
    "IWHBYD",
    "Jacked",
    "Malfunction",
    "Masterblaster",
    "Mythic",
    "Pinata",
    "Recession",
    "SO...ANGRY...",
    "Swarm",
    "That's Just... Wrong",
    "Thunderstorm",
    "Tilt",
    "Tough Luck",
]

_H4: list[str] = [
    "Acrophobia",
    "Bandana",
    "Black Eye",
    "Blind",
    "Catch",
    "Cowbell",
    "Famine",
    "Fog",
    "Grunt Birthday Party",
    "Iron",
    "IWHBYD",
    "Mythic",
    "Thunderstorm",
    "Tilt",
    "Tough Luck",
]

_REACH: list[str] = [
    "Acrophobia",
    "Bandana",
    "Black Eye",
    "Blind",
    "Catch",
    "Cowbell",
    "Famine",
    "Fog",
    "Grunt Birthday Party",
    "Iron",
    "IWHBYD",
    "Mythic",
    "Thunderstorm",
    "Tilt",
    "Tough Luck",
]

GAME_SKULLS: dict[str, list[str]] = {
    "ce":    _CE,
    "h2a":   _H2A,
    "h3":    _H3,
    "odst":  _ODST,
    "h4":    _H4,
    "reach": _REACH,
}

_CENS: list[str] = [
    "Bandana",
    "Boom",
    "Ghost",
    "Grunt Birthday Party",
    "Grunt Funeral",
    "Malfunction",
    "Pinata",
    "Sputnik",
    "Acrophobia"
]

_H2ANS: list[str] = []

_H3NS: list[str] = []

_ODSTNS: list[str] = []

_H4NS: list[str] = []

_REACHNS: list[str] = []

NON_SCORING_SKULLS: dict[str, list[str]] = {
    "ce": _CENS,
    "h2a": _H2ANS,
    "h3": _H3NS,
    "odst": _ODSTNS,
    "h4": _H4NS,
    "reach": _REACHNS,
}

# 1.00x multiplier - placed in item pool but no score effect
NON_SCORING: frozenset[str] = frozenset({
    "Boom",
    "Cowbell",
    "Feather",
    "Ghost",
    "Grunt Birthday Party",
    "Grunt Funeral",
    "IWHBYD",
    "Malfunction",
    "Pinata",
    "Prophet Birthday Party",
    "SO...ANGRY...",
    "Sputnik",
    "Swarm",
    "They Come Back",
    "Acrophobia",
    "Bandana",
    "Bonded Pair",
    "Envy",
    "Scarab",
})

@dataclass
class SkullData:
    id: int
    type: str
    games: list[str]

SKULL_DATA: dict[str, SkullData] = {
    "Acrophobia":   SkullData(id = SKULL_OFFSET +1,type = "Non Scoring",   games = ["CE","2","3","ODST","4","Reach"]),
    "Anger":        SkullData(id = SKULL_OFFSET +2,type = "Scoring",       games = ["CE","2","3","ODST"]),
    "Assassin":     SkullData(id = SKULL_OFFSET +3,type = "Scoring",       games = ["2"]),
    "Bandanna":     SkullData(id = SKULL_OFFSET +4,type = "Non Scoring",   games = ["CE","2","3","ODST","4","Reach"]),
    "Black Eye":    SkullData(id = SKULL_OFFSET +5,type = "Scoring",       games = ["CE","2","3","ODST","4","Reach"]),
    "Blind":        SkullData(id = SKULL_OFFSET +6,type = "Scoring",       games = ["CE","2","3","ODST","4","Reach"]),
    "Bonded Pair":  SkullData(id = SKULL_OFFSET +7,type = "Non Scoring",   games = ["2","3","ODST"]),
    "Boom":         SkullData(id = SKULL_OFFSET +8,type = "Non Scoring",   games = ["CE","2","3","ODST"]),
    "Catch":        SkullData(id = SKULL_OFFSET +9,type = "Scoring",       games = ["CE","2","3","ODST","4","Reach"]),
    "Cowbell":      SkullData(id = SKULL_OFFSET +10,type = "Non Scoring",  games = ["3","ODST","4","Reach"]),
    "Envy":         SkullData(id = SKULL_OFFSET +11,type = "Non Scoring",  games = ["2"]),
    "Eye Patch":    SkullData(id = SKULL_OFFSET +12,type = "Scoring",      games = ["CE","2","3","ODST"]),
    "Famine":       SkullData(id = SKULL_OFFSET +13,type = "Scoring",      games = ["CE","2","3","ODST","4","Reach"]),
    "Feather":      SkullData(id = SKULL_OFFSET +14,type = "Non Scoring",  games = ["2"]),
    "Fog":          SkullData(id = SKULL_OFFSET +15,type = "Scoring",      games = ["CE","2","3","4","Reach"]),
    "Foreign":      SkullData(id = SKULL_OFFSET +16,type = "Scoring",      games = ["CE","3","ODST"]),
    "Ghost":        SkullData(id = SKULL_OFFSET +17,type = "Non Scoring",  games = ["CE","2","3","ODST"]),
    "Grunt Birthday Party": SkullData(id = SKULL_OFFSET +18,type = "Non Scoring", games = ["CE","2","3","ODST","4","Reach"]),
    "Grunt Funeral":SkullData(id = SKULL_OFFSET +19,type = "Non Scoring",  games = ["CE","2"]),
    "Iron":         SkullData(id = SKULL_OFFSET +20,type = "Scoring",      games = ["CE","2","3","ODST","4","Reach"]),
    "IWHBYD":       SkullData(id = SKULL_OFFSET +21,type = "Scoring",      games = ["2","3","ODST","4","Reach"]),
    "Jacked":       SkullData(id = SKULL_OFFSET +22,type = "Scoring",      games = ["2","3","ODST"]),
    "Malfunction":  SkullData(id = SKULL_OFFSET +23,type = "Non Scoring",  games = ["CE","2","3","ODST"]),
    "Masterblaster":SkullData(id = SKULL_OFFSET +24,type = "Scoring",      games = ["2","3","ODST"]),
    "Mythic":       SkullData(id = SKULL_OFFSET +25,type = "Scoring",      games = ["CE","2","3","ODST","4","Reach"]),
    "Pinata":       SkullData(id = SKULL_OFFSET +26,type = "Non Scoring",  games = ["CE","2","3","ODST"]),
    "Prophet Birthday Party":SkullData(id = SKULL_OFFSET +27,type = "Non Scoring", games = ["2"]),
    "Recession":    SkullData(id = SKULL_OFFSET +28,type = "Scoring",      games = ["CE","2","3","ODST"]),
    "Scarab":       SkullData(id = SKULL_OFFSET +29,type = "Non Scoring",  games = ["2"]),
    "SO...ANGRY...":SkullData(id = SKULL_OFFSET +30,type = "Non Scoring",  games = ["2","3","ODST"]),
    "Sputnik":      SkullData(id = SKULL_OFFSET +31,type = "Non Scoring",  games = ["CE","2"]),
    "Streaking":    SkullData(id = SKULL_OFFSET +32,type = "Scoring",      games = ["2"]),
    "Swarm":        SkullData(id = SKULL_OFFSET +33,type = "Non Scoring",  games = ["2","3","ODST"]),
    "That's Just... Wrong":SkullData(id = SKULL_OFFSET +34,type = "Scoring",games = ["CE","2","3","ODST"]),
    "They Come Back":SkullData(id = SKULL_OFFSET +35,type = "Non Scoring", games = ["2","3"]),
    "Thunderstorm": SkullData(id = SKULL_OFFSET +36,type = "Scoring",      games = ["CE","2","3","ODST","4","Reach"]),
    "Tilt":         SkullData(id = SKULL_OFFSET +37,type = "Scoring",      games = ["3","ODST","4","Reach"]),
    "Tough Luck":   SkullData(id = SKULL_OFFSET +38,type = "Scoring",      games = ["CE","3","ODST","4","Reach"]),
}