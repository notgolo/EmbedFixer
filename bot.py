import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
import re

load_dotenv()
token=os.getenv("DISCORD_TOKEN")

handler=logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents=discord.Intents.default()
intents.message_content=True
intents.members=True

bot=commands.Bot(command_prefix="!", intents=intents)

FIXES=[
        (re.compile(r"(!<vx)(?:www\.)?(?:twitter|x)\.com"), "vxtwitter.com"),
        (re.compile(r"(!<!(kk||dd))(?:www\.)?instagram\.com"), "kkinstagram.com"),
        (re.compile(r"(!:www\.)?tiktok\.com"), "tnktok.com"),
        (re.compile(r"(!<!vx)(?:www\.)(?:reddit|old\.reddit)\.com"), "vxreddit.com"),
]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    fixed=message.content
    for pattern, replacement in FIXES:
        fixed=pattern.sub(replacement, fixed)
    
    if fixed!=message.content:
        try:
            await message.channel.send(f"{message.author.mention} posted: {fixed}")
            await message.delete()
        except discord.Forbidden as e:
            print(f"Missing permissions: {e}")
        except discord.HTTPException as e:
            print(f"HTTP error: {e}")

webserver.keep_alive()

bot.run(token, log_handler=handler)
