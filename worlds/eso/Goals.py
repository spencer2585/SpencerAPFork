def set_goals(world):
    player = world.player
    mw = world.multiworld

    # Completion condition: restore the Amulet of Kings
    mw.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )
