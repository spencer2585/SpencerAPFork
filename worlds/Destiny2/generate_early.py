from BaseClasses import MultiWorld
from .items import items_dict, D2Item

primaryFrames = ["Auto Rifles", "Scout Rifle","Pulse Rifle","Hand Cannon","Submachine Gun","Sidearm","Bow"]
specialFrames = ["Shotgun","Grenade Launcher","Fusion Rifle","Sniper Rifle","Glaive"]
powerFrames = ["Sword","Grenade Launcher", "Rocket Launcher", "Linear Fusion Rifle", "Machine Gun"]
def generate_early(world):
    #Select starting frames
    true_primary_frames = primaryFrames.copy()
    true_special_frames = specialFrames.copy()
    true_power_frames = powerFrames.copy()
    starting_frames = []
    primary_frame_count = world.options.primary_frames
    special_frame_count = world.options.special_frames
    power_frame_count = world.options.power_frames

    world.startingFrames = []

    for frame in world.options.rare_special_frames:
        if frame not in true_special_frames:
            true_special_frames.append(frame)

    for frame in true_power_frames:
        if frame not in true_primary_frames:
            true_primary_frames.append(frame)

    #select primary frames
    while primary_frame_count > 0:
        #quit if no valid primary frames left
        if not true_primary_frames:
            break
        #choose a random frame from the list
        selected_frame = world.random.choice(true_primary_frames)
        #if frame is also a special weapon frame
        if selected_frame in true_special_frames:
            if special_frame_count > 0:
                special_frame_count -= 1
                primary_frame_count -= 1
                starting_frames.append(selected_frame)
                true_primary_frames.remove(selected_frame)
                true_special_frames.remove(selected_frame)
            else:
                #remove from candidates
                true_primary_frames.remove(selected_frame)
                continue
        #if frame is also a power weapon frame
        elif selected_frame in true_power_frames:
            if power_frame_count > 0:
                power_frame_count -= 1
                primary_frame_count -= 1
                starting_frames.append(selected_frame)
                true_primary_frames.remove(selected_frame)
                true_power_frames.remove(selected_frame)
            else:
                true_primary_frames.remove(selected_frame)
                continue
        #normal primary only frame
        else:
            true_primary_frames.remove(selected_frame)
            starting_frames.append(selected_frame)

    #special weapon frames
    while special_frame_count > 0:
        if not true_special_frames:
            break
        selected_frame = world.random.choice(true_special_frames)
        if selected_frame in primaryFrames:
            true_special_frames.remove(selected_frame)
            continue
        if selected_frame in true_power_frames:
            if power_frame_count > 0:
                power_frame_count -= 1
                starting_frames.append(selected_frame)
                true_power_frames.remove(selected_frame)
                true_special_frames.remove(selected_frame)
                special_frame_count -= 1
            else:
                true_special_frames.remove(selected_frame)
                continue
        else:
            special_frame_count -= 1
            true_special_frames.remove(selected_frame)
            starting_frames.append(selected_frame)

    while power_frame_count > 0:
        if not true_power_frames:
            break
        selected_frame = world.random.choice(true_power_frames)
        if selected_frame in primaryFrames:
            true_power_frames.remove(selected_frame)
            continue
        else:
            power_frame_count -= 1
            true_power_frames.remove(selected_frame)
            starting_frames.append(selected_frame)

    #start inventory all starting frames
    for frame in starting_frames:
        name = f"{frame} Frame"
        data = items_dict[name]
        world.startingFrames.append(name)
        world.multiworld.push_precollected(D2Item(name, data.classification,data.id, world.player))

