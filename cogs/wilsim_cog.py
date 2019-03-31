import discord
import requests
from discord.ext import commands

WILSIM_BASE_URL = 'https://lineagenode-tz18.c9users.io/WILSIM/'

WILSIM_ADOPT = '/adopt'

WILSIM_STATUS = '/status'

WILSIM_PAINT = '/paint'

WILSIM_FEED = '/feed'

WILSIM_PLAY = '/play'


async def interact(ctx, action):
    """Generic interaction function"""

    wilsim_interaction_url = WILSIM_BASE_URL + str(ctx.guild.id) + "/1" + action

    wilsim_interaction = requests.get(wilsim_interaction_url)

    print(wilsim_interaction_url)

    if wilsim_interaction.status_code is 200:
        await ctx.send(wilsim_interaction.json()['flavortext'])



async def check_status(ctx):
    """Checks WilSim's status. Returns a Requests object."""
    status_url = WILSIM_BASE_URL + str(ctx.guild.id) + "/1" + WILSIM_STATUS
    wilsim_status = requests.get(status_url)

    print(status_url)

    return wilsim_status


async def format_status(ctx):
    """Creates a Discord formatted status for WilSim."""

    wilsim_status = await check_status(ctx)

    if wilsim_status.status_code is 200:

        name = wilsim_status.json()['name']
        hunger = wilsim_status.json()['hunger']
        thirst = wilsim_status.json()['thirst']
        painted = wilsim_status.json()['painted']

        message = """```Name: {0}\nHunger: {1}\nThirst: {2}\nPaint Level: {3}/100```""".\
            format(name, hunger, thirst, painted)

        return message
    else:
        return "We could not find a registered pet!"


class WilSimCore(commands.Cog):
    """TranslateCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='adopt')
    async def adopt(self, ctx):

        wilsim_status = await check_status(ctx)

        if wilsim_status.status_code is 200:
            await ctx.send("You have already registered WilSim to this server!")
            return

        if wilsim_status.status_code is not 200:
            register_url = WILSIM_BASE_URL + str(ctx.guild.id) + "/1" + WILSIM_ADOPT

            wilsim_register = requests.get(register_url)
            print(register_url)

            if wilsim_register.status_code is 200:
                await ctx.send("Congratulations, {0}! You have successfully adopted {1}!".format(
                                ctx.guild.name, wilsim_register.json()['name']))

    @commands.command(name='status')
    async def status(self, ctx):

        wilsim_status_message = await format_status(ctx)

        await ctx.send(wilsim_status_message)

    @commands.command(name='paint')
    async def paint(self, ctx):
        """Paint Wilsim"""
        await interact(ctx, WILSIM_PAINT)

    @commands.command(name='feed')
    async def feed(self, ctx):
        """Feed Wilsim"""
        await interact(ctx, WILSIM_FEED)

    @commands.command(name='play')
    async def play(self, ctx):
        """Play with Wilsim"""
        await interact(ctx, WILSIM_PLAY)


def setup(bot):
    bot.add_cog(WilSimCore(bot))
    print("WilSimCore cog loaded.")
