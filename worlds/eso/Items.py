from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

ALLIANCE_STARTING_REGIONS = {
    0: "Khenarthi's Roost Access",  # AD
    1: "Stros M'kai Access",        # DC
    2: "Bleakrock Isle Access",     # EP
}

eso_base_id: int = 150000
eso_region_unlock_id: int = eso_base_id

class ESOItem(Item):
    game: str = "Elder Scrolls Online"

class ESOItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1
    zone: Optional[str] = None  # If set, item is only included when this zone is selected

def get_items_by_category(category: str) -> Dict[str, ESOItemData]:
    item_dict: Dict[str, ESOItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict

def get_starting_region_item_name(alliance_value: int) -> str:
    return ALLIANCE_STARTING_REGIONS[alliance_value]

item_table: Dict[str, ESOItemData] = {
    "1000 Gold Expansion":      ESOItemData("Filler",       eso_base_id-6),
    "Victory":                  ESOItemData("Main Quest",   eso_base_id - 5,            ItemClassification.progression, 0),
    "Progressive Main Quest":   ESOItemData("Main Quest",   eso_base_id-4,              ItemClassification.progression,9),
    #Zone Access Items
    "Glenumbra Access":         ESOItemData("Zone Access",  eso_region_unlock_id+3,     ItemClassification.progression, 1, 1 , "Glenumbra"),
    "Stormhaven Access":        ESOItemData("Zone Access",  eso_region_unlock_id+19,    ItemClassification.progression, 1, 1, "Stormhaven"),
    "Rivenspire Access":        ESOItemData("Zone Access",  eso_region_unlock_id+20,    ItemClassification.progression, 1, 1, "Rivenspire"),
    "Stonefalls Access":        ESOItemData("Zone Access",  eso_region_unlock_id+41,    ItemClassification.progression, 1, 1, "Stonefalls"),
    "Deshaan Access":           ESOItemData("Zone Access",  eso_region_unlock_id+57,    ItemClassification.progression, 1, 1, "Deshaan"),
    "Malabal Tor Access":       ESOItemData("Zone Access",  eso_region_unlock_id+58,    ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Bangkorai Access":         ESOItemData("Zone Access",  eso_region_unlock_id+92,    ItemClassification.progression, 1, 1, "Bangkorai"),
    "Eastmarch Access":         ESOItemData("Zone Access",  eso_region_unlock_id+101,   ItemClassification.progression, 1, 1, "Eastmarch"),
    "The Rift Access":          ESOItemData("Zone Access",  eso_region_unlock_id+103,   ItemClassification.progression, 1, 1, "The Rift"),
    "Alik'r Desert Access":     ESOItemData("Zone Access",  eso_region_unlock_id+104,   ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Greenshade Access":        ESOItemData("Zone Access",  eso_region_unlock_id+108,   ItemClassification.progression, 1, 1, "Greenshade"),
    "Shadowfen Access":         ESOItemData("Zone Access",  eso_region_unlock_id+117,   ItemClassification.progression, 1, 1, "Shadowfen"),
    "Shrine of the Black Maw Access":ESOItemData("Delve Access",eso_region_unlock_id+270,ItemClassification.progression,1,1,"Shadowfen"),
    "Broken Tusk Access":       ESOItemData("Delve Access",eso_region_unlock_id+271,  ItemClassification.progression, 1, 1, "Shadowfen"),
    "Atanaz Runs Access":       ESOItemData("Delve Access",eso_region_unlock_id+272,  ItemClassification.progression, 1, 1, "Shadowfen"),
    "Chid-Moska Ruins Access":  ESOItemData("Delve Access",eso_region_unlock_id+273,  ItemClassification.progression, 1, 1, "Shadowfen"),
    "Onkobra Kwama Mine Access":ESOItemData("Delve Access",eso_region_unlock_id+274,  ItemClassification.progression, 1, 1, "Shadowfen"),
    "Gandranen Ruins Access":   ESOItemData("Delve Access",eso_region_unlock_id+275,  ItemClassification.progression, 1, 1, "Shadowfen"),
    "Bleakrock Isle Access":    ESOItemData("Zone Access",  eso_region_unlock_id+280,   ItemClassification.progression, 1, 1, "Bleakrock Isle"),
    "Bal Foyen Access":         ESOItemData("Zone Access",  eso_region_unlock_id+281,   ItemClassification.progression, 1, 1, "Bal Foyen"),
    "Inner Sea Armature Access":ESOItemData("Delve Access",eso_region_unlock_id+287,  ItemClassification.progression, 1, 1, "Stonefalls"),
    "Mephala's Nest Access":    ESOItemData("Delve Access",eso_region_unlock_id+288,  ItemClassification.progression, 1, 1, "Stonefalls"),
    "Softloam Cavern Access":   ESOItemData("Delve Access",eso_region_unlock_id+289,  ItemClassification.progression, 1, 1, "Stonefalls"),
    "Hightide Hollow Access":   ESOItemData("Delve Access",eso_region_unlock_id+290,  ItemClassification.progression, 1, 1, "Stonefalls"),
    "Sheogorath's Tongue Access":ESOItemData("Delve Access",eso_region_unlock_id+291, ItemClassification.progression, 1, 1, "Stonefalls"),
    "Emberflint Mine Access":   ESOItemData("Delve Access",eso_region_unlock_id+296,  ItemClassification.progression, 1, 1, "Stonefalls"),
    "Ilessan Tower Access":     ESOItemData("Delve Access",eso_region_unlock_id+309,  ItemClassification.progression, 1, 1, "Glenumbra"),
    "Silumm Access":            ESOItemData("Delve Access",eso_region_unlock_id+310,  ItemClassification.progression, 1, 1, "Glenumbra"),
    "The Mines of Khuras Access":ESOItemData("Delve Access",eso_region_unlock_id+311, ItemClassification.progression, 1, 1, "Glenumbra"),
    "Enduum Access":            ESOItemData("Delve Access",eso_region_unlock_id+312,  ItemClassification.progression, 1, 1, "Glenumbra"),
    "Ebon Crypt Access":        ESOItemData("Delve Access",eso_region_unlock_id+313,  ItemClassification.progression, 1, 1, "Glenumbra"),
    "Cryptwatch Fort Access":   ESOItemData("Delve Access",eso_region_unlock_id+314,  ItemClassification.progression, 1, 1, "Glenumbra"),
    "Portdun Watch Access":     ESOItemData("Delve Access",eso_region_unlock_id+315,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Koeglin Mine Access":      ESOItemData("Delve Access",eso_region_unlock_id+316,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Pariah Catacombs Access":  ESOItemData("Delve Access",eso_region_unlock_id+317,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Farangal's Delve Access":  ESOItemData("Delve Access",eso_region_unlock_id+318,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Bearclaw Mine Access":     ESOItemData("Delve Access",eso_region_unlock_id+319,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Norvulk Ruins Access":     ESOItemData("Delve Access",eso_region_unlock_id+320,  ItemClassification.progression, 1, 1, "Stormhaven"),
    "Crestshade Mine Access":   ESOItemData("Delve Access",eso_region_unlock_id+321,  ItemClassification.progression, 1, 1, "Rivenspire"),
    "Flyleaf Catacombs Access": ESOItemData("Delve Access",eso_region_unlock_id+322,  ItemClassification.progression, 1, 1, "Rivenspire"),
    "Tribulation Crypt Access": ESOItemData("Delve Access",eso_region_unlock_id+323,  ItemClassification.progression, 1, 1, "Rivenspire"),
    "Orc's Finger Ruins Access":ESOItemData("Delve Access",eso_region_unlock_id+324,  ItemClassification.progression, 1, 1, "Rivenspire"),
    "Erokii Ruins Access":      ESOItemData("Delve Access",eso_region_unlock_id+325,  ItemClassification.progression, 1, 1, "Rivenspire"),
    "Hildune's Secret Refuge Access":ESOItemData("Delve Access",eso_region_unlock_id+326,ItemClassification.progression,1,1,"Rivenspire"),
    "Santaki Access":           ESOItemData("Delve Access",eso_region_unlock_id+327,  ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Divad's Chagrin Mine Access":ESOItemData("Delve Access",eso_region_unlock_id+328,ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Aldunz Access":            ESOItemData("Delve Access",eso_region_unlock_id+329,  ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Coldrock Diggings Access": ESOItemData("Delve Access",eso_region_unlock_id+330,  ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Sandblown Mine Access":    ESOItemData("Delve Access",eso_region_unlock_id+331,  ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Yldzuun Access":           ESOItemData("Delve Access",eso_region_unlock_id+332,  ItemClassification.progression, 1, 1, "Alik'r Desert"),
    "Torog's Spite Access":      ESOItemData("Delve Access",eso_region_unlock_id+333,  ItemClassification.progression, 1, 1, "Bangkorai"),
    "Troll's Toothpick Access": ESOItemData("Delve Access",eso_region_unlock_id+334,  ItemClassification.progression, 1, 1, "Bangkorai"),
    "Viridian Watch Access":    ESOItemData("Delve Access",eso_region_unlock_id+335,  ItemClassification.progression, 1, 1, "Bangkorai"),
    "Crypt of the Exiles Access":ESOItemData("Delve Access",eso_region_unlock_id+336, ItemClassification.progression, 1, 1, "Bangkorai"),
    "Klathzgar Access":         ESOItemData("Delve Access",eso_region_unlock_id+337,  ItemClassification.progression, 1, 1, "Bangkorai"),
    "Rubble Butte Access":      ESOItemData("Delve Access",eso_region_unlock_id+338,  ItemClassification.progression, 1, 1, "Bangkorai"),
    "Coldharbour Access":       ESOItemData("Zone Access",  eso_region_unlock_id+347,   ItemClassification.progression, 1, 1, "Coldharbour"),
    "The Chill Hollow Access":  ESOItemData("Delve Access",eso_region_unlock_id+359,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "Icehammer's Vault Access": ESOItemData("Delve Access",eso_region_unlock_id+360,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "Old Sord's Cave Access":   ESOItemData("Delve Access",eso_region_unlock_id+361,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "The Frigid Grotto Access": ESOItemData("Delve Access",eso_region_unlock_id+362,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "Stormcrag Crypt Access":   ESOItemData("Delve Access",eso_region_unlock_id+363,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "The Bastard's Tomb Access":ESOItemData("Delve Access",eso_region_unlock_id+364,  ItemClassification.progression, 1, 1, "Eastmarch"),
    "Auridon Access":           ESOItemData("Zone Access",  eso_region_unlock_id+381,   ItemClassification.progression, 1, 1, "Auridon"),
    "Reaper's March Access":    ESOItemData("Zone Access",  eso_region_unlock_id+382,   ItemClassification.progression, 1, 1, "Reaper's March"),
    "Grahtwood Access":         ESOItemData("Zone Access",  eso_region_unlock_id+383,   ItemClassification.progression, 1, 1, "Grahtwood"),
    "Ondil Access":             ESOItemData("Delve Access",eso_region_unlock_id+396,  ItemClassification.progression, 1, 1, "Auridon"),
    "Del's Claim Access":       ESOItemData("Delve Access",eso_region_unlock_id+397,  ItemClassification.progression, 1, 1, "Auridon"),
    "Entila's Folly Access":    ESOItemData("Delve Access",eso_region_unlock_id+398,  ItemClassification.progression, 1, 1, "Auridon"),
    "Wansalen Access":          ESOItemData("Delve Access",eso_region_unlock_id+399,  ItemClassification.progression, 1, 1, "Auridon"),
    "Mehrunes' Spite Access":   ESOItemData("Delve Access",eso_region_unlock_id+400,  ItemClassification.progression, 1, 1, "Auridon"),
    "Bewan Access":             ESOItemData("Delve Access",eso_region_unlock_id+401,  ItemClassification.progression, 1, 1, "Auridon"),
    "Lady Llarel's Shelter Access":ESOItemData("Delve Access",eso_region_unlock_id+405,ItemClassification.progression,1, 1, "Deshaan"),
    "Lower Bthanual Access":    ESOItemData("Delve Access",eso_region_unlock_id+406,  ItemClassification.progression, 1, 1, "Deshaan"),
    "Triple Circle Mine Access":ESOItemData("Delve Access",eso_region_unlock_id+407,  ItemClassification.progression, 1, 1, "Deshaan"),
    "Taleon's Crag Access":     ESOItemData("Delve Access",eso_region_unlock_id+408,  ItemClassification.progression, 1, 1, "Deshaan"),
    "Knife Ear Grotto Access":  ESOItemData("Delve Access",eso_region_unlock_id+409,  ItemClassification.progression, 1, 1, "Deshaan"),
    "The Corpse Garden Access": ESOItemData("Delve Access",eso_region_unlock_id+410,  ItemClassification.progression, 1, 1, "Deshaan"),
    "Avanchnzel Access":        ESOItemData("Delve Access",eso_region_unlock_id+413,  ItemClassification.progression, 1, 1, "The Rift"),
    "Ne Salas Access":          ESOItemData("Delve Access",eso_region_unlock_id+442,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Burroot Kwama Mine Access":ESOItemData("Delve Access",eso_region_unlock_id+444,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Mobar Mine Access":        ESOItemData("Delve Access",eso_region_unlock_id+447,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Thibaut's Cairn Access":   ESOItemData("Delve Access",eso_region_unlock_id+462,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Kuna's Delve Access":      ESOItemData("Delve Access",eso_region_unlock_id+463,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Fardir's Folly Access":    ESOItemData("Delve Access",eso_region_unlock_id+464,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Claw's Strike Access":     ESOItemData("Delve Access",eso_region_unlock_id+465,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Weeping Wind Cave Access": ESOItemData("Delve Access",eso_region_unlock_id+466,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Jode's Light Access":      ESOItemData("Delve Access",eso_region_unlock_id+467,  ItemClassification.progression, 1, 1, "Reaper's March"),
    "Dead Man's Drop Access":   ESOItemData("Delve Access",eso_region_unlock_id+468,  ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Tomb of the Apostates Access":ESOItemData("Delve Access",eso_region_unlock_id+469,ItemClassification.progression,1, 1, "Malabal Tor"),
    "Hoarvor Pit Access":       ESOItemData("Delve Access",eso_region_unlock_id+470,  ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Shael Ruins Access":       ESOItemData("Delve Access",eso_region_unlock_id+471,  ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Roots of Silvenar Access": ESOItemData("Delve Access",eso_region_unlock_id+472,  ItemClassification.progression, 1, 1, "Malabal Tor"),
    "Black Vine Ruins Access":  ESOItemData("Delve Access",eso_region_unlock_id+473,  ItemClassification.progression, 1, 1, "Malabal Tor"),
    "The Scuttle Pit Access":   ESOItemData("Delve Access",eso_region_unlock_id+475,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Vinedeath Cave Access":    ESOItemData("Delve Access",eso_region_unlock_id+477,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Wormroot Depths Access":  ESOItemData("Delve Access",eso_region_unlock_id+478,  ItemClassification.progression, 1, 1, "Grahtwood"),
    "Snapleg Cave Access":      ESOItemData("Delve Access",eso_region_unlock_id+480,  ItemClassification.progression, 1, 1, "The Rift"),
    "Fort Greenwall Access":    ESOItemData("Delve Access",eso_region_unlock_id+481,  ItemClassification.progression, 1, 1, "The Rift"),
    "Shroud Hearth Barrow Access":ESOItemData("Delve Access",eso_region_unlock_id+482,ItemClassification.progression, 1, 1, "The Rift"),
    "Faldar's Tooth Access":   ESOItemData("Delve Access",eso_region_unlock_id+484,  ItemClassification.progression, 1, 1, "The Rift"),
    "Broken Helm Hollow Access":ESOItemData("Delve Access",eso_region_unlock_id+485,  ItemClassification.progression, 1, 1, "The Rift"),
    "Stros M'kai Access":       ESOItemData("Zone Access",  eso_region_unlock_id+534,   ItemClassification.progression, 1, 1,"Stros M'kai"),
    "Betnikh Access":           ESOItemData("Zone Access",  eso_region_unlock_id+535,   ItemClassification.progression, 1, 1, "Betnikh"),
    "Khenarthi's Roost Access": ESOItemData("Zone Access",  eso_region_unlock_id+537,   ItemClassification.progression, 1, 1, "Khenarthi's Roost"),
    "Carac Dena Access":        ESOItemData("Delve Access",eso_region_unlock_id+575,  ItemClassification.progression, 1, 1, "Greenshade"),
    "Gurzag's Mine Access":     ESOItemData("Delve Access",eso_region_unlock_id+576,  ItemClassification.progression, 1, 1, "Greenshade"),
    "The Underroot Access":     ESOItemData("Delve Access",eso_region_unlock_id+577,  ItemClassification.progression, 1, 1, "Greenshade"),
    "Naril Nagaia Access":      ESOItemData("Delve Access",eso_region_unlock_id+578,  ItemClassification.progression, 1, 1, "Greenshade"),
    "Harridan's Lair Access":   ESOItemData("Delve Access",eso_region_unlock_id+579,  ItemClassification.progression, 1, 1, "Greenshade"),
    "Barrow Trench Access":     ESOItemData("Delve Access",eso_region_unlock_id+580,  ItemClassification.progression, 1, 1, "Greenshade"),
    "Craglorn Access":          ESOItemData("Zone Access",  eso_region_unlock_id+888,   ItemClassification.progression, 1, 1, "Craglorn"),
    "Molavar Access":           ESOItemData("Delve Access",eso_region_unlock_id+889,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Rkundzelft Access":        ESOItemData("Delve Access",eso_region_unlock_id+890,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Serpent's Nest Access":    ESOItemData("Delve Access",eso_region_unlock_id+891,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Ilthag's Undertower Access":ESOItemData("Delve Access",eso_region_unlock_id+892, ItemClassification.progression, 1, 1, "Craglorn"),
    "Ruins of Kardala Access":  ESOItemData("Delve Access",eso_region_unlock_id+893,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Loth'Na Caverns Access":   ESOItemData("Delve Access",eso_region_unlock_id+894,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Rkhardahrk Access":        ESOItemData("Delve Access",eso_region_unlock_id+895,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Haddock's Market Access":  ESOItemData("Delve Access",eso_region_unlock_id+896,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Chiselshriek Mine Access": ESOItemData("Delve Access",eso_region_unlock_id+897,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Buried Sands Access":      ESOItemData("Delve Access",eso_region_unlock_id+898,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Mtharnaz Access":          ESOItemData("Delve Access",eso_region_unlock_id+899,  ItemClassification.progression, 1, 1, "Craglorn"),
    "The Howling Sepulchers Access":ESOItemData("Delve Access",eso_region_unlock_id+900,ItemClassification.progression,1,1, "Craglorn"),
    "Balamath Access":          ESOItemData("Delve Access",eso_region_unlock_id+901,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Fearfangs Cavern Access":  ESOItemData("Delve Access",eso_region_unlock_id+902,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Exarch's Stronghold Access":ESOItemData("Delve Access",eso_region_unlock_id+903, ItemClassification.progression, 1, 1, "Craglorn"),
    "Zalgaz's Den Access":      ESOItemData("Delve Access",eso_region_unlock_id+904,  ItemClassification.progression, 1, 1, "Craglorn"),
    "Tombs of the Na-Totambu Access":ESOItemData("Delve Access",eso_region_unlock_id+905,ItemClassification.progression,1,1,"Craglorn"),
    "Hircine's Haunt Access":   ESOItemData("Delve Access",eso_region_unlock_id+906,  ItemClassification.progression, 1, 1, "Craglorn"),
    }
