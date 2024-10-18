from discord.ext import commands
from discord import app_commands
import asyncio
from typing import TYPE_CHECKING
from modules.autocomplete.world import world_autocomplete
from utils.data.user import DiscordUser

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

    @commands.hybrid_command()
    @app_commands.autocomplete(default_world=world_autocomplete)
    async def set_default_world(self, ctx: commands.Context, default_world: str):
        """Set the default world for the user when none is provided in a command.
        
        Args:
            ctx (commands.Context): The context of the command.
            default_world (str): The world to set as the default.
        """
        await ctx.defer()

        user =  DiscordUser.from_database(ctx.author.id)
        user.default_world = default_world
        user.save()

        await ctx.send(f"Set default world to {default_world}.")
