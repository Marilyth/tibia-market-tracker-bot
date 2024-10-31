from discord.ext import commands
from discord import app_commands
import asyncio
from typing import TYPE_CHECKING
from modules.autocomplete.world import world_autocomplete
from utils.data.user import DiscordUser
from utils.data.discord_server import DiscordServer
from utils.market_api import MarketApi

if TYPE_CHECKING:
    from main import MarketBot


class General(commands.Cog):
    """A set of commands to interact with the Tibia Market API.
    """
    def __init__(self, bot: "MarketBot"):
        self.bot = bot

    @commands.hybrid_command(name='ping')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        """Responds with 'Pong' after a 1 second delay.
        This is just a test command to check if the bot is working.
        """
        await ctx.defer()
        await asyncio.sleep(1)
        await ctx.send('Pong')

    @commands.hybrid_command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @app_commands.autocomplete(default_world=world_autocomplete)
    async def default_world(self, ctx: commands.Context, default_world: str):
        """Set the default Tibia world for the user when none is provided in a command.
        
        Args:
            ctx (commands.Context): The context of the command.
            default_world (str): The world to set as the default.
        """
        await ctx.defer()

        user = DiscordUser.from_database(ctx.author.id)[0]
        default_world = MarketApi().normalize_world(default_world)
        await MarketApi().throw_if_world_not_found(default_world)

        user.default_world = default_world
        user.save()

        await ctx.send(f"Set your default world to {default_world}.")

    @commands.hybrid_command()
    @commands.cooldown(1, 1, commands.BucketType.guild)
    @app_commands.autocomplete(default_world=world_autocomplete)
    @commands.has_permissions(manage_guild=True)
    async def server_default_world(self, ctx: commands.Context, default_world: str):
        """Set the default Tibia world for the whole discord server when none is provided in a command.
        
        Args:
            ctx (commands.Context): The context of the command.
            default_world (str): The world to set as the default.
        """
        await ctx.defer()

        server =  DiscordServer.from_database(ctx.guild.id)[0]
        default_world = MarketApi().normalize_world(default_world)
        await MarketApi().throw_if_world_not_found(default_world)

        server.default_world = default_world
        server.save()

        await ctx.send(f"Set {ctx.guild.name}'s default world to {server.default_world}.")
