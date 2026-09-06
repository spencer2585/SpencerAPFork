from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class MCF7Web(WebWorld):
    theme = 'stone'
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to set up MCC for AP",
        "English",
        "mcc_en.md",
        "mcc/en",
        ["Spencer2585"]
    )]