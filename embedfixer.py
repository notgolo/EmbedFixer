import re
import discord

EMBED_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(www\.twitter\.com|https://www\.twitter\.com|https://twitter\.com)"), "https://www.vxtwitter.com"),
    (re.compile(r"\b(www\.x\.com|https://www\.x\.com|https://x\.com)"), "https://www.vxtwitter.com"),

    (re.compile(r"\b(www\.reddit\.com|https://www\.reddit\.com|https://reddit\.com)"), "https://www.vxreddit.com"),
    (re.compile(r"\b(old\.reddit\.com|https://old\.reddit\.com)"), "https://www.vxreddit.com"),
    
    (re.compile(r"\b(www\.instagram\.com|https://www\.instagram\.com|https://instagram\.com)"), "https://www.kkinstagram.com"),
    (re.compile(r"\b(www\.tiktok\.com|https://www\.tiktok\.com|https://tiktok\.com)"), "https://www.tnktok.com"),
    (re.compile(r"\b(www\.bsky\.app|https://www\.bsky\.app|https://bsky\.app)"), "https://www.bskye.app"),
    (re.compile(r"\b(www\.threads\.com|https://www\.threads\.com|https://threads\.com)"), "https://www.vxthreads.com"),
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