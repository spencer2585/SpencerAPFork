import asyncio
import colorama
import logging
from CommonClient import CommonContext, ClientCommandProcessor, ClientStatus, get_base_parser, gui_enabled, server_loop
from Utils import async_start
from pathlib import Path
import time
from . import ESOWorld, constants
from .data.ZoneQuestData import ZONE_QUEST_DATA

logger = logging.getLogger("Client")

VICTORY_ITEM_ID = 149995  # eso_base_id - 5

mods_folder_str = str(ESOWorld.settings.mods_folder)
mods_folder_path = Path(mods_folder_str)


class ESOConfig:
    """Holds ESO file paths that can be updated at runtime."""

    def __init__(self):
        self.checked_locations = set()
        if mods_folder_path.exists():
            self.base = mods_folder_path
        else:
            print("something wrong")
            self.base = Path.home() / "Documents" / "Elder Scrolls Online"
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
        self.version = (0, 3, 0)
        self.char_id = None
        self.node_info = []
        self.completed_quests = set()
        self.completed_delves = set()


class SavedVariablesReader:

    def parse(self, path: Path, seed: str, locked_char_id: str = None):
        """Parse SavedVariables file for a specific seed.

        Args:
            path: Path to the SavedVariables file
            seed: The seed string to look up in savedVariables
            locked_char_id: If provided, use this character ID for quest lookups
        """
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print("Failed to read SavedVariables:", e)
            return None

        state = EsoState()

        char_id_marker = '["char_id"]'
        char_id_idx = text.find(char_id_marker)
        if char_id_idx != -1:
            # Find the value after the = sign
            eq_idx = text.find("=", char_id_idx)
            if eq_idx != -1:
                line_end = text.find("\n", eq_idx)
                value = text[eq_idx + 1:line_end].strip().strip(",").strip('"')
                if locked_char_id is None:
                    state.char_id = value
                else:
                    state.char_id = locked_char_id


        # Find the seed-specific block
        seed_marker = f'["{seed}"]'
        seed_idx = text.find(seed_marker)

        if seed_idx == -1:
            print(f"[ESO] Seed '{seed}' not found in SavedVariables")
            return None

        # Find the braces for this seed's data block
        seed_block_start = text.find("{", seed_idx)
        seed_block_end = self.find_matching_brace(text, seed_block_start)

        if seed_block_start == -1 or seed_block_end == -1:
            print(f"[ESO] Could not parse seed block for '{seed}'")
            return None

        seed_block = text[seed_block_start:seed_block_end + 1]

        # NODE INFO
        idx = seed_block.find("NodeInfo")
        if idx != -1:
            b1 = seed_block.find("{", idx)
            b2 = self.find_matching_brace(seed_block, b1)
            if b1 != -1 and b2 != -1:
                block = seed_block[b1 + 1:b2]
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("--"):
                        continue
                    lb = line.find("[")
                    rb = line.find("]")
                    if lb != -1 and rb != -1 and "true" in line:
                        try:
                            node_id = int(line[lb + 1:rb])
                            # Convert to location ID: base 150000 + node_id
                            location_id = 150_000 + node_id
                            state.node_info.append(location_id)
                        except ValueError:
                            pass

        # COMPLETED QUESTS
        idx = seed_block.find("CompletedQuests")
        if idx != -1:
            b1 = seed_block.find("{", idx)
            b2 = self.find_matching_brace(seed_block, b1)
            if b1 != -1 and b2 != -1:
                block = seed_block[b1 + 1:b2]
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("--"):
                        continue
                    lb = line.find("[")
                    rb = line.find("]")
                    if lb != -1 and rb != -1 and "true" in line:
                        try:
                            quest_id = int(line[lb + 1:rb])
                            # Convert to location ID: base 151000 + quest_id
                            location_id = constants.QUEST_OFFSET + quest_id
                            state.completed_quests.add(location_id)
                        except ValueError:
                            pass

        # DELVE CLEARS
        idx = seed_block.find("delveClears")
        if idx != -1:
            b1 = seed_block.find("{", idx)
            b2 = self.find_matching_brace(seed_block, b1)
            if b1 != -1 and b2 != -1:
                block = seed_block[b1 + 1:b2]
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("--"):
                        continue
                    lb = line.find("[")
                    rb = line.find("]")
                    if lb != -1 and rb != -1 and "true" in line:
                        try:
                            delve_id = int(line[lb + 1:rb])
                            # Convert to location ID: base 11000 + delve_id
                            location_id = constants.DELVE_LOCATION_OFFSET + delve_id
                            state.completed_delves.add(location_id)
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
        self.items.append(item_id)
        self.write_file()

    def set_all(self, items):
        self.items = list(items)
        self.write_file()

    def write_file(self):
        lines = ["APESO_ReceivedItems = {"]

        for item_id in self.items:
            lines.append(f"    {{ item_id = {item_id}}},")

        lines.append("}")

        try:
            eso_config.items_file.parent.mkdir(parents=True, exist_ok=True)
            eso_config.items_file.write_text("\n".join(lines), encoding="utf-8")
            print(f"[ESO] Wrote items.lua with {len(self.items)} items.")
        except Exception as e:
            print("[ESO] Failed to write items.lua", e)


class OptionsWriter:
    def __init__(self):
        self.current_seed = None

    def write_file(self, slot_data):
        """Write options from slot_data to Options.lua"""
        self.current_seed = str(slot_data.get("seed", ""))

        lines = ["APESO_options = {"]

        lines.append(f'    [\"seed\"] = "{self.current_seed}",')

        # Extract options from slot_data
        lines.append(f"    [\"alliance\"] = {slot_data.get('Alliance', 0)},")
        lines.append(f"    [\"goal\"] = {slot_data.get('Goal', 0)},")
        lines.append(f'    [\"goal_zone\"] = "{slot_data.get("GoalZone", "")}",')
        lines.append(f"    [\"zone_quests_enabled\"] = {1 if slot_data.get('ZoneQuestsEnabled', True) else 0},")
        lines.append(f"    [\"wayshrine_checks_enabled\"] = {1 if slot_data.get('WayshrineChecksEnabled', True) else 0},")
        lines.append(
            f"    [\"delves_per_region\"] = {slot_data.get('DelvesNum', 0)},")  # Note: uses 'DelvesNum' from your fill_slot_data
        lines.append(f"    [\"goldCap\"] = {slot_data.get('GoldCap', 0)},")

        lines.append("}")

        try:
            eso_config.options_file.parent.mkdir(parents=True, exist_ok=True)
            eso_config.options_file.write_text("\n".join(lines), encoding="utf-8")
            print(f"[ESO] Wrote Options.lua with seed: {self.current_seed}")
        except Exception as e:
            print("[ESO] Failed to write Options.lua", e)

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
                    print(f"[ESO] mtime: {modified}, last: {self.last_modified}")
                    if modified != self.last_modified:
                        print("[ESO] Change detected, calling on_change")
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

        seed = self.ctx.options_writer.current_seed
        if not seed:
            print("[ESO] No seed available yet, skipping parse")
            return

        # Pass the locked character ID so quests are read for the correct character
        state = self.reader.parse(eso_config.saved_variables, str(self.ctx.slot_data.get("seed", "")))
        if state:
            await self.ctx.handle_eso_state(state)
        print("end onchange")





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
        self.options_writer = OptionsWriter()
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
            self.items_writer.add_item(item.item)

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
        print("ESO State fired")
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
        print("past char check")
        # convert checks to AP IDs
        locations = set()

        locations.update(state.node_info)
        locations.update(state.completed_delves)
        locations.update(state.completed_quests)

        new = locations - self.checked_locations
        self.checked_locations.update(new)
        print("past new")

        if new:
            await self.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(new)
            }])

        print("past send")

        if self.slot_data.get("Goal") == 0:  # main quest
            final_id = constants.QUEST_OFFSET+4847
            if final_id in state.completed_quests:
                if not self.finished_game:
                    await self.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    self.finished_game = True

        elif self.slot_data.get("Goal") == 1:  # zone quest
            final_id = None
            for questName, questData in ZONE_QUEST_DATA.items():
                if questData.zone == self.slot_data.get("GoalZone") and questData.is_final:
                    final_id = constants.QUEST_OFFSET+questData.quest_id
                    break
            if final_id in state.completed_quests:
                if not self.finished_game:
                    await self.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    self.finished_game = True

        elif self.slot_data.get("Goal") == 2:  # all_delves goal
            selected_delves = set(self.slot_data.get("SelectedDelves", []))
            if selected_delves and selected_delves.issubset(state.completed_delves):
                if not self.finished_game:
                    await self.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    self.finished_game = True
        print("end eso State")



    def on_package(self, cmd: str, args: dict):
        """Handle incoming packets from the server."""
        if cmd == "Connected":
            self.force_resync_on_connect = True
            print("[ESO] Connected packet received!")
            print("[ESO] Connected → clearing Items.lua")
            self.items_writer.reset()
            self.slot_data = args.get("slot_data", {})

            self.options_writer.write_file(self.slot_data)
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
                    item.item
                    for item in ctx.items_received
                )

                ctx._last_item_count = len(ctx.items_received)
                ctx.force_resync_on_connect = False

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
