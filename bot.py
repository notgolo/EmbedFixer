#what in the clartington to the fartington is this shit

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
import re

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)

#embed fixing
FIXES = [
        (re.compile(r"(?<!vx)(?<!fx)(?:www\.)?(?:twitter|x)\.com"), "www.vxtwitter.com"),
        (re.compile(r"(?<!kk)(?<!dd)(?:www\.)?instagram\.com"), "www.kkinstagram.com"),
        (re.compile(r"(?:www\.)?tiktok\.com"), "www.tnktok.com"),
        (re.compile(r"(?<!vx)(?:(?:www\.)?old\.)?(?:www\.)?(?:reddit)\.com"), "www.vxreddit.com")
]

#p3r
p3rSoullessSlopLink: str = "https://static2.klipy.com/ii/e7539ef2aad336edaa067c28ee130b3c/82/d8/xXGMoeJRZCQKj09dsj.gif"
TRIGGERWORDS = [
        re.compile(r"\bp3r\b", re.IGNORECASE),
        re.compile(r"\bpersona 3 reload\b", re.IGNORECASE)
]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    #embed fixing
    fixed = message.content
    for pattern, replacement in FIXES:
        fixed = pattern.sub(replacement, fixed)
    
    if fixed != message.content:
        try:
            await message.channel.send(f"{message.author.mention} posted: {fixed}")
            await message.delete()
        except discord.Forbidden as e:
            print(f"Missing permissions: {e}")
        except discord.HTTPException as e:
            print(f"HTTP error: {e}")

    #p3r
    for pattern in TRIGGERWORDS:
        if pattern.search(message.content):
            message.channel.send(p3rSoullessSlopLink)
            break
 
webserver.keep_alive()

bot.run(token, log_handler = handler)