from pydantic import BaseModel
from tinydb import Query
from utils import database


class DiscordUser(BaseModel):
    """A data class containing information and settings for a user."""

    id: int
    """The discord id of the user."""
    default_world: str = "Antica"
    """The default Tibia world of the user."""

    def save(self):
        """Saves the user to the database."""
        table = database.get_table(DiscordUser)
        table.update_data(self, Query().id == self.id)

    @staticmethod
    def from_database(user_id: int) -> "DiscordUser":
        """Loads the user from the database if it exists, otherwise creates a new one.

        Args:
            user_id (int): The discord id of the user.

        Returns:
            DiscordUser: The DiscordUser object.
        """
        table = database.get_table(DiscordUser)
        user_data = table.get_data(Query().id == user_id)

        if not user_data:
            return DiscordUser(id=user_id)

        return user_data[0]
