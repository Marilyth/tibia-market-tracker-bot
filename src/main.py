import discord
import os
import json
import discord.ext
import discord.ext.commands
from discord.ext.commands import BotT
from typing import Dict
from modules.market import Market
from modules.general import General
from modules.status_reel import StatusReel
from modules.embedder.default import get_default_error_embed
from utils.market_api import MarketApi
from utils import database


class MarketBot(discord.ext.commands.AutoShardedBot):
    """A discord bot that provides information about the Tibia market."""

    def __init__(self, config: Dict[str, str]):
        super().__init__(intents=discord.Intents.default(), command_prefix=discord.ext.commands.when_mentioned)
        self.config = config
        database.setup_database()
        self.market_api = MarketApi(config["market_api_token"])
        self.status_reel: StatusReel = StatusReel(self)

    async def on_command_error(self, context: discord.ext.commands.Context[BotT], exception: discord.ext.commands.errors.CommandError, /) -> None:
        """Notify the user on command errors.

        Args:
            context (discord.ext.commands.Context): The context of the command.
            exception (discord.ext.commands.errors.CommandError): The exception that was raised.
        """
        arguments = ", ".join([f"{key}=\"{value}\"" for key, value in context.kwargs.items()])
        command_name = context.command.qualified_name if context.command else "Unknown command"

        if arguments:
            arguments = f"({arguments})"

        embed = get_default_error_embed(f"{command_name}", exception)
        await context.send(embed=embed)

        await super().on_command_error(context, exception)

    async def on_ready(self):
        """Start the status reel when the bot is ready."""
        print(f"Logged in as {self.user}")
        self.status_reel.start_reel()

    async def setup_hook(self):
        """Add all cogs to the bot and sync the command tree."""
        await self.load_modules()
        await self.tree.sync()

    async def load_modules(self):
        """Load all module in the modules directory and add them as cogs to the bot."""
        await self.add_cog(Market(self))
        await self.add_cog(General(self))

    def run(self, *args, **kwargs):
        """Run the bot with the provided config."""
        super().run(self.config["discord_token"], *args, **kwargs)

def get_config():
    """Gets or creates the config for the bot."""
    config_location = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    rewrite_config = False

    os.makedirs(os.path.dirname(config_location), exist_ok=True)

    config = {
        "discord_token": "",
        "market_api_token": ""
    }

    # Load the config file if it exists.
    if os.path.exists(config_location):
        with open(config_location, mode="r+", encoding="utf-8") as f:
            saved_config = json.load(f)

        for key in saved_config:
            if key in config:
                config[key] = saved_config[key]

    # Prompt the user for any missing values.
    for key, value in config.items():
        if not value:
            config[key] = input(f"Enter your {key}: ")
            rewrite_config = True

    # Write the config file if it was modified.
    if rewrite_config:
        with open(config_location, mode="w+", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        print(f"Config file created. You can modify it at {config_location}.")

    return config

if __name__ == '__main__':
    MarketBot(get_config()).run()
