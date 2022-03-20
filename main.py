import asyncio
from mailbox import Mailbox
from imap_tools import MailBox, AND
import discord
from discord.ext import commands
from config import *
from Utils.misc import Sanitize

Aster = commands.Bot(command_prefix="*")

async def SendEmbed(payload):
    channel = Aster.get_channel(CHANNELID)
    await channel.send(embed=payload)

async def SendFile(payload):
    channel = Aster.get_channel(CHANNELID)
    with open("mailbody.txt", "rb") as file:
        await channel.send(embed=payload, file=discord.File(file, "mailbody.txt"))

async def CreateEmbed(Header, Desc, Body):
    embed=discord.Embed(title=Header, description=Desc, color=0x8d9bbc)
    embed.add_field(name="Body", value=Body, inline=False)
    return embed

async def Pulse():
    while True:
        mb = MailBox(SERVER).login(USERNAME, PASSWORD)
        messages = mb.fetch(criteria=AND(seen=False), mark_seen=True, charset="UTF-8")
        
        try:
            for msg in messages:
                message = msg.text
                if len(msg.text) > 350:
                    with open("mailbody.txt", "w") as file:
                        file.write(message)
                    embed = await CreateEmbed(msg.subject, msg.from_, "See attached file")
                else:    
                    embed = await CreateEmbed(msg.subject, msg.from_, await Sanitize(message))
                    await SendEmbed(embed)
                await asyncio.sleep(1)
        except:
            continue
        await asyncio.sleep(10)

@Aster.event
async def on_ready():
    print("Pulse")
    asyncio.get_event_loop().create_task(Pulse())
    
Aster.run(TOKEN)