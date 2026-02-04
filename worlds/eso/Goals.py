def set_goals(world):
    player = world.player
    mw = world.multiworld

    # Completion condition: Victory is placed at "Main Quest - God of Schemes" in Rules.py
    mw.completion_condition[player] = lambda state: state.has("Victory", player)
