from discord.ext import commands
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MarketBot


class General(commands.Cog):
    """A set of commands to interact with the Tibia Market API.
    """
    def __init__(self, bot: "MarketBot"):
        self.bot = bot

    @commands.hybrid_command(name='ping')
    async def ping(self, ctx: commands.Context):
        """Responds with 'Pong' after a 1 second delay.
        This is just a test command to check if the bot is working.
        """
        await ctx.defer()
        await asyncio.sleep(1)
        await ctx.send('Pong')
