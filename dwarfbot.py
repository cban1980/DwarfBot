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

bot = discord.ext.commands.Bot(command_prefix = "!");

@bot.command(name='husman', pass_context=True)
async def husman(ctx):
    htmldata = requests.get('https://restauranghusman.se/')
    soup = bs(htmldata.text, 'html5lib')
    mat = soup.find("div", class_ = "todays-menu")
    mat = mat.get_text().strip()
    await ctx.channel.send(mat)


@bot.command(name='streams', pass_context=True)
async def streams(ctx):
    htmldata = requests.get('https://www.returnofreckoning.com/')
    soup = bs(htmldata.text, 'html5lib')
    outstuff = []
    for link in soup.findAll(class_="topictitle"):
        outstuffers = link.getText().rstrip()
        outstuff.append(" ⟿  "  + "[" + str(outstuffers) + "]" + "(" + link.get('href') + ")" + "£")
    outstuff = ''.join(outstuff)
    outstuff = outstuff.replace("£", "\n")
    embed=discord.Embed(title=" ")
    embed.add_field(name="Currently running ROR Streams:", value=str(outstuff), inline=False)
    await ctx.channel.send(embed=embed) 

bot.run(TOKEN)