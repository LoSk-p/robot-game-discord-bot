from discord import User, Member
import typing as tp
import asyncio

from .discord_client import Discord
from .player_manager import PlayersManager
from .robonomics import Robonomics
from .seed_manager import SeedManager
from .game_timer import GameTimer
from .logger import get_logger

#TODO StateManager:
#         save rounds history
#         save current stage with data: current_seed, current_players, current time
#         read current stage with data
# Player should't save all discord acc, only name

logger = get_logger(__name__)

class Coordinator:
    def __init__(self) -> None:
        self.robonomics = Robonomics()
        self.seed_manager = SeedManager()
        self.players_manager = PlayersManager()
        self.discord = Discord(self._start_round)
        self.game_timer = GameTimer()
        self.stop_wait_for_addresses: tp.Optional[tp.Callable] = None
        self.event_loop = None

    def start_game_bot(self):
        self.event_loop = asyncio.new_event_loop()
        self.event_loop.create_task(self._start_discord_client())
        self.event_loop.run_forever()

    async def _start_discord_client(self):
        await self.discord.start()

    async def _start_round(self):
        logger.info("Start new round")
        await self.discord.send_start_message()
        self.stop_wait_for_addresses = self.discord.wait_for_addresses(self._got_address_in_discord)
        self.game_timer.start(self._first_stage_time_is_finished)

    async def _got_address_in_discord(self, address: str, message_author: tp.Union[User, Member]):
        logger.info(f"Got address in discord {address} from {message_author}")
        if self.players_manager.discord_acc_in_players(message_author.name):
            await self.discord.send_message_second_address_from_user(message_author)
            return
        self.players_manager.add_player(message_author.name, address)
        if self.players_manager.full:
            self.stop_wait_for_addresses()
            if not self.game_timer.is_running:
                await self._second_stage()

    async def _first_stage_time_is_finished(self):
        if self.players_manager.empty:
            logger.info("Wait for the first player")
        else:
            await self._second_stage()

    async def _second_stage(self):
        logger.info("Start second stage: set rws devices, get seed, sed launch, wait for datalog")
        new_devices = self.players_manager.get_players_addresses()
        await self.robonomics.set_new_rws_devices_list(new_devices)
        new_seed = self.seed_manager.get_new()
        await self.robonomics.send_start_command_to_robot(new_seed)
        self.robonomics.wait_for_datalog(self._second_stage_finished)
    
    def _second_stage_finished(self):
        self.event_loop.create_task(self._third_stage())

    async def _third_stage(self):
        logger.info("Start third stage: wait for transfer")
        await self.discord.send_message_with_dapp()
        self.robonomics.wait_for_transfer(self.seed_manager.current_seed, self._got_winner)
        pass

    def _got_winner(self, winner_address: str):
        winner_player = self.players_manager.get_player_for_address(winner_address)
        if winner_player is None:
            winner_user_name = None
        else:
            winner_user_name = winner_player.discord_account_name
        self.event_loop.create_task(self._last_stage(winner_address, winner_user_name))

    async def _last_stage(self, winner_address: str, winner_user_name: tp.Optional[str]):
        await self.discord.send_message_with_winner(winner_address, winner_user_name)
        await self.robonomics.clear_rws_devices()
        self.players_manager.clear_players()
        await self._start_round()

