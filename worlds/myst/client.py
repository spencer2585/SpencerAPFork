import asyncio
import colorama
import json
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop

host = "localhost"
port = 35000
SIZE_CAP = 10 * 1024 * 1024 #10mb
PROTOCOL_VERSION = 1
ACCEPTED_GAMES = {"RealMyst"}

class MystContext(CommonContext):
    game = "Myst"
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


    def run_gui(self):
        from kvui import GameManager

        class MystManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Myst Client"

            def build(self):
                ret = super().build()
                return ret

        self.ui = MystManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def handle_dll(self, reader, writer):
        self.game_writer = writer
        try:
            while not self.exit_event.is_set():
                size = await get_message_size(reader)
                data = await get_message_body(reader, size)
                await self.dispatch(data)

        except(asyncio.IncompleteReadError, ConnectionError, ValueError) as e:
            print(f"game connection closed: {e}")
        finally:
            self.game_writer = None
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

    async def dispatch(self, data):
        msg_type = data.get("type")
        print(f"Got Message type: {msg_type}")
        if msg_type == "connection":
            if data.get("protocol_version") != PROTOCOL_VERSION:
                await send_message(self.game_writer, {"type": "connection_ack", "accepted": False, "reason": "protocol_mismatch"})
            elif data.get("game") not in ACCEPTED_GAMES:
                await send_message(self.game_writer, {"type": "connection_ack", "accepted": False, "reason": "game_mismatch"})
            else:
                await send_message(self.game_writer, {"type": "connection_ack", "accepted": True})



async def get_message_size(reader):
    data = await reader.readexactly(4)
    number = int.from_bytes(data, "big")
    if number > SIZE_CAP:
        raise ValueError(f"messsage size {number} exceeds cap")
    return number

async def get_message_body(reader, size):
    data = await reader.readexactly(size)
    return json.loads(data.decode("utf-8"))

async def send_message(writer, message):
    body_bytes = json.dumps(message).encode("utf-8")
    prefix = len(body_bytes).to_bytes(4, "big")
    writer.write(prefix)
    writer.write(body_bytes)
    await writer.drain()

async def async_main(parsed_args):
    ctx = MystContext(parsed_args.connect, parsed_args.password)

    ctx.run_gui()
    server = await asyncio.start_server(ctx.handle_dll, host , port )

    await ctx.exit_event.wait()
    await server.wait_closed()
    await ctx.shutdown()



def main(args=None):
    colorama.init()
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    asyncio.run(async_main(parsed_args))


def launch(args=None):
    main(args)