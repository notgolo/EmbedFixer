#what in the clartington to the fartington is this shit
#dogshit language

import asyncio
import datetime
import os
from discord import permissions
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

galeID: int = 221075470437842944
goloID: int = 424304430184398849
lintyID: int = 272210308846583808
adminIDs: list[int] = [galeID, goloID]

gifRepliesEnabled: bool = False

timeLastMessageSent: dict[int, datetime.datetime]

standoffEmbedRemoveTriggerTime: int = 60
standoffRoundTime: int = 30
standoffRemoveEmbedActive: bool = False
standoffTargets: dict[int, int] = {}

EMBED_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?<!vx)(?<!fx)(?:www\.)?(?:twitter|x)\.com"), "www.vxtwitter.com"),
    (re.compile(r"(?<!kk)(?<!dd)(?:www\.)?instagram\.com"), "www.kkinstagram.com"),
    (re.compile(r"(?:www\.)?tiktok\.com"), "www.tnktok.com"),
    (re.compile(r"(?<!vx)(?:(?:www\.)?old\.)?(?:www\.)?(?:reddit)\.com"), "www.vxreddit.com"),
    (re.compile(r"(?:www\.)?bsky\.app"), "bskye.app"),
    (re.compile(r"(?:www\.)?threads\.com"), "www.vxthreads.com"),
]

GIF_REPLIES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bp3r\b|\bpersona 3 reload\b|\bpersona_3_reload\b", re.IGNORECASE), "https://static2.klipy.com/ii/e7539ef2aad336edaa067c28ee130b3c/82/d8/xXGMoeJRZCQKj09dsj.gif"),
    (re.compile(r"\bjunpei\b|\biori\b", re.IGNORECASE), "https://static2.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/b7/b1/NMPtgjVV.gif"),
    (re.compile(r"\bive been waiting for this\b|\bi've been waiting for this\b", re.IGNORECASE), "https://klipy.com/gifs/persona-3-dancing-akihiko-dance-ive-been-waiting-for-this-persona3"),
    (re.compile(r"\bi used to work at blizzard\b", re.IGNORECASE), "https://static2.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/99/b4/YmQ7rbgLeYDeBIgHIYEo.gif"),
    (re.compile(r"\bclartation\b", re.IGNORECASE), "https://cdn.discordapp.com/attachments/667770592015024129/1517702508490002502/Screenshot_2026-06-19_212700.gif?ex=6abbbcdb&is=6aba6b5b&hm=cdc554548e81d7767be6abafdabe69b48c890f8037df35561e5af750fd0891c7&"),
    (re.compile(r"\bkms\b", re.IGNORECASE), "https://static2.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/7b/f9/pDTFcfyOIo8iQ.gif"),
    (re.compile(r"\bkys\b", re.IGNORECASE), "https://cdn.discordapp.com/attachments/1293267621554425938/1554513494190071880/caption.gif?ex=6abd2902&is=6abbd782&hm=6d6d0c9831871f81352f06b24b8f098f69b80aa67f76ea5cad7c4c06a8d42543&"),
    (re.compile(r"\brip pokimanes cat\b", re.IGNORECASE), "https://static2.klipy.com/ii/f87f46a2c5aeaeed4c68910815f73eaf/fe/9e/JZMsbFqu.gif"),
    (re.compile(r"\bntr\b", re.IGNORECASE), "https://static2.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/42/da/uHc1olriiQY66CF.gif"),
    (re.compile(r"\bwednesday\b", re.IGNORECASE), "https://static2.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/b6/41/XKpuYeFIeti8Vhe.gif"),
    (re.compile(r"\bfriday\b", re.IGNORECASE), "https://static2.klipy.com/ii/4493325008d34b7bf8cd6813cd5c1619/24/80/hTK1G9Uq2SuBn.gif")
]

def parse_member_id(guild: discord.Guild | None, possibleID: str | None) -> int | None:
    if guild is None or possibleID is None:
        return None
    
    possibleID = possibleID.strip();
    try:
        if possibleID.startswith("<@") and possibleID.endswith(">"):
            userID: int = int(possibleID[2:len(possibleID) - 1])
            if guild_has_member(guild, userID):
                return None
            return userID
    except ValueError:
        return None

    return None

def chat_handle_from_id(handle: int | None) -> str:
    return f"<@{handle}>"

def guild_has_member(guild: discord.Guild, userID: int) -> bool:
    return get_member(guild, userID) is not None
def get_member(guild: discord.Guild | None, userID: int | None) -> discord.Member | None:
    if guild is None or userID is None:
        return None

    return guild.get_member(userID)

#@bot.event
#async def on_ready() -> None:
    #for guild in bot.guilds:
        #if guild is None:
            #break
    
        #role: discord.Role | None = discord.utils.get(guild.roles, name = "Timed Out Standoff")
        #if role is None:        
            #newPermissions: discord.Permissions = discord.Permissions()
            #newPermissions.embed_links = False

            #role = await guild.create_role(name = "Timed Out Standoff", permissions = newPermissions)

@bot.event
async def on_message(message: discord.Message) -> None:
    global gifRepliesEnabled
    
    if message.author.bot:
        return

    #timeLastMessageSent[message.author.id] = datetime.datetime.now()

    command: str = message.content.strip().lower()
    if len(command) > 0 and command[0] == '&':
        command = re.sub(r" {2,}", " ", command) #set all remaining whitespace to one whitespace/remove all double spaces
        commandSections: list[str] = command.split(" ")

        if commandSections[0] == "&setgifreplies" and  len(commandSections) > 1:
            if message.author.id not in adminIDs:
                if message.author.id == lintyID:
                    await message.reply("stfu")
                else:
                    await message.reply("you do NYAT have perms for dat! ^. .^₎⟆")
                return

            enabled: str = commandSections[1].lower()
            if(enabled == "true"):
                gifRepliesEnabled = True
                if message.author.id == goloID:
                    await message.reply("gif replies: enabled, nyaa (⸝⸝⸝O﹏ O⸝⸝⸝)")
                else:
                    await message.reply("Gif replies enabled")
            elif (enabled == "false"):
                gifRepliesEnabled = False
                if message.author.id == goloID:
                    await message.reply("nyaaaa, gif replies: disabled ૮꒰ ˶- ༝ - ˶꒱ა ♡")
                else:                    
                    await message.reply("Gif replies disabled")
            elif message.author.id == goloID:
                await message.reply("nyaaaa, gif replies: disabled ૮꒰ ˶- ༝ - ˶꒱ა ♡")
            else:                    
                await message.reply("Gif replies disabled")
         
        #elif commandSections[0] == "&standoff" and len(commandSections) > 2:
            #if commandSections[1] == "embedremove":
                #targetMember: discord.Member | None = get_member(message.guild, parse_member_id(message.guild, commandSections[2]))
                #if targetMember is None:
                    #return
                
                #secondsSinceLastMessage: float = (datetime.datetime.now() - timeLastMessageSent[targetMember.id]).total_seconds()
                #if secondsSinceLastMessage > standoffEmbedRemoveTriggerTime and targetMember not in standoffTargets:
                    #await message.reply(f"Cannot initiate embed remover standoff unless last message sent from target was less than {standoffEmbedRemoveTriggerTime}s ago or they are apart of the standoff as a challenger!")
                    #return

                #global standoffRemoveEmbedActive
                #if standoffRemoveEmbedActive == True:
                    #await message.channel.send(f"Embed Block Standoff: {message.author.mention} has fired at {targetMember.mention}!");
                    #standoffTargets[message.author.id] = targetMember.id
                #else:
                    #standoffRemoveEmbedActive = True

                    #await message.channel.send(f"Embed Block Standoff: Initiated by {message.author.mention}!")
                    #await message.channel.send(f"Embed Block Standoff: {message.author.mention} has fired at {targetMember.mention}!");
                    #standoffTargets[message.author.id] = targetMember.id

                    #await asyncio.sleep(30)

                    #standoffRemoveEmbedActive = False
                    #standoffTargets.clear()

        return

    fixed: str = message.content
    for pattern, replacement in EMBED_FIXES:
        fixed = pattern.sub(replacement, fixed)
    
    if fixed != message.content:
        try:
            await message.channel.send(f"{message.author.mention} posted: {fixed}")
            await message.delete()
        except discord.Forbidden as e:
            print(f"Missing permissions: {e}")
        except discord.HTTPException as e:
            print(f"HTTP error: {e}")
                
    if gifRepliesEnabled:
        for pattern, reply in GIF_REPLIES:
            if pattern.search(message.content):
                replyMessage: discord.Message
                if(message.reference is None or message.reference.message_id is None):
                    replyMessage = message
                else:
                    replyMessage = await message.channel.fetch_message(message.reference.message_id)
                await replyMessage.reply(reply)
                break

#Begin
webserver.keep_alive()

if isinstance(token, str):
    bot.run(token, log_handler = handler)
