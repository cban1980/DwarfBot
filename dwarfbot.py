#!/usr/bin/env python
include discord
from discord.ext import commands
# External settings from dot dir
# Yes MR Polnäs, you need an external token directory
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/.DwarfSettings/" % (HOMEDIR)
with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

bot = commands.Bot(command_prefix='!')
ot.run(TOKEN)