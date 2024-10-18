# pylint: disable=W0613
from discord import app_commands
from discord.interactions import Interaction
from typing import List
from utils.market_api import MarketApi


async def item_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice]:
    """Returns a list of item names that match the string.

    Args:
        interaction (Interaction): The interaction that triggered the autocomplete.
        current (str): The current string to match.
    """
    market_api: MarketApi = MarketApi()
    normalized_current: str = market_api.normalize_identifier(current)

    items = await market_api.meta_data.get_async()

    # Create a list of choices that match the current string.
    matches: List[app_commands.Choice] = []
    for item_id in items:
        item = items[item_id]
        item_name = item.wiki_name if item.wiki_name else item.name

        if normalized_current in market_api.normalize_identifier(item_name):
            matches.append(app_commands.Choice(name=item_name, value=item_name))

    # Sort the matches by length and return the first 25.
    matches = sorted(matches, key=lambda x: len(x.name))[:25]

    return matches
