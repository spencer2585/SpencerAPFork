import asyncio
import colorama
import logging
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop
from Utils import async_start
from pathlib import Path
import time
from . import ESOWorld

logger = logging.getLogger("Client")

VICTORY_ITEM_ID = 149995  # eso_base_id - 5

mods_folder_str = str(ESOWorld.settings.mods_folder)
mods_folder_path = Path(mods_folder_str)


class ESOConfig:
    """Holds ESO file paths that can be updated at runtime."""

    def __init__(self):
        if mods_folder_path.exists():
            self.base = mods_folder_path
        else:
            print("something wrong")
            self.base = Path.home() / "Documents" / "Elder Scrolls Online" / "live"
        self.update_paths()

    def update_paths(self):
        """Update all derived paths based on current base path."""
        self.saved_variables = self.base /"live" / "SavedVariables" / "APESO.lua"
        self.items_file = self.base /"live" / "AddOns" / "APESO" / "Items.lua"
        self.options_file = self.base /"live" / "AddOns" / "APESO" / "Options.lua"
        self.apeso_addon_dir = self.base /"live" / "AddOns" / "APESO"

    def set_base(self, new_path: Path):
        """Set a new base path and update all derived paths."""
        self.base = new_path
        self.update_paths()


# Create global config instance
eso_config = ESOConfig()

# For backwards compatibility, expose as module-level variables
ESO_BASE = eso_config.base
SAVED_VARIABLES = eso_config.saved_variables
ITEMS_FILE = eso_config.items_file
APESO_ADDON_DIR = eso_config.apeso_addon_dir


def check_eso_installation_get_errors():
    """Check for ESO installation and APESO addon files, return list of errors."""
    errors = []

    # Check for Elder Scrolls Online base directory
    if not eso_config.base.exists():
        errors.append(
            f"Elder Scrolls Online directory not found at: {eso_config.base}. \n"
            f"Expected structure: Documents/Elder Scrolls Online/live/. \n"
            f"Please verify your ESO installation is correct.\n"
            f"If your mods folder is not located at: {eso_config.base} check the readme on github for more details "
        )
        return errors

    # Check for SavedVariables folder
    if not (eso_config.base / "live").exists():
        errors.append(f"Elder Scrolls Online directory not found at: {eso_config.base}. "
            f"Expected structure: Documents/Elder Scrolls Online/live/. "
            f"Please verify your ESO installation is correct."
            f"If your mods folder is not located at: {eso_config.base} check the readme on github for more details "
        )
        return errors
    if not (eso_config.base / "live" / "SavedVariables").exists():
        errors.append(
            f"SavedVariables folder not found at: {eso_config.base / 'SavedVariables'}. "
            f"This folder should be created automatically by ESO. Have you launched ESO at least once?"
        )

    # Check for AddOns folder
    if not (eso_config.base / "live" / "AddOns").exists():
        errors.append(
            f"AddOns folder not found at: {eso_config.base / 'AddOns'}. "
            f"This folder should be created automatically by ESO. Have you launched ESO at least once?"
        )
        return errors

    # Check for APESO addon folder
    if not eso_config.apeso_addon_dir.exists():
        errors.append(
            f"APESO addon folder not found at: {eso_config.apeso_addon_dir}. "
            f"Please install the APESO addon to your ESO AddOns folder."
        )
        return errors

    # Check for Items.lua
    if not eso_config.items_file.exists():
        errors.append(
            f"Items.lua not found at: {eso_config.items_file}. "
            f"This file will be created automatically when you connect to the server."
        )

    # Check for APESO.lua in SavedVariables
    if not eso_config.saved_variables.exists():
        errors.append(
            f"APESO.lua not found in SavedVariables at: {eso_config.saved_variables}. "
            f"This file is created by the APESO addon when you log into a character. "
            f"Please launch ESO, load a character, and then reload the UI (/reloadui)."
        )

    return errors


class EsoState:
    def __init__(self):
        self.version = None
        self.char_id = None
        self.node_info = []
        self.completed_quests = set()
        self.completed_delves = set()

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

        #Delves
        idx = text.find("delveClears")
        if idx != -1:
            b1 = text.find("{", idx)
            b2 = self.find_matching_brace(text, b1)
            if b1 != -1 and b2 != -1:
                block = text[b1 + 1:b2]
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("--"):
                        continue
                    lb = line.find("[")
                    rb = line.find("]")
                    if lb != -1 and rb != -1 and "true" in line:
                        try:
                            delve_id = int(line[lb + 1:rb])
                            state.completed_delves.add(delve_id)
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
            eso_config.items_file.parent.mkdir(parents=True, exist_ok=True)
            eso_config.items_file.write_text("\n".join(lines), encoding="utf-8")
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
                if eso_config.saved_variables.exists():
                    modified = eso_config.saved_variables.stat().st_mtime
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
        state = self.reader.parse(eso_config.saved_variables, self.ctx.current_char_id)
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

    def _cmd_eso_goal(self) -> bool:
        """Display your victory condition for this ESO seed.
        """
        ctx: ESOContext = self.ctx

        if not hasattr(ctx, 'slot_data') or not ctx.slot_data:
            self.output("[ESO] Goal information not yet available. Connect to the server first.")
            return True

        slot_data = ctx.slot_data

        # Get goal type (0 = main quest, 1 = final zone quest)
        goal_type = slot_data.get("Goal", 0)
        alliance = slot_data.get("Alliance", 0)
        goal_zone = slot_data.get("GoalZone")

        # Alliance names
        alliance_names = {
            0: "Aldmeri Dominion",
            1: "Daggerfall Covenant",
            2: "Ebonheart Pact"
        }

        alliance_name = alliance_names.get(alliance, "Unknown")

        self.output("=" * 50)
        self.output(f"[ESO] Your Alliance: {alliance_name}")

        if goal_type == 0:
            # Main Quest goal
            self.output("[ESO] Victory Condition: Complete the Main Quest")
            self.output("[ESO] Final Quest: 'God of Schemes' in Coldharbour")
        else:
            # Final Zone Quest goal
            if goal_zone:
                self.output(f"[ESO] Victory Condition: Complete the final quest in {goal_zone}")

        self.output("=" * 50)
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
        self._last_item_count = 0
        self.slot_data = {}
        self.force_resync_on_connect = True

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
        if not eso_config.saved_variables.exists():
            logger.info("[ESO] SavedVariables file not found.")
            return
        reader = SavedVariablesReader()
        state = reader.parse(eso_config.saved_variables, self.current_char_id)
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

        for delve_id in state.completed_delves:
            locations.add(11_000 + delve_id)

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
            self.slot_data = args.get("slot_data", {})
            print(f"[ESO] Goal information loaded: {self.slot_data.get('Goal')} - {self.slot_data.get('GoalZone', 'Main Quest')}")

    def run_gui(self):
        from kvui import GameManager

        class EsoManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago ESO Client"

            def build(self):
                ret = super().build()
                return ret

        self.ui = EsoManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


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
                ctx.force_resync_on_connect = False

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

    ctx.run_gui()

    try:
        import asyncio as _a
        async def _after():
            for d in (0.2, 0.6):
                await _a.sleep(d)
                errors = check_eso_installation_get_errors()
                if errors and d == 0.6:
                    logger.info(errors)
                elif d == 0.6:
                    logger.info("Successfully connected to mod.")

        _a.get_event_loop().create_task(_after())
    except Exception:
        pass

    await ctx.exit_event.wait()
    await ctx.shutdown()



def main(args=None):
    colorama.init()
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    asyncio.run(async_main(parsed_args))


def launch(args=None):
    main(args)
