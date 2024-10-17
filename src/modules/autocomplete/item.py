import discord.ext.commands as commands
import discord.app_commands as app_commands
from discord.interactions import Interaction
from typing import List, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from main import MarketBot


async def item_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice]:
    """Returns a list of item names that match the string.

    Args:
        interaction (Interaction): The interaction of the command.
        current (str): The current string to match.
    """
    bot: "MarketBot" = cast("MarketBot", interaction.client)
    normalized_current: str = bot.market_api.normalize_identifier(current)

    items = await bot.market_api.meta_data.get_async()
    
    # Create a list of choices that match the current string.
    matches: List[app_commands.Choice] = []
    for item_id in items:
        item = items[item_id]
        item_name = item.wiki_name if item.wiki_name else item.name

        if normalized_current in bot.market_api.normalize_identifier(item_name):
            matches.append(app_commands.Choice(name=item.name, value=item.name))

    # Sort the matches by length and return the first 25.
    matches = sorted(matches, key=lambda x: len(x.name))[:25]

    return matches
