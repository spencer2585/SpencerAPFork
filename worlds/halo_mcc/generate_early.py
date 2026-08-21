from .data.skulls import *

def generate_early(world):
    missions = [
        "The Pillar of Autumn",
        "Halo (CE)",
        "The Truth and Reconciliation",
        "The Silent Cartographer",
        "Assault on the Control Room",
        "343 Guilty Spark",
        "The Library",
        "Two Betrayals",
        "Keyes",
        "The Maw",
    ]

    if world.options.ce_final_mission == 11:
        world.final_mission = world.random.choice(missions)
    else:
        index = world.options.ce_final_mission - 1
        world.final_mission = missions[index]
    missions.remove(world.final_mission)
    world.starting_mission = world.random.choice(missions)
    world.missions = [m for m in missions]
    print("final Mission: " + world.final_mission)

    if world.options.skullsanity.value >=2:
        if world.options.ce_enabled.value == 1:
            skull_list = []
            for i in GAME_SKULLS["ce"]:
                i = f"{i} Skull"
                if i not in skull_list:
                    skull_list.append(i)

        world.ceskulls = [i for i in skull_list]



