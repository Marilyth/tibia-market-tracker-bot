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

    @staticmethod
    def id_to_wiki_link(item_id: int) -> str:
        """Converts an item id to a wiki link.

        Args:
            item_id (int): The item id.

        Returns:
            str: The wiki link of the item.
        """
        return f"https://tibia.fandom.com/wiki/{item_id}"

    @staticmethod
    def id_to_image_link(item_id: int) -> str:
        """Converts an item id to an image link.

        Args:
            item_id (int): The item id.

        Returns:
            str: The image link of the item.
        """
        return f"https://www.tibiamarket.top/sprites/{item_id}.gif"

    def get_wiki_link(self) -> str:
        """Returns the wiki link of the item.

        Returns:
            str: The wiki link of the item.
        """
        return self.id_to_wiki_link(self.id)

    def get_image_link(self) -> str:
        """Returns the image link of the item.

        Returns:
            str: The image link of the item.
        """
        return self.id_to_image_link(self.id)
