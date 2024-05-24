import typing as tp

import discord

from ..config.config import CHANNEL, GUILD
from ..logger import get_logger

logger = get_logger(__name__)


class DiscordClient(discord.Client):
    def __init__(
        self, on_message_callback: tp.Awaitable, on_ready_callback: tp.Awaitable
    ) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.on_message_callback = on_message_callback
        self.on_ready_callback = on_ready_callback
        self.channel: discord.GroupChannel = None

    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == GUILD:
                break
        logger.info(f"{self.user} is connected to the {guild.name}\n")
        self.channel = discord.utils.get(guild.channels, name=CHANNEL)
        await self.on_ready_callback()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if str(message.channel) == CHANNEL:
            logger.info(f"Message from {message.author}: {message.content}")
            await self.on_message_callback(message)

    async def send_message(self, message: str) -> None:
        await self.channel.send(message)
