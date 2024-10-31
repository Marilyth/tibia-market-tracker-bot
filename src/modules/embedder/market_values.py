from datetime import datetime
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from modules.embedder.default import get_default_embed


def market_value_to_embedding(item_name: str, world: str, market_values: MarketValues):
    """Converts a MarketValues object to a discord.Embed object.
    
    Args:
        item_name (str): The name of the item.
        world (str): The name of the world.
        market_values (MarketValues): The market values of the item.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = get_default_embed()
    embed.title = f"{item_name} on {world}"
    embed.timestamp = datetime.fromtimestamp(market_values.time)
    embed.url = ItemMetaData.name_to_wiki_link(item_name)

    embed.set_thumbnail(url=ItemMetaData.id_to_image_link(market_values.id))

    sell_values = {
        "Sell price": market_values.day_average_sell if market_values.day_average_sell > 0 else market_values.sell_offer,
        "Sellers": market_values.sell_offers,
        "": None,
        "Highest price": market_values.month_highest_sell,
        "Average price": market_values.month_average_sell,
        "Lowest price": market_values.month_lowest_sell
    }

    buy_values = {
        "Buy offer": market_values.buy_offer if market_values.buy_offer > 0 else market_values.day_average_buy,
        "Buyers": market_values.buy_offers,
        "": None,
        "Highest price": market_values.month_highest_buy,
        "Average price": market_values.month_average_buy,
        "Lowest price": market_values.month_lowest_buy
    }

    embed.add_field(name="Sell data", value="\n".join([f"**{key}:** {value:,}" if value else "\n" for key, value in sell_values.items()]), inline=True)
    embed.add_field(name="Buy data", value="\n".join([f"**{key}:** {value:,}" if value else "\n" for key, value in buy_values.items()]), inline=True)

    return embed
