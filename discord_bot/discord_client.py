import typing as tp

import discord

from .config.config import DISCORD_TOKEN
from .discord_helpers.discord_client import DiscordClient
from .discord_helpers.message_address_handler import MessageWithAddressHandler
from .discord_helpers.message_manager import MessageManager
from .exceptions.message_exceptions import (
    AddressIsInWrongFormat,
    AddressIsNotED25519,
    NoAddressInMessage,
)
from .logger import get_logger

logger = get_logger(__name__)


class Discord:
    def __init__(self, wait_for_ready_callback: tp.Awaitable) -> None:
        self.discord_client = DiscordClient(
            self._on_message_callback, wait_for_ready_callback
        )
        self.got_address_callback: tp.Awaitable = None

    async def start(self) -> None:
        logger.info("Starting discord client")
        await self.discord_client.start(DISCORD_TOKEN)

    def wait_for_addresses(self, callback: tp.Awaitable) -> tp.Callable:
        logger.info("Start wait for addresses")
        self.got_address_callback = callback
        return self._stop_wait_for_addresses

    async def send_start_message(self) -> None:
        await self.discord_client.send_message(MessageManager.start_round_message())

    async def send_message_with_dapp(self) -> None:
        await self.discord_client.send_message(MessageManager.message_with_dapp())

    async def send_message_with_winner(self, winner_address: str) -> None:
        await self.discord_client.send_message(
            MessageManager.message_with_winner(winner_address)
        )

    async def send_message_timer_finished_no_address(self) -> None:
        await self.discord_client.send_message(
            MessageManager.timer_finished_no_address_message()
        )

    async def send_message_timer_reminder(self, minutes_left: int) -> None:
        await self.discord_client.send_message(
            MessageManager.timer_reminder_message(minutes_left)
        )

    async def send_message_address_added(self, address: str) -> None:
        await self.discord_client.send_message(
            MessageManager.address_added_message(address)
        )

    async def send_message_timer_finished_start(self, addresses: tp.List[str]) -> None:
        await self.discord_client.send_message(
            MessageManager.timer_finished_start_message(addresses)
        )

    async def send_message_second_address_from_user(
        self, user: tp.Union[discord.User, discord.Member]
    ) -> None:
        await self.discord_client.send_message(
            MessageManager.second_address_from_one_user(user)
        )

    def _stop_wait_for_addresses(self) -> None:
        logger.info("Stop wait for addresses")
        self.got_address_callback = None

    async def _on_message_callback(self, message: discord.Message):
        logger.info(f"Got message: {message}")
        if self.got_address_callback is not None:
            address = await self._get_address_from_message(message)
            logger.info(f"Got address in message: {address}")
            if address is not None:
                await self.got_address_callback(address, message.author)

    async def _get_address_from_message(
        self, message: discord.Message
    ) -> tp.Optional[str]:
        try:
            address = MessageWithAddressHandler(message).get_address()
        except NoAddressInMessage:
            logger.info("No address in message")
            return None
        except AddressIsInWrongFormat:
            logger.info(f"Given address is in wrong format: {message.content}")
            await self.discord_client.send_message(
                MessageManager.wrong_format_message(address, message)
            )
        except AddressIsNotED25519:
            logger.info(f"Given address is not ed type: {message.content}")
            await self.discord_client.send_message(
                MessageManager.wrong_type_message(address, message)
            )
        return address
