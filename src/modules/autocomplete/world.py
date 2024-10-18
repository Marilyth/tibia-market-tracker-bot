from discord import app_commands
from discord.interactions import Interaction
from typing import List, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from main import MarketBot


async def world_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice]:
    """Returns a list of item names that match the string.

    Args:
        interaction (Interaction): The interaction of the command.
        current (str): The current string to match.
    """
    bot: "MarketBot" = cast("MarketBot", interaction.client)
    normalized_current: str = bot.market_api.normalize_identifier(current)

    worlds = await bot.market_api.world_data.get_async()

    # Create a list of choices that match the current string.
    matches: List[app_commands.Choice] = []
    for world_name in worlds:
        if normalized_current in bot.market_api.normalize_identifier(world_name):
            matches.append(app_commands.Choice(name=world_name, value=world_name))

    # Sort the matches by length and return the first 25.
    matches = sorted(matches, key=lambda x: len(x.name))[:25]

    return matches
