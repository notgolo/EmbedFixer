import re

import discord

gifRepliesEnabled: bool = False

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

def setGIFReplies(state: bool) -> None:
    gifRepliesEnabled = state

async def gifReply(message: discord.Message) -> None:        
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