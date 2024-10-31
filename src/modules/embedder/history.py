import discord
from typing import List, Tuple
from datetime import datetime
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from utils import GOLD_COIN_EMOJI
from modules.embedder.default import get_default_embed
from io import BytesIO


def history_to_embedding(world: str, market_values: List[MarketValues], meta_data: ItemMetaData) -> Tuple[discord.Embed, discord.File]:
    """Converts a history to a discord.Embed object.
    
    Args:
        world (str): The name of the world.
        market_values (List[MarketValues]): The market value history of the item.
        meta_data (ItemMetaData): The meta data of the item.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = get_default_embed()
    embed.description = f"[{meta_data.wiki_name if meta_data.wiki_name else meta_data.name}]({meta_data.get_wiki_link()}) on {world}"
    embed.timestamp = datetime.fromtimestamp(max(market_values, key=lambda x: x.time).time)
    embed.set_thumbnail(url=meta_data.get_image_link())

    bytesio: BytesIO = MarketValues.generate_price_history_plot(market_values)
    file = discord.File(bytesio, filename="plot.png")
    embed.set_image(url="attachment://plot.png")

    max_sell = max_sell_timestamp = min_sell = min_sell_timestamp = avg_sell = -1
    max_buy = max_buy_timestamp = min_buy = min_buy_timestamp = avg_buy = -1
    valid_sell_values = valid_buy_values = 0

    for market_value in market_values:
        current_sell_value = market_value.day_average_sell if market_value.day_average_sell > -1 else market_value.sell_offer
        current_buy_value = market_value.day_average_buy if market_value.day_average_buy > -1 else market_value.buy_offer

        if current_sell_value > 0:
            valid_sell_values += 1
            avg_sell += current_sell_value
            if current_sell_value > max_sell:
                max_sell = current_sell_value
                max_sell_timestamp = int(market_value.time)
            if min_sell == -1 or current_sell_value < min_sell:
                min_sell = current_sell_value
                min_sell_timestamp = int(market_value.time)

        if current_buy_value > 0:
            valid_buy_values += 1
            avg_buy += current_buy_value
            if current_buy_value > max_buy:
                max_buy = current_buy_value
                max_buy_timestamp = int(market_value.time)
            if min_buy == -1 or current_buy_value < min_buy:
                min_buy = current_buy_value
                min_buy_timestamp = int(market_value.time)

    avg_sell = avg_sell // valid_sell_values if valid_sell_values > 0 else 0
    avg_buy = avg_buy // valid_buy_values if valid_buy_values > 0 else 0

    if valid_sell_values:
        embed.add_field(name="Sell data", value=f"`Max`: {max_sell:,}{GOLD_COIN_EMOJI} <t:{max_sell_timestamp}:R>\n`Min`: {min_sell:,}{GOLD_COIN_EMOJI} <t:{min_sell_timestamp}:R>\n`Avg`: {avg_sell:,}")

    if valid_buy_values:
        embed.add_field(name="Buy data", value=f"`Max`: {max_buy:,}{GOLD_COIN_EMOJI} <t:{max_buy_timestamp}:R>\n`Min`: {min_buy:,}{GOLD_COIN_EMOJI} <t:{min_buy_timestamp}:R>\n`Avg`: {avg_buy:,}")

    return embed, file
