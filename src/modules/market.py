from discord.ext import commands
from discord import app_commands
from typing import TYPE_CHECKING
from modules.autocomplete.item import item_autocomplete
from modules.autocomplete.world import world_autocomplete
from modules.embedder.market_values import market_value_to_embedding
from utils.market_api import MarketApi
from utils.data.user import DiscordUser

if TYPE_CHECKING:
    from main import MarketBot


class Market(commands.Cog):
    """A set of commands to interact with the Tibia Market API.
    """
    def __init__(self, bot: "MarketBot"):
        self.bot = bot
        self.market_api = MarketApi()

    @commands.hybrid_command(name='market_value')
    @app_commands.autocomplete(item=item_autocomplete, world=world_autocomplete)
    async def market_value(self, ctx: commands.Context, item: str, world: str = None):
        """Responds with the current market value of an item.

        Args:
            ctx (commands.Context): The context of the command.
            item (str): The name of the item to get the market value of.
            world (str, optional): The world to get the market value from. Defaults to Antica, or the user's default world.
        """
        await ctx.defer()

        # Get the default world if none is provided.
        if not world:
            world = DiscordUser.from_database(ctx.author.id).default_world

        # Fetch the market values from the API.
        market_values = await self.market_api.get_market_values(world, item)

        # Create a pretty embed with the market values.
        embed = market_value_to_embedding(item, world, market_values)

        # Send the embed.
        await ctx.send(embed=embed)
