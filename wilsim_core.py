# pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py

import discord
from discord.ext import commands

with open('bot_token.txt') as file:
    TOKEN = file.read()


def get_prefix(bot, message):

    prefixes = ['!']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


extensions = ['cogs.wilsim_cog']

bot = commands.Bot(command_prefix=get_prefix, description='WilSim bot')

for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.')


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    print(f'Successfully logged in and booted...!')


bot.run(TOKEN, bot=True, reconnect=True)
