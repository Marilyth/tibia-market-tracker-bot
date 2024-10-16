import discord
import os
import json
import discord.ext
import discord.ext.commands
import modules
import modules.market


class MarketBot(discord.ext.commands.AutoShardedBot):
    """A discord bot that provides information about the Tibia market.
    """
    def __init__(self):
        super().__init__(intents=discord.Intents.default(), command_prefix=discord.ext.commands.when_mentioned)

    async def setup_hook(self):
        await self.load_modules()
        await self.tree.sync()

    async def load_modules(self):
        """Load all module in the modules directory and add them as cogs to the bot.
        """
        await self.add_cog(modules.market.Market(self))


if __name__ == '__main__':
    config_location = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    with open(config_location, mode="r+", encoding="utf-8") as f:
        config = json.load(f)

    MarketBot().run(config["token"])
    