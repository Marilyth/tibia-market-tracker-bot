from typing import List, Optional
from pydantic import BaseModel


class NPCSaleData(BaseModel):
    """A data class containing information about an NPC item sale.
    """
    name: str
    location: str
    price: int
    currency_object_type_id: int
    currency_quest_flag_display_name: str

    def is_gold(self) -> bool:
        """Returns True if the currency is gold, False otherwise.

        Returns:
            bool: True if the currency is gold, False otherwise.
        """
        return self.currency_object_type_id == 0 and self.currency_quest_flag_display_name == ""


class ItemMetaData(BaseModel):
    """A data class containing meta information about an item.
    """
    id: int
    category: Optional[str] = None
    tier: int = -1
    name: Optional[str] = None
    npc_sell: List[NPCSaleData] = None
    npc_buy: List[NPCSaleData] = None
    wiki_name: Optional[str] = None