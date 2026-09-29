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
from discord import permissions, Message, Intents
from discord.ext.commands import Bot

#local imports
import webserver
import general
import embedfixer 
import gifreply
import pinning

version: int = 2

load_dotenv()
token: str | None = os.getenv("DISCORD_TOKEN")

handler: FileHandler = FileHandler(filename = "discord.log", encoding = "utf-8", mode = "w")

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True

bot: Bot = Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_message(message: Message) -> None:
    global version

    if message.author.bot:
        return

    command: str = message.content.strip().lower()
    if len(command) > 0 and command[0] == '&':
        command = re.sub(r" {2,}", " ", command) #set all remaining whitespace to one whitespace/remove all double spaces
        commandSections: list[str] = command.split(" ")

        if commandSections[0] == "&version":
            if not general.isAdmin(message.author.id):
                return

            await message.reply(f"Current Version is {version}.")
        elif commandSections[0] == "&pin" and len(commandSections) > 1:
            if message.author.id != general.galeID:
                await message.reply("Your mother has hairy toes")
                return

            if message.reference is None:
                await message.reply("Reply to message you want to pin dumbass")
                return
            
            if message.reference.message_id is None:
                await message.reply("I don't know why your command did't work")
                return
                
            pinMessage: Message = await message.channel.fetch_message(message.reference.message_id)

            if commandSections[1] == "check":
                await pinning.checkPin(message, pinMessage)
            elif commandSections[0] == "remove":
                await pinMessage.unpin()
        elif commandSections[0] == "&setgifreplies" and  len(commandSections) > 1:
            if general.isAdmin(message.author.id) == False:
                if message.author.id == general.lintyID:
                    await message.reply("stfu")
                else:
                    await message.reply("you do NYAT have perms for dat! ^. .^₎⟆")
                return

            enabled: str = commandSections[1].lower()
            if enabled == "true":
                gifreply.setGIFReplies(True)
                if message.author.id == general.galeID:
                    await message.reply("Gif replies enabled")
                else:
                    await message.reply("gif replies: enabled, nyaa (⸝⸝⸝O﹏ O⸝⸝⸝)")
            elif enabled == "false":
                gifreply.setGIFReplies(False)
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

        return

    await embedfixer.fixEmbed(message);
    await gifreply.gifReply(message);

@bot.event
async def on_raw_reaction_add(rawReactionActionEvent: discord.RawReactionActionEvent) -> None:
    await pinning.checkPinMessage(bot, rawReactionActionEvent)

#Begin
webserver.keep_alive()

if isinstance(token, str):
    bot.run(token, log_handler = handler)
