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

async def checkPin( pinMessage: Message) -> None:
    debugMessage: str = "";
    
    pushpins: int = 0
    for reaction in pinMessage.reactions:
        if not isinstance(reaction.emoji, str):
            continue

        if str(reaction.emoji) != "📌":
            continue

        pushpins = reaction.count
        break

    if pushpins > 3:
        await pinMessage.pin(reason = "Pinned via bot vote.")

async def checkPinMessage(bot: commands.Bot, payload: discord.RawReactionActionEvent) -> None:
    if str(payload.emoji) != "📌":
        return None;

    message: Message | None = await get_message(bot, payload);
    if message is None:
        return None
    
    await checkPin(message)
