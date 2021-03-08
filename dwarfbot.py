#!/usr/bin/env python
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import requests
from bs4 import BeautifulSoup as bs

# External settings from dot dir
# Yes Mr Polnäs, you need an external token directory
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/.DwarfSettings/" % (HOMEDIR)

with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

bot = discord.ext.commands.Bot(command_prefix = "your_prefix");

@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.green())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000} ms'
    await ctx.send(embed=em)

bot.run(TOKEN)