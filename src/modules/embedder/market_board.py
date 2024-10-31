import discord
from typing import List
from datetime import datetime
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_board import MarketBoard
from modules.embedder.default import get_default_embed


def dict_to_table(data: List[dict], line_limit: int = 5) -> str:
    """Converts a list of homogenous dictionaries to a markdown table.
    
    Args:
        data (dict): The dictionary to convert.
        
    Returns:
        str: The markdown table.
    """
    keys = data[0].keys()
    sub_data = data[:line_limit]

    key_lengths = [max([len(str(data_item[key])) for data_item in sub_data] + [len(key)]) for key in keys]
    table = "```sql\n"
    header = " | ".join([f"{key:<{key_lengths[i]}}" for i, key in enumerate(keys)]) + "\n"
    table += header
    table += "-" * (len(header) - 1) + "\n"

    for data_item in sub_data:
        table += " | ".join([f"{data_item[key]:<{key_lengths[i]}}" for i, key in enumerate(data_item)]) + "\n"

    table += "```"

    if len(data) > line_limit:
        table += f"\n_And {len(data) - line_limit} more..._"

    return table


def market_board_to_embedding(world: str, market_board: MarketBoard, meta_data: ItemMetaData) -> discord.Embed:
    """Converts a MarketBoard object to a discord.Embed object.
    
    Args:
        world (str): The name of the world.
        market_board (MarketBoard): The market board of the item.
        meta_data (ItemMetaData): The meta data of the item.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = get_default_embed()
    embed.description = f"[{meta_data.wiki_name if meta_data.wiki_name else meta_data.name}]({meta_data.get_wiki_link()}) on {world}"
    embed.timestamp = datetime.fromtimestamp(market_board.update_time)

    embed.set_thumbnail(url=meta_data.get_image_link())

    date_format = "%m/%d/%Y"

    # Add the market values to the embed.
    sell_board = market_board.sellers
    buy_board = market_board.buyers

    sell_board = [{"Name": seller.name, "Amount": f"{seller.amount:,}", "Price": f"{seller.price:,}", "Ends": datetime.fromtimestamp(seller.time).strftime(date_format)} for seller in sell_board]
    buy_board = [{"Name": buyer.name, "Amount": f"{buyer.amount:,}", "Price": f"{buyer.price:,}", "Ends": datetime.fromtimestamp(buyer.time).strftime(date_format)} for buyer in buy_board]

    embed.add_field(name="Sell offers", value=dict_to_table(sell_board), inline=False)
    embed.add_field(name="Buy offers", value=dict_to_table(buy_board), inline=False)

    return embed
