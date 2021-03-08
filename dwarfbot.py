#!/usr/bin/env python
import discord
from discord.ext import commands
import os
# External settings from dot dir
# Yes Mr Polnäs, you need an external token directory
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/.DwarfSettings/" % (HOMEDIR)
with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

async def acommand(ctx, argument):
   await bot.say("Stuff")

bot = commands.Bot(command_prefix='!')
bot.run(TOKEN)