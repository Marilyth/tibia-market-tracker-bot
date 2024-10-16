import discord
import discord.ext.commands
import asyncio
from typing import List, Awaitable, Callable


class StatusReel:
    """A class that changes the bot's status every 30 seconds."""

    def __init__(self, bot: discord.ext.commands.AutoShardedBot):
        self.bot = bot
        self.reel_text_getters: List[Awaitable[Callable[[], str]]] = []

    def start_reel(self):
        """Starts the status reel."""
        self.reel_text_getters.append(self.get_guild_count_expression)
        self.reel_text_getters.append(self.get_ping_expression)

        self.bot.loop.create_task(self._reel())

    async def get_guild_count_expression(self):
        """Returns a string expression for the bot's status that shows the number of guilds it is in."""
        return f"Watching {len(self.bot.guilds)} guilds"

    async def get_ping_expression(self):
        """Returns a string expression for the bot's status that shows the bot's latency."""
        return f"{round(self.bot.latency * 1000)}ms ping"

    async def _reel(self):
        """Loops through the reel_text_getters and changes the bot's status every 30 seconds."""
        index = 0

        while True:
            if index >= len(self.reel_text_getters):
                index = 0

            try:
                if self.reel_text_getters:
                    text = await self.reel_text_getters[index]()
                    activity = discord.CustomActivity(name=text)
                    await self.bot.change_presence(activity=activity)
            except Exception as e:
                print(f"Error changing status: {e}")

            await asyncio.sleep(30)

            index += 1
