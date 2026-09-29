import discord
from discord.ext import commands
from discord import Guild, TextChannel, Message, Emoji, PartialEmoji
from discord.abc import GuildChannel

async def get_message(bot: commands.Bot, payload: discord.RawReactionActionEvent) -> Message | None:
    if payload.guild_id is None:
        return None

    guild: Guild | None = bot.get_guild(payload.guild_id)
    if guild is None:
        return None

    channel: GuildChannel | None = guild.get_channel(payload.channel_id)
    if channel is None or not isinstance(channel, TextChannel):
        return None

    return await channel.fetch_message(payload.message_id)

async def checkPin(commandMessage: Message | None, pinMessage: Message) -> None:
    debugMessage: str = "";
    
    pushpins: int = 0
    for reaction in pinMessage.reactions:
        if not isinstance(reaction.emoji, str):
            continue

        if reaction.emoji != "📌":
            debugMessage += f"''NOT FOUND '{reaction.emoji}''"
            continue

        debugMessage += f"''FOUND '{reaction.emoji}''"
        pushpins = reaction.count
        break

    if pushpins > 3:
        await pinMessage.pin(reason = "Pinned via bot vote.")
    elif commandMessage is not None:
        await commandMessage.reply(f"Failed {debugMessage}");

async def checkPinMessage(bot: commands.Bot, payload: discord.RawReactionActionEvent) -> None:
    if payload.emoji != "📌":
        return None;

    message: Message | None = await get_message(bot, payload);
    if message is None:
        return None
    
    await checkPin(None, message)
