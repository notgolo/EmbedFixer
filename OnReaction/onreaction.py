from pinning import *

from discord import Message

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