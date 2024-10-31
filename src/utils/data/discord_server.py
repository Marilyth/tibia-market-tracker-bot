from pydantic import BaseModel
from tinydb import Query
from utils import database
from typing import Tuple


class DiscordServer(BaseModel):
    """A data class containing information and settings for a discord server."""

    id: int
    """The discord id of the server."""
    default_world: str = "Antica"
    """The default Tibia world of the server."""

    def save(self):
        """Saves the server to the database."""
        table = database.get_table(DiscordServer)
        table.update_data(Query().id == self.id, self)

    @staticmethod
    def from_database(server_id: int) -> Tuple["DiscordServer", bool]:
        """Loads the discord server settings from the database if it exists, otherwise creates a new one.

        Args:
            server_id (int): The discord server id.

        Returns:
            Tuple[DiscordServer, bool]: A tuple containing the DiscordServer object and a boolean indicating if the server was found in the database.
        """
        table = database.get_table(DiscordServer)
        server_data = table.get_data(Query().id == server_id)

        if not server_data:
            return DiscordServer(id=server_id), False

        return server_data[0], True
