from pydantic import BaseModel


class MarketValues(BaseModel):
    """A data class containing information about the market values of an item.
    """
    id: int
    time: float
    is_full_data: bool = False
    buy_offer: int = -1
    sell_offer: int = -1
    month_average_sell: int = -1
    month_average_buy: int = -1
    month_sold: int = -1
    month_bought: int = -1
    active_traders: int = -1
    month_highest_sell: int = -1
    month_lowest_buy: int = -1
    month_lowest_sell: int = -1
    month_highest_buy: int = -1
    buy_offers: int = -1
    sell_offers: int = -1
    day_average_sell: int = -1
    day_average_buy: int = -1
    day_sold: int = -1
    day_bought: int = -1
    day_highest_sell: int = -1
    day_lowest_sell: int = -1
    day_highest_buy: int = -1
    day_lowest_buy: int = -1
    total_immediate_profit: int = -1
    total_immediate_profit_info: str = ""
