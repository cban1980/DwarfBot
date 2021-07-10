#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import requests
from bs4 import BeautifulSoup as bs
import re
import io
import aiohttp
import random
import datetime

HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/tokens/" % (HOMEDIR)

with open(TOKENHOME + "dogbot.txt", "r") as readfile:
    TOKEN = readfile.read().strip()

bot = discord.ext.commands.Bot(command_prefix = "!");

def cssformat(input):
    return "```css\n" + input + "```"


def iniformat(input):
    return "```ini\n" + input + "```"


def htmlformat(input):
    return "```html\n" + input + "```"


def bold(input):
    return "**" + input + "**"

@bot.event
async def on_message(message: discord.Message):
    time_now  = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S') 
    image_types = ["png", "jpeg", "gif", "jpg", "webp"]
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            if os.path.isdir('{0}/images/{1}'.format(HOMEDIR, message.author)):
                await attachment.save('{0}/images/{1}/{2}'.format(HOMEDIR, message.author, time_now) + attachment.filename)
            else:
                 os.makedirs('{0}/images/{1}'.format(HOMEDIR, message.author))
                 await attachment.save('{0}/images/{1}/{2}'.format(HOMEDIR, message.author, time_now) + attachment.filename)

            
@bot.command(name='pornhub', pass_context=True)
async def pornhub(ctx):
    if ctx.message.channel.id != 700643276415565845:
        pass
    else:
        lines = open('{0}/discordbots/files/porn.txt'.format(HOMEDIR)).read().splitlines()
        randline = random.choice(lines)
        await ctx.channel.send("{0} {1}".format(ctx.message.author.mention, randline))

@bot.event
async def on_ready():
   url_data = requests.get('http://www.fortunecookiemessage.com/').text
   soup = bs(url_data, 'html.parser')
   cookie = soup.find(class_="cookie-link").getText()
   activity = discord.Game(name=cookie)
   await bot.change_presence(activity=activity)

@bot.command(name='weather', pass_context=True)
async def väder(ctx, *, args):
    args = args.capitalize()
    url = "https://wttr.in/{0}.png?0pq&lang=en".format(args)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('Could not fetch image..')
            data = io.BytesIO(await resp.read())
        await ctx.channel.send(file=discord.File(data, 'weather.png'))
   
@bot.command(name='dogbot', pass_context=True)
async def dogbot(ctx):
    embed = discord.Embed(title="𝐃𝐨𝐠𝐁𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:", description=" ", color=0xeee657)
    embed.add_field(name="!streams", value="Displays currently running ROR twitch streams.", inline=False)
    embed.add_field(name="!dice", value="Rolls the dices! Syntax: !dice <amount of dices> <number>. Max 5 dices.", inline=False)
    embed.add_field(name="!warpop", value="Displays the current amount of population on the server, and currently players in T1 and T2+ ( excluding anonymous players)", inline=False)
    embed.add_field(name="!serverinvite", value="Generates an invitelink to this Discord server. Will be sent to you in a private message.", inline=False)
    embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/81-yKbVND-L._SY355_.png")
    await ctx.channel.send(embed=embed)


@bot.command(name='warpop', pass_context=True)
async def warpop():
    htmldata = requests.get('https://www.returnofreckoning.com/whos_online.php').text
    soup = bs(htmldata, "html5lib")
    pop = soup.find(class_="realm-info realm-info-detail").getText()
    pop = pop.replace("Total :", "")
    pop = pop.replace("Faction ratio (Order/Destruction) :", "")
    pop = pop.replace(":", "")
    pop = pop.replace("Martyrs Square (EN)", "")
    pop = pop.strip().splitlines()
    pop = list(filter(None, pop))
    pop = '\n'.join(pop)
    await ctx.channel.send(cssformat(str(pop)))


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


@bot.command(name='dice', pass_context=True)
async def dice(ctx, *args):
    if not args:
        number = [random.randint(1, 20)]
        await bot.say("The dice tumbles and rolls for " + ctx.message.author.mention + " and it gives the number: " + iniformat(str(number)))
    else:
        min = 1
        max = int(args[1])
        if int(args[0]) >= 6:
            await bot.say("To many dices, try 5 or less")
        else:
            number = []
            for i in range(1, int(args[0])+1):
                number.append(random.randint(min, max))
        total = sum(number)
        await ctx.channel.send("The dices tumbles and rolls for " + ctx.message.author.mention + " and they gives the numbers: " + iniformat(str(number)) + cssformat(" Total: " + str(total)))


@bot.command(name='serverinvite', pass_context=True)
async def inv(ctx):
    invite = await bot.create_invite(ctx.message.channel, max_uses=1, xkcd=True)
    await ctx.send_message(ctx.message.author, "Invite URL is {}".format(invite.url))
    await ctx.channel.send(ctx.message.author.mention + " Invite URL generated, check your PM's! ")

bot.run(TOKEN)
