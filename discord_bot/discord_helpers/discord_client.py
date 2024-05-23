import discord
import typing as tp
from ..config.config import GUILD, CHANNEL

class DiscordClient(discord.Client):
    def __init__(self, on_message_callback: tp.Callable) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.on_message_callback = on_message_callback
        self.channel: discord.GroupChannel = None

    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{self.user} is connected to the {guild.name}\n'
        )
        self.channel = discord.utils.get(guild.channels, name=CHANNEL)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if str(message.channel) == CHANNEL:
            print(f'Message from {message.author}: {message.content}')
            await self.on_message_callback(message)

    async def send_message(self, message: str) -> None:
        await self.channel.send(message)