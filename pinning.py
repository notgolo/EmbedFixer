import discord
from discord.ext import commands
from discord import Guild, TextChannel, Message, Emoji
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
    debugMessage: str = f"{len(pinMessage.reactions)}   ";

    pushpins: int = 0
    for reaction in pinMessage.reactions:
        if reaction.emoji is not Emoji:
            continue
        
        debugMessage = f"{debugMessage}, {reaction.emoji.id}";

        if reaction.emoji.name is None or reaction.emoji.name != "pushpin":
            continue

        pushpins = reaction.count
        break

    if commandMessage is not None:
        await commandMessage.reply(f"Found emoji IDs: {debugMessage}");

    if pushpins > 3:
        await pinMessage.pin(reason = "Pinned via bot vote.")
    else:
        await pinMessage.reply("Failed to pin");

async def checkPinMessage(bot: commands.Bot, payload: discord.RawReactionActionEvent) -> None:
    if payload.emoji != "📌":
        return None;

    message: Message | None = await get_message(bot, payload);
    if message is None:
        return None
    
    pushpins: int = 0
    for reaction in message.reactions:
        if reaction.emoji != "📌":
            continue

        pushpins = reaction.count
        break

    if pushpins > 3:
        await message.pin(reason = "Pinned via bot vote.")