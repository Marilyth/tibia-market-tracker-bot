import discord
from datetime import datetime
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues


def market_value_to_embedding(item_name: str, world: str, market_values: MarketValues):
    """Converts a MarketValues object to a discord.Embed object.
    
    Args:
        item_name (str): The name of the item.
        world (str): The name of the world.
        market_values (MarketValues): The market values of the item.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = discord.embeds.Embed(
        title=f"{item_name} on {world}",
        timestamp=datetime.fromtimestamp(market_values.time),
        color=discord.Color.blue(),
        url=ItemMetaData.id_to_wiki_link(market_values.id)
    )

    embed.set_thumbnail(url=ItemMetaData.id_to_image_link(market_values.id))
    embed.add_field(name="Sell offer", value=market_values.sell_offer, inline=True)
    embed.add_field(name="Buy offer", value=market_values.buy_offer, inline=True)

    # Force a new line.
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="Sellers", value=market_values.sell_offers, inline=True)
    embed.add_field(name="Buyers", value=market_values.buy_offers, inline=True)

    return embed
