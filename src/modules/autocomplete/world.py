# pylint: disable=W0613
from discord import app_commands
from discord.interactions import Interaction
from typing import List
from utils.market_api import MarketApi


async def world_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice]:
    """Returns a list of world names that match the string.

    Args:
        interaction (Interaction): The interaction that triggered the autocomplete
        current (str): The current string to match.
    """
    market_api: MarketApi = MarketApi()
    normalized_current: str = market_api.normalize_identifier(current)

    worlds = await market_api.world_data.get_async()

    # Create a list of choices that match the current string.
    matches: List[app_commands.Choice] = []
    for world_name in worlds:
        if normalized_current in market_api.normalize_identifier(world_name):
            matches.append(app_commands.Choice(name=world_name, value=world_name))

    # Sort the matches by length and return the first 25.
    matches = sorted(matches, key=lambda x: len(x.name))[:25]

    return matches
