from typing import List
from pydantic import BaseModel


class MarketBoardTraderData(BaseModel):
    """A data class containing information about a trader in the market board.
    """
    name: str
    amount: int
    price: int
    time: float


class MarketBoard(BaseModel):
    """A data class containing information about the market board of an item.
    The sellers, buyers, amounts, prices and time are stored in this class.
    """
    id: int
    sellers: List[MarketBoardTraderData]
    buyers: List[MarketBoardTraderData]
    update_time: float
