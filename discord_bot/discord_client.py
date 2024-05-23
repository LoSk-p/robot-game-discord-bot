import typing as tp
import discord

from .player_manager import PlayersManager
from .discord_helpers.message_address_handler import MessageWithAddressHandler
from .discord_helpers.message_manager import MessageManager
from .discord_helpers.discord_client import DiscordClient
from .exceptions.message_exceptions import AddressIsInWrongFormat, AddressIsNotED25519, NoAddressInMessage
from .models.player import Player

from .config.config import DISCORD_TOKEN


class Discord:
    def __init__(self, players_manager: PlayersManager) -> None:
        self.discord_client = DiscordClient(self._on_message_callback)
        self.got_address_callback: tp.Awaitable = None
        self.players_manager = players_manager

    async def start(self) -> None:
        await self.discord_client.start(DISCORD_TOKEN)

    def wait_for_addresses(self, callback: tp.Awaitable) -> tp.Callable:
        self.got_address_callback = callback
        return self._stop_wait_for_addresses
    
    async def send_start_message(self) -> None:
        self.discord_client.send_message(MessageManager.start_round_message())

    async def send_message_with_dapp(self) -> None:
         self.discord_client.send_message(MessageManager.message_with_dapp())

    async def send_message_with_winner(self, winner: Player) -> None:
         self.discord_client.send_message(MessageManager.message_with_winner(winner))

    async def send_message_second_address_from_user(self, user: tp.Union[discord.User, discord.Member]) -> None:
         self.discord_client.send_message(MessageManager.second_address_from_one_user(user))

    def _stop_wait_for_addresses(self) -> None:
        self.got_address_callback = None

    async def _on_message_callback(self, message: discord.Message):
        if self.got_address_callback is not None:
            address = await self._get_address_from_message(message)
            if address is not None:
                await self.got_address_callback(address, message.author)

    async def _get_address_from_message(self, message: discord.Message) -> tp.Optional[str]:
        try:
            address = MessageWithAddressHandler.get_address(message)
        except NoAddressInMessage:
            return None
        except AddressIsInWrongFormat:
            await self.discord_client.send_message(MessageManager.wrong_format_message(address, message))
        except AddressIsNotED25519:
            await self.discord_client.send_message(MessageManager.wrong_type_message(address, message))
        return address
    
    



