import asyncio
import colorama
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop

host = "localhost"
port = 35000

class MCCContext(CommonContext):
    game = "Halo The Master Chief Collection"
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


    def on_package(self, cmd: str, args: dict):
        """Handle incoming packets from the server."""
        if cmd == "Connected":
            print("connected")

    def run_gui(self):
        from kvui import GameManager

        class MCCManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Halo MCC Client"

            def build(self):
                ret = super().build()
                return ret

        self.ui = MCCManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def handle_dll(self, reader, writer):
        print("DLL connected")


async def async_main(parsed_args):
    ctx = MCCContext(parsed_args.connect, parsed_args.password)

    ctx.run_gui()
    await asyncio.start_server(ctx.handle_dll, host , port )

    await ctx.exit_event.wait()
    await ctx.shutdown()



def main(args=None):
    colorama.init()
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    asyncio.run(async_main(parsed_args))


def launch(args=None):
    main(args)