from pydantic import BaseModel


class DiscordUser(BaseModel):
    """A data class containing information and settings for a user."""

    id: int
    """The discord id of the user."""
    default_world: str = "Antica"
    """The default Tibia world of the user."""
