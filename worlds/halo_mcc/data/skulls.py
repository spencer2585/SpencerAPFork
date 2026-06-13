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


# Bitmap positions fixed for all games in shared UI code.
# Pointer chain: exe+0x4004230 -> +0x8 -> +0xB8 -> +0x20 -> +0x708 (uint64_t)
SKULL_BITS: dict[str, int | None] = {
    "Anger":                  0x1,           # bit  0 - CE H2A H3 ODST
    "Bandana":                0x4,           # bit  2 - all 6
    "Black Eye":              0x8,           # bit  3 - all 6
    "Blind":                  0x10,          # bit  4 - all 6
    "Bonded Pair":            0x20,          # bit  5 - H2A H3 ODST
    "Boom":                   0x40,          # bit  6 - CE H2A H3 ODST
    "Catch":                  0x80,          # bit  7 - all 6
    "Cowbell":                0x100,         # bit  8 - H3 ODST H4 Reach
    "Eye Patch":              0x400,         # bit 10 - CE H2A H3 ODST
    "Famine":                 0x800,         # bit 11 - all 6
    "Fog":                    0x2000,        # bit 13 - CE H2A H3 H4 Reach
    "Foreign":                0x4000,        # bit 14 - CE H3 ODST
    "Ghost":                  0x8000,        # bit 15 - CE H2A H3 ODST
    "Grunt Birthday Party":   0x10000,       # bit 16 - all 6
    "Grunt Funeral":          0x20000,       # bit 17 - CE H2A
    "Iron":                   0x40000,       # bit 18 - all 6
    "IWHBYD":                 0x80000,       # bit 19 - H2A H3 ODST H4 Reach
    "Jacked":                 0x100000,      # bit 20 - H2A H3 ODST
    "Malfunction":            0x200000,      # bit 21 - CE H2A H3 ODST
    "Masterblaster":          0x400000,      # bit 22 - H2A H3 ODST
    "Mythic":                 0x800000,      # bit 23 - all 6
    "Pinata":                 0x1000000,     # bit 24 - CE H2A H3 ODST
    "Recession":              0x4000000,     # bit 26 - CE H2A H3 ODST
    "SO...ANGRY...":          0x10000000,    # bit 28 - H2A H3 ODST
    "Sputnik":                0x20000000,    # bit 29 - CE H2A
    "Swarm":                  0x80000000,    # bit 31 - H2A H3 ODST
    "That's Just... Wrong":   0x100000000,   # bit 32 - CE H2A H3 ODST
    "Thunderstorm":           0x400000000,   # bit 34 - all 6
    "Tilt":                   0x800000000,   # bit 35 - H3 ODST H4 Reach
    "Tough Luck":             0x1000000000,  # bit 36 - CE H3 ODST H4 Reach
    "Acrophobia":             0x2000000000,  # bit 37 - all 6
    # H2A-exclusive;
    "Assassins":              None,
    "Envy":                   None,
    "Feather":                None,
    "Prophet Birthday Party": None,
    "Scarab":                 None,
    "Streaking":              None,
    "They Come Back":         None,          # also H3
}


def skull_enforce_mask(game: str) -> int:
    """Bitmask of all known skull bits for a game; OR these on each DLL tick."""
    mask = 0
    for skull in GAME_SKULLS[game]:
        bit = SKULL_BITS.get(skull)
        if bit is not None:
            mask |= bit
    return mask


_CE: list[str] = [
    "Acrophobia",
    "Anger",
    "Bandana",
    "Black Eye",
    "Blind",
    "Boom",
    "Catch",
    "Eye Patch",
    "Famine",
    "Fog",
    "Foreign",
    "Ghost",
    "Grunt Birthday Party",
    "Grunt Funeral",
    "Iron",
    "Malfunction",
    "Mythic",
    "Pinata",
    "Recession",
    "Sputnik",
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

# Skulls logically required to complete any mission per CE skullsanity tier.
# Hard requires more disablers in-hand before missions are considered beatable;
# Harder requires fewer, making progression easier to unlock but gameplay harder.
CE_HARD_REQUIRED: frozenset[str] = frozenset({
    "Iron", "Black Eye", "Blind", "Eye Patch",
    "Famine", "Foreign", "Mythic", "Thunderstorm", "Recession",
})
CE_HARDER_REQUIRED: frozenset[str] = frozenset({
    "Iron", "Blind", "Famine", "Foreign", "Mythic",
})

# 0.00x multiplier - always forced off, never placed in item pool for now
PERM_DISABLED: frozenset[str] = frozenset({
    "Acrophobia",
    "Bandana",
    "Bonded Pair",
    "Envy",
    "Scarab",
})

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
})
