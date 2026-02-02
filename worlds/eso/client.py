import asyncio
import colorama
from CommonClient import CommonContext, get_base_parser, gui_enabled, server_loop
from pathlib import Path
import time

ESO_BASE = Path.home() / "Documents" / "Elder Scrolls Online" / "live"
SAVED_VARIABLES = ESO_BASE / "SavedVariables" / "APESO.lua"
ITEMS_FILE = ESO_BASE / "AddOns" / "APESO" / "Items.lua"

class EsoState:
    def __init__(self):
        self.version = None
        self.char_id = None
        self.node_info = []
        self.completed_quests = set()


class SavedVariablesReader:

    def parse(self, path: Path):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print("Failed to read SavedVariables:", e)
            return None

        state = EsoState()

        # VERSION
        idx = text.find("version")
        if idx != -1:
            eq = text.find("=", idx)
            end = min([p for p in [
                text.find(",", eq), text.find("\n", eq), text.find("}", eq)
            ] if p != -1], default=-1)
            if eq != -1 and end != -1:
                try:
                    state.version = int(text[eq + 1:end].strip())
                except ValueError:
                    pass

        # CHAR ID
        idx = text.find("CharID")
        if idx != -1:
            eq = text.find("=", idx)
            q1 = text.find('"', eq)
            q2 = text.find('"', q1 + 1)
            if q1 != -1 and q2 != -1:
                state.char_id = text[q1 + 1:q2].strip()

        # NODE INFO
        idx = text.find("NodeInfo")
        if idx != -1:
            b1 = text.find("{", idx)
            b2 = self.find_matching_brace(text, b1)
            if b1 != -1 and b2 != -1:
                block = text[b1 + 1:b2]
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("--"):
                        continue
                    if "true" in line:
                        state.node_info.append(True)
                    elif "false" in line:
                        state.node_info.append(False)

        # COMPLETED QUESTS BY CHAR
        idx = text.find("CompletedQuestsByChar")
        if idx != -1 and state.char_id:
            b1 = text.find("{", idx)
            b2 = self.find_matching_brace(text, b1)
            if b1 != -1 and b2 != -1:
                block = text[b1 + 1:b2]
                marker = f'["{state.char_id}"]'
                cidx = block.find(marker)
                if cidx != -1:
                    cb1 = block.find("{", cidx)
                    cb2 = self.find_matching_brace(block, cb1)
                    if cb1 != -1 and cb2 != -1:
                        char_block = block[cb1 + 1:cb2]
                        for line in char_block.splitlines():
                            line = line.strip()
                            if line.startswith("--"):
                                continue
                            lb = line.find("[")
                            rb = line.find("]")
                            if lb != -1 and rb != -1 and "true" in line:
                                try:
                                    state.completed_quests.add(int(line[lb+1:rb]))
                                except ValueError:
                                    pass

        return state

    def find_matching_brace(self, text, open_index):
        depth = 0
        for i in range(open_index, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return i
        return -1


class ItemsWriter:
    def __init__(self):
        self.items = []

    def reset(self):
        self.items.clear()
        self.write_file()

    def add_item(self, item_id, location_id):
        self.items.append((item_id, location_id))
        self.write_file()

    def set_all(self, items):
        self.items = list(items)
        self.write_file()

    def write_file(self):
        lines = ["APESO_ReceivedItems = {"]

        for item_id, location_id in self.items:
            lines.append(f"    {{ item_id = {item_id}, location_id = {location_id} }},")

        lines.append("}")

        try:
            ITEMS_FILE.parent.mkdir(parents=True, exist_ok=True)
            ITEMS_FILE.write_text("\n".join(lines), encoding="utf-8")
            print(f"[ESO] Wrote items.lua with {len(self.items)} items.")
        except Exception as e:
            print("[ESO] Failed to write items.lua", e)



class EsoFilePoller:

    def __init__(self, ctx):
        self.ctx = ctx
        self.last_modified = 0
        self.reader = SavedVariablesReader()

    async def run(self):
        while not self.ctx.exit_event.is_set():
            try:
                if SAVED_VARIABLES.exists():
                    modified = SAVED_VARIABLES.stat().st_mtime
                    if modified != self.last_modified:
                        self.last_modified = modified
                        await self.on_change(modified)
                await asyncio.sleep(1.5)
            except asyncio.CancelledError:
                return
            except Exception as e:
                self.ctx.logger.exception("ESO poller error", exc_info=e)

    async def on_change(self, modified):
        if time.time() - modified > 10:
            print("Ignoring stale SavedVariables.")
            return

        state = self.reader.parse(SAVED_VARIABLES)
        if state:
            await self.ctx.handle_eso_state(state)





class ESOContext(CommonContext):
    game = "Elder Scrolls Online"
    items_handling = 7

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        # ESO state
        self.current_char_id = None
        self.char_locked = False

        # Item handling
        self.items_writer = ItemsWriter()
        self._last_item_count = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()


    async def on_items_received(self, items):
        print("[ESO] on_items_received", len(items))

        # full resync always sent on connect
        self.items_writer.reset()

        for item in items:
            self.items_writer.add_item(item.item, item.location)

    async def handle_eso_state(self, state: EsoState):

        # ---- character protection ----
        if self.current_char_id is None:
            self.current_char_id = state.char_id
            print("Locked to character:", self.current_char_id)

        elif state.char_id != self.current_char_id:
            if not self.char_locked:
                self.char_locked = True
                self.logger.warning("Character switched! Client paused.")
                await self.gui_error("Character changed! Restart client or override.")
            return

        # ---- convert checks to AP IDs ----
        locations = set()

        for idx, done in enumerate(state.node_info, start=1):
            if done:
                locations.add(150_000 + (idx - 1))

        for q in state.completed_quests:
            locations.add(151_000 + q)

        new = locations - self.checked_locations

        if new:
            await self.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(new)
            }])

    async def on_package(self, cmd, args):
        print("[AP PACKET]", cmd)
        super().on_package(cmd, args)

        if cmd == "Connected":
            print("[ESO] Connected → clearing Items.lua")
            self.items_writer.reset()


async def item_watcher(ctx: ESOContext):
    try:
        while not ctx.exit_event.is_set():
            await ctx.watcher_event.wait()
            ctx.watcher_event.clear()

            print("[DEBUG] watcher fired")

            if len(ctx.items_received) != ctx._last_item_count:
                print(f"[ESO] Item sync: {len(ctx.items_received)} items")

                ctx.items_writer.set_all(
                    (item.item, item.location)
                    for item in ctx.items_received
                )

                ctx._last_item_count = len(ctx.items_received)
    except Exception as e:
        print("[FATAL] Item watcher crashed:", e)
        raise


async def async_main(parsed_args):
    ctx = ESOContext(parsed_args.connect, parsed_args.password)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    poller = EsoFilePoller(ctx)
    ctx.poller_task = asyncio.create_task(poller.run(), name="eso poller")
    ctx.item_task = asyncio.create_task(item_watcher(ctx), name="item watcher")

    if gui_enabled:
        ctx.run_gui()
    else:
        ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()



def main(args=None):
    colorama.init()
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    asyncio.run(async_main(parsed_args))


def launch(args=None):
    main(args)
