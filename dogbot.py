#!/usr/bin/env python3
# The Discord DogBot.
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
import platform
from urlextract import URLExtract
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
####################################
# Variables
####################################

status = False
initiator = ""
witchstamp = ""

####################################
# Settings
####################################

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

#######################################
# Main
#######################################

@bot.command(name='slaanesh', pass_context=True)
async def slaanesh(ctx):
    if ctx.message.channel.id != 700643276415565845:
        pass
    else:
        lines = open('{0}/files/porn.txt'.format(HOMEDIR)).read().splitlines()
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
async def weather(ctx, *, args):
    args = args.capitalize()
    url = "https://wttr.in/{0}.png?0pq&lang=en".format(args)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('Could not fetch image..')
            data = io.BytesIO(await resp.read())
        await ctx.channel.send(file=discord.File(data, 'weather.png'))

@bot.command(name='warpop', pass_context=True)
async def warpop(ctx):
    extractor = URLExtract()
    if os.path.isfile('tier/output.pngt'):
        os.remove("tier/output.png")
    url_data = requests.get('https://www.returnofreckoning.com/').text
    soup = bs(url_data, 'html5lib')
    soupdivs = soup.findAll("div", {"class": "faction_bar"},)
    soupdivs2 = soup.findAll("div", {"class": "player_bar"},)
    stringdivs2 = str(soupdivs2)
    stringdivs = str(soupdivs)
    totalpop= soup.findAll("div", {"class": "player-count"},)
    totalpop = str(totalpop)
    totalpop = totalpop.splitlines()[2]
    totalpop = totalpop[28:-4]
    tierpop = soup.find('div', attrs={'style': 'margin: 5px 0 2px 0;'})
    tier1pop = str(tierpop)
    tier2pop = str(tierpop)
    tier1pop = tier1pop[34:-8]
    tier2pop = soup.findAll('div', attrs={'style': 'margin: 5px 0 2px 0;'})
    tier2pop = str(tier2pop)
    tier2pop = tier2pop[:-9]
    tier2pop = tier2pop.split('>')[-1]
    url2 = re.sub('amp;', '', stringdivs2)
    urls = re.sub('amp;', '', stringdivs)
    urls = extractor.find_urls(urls)
    url2 = extractor.find_urls(url2)
    async with aiohttp.ClientSession() as session:
            async with session.get(url2[0]) as players:
                if players.status != 200:
                    return await ctx.channel.send('Could not tier listing...')
                players = io.BytesIO(await players.read())
                with open("tier/players.png", "wb") as f:
                    f.write(players.getbuffer())
            async with session.get(urls[0]) as tier1:
                if tier1.status != 200:
                    return await ctx.channel.send('Could not get tier listing...')
                tier1 = io.BytesIO(await tier1.read())
                with open("tier/tier1.png", "wb") as f:
                    f.write(tier1.getbuffer())
            async with session.get(urls[1]) as tier2:
                if tier2.status != 200:
                    return await ctx.channel.send('Could not get tier listing...')
                tier2 = io.BytesIO(await tier2.read())
                with open("tier/tier2.png", "wb") as f:
                    f.write(tier2.getbuffer())
            async with session.get(urls[2]) as total:
                if total.status != 200:
                    return await ctx.channel.send('Could not get tier listing...')
                total = io.BytesIO(await total.read())
                with open("tier/total.png", "wb") as f:
                    f.write(total.getbuffer())
            font = cv2.FONT_HERSHEY_SIMPLEX
            blank_image1 = np.zeros((35,207,3), np.uint8)
            blank_image2 = np.zeros((35,207,3), np.uint8)
            blank_image3 = np.zeros((35,207,3), np.uint8)
            blank_image4 = np.zeros((35,207,3), np.uint8)
            cv2.putText(blank_image1,"Players: {0}".format(totalpop),(30,18), font, 0.5,(0,255,0),2)
            cv2.putText(blank_image2,'{0}'.format(tier1pop),(30,18), font, 0.5,(0,255,0),2)
            cv2.putText(blank_image3,'{0}'.format(tier2pop),(30,18), font, 0.5,(0,255,0),2)
            cv2.putText(blank_image4,'Total',(72,22), font, 0.5,(0,255,0),2)
            cv2.imwrite('tier/text1.png', blank_image1)
            cv2.imwrite('tier/text2.png', blank_image2)
            cv2.imwrite('tier/text3.png', blank_image3)
            cv2.imwrite('tier/text4.png', blank_image4)
            b1 = cv2.imread('tier/text1.png', 1)
            b2 = cv2.imread('tier/text2.png', 1)
            b3 = cv2.imread('tier/text3.png', 1)
            b4 = cv2.imread('tier/text4.png', 1)     
            im1 = cv2.imread('tier/players.png', 1)
            im2 = cv2.imread('tier/tier1.png', 1)
            im3 = cv2.imread('tier/tier2.png', 1)
            im4 = cv2.imread('tier/total.png', 1)
            im_v = cv2.vconcat([b1, im1, b2, im2, b3, im3, b4, im4])
            cv2.imwrite('tier/output.png', im_v)
            file = discord.File("tier/output.png", filename="warpop.png")
            time_now = datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')
            embed = discord.Embed(title="Current population on ROR:", description="", color=0xc27c0e)
            embed.set_image(url="attachment://warpop.png")
            await ctx.channel.send(file=file)

@bot.command(name='dogbot', pass_context=True)
async def dogbot(ctx):
    embed = discord.Embed(title="𝐃𝐨𝐠𝐁𝐨𝐭 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:", description=" ", color=0xeee657)
    embed.add_field(name="!weather <location>", value="Posts PNG with the weather in <location>, curtesy of wttr.in.", inline=False)
    embed.add_field(name="!slaanesh", value="Makes DogBot speak with the voice of Slaanesh, only useable in the #Brothel channel.", inline=False)
    embed.add_field(name="!streams", value="Displays currently running ROR twitch streams.", inline=False)
    embed.add_field(name="!dice", value="Rolls the dices! Syntax: !dice <amount of dices> <number>. Max 5 dices.", inline=False)
    embed.add_field(name="!warpop", value="Displays the current amount of population on the server, and currently players in T1 and T2+ ( excluding anonymous players)", inline=False)
    embed.add_field(name="!serverinvite", value="Generates an invitelink to this Discord server. Will be sent to you in a private message.", inline=False)
    embed.add_field(name="!witching start/stop", value="Starts/stops the witching hour, only useable by Shabtys!", inline=False)
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/L0Au88PJUyWxkjOpPop-QnSSrC--fWuurhMeRLZJs6I/https/i.imgur.com/pA3EPkO.png")
    embed.set_footer(text='DogBot currently runs on: ({0}-{1} / Python:{2}) and was made by Tanish.'.format(platform.system(), platform.release(), platform.python_version()),icon_url="https://icons-for-free.com/iconfiles/png/512/bxl+tux-1325051940415123278.png")
    await ctx.channel.send(embed=embed)

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

@bot.command(name='witching', pass_context=True)
@commands.has_any_role('Shabty', 'Beastlord')
async def witching(ctx, arg):
    global status
    global initiator
    if arg == 'start' and status == False:
        status = True
        initiator = ctx.message.author.mention
        witchstamp = datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')
        file = discord.File("files/Witching_Hour.jpg", filename="Witching_Hour.jpg")
        time_now = datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')
        embed = discord.Embed(title="The witching hour has begun!", description="Initiated by **{0}**.".format(ctx.message.author.mention), color=0xc27c0e)
        embed.add_field(name="Started at: ", value=time_now, inline=False)
        embed.set_image(url="attachment://Witching_Hour.jpg")
        await ctx.channel.send(file=file, embed=embed)
    elif arg == 'start' and status == True:
        await ctx.channel.send("{0} a witching hour is already in progress. Initiated by {1} at {2}".format(ctx.message.author.mention, initiator, witchstamp))
    elif arg == 'stop' and status == True:
        status = False
        file = discord.File("files/Witching_Hour.jpg", filename="Witching_Hour.jpg")
        time_now = datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')
        embed = discord.Embed(title="The witching hour has come to an end!", description="By decree of **{0}**.".format(ctx.message.author.mention), color=0xc27c0e)
        embed.add_field(name="Stopped at: ", value=time_now, inline=False)
        embed.set_image(url="attachment://Witching_Hour.jpg")
        await ctx.channel.send(file=file, embed=embed)
        initiator = []
    else:
        await ctx.channel.send("{0} There is no Witching hour in progress..".format(ctx.message.author.mention))


@bot.listen('on_message')
async def attachsave(message: discord.Message):
    time_now  = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S') 
    image_types = ["png", "jpeg", "gif", "jpg", "webp"]
    if message.author.bot: 
        return
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            if os.path.isdir('{0}/images/{1}'.format(HOMEDIR, message.author.name)):
                await attachment.save('{0}/images/{1}/{2}'.format(HOMEDIR, message.author.name, time_now) + attachment.filename)
            else:
                 os.makedirs('{0}/images/{1}'.format(HOMEDIR, message.author.name))
                 await attachment.save('{0}/images/{1}/{2}'.format(HOMEDIR, message.author.name, time_now) + attachment.filename)
                

bot.run(TOKEN)
