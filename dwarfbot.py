#!/usr/bin/env python
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import requests
from bs4 import BeautifulSoup as bs
import re
import yfinance as yf

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
    husmat = []
    for ul in mat:
        for li in ul.findAll('li'):
            husmat += li
    values = "\n".join(map(str, husmat))
    await ctx.channel.send('**Dagens meny hos Husman:**\n' + values)

@bot.command(name='gme', pass_context=True)
async def gme(ctx):
    tickerSymbol = 'GME'
    tickerData = yf.Ticker(tickerSymbol)
    await ctx.channel.send(tickerData.recommendations)

@bot.command(name='chili', pass_context=True)
async def chili(ctx):
    htmldata = requests.get('http://www.chili-lime.se/')
    soup = bs(htmldata.text, 'html5lib')
    mat = soup.find("td", width=571).text.strip()
    mat = re.sub(r'(?m)^[ \t]*$\n?', '', mat)
    mat = mat.split('\n',4)[-1]
    mat = mat.rsplit("\n", 1)[0]
    maten = []
    for line in mat:
        if line[:1].isdigit():
            pass
        else:
            if line.startswith('.'):
                pass
            else:
                maten += line
    snasket = "".join(map(str, maten))
    snasket = re.sub("\n\s*\n*", "\n", snasket).lstrip()
    await ctx.channel.send('**Dagens meny hos Chili&Lime:**\n' + snasket)

@bot.command(name='hjalp', pass_context=True)
async def hjalp(ctx):
    embed = discord.Embed(title="𝐃𝐢𝐬𝐜𝐨𝐫𝐝𝐛𝐨𝐭𝐞𝐧 DwarBot", description="Kommandolista:", color=0xeee657)
    embed.add_field(name="!husman", value="Visar dagens meny från husman.", inline=False)
    embed.add_field(name="!chili", value="Visar dagens meny från Chili&Lime.", inline=False)
    embed.set_thumbnail(url="https://hekint.org/images/All_journal_images/2015_Briefs/Goyri/Goyri_Figure%205.jpg")
    await ctx.channel.send(embed=embed)

bot.run(TOKEN)