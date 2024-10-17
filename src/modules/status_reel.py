import discord
import discord.ext.commands
import asyncio
from typing import List, Awaitable, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from main import MarketBot


class StatusReel:
    """A class that changes the bot's status every 30 seconds."""

    def __init__(self, bot: "MarketBot"):
        self.bot = bot
        self.reel_text_getters: List[Awaitable[Callable[[], str]]] = []

    def start_reel(self):
        """Starts the status reel."""
        self.reel_text_getters.append(self.get_item_count_expression)
        self.reel_text_getters.append(self.get_world_count_expression)
        self.reel_text_getters.append(self.get_guild_count_expression)
        self.reel_text_getters.append(self.get_ping_expression)

        self.bot.loop.create_task(self._reel())

    async def get_guild_count_expression(self):
        """Returns a string expression for the bot's status that shows the number of guilds it is in."""
        return f"Serving {len(self.bot.guilds)} discord servers"

    async def get_ping_expression(self):
        """Returns a string expression for the bot's status that shows the bot's latency."""
        return f"{round(self.bot.latency * 1000)}ms ping"
    
    async def get_item_count_expression(self):
        """Returns a string expression for the bot's status that shows the number of items in the market database."""
        return f"Tracking {len(await self.bot.market_api.meta_data.get_async())} items"
    
    async def get_world_count_expression(self):
        """Returns a string expression for the bot's status that shows the number of worlds in the market database."""
        return f"Tracking {len(await self.bot.market_api.world_data.get_async())} worlds"

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
