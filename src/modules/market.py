from discord.ext import commands
from discord import app_commands
import asyncio


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='market')
    async def market(self, ctx: commands.Context):
        await ctx.defer()
        await asyncio.sleep(10)
        await ctx.send('Response')
