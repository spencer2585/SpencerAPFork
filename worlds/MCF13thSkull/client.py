import asyncio
import colorama
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop

#Process order
#1. Open Client
#2. Connect to server
#3. Copy files to be patched to temp directory to keep unpatched versions
#4. Patch Files / Create in file
#5. Open Game
#6. await out file creation
#7. connect to out file
#8. Begin loop
#9. On Close: delete Patched Files
#10. Move unpatched files to original Location
#11. Quit Client

class MCF7Context(CommonContext):
    game = "Mystery Case Files: The 13th Skull"
    items_handling = 7
    command_processor = ClientCommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        # Item handling
        self.slot_data = {}
        self.force_resync_on_connect = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()


    async def on_items_received(self, items):
        print("[MCF] on_items_received", len(items))

    def on_package(self, cmd: str, args: dict):
        """Handle incoming packets from the server."""
        if cmd == "Connected":
            print("connected")

    def run_gui(self):
        from kvui import GameManager

        class MCF7Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "MCF: 13th Skull Client"

            def build(self):
                ret = super().build()
                return ret

        self.ui = MCF7Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

async def async_main(parsed_args):
    ctx = MCF7Context(parsed_args.connect, parsed_args.password)

    ctx.run_gui()

    await ctx.exit_event.wait()
    await ctx.shutdown()



def main(args=None):
    colorama.init()
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    asyncio.run(async_main(parsed_args))


def launch(args=None):
    main(args)