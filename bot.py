#what in the clartington to the fartington is this shit
#dogshit language

#python imports
import datetime
import os
import re

from logging import FileHandler
from dotenv import load_dotenv

#discord imports
import discord
from discord import permissions
from discord.ext import commands

#local imports
import webserver

import general

import onmessage
import onreaction

load_dotenv()
token: str | None = os.getenv("DISCORD_TOKEN")

handler: FileHandler = FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix = "!", intents = intents)

timeLastMessageSent: dict[int, datetime.datetime]

standoffEmbedRemoveTriggerTime: int = 60
standoffRoundTime: int = 30
standoffRemoveEmbedActive: bool = False
standoffTargets: dict[int, int] = {}

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
async def fixEmbed(message: discord.Message) -> None:
    if message.author.bot:
        return

    #timeLastMessageSent[message.author.id] = datetime.datetime.now()

    command: str = message.content.strip().lower()
    if len(command) > 0 and command[0] == '&':
        command = re.sub(r" {2,}", " ", command) #set all remaining whitespace to one whitespace/remove all double spaces
        commandSections: list[str] = command.split(" ")

        if commandSections[0] == "&setgifreplies" and  len(commandSections) > 1:
            if general.isAdmin(message.author.id) == False:
                if message.author.id == general.lintyID:
                    await message.reply("stfu")
                else:
                    await message.reply("you do NYAT have perms for dat! ^. .^₎⟆")
                return

            enabled: str = commandSections[1].lower()
            if enabled == "true":
                onmessage.setGIFReplies(True)
                if message.author.id == general.galeID:
                    await message.reply("Gif replies enabled")
                else:
                    await message.reply("gif replies: enabled, nyaa (⸝⸝⸝O﹏ O⸝⸝⸝)")
            elif enabled == "false":
                onmessage.setGIFReplies(False)
                if message.author.id == general.galeID:
                    await message.reply("Gif replies disabled")
                else:
                    await message.reply("nyaaaa, gif replies: disabled ૮꒰ ˶- ༝ - ˶꒱ა ♡")
            elif message.author.id == general.galeID:
                await message.reply("Usage: &setgifreplies [true/false]")
            else:
                await message.reply("purr, you are NYAT using proper syntax! use: &setgifreplies [true/false] (˶˃ᆺ˂˶)")
        elif commandSections[0] == "&pingcheese":
            await message.channel.send(f"Hourly {general.chat_handle_from_id(421792271843721216)} ping!");
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

    await onmessage.fixEmbed(message);
    await onmessage.gifReply(message);

@bot.event
async def on_raw_reaction_add(rawReactionActionEvent: discord.RawReactionActionEvent) -> None:
    await onreaction.checkPinMessage(bot, rawReactionActionEvent)

#Begin
webserver.keep_alive()

if isinstance(token, str):
    bot.run(token, log_handler = handler)
