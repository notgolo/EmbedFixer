import discord
from discord.ext import commands
from discord import Guild, TextChannel, Message
from discord.abc import GuildChannel

import onreaction

async def checkPinMessage(bot: commands.Bot, payload: discord.RawReactionActionEvent) -> None:
    if payload.emoji != "📌":
        return None;

    message: Message | None = await onreaction.get_message(bot, payload);
    if message is None:
        return None
    
    pushpins = next((r.count for r in message.reactions if str(r.emoji) == "📌"), 0)

    pushpins: int = 0
    for reaction in message.reactions:
        if reaction.emoji != "📌":
            continue

        pushpins = reaction.count
        break

    if pushpins > 3:
        await message.pin(reason = "Pinned via bot vote.")