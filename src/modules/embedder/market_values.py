import discord
from typing import List
from datetime import datetime
from utils.data.item_meta_data import ItemMetaData, NPCSaleData
from utils.data.market_values import MarketValues
from utils.market_api import MarketApi
from utils import GOLD_COIN_EMOJI
from modules.embedder.default import get_default_embed


def sale_data_to_expression(sale_data: List[NPCSaleData]) -> str:
    """Converts a list of NPCSaleData objects to a string expression that can be used in an embed field.
    
    Args:
        sale_data (List[NPCSaleData]): The list of NPCSaleData objects.
        
    Returns:
        str: The string expression.
    """
    api = MarketApi()

    sale_data_expressions = []

    for sale_data_item in sale_data:
        currency_id = sale_data_item.currency_object_type_id
        npc_name = f"[{sale_data_item.name}]({ItemMetaData.name_to_wiki_link(sale_data_item.name)})"

        # Check if the currency is gold, if so, use the gold coin emoji.
        if currency_id == 0:
            currency = GOLD_COIN_EMOJI
        # Check if the currency is a known item, if so, use the item name and link.
        elif currency_id in api.meta_data.value:
            currency_metadata = api.meta_data.value[currency_id]
            currency = currency_metadata.wiki_name if currency_metadata.wiki_name else currency_metadata.name
            currency = f"[{currency}]({currency_metadata.get_wiki_link()})"
        # If the currency is unknown, use the object type id.
        else:
            currency = f"_UnknownCurrency:{sale_data_item.currency_object_type_id}_"

        sale_data_expressions.append(f"{npc_name} in {sale_data_item.location} for {sale_data_item.price:,} {currency}")

    return "\n".join(sale_data_expressions)[:1024]

def market_value_to_embedding(world: str, market_values: MarketValues, meta_data: ItemMetaData) -> discord.Embed:
    """Converts a MarketValues object to a discord.Embed object.
    
    Args:
        world (str): The name of the world.
        market_values (MarketValues): The market values of the item.
        meta_data (ItemMetaData): The meta data of the item.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = get_default_embed()
    embed.description = f"[{meta_data.wiki_name if meta_data.wiki_name else meta_data.name}]({meta_data.get_wiki_link()}) on {world}"
    embed.timestamp = datetime.fromtimestamp(market_values.time)

    embed.set_thumbnail(url=ItemMetaData.id_to_image_link(market_values.id))

    # Add the market values to the embed.
    sell_values = {
        "Price": f"{market_values.day_average_sell if market_values.day_average_sell > 0 else market_values.sell_offer:,}{GOLD_COIN_EMOJI}",
        "Sellers": market_values.sell_offers,
        "Sold": market_values.month_sold,
        "": None,
        "Highest": f"{market_values.month_highest_sell:,}{GOLD_COIN_EMOJI}",
        "Average": f"{market_values.month_average_sell:,}{GOLD_COIN_EMOJI}",
        "Lowest": f"{market_values.month_lowest_sell:,}{GOLD_COIN_EMOJI}"
    }

    buy_values = {
        "Price": f"{market_values.buy_offer if market_values.buy_offer > 0 else market_values.day_average_buy:,}{GOLD_COIN_EMOJI}",
        "Buyers": market_values.buy_offers,
        "Bought": market_values.month_bought,
        "": None,
        "Highest": f"{market_values.month_highest_buy:,}{GOLD_COIN_EMOJI}",
        "Average": f"{market_values.month_average_buy:,}{GOLD_COIN_EMOJI}",
        "Lowest": f"{market_values.month_lowest_buy:,}{GOLD_COIN_EMOJI}"
    }

    embed.add_field(name="Sell data", value="\n".join([f"`{key}`: {value}" if key else "\n" for key, value in sell_values.items()]), inline=True)
    embed.add_field(name="Buy data", value="\n".join([f"`{key}`: {value}" if key else "\n" for key, value in buy_values.items()]), inline=True)

    # Add the NPC sale and buy data to the embed if available.
    if meta_data.npc_sell:
        embed.add_field(name="Buy from", value=sale_data_to_expression(meta_data.npc_sell), inline=False)

    if meta_data.npc_buy:
        embed.add_field(name="Sell to", value=sale_data_to_expression(meta_data.npc_buy), inline=False)

    return embed
