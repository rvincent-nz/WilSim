import discord
from discord.ext import commands


class WilSimCore(commands.Cog):
    """TranslateCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):

        await ctx.send("Hi! I'm WilSim!")


def setup(bot):
    bot.add_cog(WilSimCore(bot))
    print("WilSimCore cog loaded.")
