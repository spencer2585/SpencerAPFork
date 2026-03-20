from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DelveData:
    zone: str
    delve_id: int
    bosses: List[str] = field(default_factory=list)

DELVE_DATA: Dict[str, DelveData] = {
    #Glenumbra
    "Ilessan Tower" : DelveData(zone="Glenumbra", delve_id=309, bosses=["Gaetane"]),
    "Silumm" : DelveData(zone="Glenumbra", delve_id=310, bosses=["Sincano"]),
    "The Mines of Khuras": DelveData(zone="Glenumbra", delve_id=311, bosses=["Lilou"]),
    "Enduum": DelveData(zone="Glenumbra", delve_id=312, bosses=["Odilon"]),
    "Ebon Crypt": DelveData(zone="Glenumbra", delve_id=313, bosses=["The Ebon Lord"]),
    "Cryptwatch Fort": DelveData(zone="Glenumbra", delve_id=314, bosses=["Valenwe"]),
    #Rivenspire
    "Hildune's Secret Refuge": DelveData(zone="Rivenspire", delve_id=326, bosses=["Leidmir Corpse-Caller"]),
    "Orc's Finger Ruins" : DelveData(zone="Rivenspire", delve_id=324, bosses=["Fingaenion Forestsmasher"]),
    "Erokii Ruins": DelveData(zone="Rivenspire", delve_id=325, bosses=["Abal-jo","Miruin Woodwalker","Earelar"]),
    "Crestshade Mines": DelveData(zone="Rivenspire", delve_id=321, bosses=["Grimtooth"]),
    "Flyleaf Catacombs": DelveData(zone="Rivenspire", delve_id=322, bosses=["Miremonwe Spellslinger"]),
    "Tribulation Crypt": DelveData(zone="Rivenspire", delve_id=323, bosses=["Alameric Daillon"]),
    #Stormhaven
    "Bearclaw Mine": DelveData(zone="Stormhaven", delve_id=319, bosses=["Octavia"]),
    "Norvulk Ruins": DelveData(zone="Stormhaven", delve_id=320, bosses=["Nariam"]),
    "Pariah Catacombs": DelveData(zone="Stormhaven", delve_id=317, bosses=["Uncle Bones"]),
    "Farangel's Delve": DelveData(zone="Stormhaven", delve_id=318, bosses=["Dimitri"]),
    "Portdun Watch": DelveData(zone="Stormhaven", delve_id=315, bosses=["Birakh-do","Ariane"]),
    "Koeglin Mine": DelveData(zone="Stormhaven", delve_id=316, bosses=["Girara"]),
    #Bankorai
    "Trolls Toothpick": DelveData(zone="Bangkorai", delve_id=334, bosses=["Pale Squnque"]),
    "Torog's Spite": DelveData(zone="Bangkorai", delve_id=333, bosses=["Lorogdu gra-Gulash"]),
    "Viridian Watch": DelveData(zone="Bangkorai", delve_id=335, bosses=["Curnard the Generous"]),
    "Crypt of the Exiles": DelveData(zone="Bangkorai", delve_id=336, bosses=["Ulbazar Thief-Lord"]),
    "Rubble Butte": DelveData(zone="Bangkorai", delve_id=338, bosses=["Lady Edwyge"]),
    "Klathzgar": DelveData(zone="Bangkorai", delve_id=337, bosses=["Urenenya's Soul","Klathzgar's Centurion"]),
    #Alik'r Desert
    "Santaki": DelveData(zone="Alik'r Desert", delve_id=327, bosses=["Tarrent Herano"]),
    "Divad's Chagrin Mine": DelveData(zone="Alik'r Desert", delve_id=328, bosses=["Nokhailaedhaz"]),
    "Aldunz": DelveData(zone="Alik'r Desert", delve_id=329, bosses=["Thinks-in-Gears"]),
    "Sandblown Mine": DelveData(zone="Alik'r Desert", delve_id=331, bosses=["Mirudda"]),
    "Yldzuun": DelveData(zone="Alik'r Desert", delve_id=332, bosses=["Captain Candidus"]),
    "Coldrock Digging": DelveData(zone="Alik'r Desert", delve_id=330, bosses=["Feremuzh"]),
    #Auridon
    "Mehrunes' Spite": DelveData(zone="Auridon", delve_id=400, bosses=["Mati"]),
    "Wansalen": DelveData(zone="Auridon", delve_id=399, bosses=["Nolonir"]),
    "Bewan": DelveData(zone="Auridon", delve_id=401, bosses=["Camandar"]),
    "Entila's Folly": DelveData(zone="Auridon", delve_id=398, bosses=["Bakhig"]),
    "Ondil": DelveData(zone="Auridon", delve_id=396, bosses=["Aluvus"]),
    "Del's Claim": DelveData(zone="Auridon", delve_id=367, bosses=["Polinus"]),
    #Grahtwood
    "Wormroot Depths": DelveData(zone="Grahtwood", delve_id=478, bosses=["Raynia"]),
    "Vinedeath Cave": DelveData(zone="Grahtwood", delve_id=477, bosses=["Madruin"]),
    "Burroot Kwama Mine": DelveData(zone="Grahtwood", delve_id=444, bosses=["Stormhead the Ravenous"]),
    "The Scuttle Pit": DelveData(zone="Grahtwood", delve_id=475, bosses=["Spider Queen"]),
    "Mobar Mine": DelveData(zone="Grahtwood", delve_id=447, bosses=["Sgolag"]),
    "Ne Salas": DelveData(zone="Grahtwood", delve_id=442, bosses=["Lieutenant Khari"]),
    #Greenshade
    "Barrow Trench": DelveData(zone="Greenshade", delve_id=580, bosses=["Overseer Basri"]),
    "The Underroot": DelveData(zone="Greenshade", delve_id=577, bosses=["Dormina Ssaranth"]),
    "Harridan's Lair": DelveData(zone="Greenshade", delve_id=579, bosses=["Razorclaw"]),
    "Gurzag's Mine": DelveData(zone="Greenshade", delve_id=576, bosses=["Retribution"]),
    "Naril Nagaia": DelveData(zone="Greenshade", delve_id=578, bosses=["Archmage Camaano"]),
    "Carac Dena": DelveData(zone="Greenshade", delve_id=575, bosses=["Urrumaz the Terrifying"]),
    #Malabal Tor
    "Black Vine Ruins": DelveData(zone="Malabal Tor", delve_id=473, bosses=["Blackvine Strangler"]),
    "Roots of Silvenar": DelveData(zone="Malabal Tor", delve_id=472, bosses=["Adavos Dren"]),
    "Shael Ruins": DelveData(zone="Malabal Tor", delve_id=471, bosses=["Arrai"]),
    "Tomb of the Apostates": DelveData(zone="Malabal Tor", delve_id=469, bosses=["Gwaeregil"]),
    "Hoarvor Pit": DelveData(zone="Malabal Tor", delve_id=470, bosses=["Oghezai"]),
    "Dead Man's Drop": DelveData(zone="Malabal Tor", delve_id=468, bosses=["Captain Shammin"]),
    #Reapers March
    "Fardir's Folly": DelveData(zone="Reaper's March", delve_id=464, bosses=["Ravo Peltrasius"]),
    "Kuna's Delve": DelveData(zone="Reaper's March", delve_id=463, bosses=["Limbrender"]),
    "Jode's Light": DelveData(zone="Reaper's March", delve_id=467, bosses=["Yenadar"]),
    "Thibaut's Cairn": DelveData(zone="Reaper's March", delve_id=462, bosses=["Worm Eremite"]),
    "Claw's Strike": DelveData(zone="Reaper's March", delve_id=465, bosses=["Lord Tawnlii-do","Fishbreath"]),
    "Weeping Wind Cave": DelveData(zone="Reaper's March", delve_id=566, bosses=["Nimriian"]),
    #Stonefalls
    "Inner Sea Armature": DelveData(zone="Stonefalls", delve_id=287, bosses=["Zozuzetharus"]),
    "Emberflint Mine": DelveData(zone="Stonefalls", delve_id=296, bosses=["Maebomaz"]),
    "Mephala's Nest": DelveData(zone="Stonefalls", delve_id=288, bosses=["Gozzark"]),
    "Hightide Hollow": DelveData(zone="Stonefalls", delve_id=290, bosses=["Oodegu"]),
    "Softloam Cavern": DelveData(zone="Stonefalls", delve_id=289, bosses=["Dugrul"]),
    "Sheogorath's Tongue": DelveData(zone="Stonefalls", delve_id=291, bosses=["Calls-to-Nature","Dezanu"]),
    #Deshaan
    "Knife Ear Grotto": DelveData(zone="Deshaan", delve_id=409, bosses=["Drulshasa"]),
    "The Corpse Garden": DelveData(zone="Deshaan", delve_id=410, bosses=["General Celdien"]),
    "Triple Circle Mine": DelveData(zone="Deshaan", delve_id=407, bosses=["Bonetooth"]),
    "Taleon's Crag": DelveData(zone="Deshaan", delve_id=408, bosses=["Egg-Eater"]),
    "Lady Llarel's Shelter": DelveData(zone="Deshaan", delve_id=405, bosses=["Lady Llarel"]),
    "Lower Bthanual": DelveData(zone="Deshaan", delve_id=406, bosses=["Bthanual Centurion"]),
    #Shadowfen
    "Shrine of the Black Maw": DelveData(zone="Shadowfen", delve_id=270, bosses=["Peers-Through-Glass"]),
    "Broken Tusk": DelveData(zone="Shadowfen", delve_id=271, bosses=["Naeraizozan"]),
    "Grandranen Ruins": DelveData(zone="Shadowfen", delve_id=275, bosses=["Fenlord"]),
    "Atanz Ruins": DelveData(zone="Shadowfen", delve_id=272, bosses=["Stormscale"]),
    "Onkobra Kwama Mine": DelveData(zone="Shadowfen", delve_id=274, bosses=["Kwama Overseer"]),
    "Chid-Moska Ruins": DelveData(zone="Shadowfen", delve_id=273, bosses=["Lirlane"]),
    #Eastmarch
    "The Chill Hollow": DelveData(zone="Eastmarch", delve_id=359, bosses=["Nomeg Chal"]),
    "Icehammer's Vault": DelveData(zone="Eastmarch", delve_id=360, bosses=["Thane Icehammer"]),
    "The Bastard's Tomb": DelveData(zone="Eastmarch", delve_id=364, bosses=["Agnenor the Blade"]),
    "Stormcrag Crypt": DelveData(zone="Eastmarch", delve_id=363, bosses=["Deathknight Stormcrag"]),
    "Old Sord's Cave": DelveData(zone="Eastmarch", delve_id=361, bosses=["Gadof","Eorim the Hammer", "Braxel"]),
    "The Frigid Grotto": DelveData(zone="Eastmarch", delve_id=362, bosses=["Frostbite Mangler"]),
    #The Rift
    "Broken Helm Hollow": DelveData(zone="The Rift", delve_id=485, bosses=["Skullcrusher"]),
    "Fort Greenwall": DelveData(zone="The Rift", delve_id=481, bosses=["Uggurek the Vile"]),
    "Faldar's Tooth": DelveData(zone="The Rift", delve_id=484, bosses=["Rozelun"]),
    "Avanchnzel": DelveData(zone="The Rift", delve_id=413, bosses=["Thzallek Eft"]),
    "Snapleg Cave": DelveData(zone="The Rift", delve_id=480, bosses=["Frostmaiden Apa"]),
    "Shroud Hearth Barrow": DelveData(zone="The Rift", delve_id=482, bosses=["Jakalor"]),
    #Craglorn
    "Fearfangs Cavern": DelveData(zone="Craglorn", delve_id=902, bosses=["Sepilisk"]),
    "Buried Sands": DelveData(zone="Craglorn", delve_id=898, bosses=["Den Mother","The Swarming Tide"]),
    "Mtharnaz": DelveData(zone="Craglorn", delve_id=899, bosses=["The Skillful Seamstress","The Brass Hatchling"]),
    "Serpent's Nest": DelveData(zone="Craglorn", delve_id=891, bosses=["Taurieae","Aurieae","Laurieae"]),
    "Ruins of Kardala": DelveData(zone="Craglorn", delve_id=893, bosses=["Rajdara the Restless One","Satagna","Izrunath the Corruptor"]),
    "Tombs of the Na-Totambu": DelveData(zone="Craglorn", delve_id=905, bosses=["Prince Tarjal the Lost","The Servile Staff","The Craven Shield","The Funbled Knife","The Glorious Coil","The Hungry Piller"]),
    "Loth'Na Caverns": DelveData(zone="Craglorn", delve_id=894, bosses=["Visskar"]),
    "Rkhardahrk": DelveData(zone="Craglorn", delve_id=895, bosses=["The Last Sentinel"]),
    "Zalgaz's Den": DelveData(zone="Craglorn", delve_id=904, bosses=["Zalgaz"]),
    "Exarch's Stronghold": DelveData(zone="Craglorn", delve_id=903, bosses=["Grothuska","Kurzoth","Exarch Braadoth","Agganor","Ordooth the Corruptor"]),
    "The Howling Sepulchers": DelveData(zone="Craglorn", delve_id=900, bosses=["Akiirdal"]),
    "Ilthag's Undertower": DelveData(zone="Craglorn", delve_id=892, bosses=["Rahk","Vosh","Zizzikkiz'Tk","Stormbringer","Vrauloch","Uzka Trollfeeder", "Killraken"]),
    "Hircine's Haunt": DelveData(zone="Craglorn", delve_id=906, bosses=["Iron Head","Packleader Sigmund"]),
    "Chiselshriek Mine": DelveData(zone="Craglorn", delve_id=897, bosses=["The Gracious Beacon"]),
    "Rkundzelft": DelveData(zone="Craglorn", delve_id=890, bosses=["Mzeklok"]),
    "Haddock's Market": DelveData(zone="Craglorn", delve_id=896, bosses=["Grandmother Thunder","Ariana At-Fara"]),
    "Balamath": DelveData(zone="Craglorn", delve_id=901, bosses=["Storm Mage Iribia","Fire Mage Linia","Frost Mage Porcia"]),
    "Molavar": DelveData(zone="Craglorn", delve_id=889, bosses=["Thalie the Voracious"]),
}