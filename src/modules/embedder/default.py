import discord
import discord.ext.commands


def get_default_embed():
    """Returns a default embed object to keep the style consistent.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = discord.embeds.Embed(color=0x7d3d24) # Tibia market icon color.

    embed.set_author(name="Click to join the support server!", icon_url="https://www.tibiamarket.top/logo.png", url="https://discord.gg/Rvc8mXtmZH")
    embed.set_footer(icon_url="https://www.tibiamarket.top/logo.png", text="Tibia Market API")

    return embed

def get_default_error_embed(command_name: str, exception: discord.ext.commands.CommandError):
    """Returns a default error embed object to keep the style consistent.
        
    Returns:
        discord.Embed: The embed object.
    """
    embed = discord.embeds.Embed(color=0xff0000)

    embed.set_author(name="Click to join the support server!", icon_url="https://www.tibiamarket.top/logo.png", url="https://discord.gg/Rvc8mXtmZH")
    embed.set_footer(icon_url="https://www.tibiamarket.top/logo.png", text="Tibia Market API")

    embed.description = f"Sorry! An error occurred while executing the command `{command_name}`.\nFeel free to join the [support server](https://discord.gg/Rvc8mXtmZH) for help."
    embed.add_field(name="Error", value=f"```{exception}```")

    return embed
