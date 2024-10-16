from datetime import datetime
from pydantic import BaseModel


class WorldData(BaseModel):
    """A data class containing information about a Tibia server, and it's last update time.
    """

    name: str
    """The name of the world."""
    last_update: datetime
    """The last update time."""
