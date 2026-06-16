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

    world.final_mission = world.random.choice(missions)
    missions.remove(world.final_mission)
    world.starting_mission = world.random.choice(missions)
    world.missions = [m for m in missions]


