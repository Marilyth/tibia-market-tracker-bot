import discord
import os
import json
import discord.ext
import discord.ext.commands
from typing import Dict
from modules.market import Market
from modules.general import General
from modules.status_reel import StatusReel
from utils.market_api import MarketApi


class MarketBot(discord.ext.commands.AutoShardedBot):
    """A discord bot that provides information about the Tibia market."""

    def __init__(self, config: Dict[str, str]):
        super().__init__(intents=discord.Intents.default(), command_prefix=discord.ext.commands.when_mentioned)
        self.config = config
        self.market_api = MarketApi(config["market_api_token"])
        self.status_reel: StatusReel = StatusReel(self)

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


if __name__ == '__main__':
    config_location = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    with open(config_location, mode="r+", encoding="utf-8") as f:
        config_dict = json.load(f)

    MarketBot(config_dict).run()
