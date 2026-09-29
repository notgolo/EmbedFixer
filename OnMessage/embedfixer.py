import re
import discord

EMBED_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?<!vx)(?<!fx)(?:www\.)?(?:twitter|x)\.com"), "www.vxtwitter.com"),
    (re.compile(r"(?<!kk)(?<!dd)(?:www\.)?instagram\.com"), "www.kkinstagram.com"),
    (re.compile(r"(?:www\.)?tiktok\.com"), "www.tnktok.com"),
    (re.compile(r"(?<!vx)(?:(?:www\.)?old\.)?(?:www\.)?(?:reddit)\.com"), "www.vxreddit.com"),
    (re.compile(r"(?:www\.)?bsky\.app"), "bskye.app"),
    (re.compile(r"(?:www\.)?threads\.com"), "www.vxthreads.com"),
]

async def fixEmbed(message: discord.Message) -> None:
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