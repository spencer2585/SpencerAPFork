from worlds.AutoWorld import World
from .webWorld import MCF7Web
from .mcf7_options import MCF7Options
from typing import Any
from worlds.LauncherComponents import Type, components, launch_subprocess, Component

class MCF13thSkullWorld(World):
    """
    yipee
    """

    game = "Mystery Case Files: The 13th Skull"
    options_dataclass = MCF7Options
    options: MCF7Options
    required_client_version = (0, 0, 1)
    web = MCF7Web()

    item_name_to_id = {}
    location_name_to_id = {}

    def run_client(*args):
        from .client import launch
        launch_subprocess(launch, name="MCF13thSkullClient", args=args)

    components.append(
        Component("MCF: 13th Skull Client", func=run_client, component_type=Type.CLIENT)
    )