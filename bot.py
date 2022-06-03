import asyncio
from asyncore import write
import datetime
import random
from time import sleep
from turtle import title
import requests as rq
from datetime import time
import datetime


import discord
from discord import Intents
from discord import user
from discord.ext import commands
from discord.ext import tasks
from discord_components import *
from discord_components import DiscordComponents
import aiohttp
import fivem
from fivem import FiveM

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

intents = Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)


### Events
@client.event
async def on_ready():
    print('Bot Is Ready!')
    client.my_current_task = live_status.start()
    DiscordComponents(client)
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1


## Live Status
@tasks.loop()
async def live_status(seconds=75):
    pcount = pc()
    Dis = client.get_guild(config.guildID) #Int

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'🐌 {pcount} Players')
    await client.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'👥 {Dis.member_count} Members')
    await client.change_presence(activity=activity)
    await asyncio.sleep(10)

## Config
class config:
    guildID = 123 #guild id (discord server ID)
    serverIP = "" #IP:PORT | Example: 87.98.246.41:30120 | Use 127.0.0.1:PORT if you're running it on same Server as FiveM Server.




def pc():
    try:
        resp = rq.get('http://'+config.serverIP+'/players.json').json()
        return(len(resp))
    except:
        return('N/A')

        
## Players Command
@client.command()
@commands.has_permissions(administrator=True)
async def players(ctx):
    while True:
         now = datetime.datetime.now().strftime("%H:%M")
         resp = rq.get('http://'+config.serverIP+'/players.json').json()
         total_players = len(resp)
         if len(resp) > 100:
          for i in range(round(len(resp) / 100)):
            embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
            embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {now} ')
            count = 0
            for player in resp:
                embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
                count += 1
                if count == 100:
                    break
                else:
                    continue

            await ctx.send(embed=embed)
            sleep(2)
            await ctx.delete()
         else:
           embed = discord.Embed(title='FiveMBot Bot', description='Server Players', color=discord.Color.blurple())
           embed.set_footer(text=f'Total Players : {total_players} | FiveMBot | {now} ')
           for player in resp:
            embed.add_field(name=player['name'], value='ID : ' + str(player['id']))
           await ctx.send(embed=embed)
           sleep(2)
           await ctx.delete()
    
@client.command()
async def ip(ctx):
    embed = discord.Embed(title=f"Hey, {ctx.author.name}", description=f"**Server IP : {config.serverIP}**\n**TeamSpeak : **", color=discord.Color.random())
    await embed.footer("Have fun!")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def run(ctx):
    
    await ctx.message.delete()
    now = datetime.datetime.now().strftime("%H:%M")
    embed=discord.Embed(title="FiveM Server", description="Join and play!", color=discord.Color.random())
    embed.set_thumbnail(url="##your thumbnail url")
    embed.set_image(url="##your image url")
    embed.add_field(name=" Paste this in F8 ", value=f"Connect {config.serverIP}", inline=False)
    embed.set_footer(text=f"Today at |{now}")
    await ctx.send(embed=embed)





client.run("YOUR BOT TOKEN")
