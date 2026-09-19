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
    "Acrophobia": SkullData(id = ,type = "Non Scoring", games = ["CE","Reach"]),
    "Anger": SkullData(id = ,type = "Scoring", games = ["CE"]),
    "Bandanna": SkullData(id = ,type = "Non Scoring", games = ["CE","Reach"]),
    "Black Eye": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Blind": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Boom": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "Catch": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Cowbell": SkullData(id = ,type = "Non Scoring", games = ["Reach"]),
    "Eye Patch": SkullData(id = ,type = "Scoring", games = ["CE"]),
    "Famine": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Fog": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Foreign": SkullData(id = ,type = "Scoring", games = ["CE"]),
    "Ghost": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "Grunt Birthday Party": SkullData(id = ,type = "Non Scoring", games = ["CE","Reach"]),
    "Grunt Funeral": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "Iron": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "IWHBYD": SkullData(id = ,type = "Scoring", games = ["Reach"]),
    "Malfunction": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "Mythic": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Pinata": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "Recession": SkullData(id = ,type = "Scoring", games = ["CE"]),
    "Sputnik": SkullData(id = ,type = "Non Scoring", games = ["CE"]),
    "That's Just... Wrong": SkullData(id = ,type = "Scoring", games = ["CE"]),
    "Thunderstorm": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
    "Tilt": SkullData(id = ,type = "Scoring", games = ["Reach"]),
    "Tough Luck": SkullData(id = ,type = "Scoring", games = ["CE","Reach"]),
}