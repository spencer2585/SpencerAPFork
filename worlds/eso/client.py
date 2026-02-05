import asyncio
import colorama
import logging
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop
from Utils import async_start
from pathlib import Path
import time

logger = logging.getLogger("Client")

VICTORY_ITEM_ID = 149995  # eso_base_id - 5

ESO_BASE = Path.home() / "Documents" / "Elder Scrolls Online" / "live"
SAVED_VARIABLES = ESO_BASE / "SavedVariables" / "APESO.lua"
ITEMS_FILE = ESO_BASE / "AddOns" / "APESO" / "Items.lua"
OPTIONS_FILE = ESO_BASE / "AddOns" / "APESO" / "Options.lua"

class EsoState:
    def __init__(self):
        self.version = None
        self.char_id = None
        self.node_info = []
        self.completed_quests = set()


class SavedVariablesReader:

    def parse(self, path: Path, locked_char_id: str = None):
        """Parse SavedVariables file.

        Args:
            path: Path to the SavedVariables file
            locked_char_id: If provided, use this character ID for quest lookups
                           instead of the CharID from the file
        """
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

        # CHAR ID (current character from file)
        idx = text.find("CharID")
        if idx != -1:
            eq = text.find("=", idx)
            q1 = text.find('"', eq)
            q2 = text.find('"', q1 + 1)
            if q1 != -1 and q2 != -1:
                state.char_id = text[q1 + 1:q2].strip()

        # NODE INFO (account-wide)
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
        # Use locked_char_id if provided, otherwise use char_id from file
        quest_char_id = locked_char_id if locked_char_id else state.char_id
        idx = text.find("CompletedQuestsByChar")
        if idx != -1 and quest_char_id:
            b1 = text.find("{", idx)
            b2 = self.find_matching_brace(text, b1)
            if b1 != -1 and b2 != -1:
                block = text[b1 + 1:b2]
                marker = f'["{quest_char_id}"]'
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


class OptionsWriter:
    """Writes slot_data options to Options.lua for the game mod."""

    def write_options(self, slot_data: dict):
        if not slot_data:
            print("[ESO] No slot_data to write.")
            return

        skill_mode = slot_data.get("SkillRandomization", 0)
        char_class = slot_data.get("CharacterClass", "")
        char_race = slot_data.get("CharacterRace", "")
        enabled_categories = slot_data.get("EnabledSkillCategories", {})

        lines = [
            "-- APESO Options",
            "-- This file is auto-generated by the Archipelago client on connection",
            "-- Do not edit manually - values will be overwritten on connection",
            "",
            "APESO_Options = {",
            f"    SkillRandomization = {skill_mode},",
            f'    CharacterClass = "{char_class}",',
            f'    CharacterRace = "{char_race}",',
            "    EnabledSkillCategories = {",
        ]

        # Write enabled categories
        for category, enabled in enabled_categories.items():
            lua_bool = "true" if enabled else "false"
            lines.append(f'        ["{category}"] = {lua_bool},')

        lines.append("    },")
        lines.append("}")

        try:
            OPTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
            OPTIONS_FILE.write_text("\n".join(lines), encoding="utf-8")
            print(f"[ESO] Wrote Options.lua (SkillMode={skill_mode}, Class={char_class}, Race={char_race})")
        except Exception as e:
            print("[ESO] Failed to write Options.lua:", e)



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

        # Pass the locked character ID so quests are read for the correct character
        state = self.reader.parse(SAVED_VARIABLES, self.ctx.current_char_id)
        if state:
            await self.ctx.handle_eso_state(state)





class ESOClientCommandProcessor(ClientCommandProcessor):
    """Command processor with ESO-specific commands."""

    def _cmd_switch(self) -> bool:
        """Switch to the pending new character."""
        ctx: ESOContext = self.ctx
        if ctx.pending_char_id and ctx.char_locked:
            # Accept the character switch
            old_char = ctx.current_char_id
            ctx.current_char_id = ctx.pending_char_id
            ctx.pending_char_id = None
            ctx.char_locked = False
            self.output(f"[ESO] Switched from {old_char} to {ctx.current_char_id}. Resuming.")
            # Trigger immediate file read to send locations/items
            async_start(ctx.sync_now(), name="switch sync")
        elif not ctx.char_locked:
            self.output("[ESO] No pending character switch.")
        else:
            self.output("[ESO] No new character detected yet.")
        return True


class ESOContext(CommonContext):
    game = "Elder Scrolls Online"
    items_handling = 7
    command_processor = ESOClientCommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        # ESO state
        self.current_char_id = None
        self.pending_char_id = None  # New character awaiting confirmation
        self.char_locked = False

        # Item handling
        self.items_writer = ItemsWriter()
        self.options_writer = OptionsWriter()
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

    async def sync_now(self):
        """Immediately read SavedVariables and process state."""
        if not SAVED_VARIABLES.exists():
            logger.info("[ESO] SavedVariables file not found.")
            return
        reader = SavedVariablesReader()
        state = reader.parse(SAVED_VARIABLES, self.current_char_id)
        if state:
            await self.handle_eso_state(state)

    async def handle_eso_state(self, state: EsoState):

        # character protection
        if self.current_char_id is None:
            # First character detected, lock to it
            self.current_char_id = state.char_id
            logger.info(f"[ESO] Locked to character: {self.current_char_id}")

        elif state.char_id == self.current_char_id:
            # Correct character - if we were locked, unlock
            if self.char_locked:
                self.char_locked = False
                self.pending_char_id = None
                logger.info("[ESO] Original character detected. Resuming.")

        else:
            # Different character detected
            if not self.char_locked or state.char_id != self.pending_char_id:
                # New character (or different from pending)
                self.char_locked = True
                self.pending_char_id = state.char_id
                logger.info(f"[ESO] New character detected: {state.char_id}")
                logger.info("[ESO] Type '/switch' to switch to this character, or switch back to your original character.")
            return  # Don't process locations while locked

        # convert checks to AP IDs
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

    def on_package(self, cmd: str, args: dict):
        """Handle incoming packets from the server."""
        if cmd == "Connected":
            print("[ESO] Connected packet received!")
            print("[ESO] Connected → clearing Items.lua")
            self.items_writer.reset()

            # Write slot_data options to Options.lua
            slot_data = args.get("slot_data", {})
            print(f"[ESO] slot_data = {slot_data}")
            if slot_data:
                print("[ESO] Writing slot_data to Options.lua...")
                self.options_writer.write_options(slot_data)
            else:
                print("[ESO] No slot_data received.")


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

                # Check for Victory item and send goal complete
                for item in ctx.items_received:
                    if item.item == VICTORY_ITEM_ID:
                        if ctx.finished_game:
                            continue
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                        ctx.finished_game = True
                        print("[ESO] Victory! Goal complete sent to server.")
                        break
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
