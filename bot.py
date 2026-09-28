#what in the clartington to the fartington is this shit

import os
import webserver
import re
from logging import FileHandler
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
token: str | None = os.getenv("DISCORD_TOKEN")

handler: FileHandler = FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix = "!", intents = intents)

#embed fixing
FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?<!vx)(?<!fx)(?:www\.)?(?:twitter|x)\.com"), "www.vxtwitter.com"),
    (re.compile(r"(?<!kk)(?<!dd)(?:www\.)?instagram\.com"), "www.kkinstagram.com"),
    (re.compile(r"(?:www\.)?tiktok\.com"), "www.tnktok.com"),
    (re.compile(r"(?<!vx)(?:(?:www\.)?old\.)?(?:www\.)?(?:reddit)\.com"), "www.vxreddit.com"),
]

#p3r
TRIGGERWORDS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bp3r\b|\bpersona 3 reload\b", re.IGNORECASE), "https://static2.klipy.com/ii/e7539ef2aad336edaa067c28ee130b3c/82/d8/xXGMoeJRZCQKj09dsj.gif"),
    (re.compile(r"\bjunpei\b|\biori\b", re.IGNORECASE), "https://static2.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/b7/b1/NMPtgjVV.gif")
]

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    #Embed Fixing
    fixed: str = message.content
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

    #P3R
    for pattern in TRIGGERWORDS:
        if pattern[0].search(message.content):
            await message.reply(pattern[1])
            break

#Begin
webserver.keep_alive()

if isinstance(token, str):
    bot.run(token, log_handler = handler)