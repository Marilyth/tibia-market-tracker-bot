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
    embed.description = f"[{item_name}]({ItemMetaData.name_to_wiki_link(item_name)}) on {world}"
    embed.timestamp = datetime.fromtimestamp(market_values.time)

    embed.set_thumbnail(url=ItemMetaData.id_to_image_link(market_values.id))

    sell_values = {
        "Price": f"{market_values.day_average_sell if market_values.day_average_sell > 0 else market_values.sell_offer:,}<:Gold_Coin:1301485099161751562>",
        "Sellers": market_values.sell_offers,
        "Sold": market_values.month_sold,
        "": None,
        "Highest": f"{market_values.month_highest_sell:,}<:Gold_Coin:1301485099161751562>",
        "Average": f"{market_values.month_average_sell:,}<:Gold_Coin:1301485099161751562>",
        "Lowest": f"{market_values.month_lowest_sell:,}<:Gold_Coin:1301485099161751562>"
    }

    buy_values = {
        "Price": f"{market_values.buy_offer if market_values.buy_offer > 0 else market_values.day_average_buy:,}<:Gold_Coin:1301485099161751562>",
        "Buyers": market_values.buy_offers,
        "Bought": market_values.month_bought,
        "": None,
        "Highest": f"{market_values.month_highest_buy:,}<:Gold_Coin:1301485099161751562>",
        "Average": f"{market_values.month_average_buy:,}<:Gold_Coin:1301485099161751562>",
        "Lowest": f"{market_values.month_lowest_buy:,}<:Gold_Coin:1301485099161751562>"
    }

    embed.add_field(name="Sell data", value="\n".join([f"`{key}`: {value}" if key else "\n" for key, value in sell_values.items()]), inline=True)
    embed.add_field(name="Buy data", value="\n".join([f"`{key}`: {value}" if key else "\n" for key, value in buy_values.items()]), inline=True)

    return embed
