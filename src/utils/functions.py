from utils.data.discord_server import DiscordServer
from utils.data.user import DiscordUser
from discord.ext import commands


def get_default_world(ctx: commands.Context) -> str:
    """Gets the default world for the user or server.

    Args:
        ctx (commands.Context): The context of the command.

    Returns:
        str: The default world.
    """
    if ctx.guild:
        default_world, has_default = DiscordServer.from_database(ctx.guild.id)

        if has_default:
            return default_world

    return DiscordUser.from_database(ctx.author.id)[0].default_world
