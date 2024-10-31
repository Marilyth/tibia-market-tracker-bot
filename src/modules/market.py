from discord.ext import commands
from discord import app_commands
from typing import TYPE_CHECKING
from modules.autocomplete.item import item_autocomplete
from modules.autocomplete.world import world_autocomplete
from modules.embedder.market_values import market_value_to_embedding
from modules.embedder.history import history_to_embedding
from modules.embedder.market_board import market_board_to_embedding
from utils.market_api import MarketApi
from utils import get_default_world

if TYPE_CHECKING:
    from main import MarketBot


class Market(commands.Cog):
    """A set of commands to interact with the Tibia Market API.
    """
    def __init__(self, bot: "MarketBot"):
        self.bot = bot
        self.market_api = MarketApi()

    @commands.hybrid_group(invoke_without_command=False)
    async def item(self, ctx: commands.Context):
        """Group command for item-related commands."""

    @item.command("value")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.autocomplete(item=item_autocomplete, world=world_autocomplete)
    async def market_value(self, ctx: commands.Context, item: str, world: str = None):
        """Responds with the current market value of an item.

        Args:
            ctx (commands.Context): The context of the command.
            item (str): The name of the item to get the market value of.
            world (str, optional): The world to get the market value from.
        """
        await ctx.defer()

        # Get the default world if none is provided.
        if not world:
            world = get_default_world(ctx)

        # Fetch the market values from the API.
        market_values = await self.market_api.get_market_values(world, item)
        meta_data = await self.market_api.get_meta_data(item)

        # Create a pretty embed with the market values.
        embed = market_value_to_embedding(world, market_values, meta_data)

        # Send the embed.
        await ctx.send(embed=embed)

    @item.command("history")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.autocomplete(item=item_autocomplete, world=world_autocomplete)
    @app_commands.choices(
        timespan=[
            app_commands.Choice(name="Last Week", value=7),
            app_commands.Choice(name="Last Month", value=30),
            app_commands.Choice(name="Last 6 Months", value=180),
            app_commands.Choice(name="Last Year", value=365),
            app_commands.Choice(name="All Time", value=9999),
        ]
    )
    async def item_history(self, ctx: commands.Context, item: str, world: str = None, timespan: int = 30):
        """Responds with the market history of an item.

        Args:
            ctx (commands.Context): The context of the command.
            item (str): The name of the item to get the market history of.
            world (str, optional): The world to get the market history from.
            timespan (int, optional): The amount of days to get the history of. Defaults to 30.
        """
        await ctx.defer()

        # Get the default world if none is provided.
        if not world:
            world = get_default_world(ctx)

        # Fetch the market history from the API.
        market_history = await self.market_api.get_history(world, item, timespan)
        meta_data = await self.market_api.get_meta_data(item)

        # Create a pretty embed with the market history.
        embed, file = history_to_embedding(world, market_history, meta_data)

        # Send the embed.
        await ctx.send(embed=embed, file=file)

    @item.command("board")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.autocomplete(item=item_autocomplete, world=world_autocomplete)
    async def item_board(self, ctx: commands.Context, item: str, world: str = None):
        """Responds with the market board of an item.

        Args:
            ctx (commands.Context): The context of the command.
            item (str): The name of the item to get the market board of.
            world (str, optional): The world to get the market board from.
        """
        await ctx.defer()

        # Get the default world if none is provided.
        if not world:
            world = get_default_world(ctx)

        # Fetch the market board from the API.
        market_board = await self.market_api.get_market_board(world, item)
        meta_data = await self.market_api.get_meta_data(item)

        embed = market_board_to_embedding(world, market_board, meta_data)

        # Send the embed.
        await ctx.send(embed=embed)
