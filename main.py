import asyncio
from imap_tools import MailBox, AND
import discord
from discord.ext import commands
from config import *

Aster = commands.Bot(command_prefix="*")
mb = MailBox(SERVER).login(USERNAME, PASSWORD)

async def Send(payload):
    channel = Aster.get_channel(CHANNELID)
    await channel.send(embed=payload)

async def CreateEmbed(Header, Desc, Body):
    embed=discord.Embed(title=Header, description=Desc, color=0x8d9bbc)
    embed.add_field(name="Body", value=Body, inline=False)
    return embed

async def Pulse():
    while True:
        messages = mb.fetch(criteria=AND(seen=False), mark_seen=True, charset="UTF-8")
        
        for msg in messages:
            message = msg.text
            if len(msg.text) > 350:
                message = msg.text[:350]
            embed = await CreateEmbed(msg.subject, msg.from_, message)
            await Send(embed)
            await asyncio.sleep(1)
        await asyncio.sleep(10)

@Aster.event
async def on_ready():
    print("Pulse")
    asyncio.get_event_loop().create_task(Pulse())
    
Aster.run(TOKEN)