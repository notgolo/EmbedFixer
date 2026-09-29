import discord

galeID: int = 221075470437842944
goloID: int = 424304430184398849
lintyID: int = 272210308846583808
adminIDs: list[int] = [galeID, goloID]

def isAdmin(userID: int) -> bool:
    return userID in adminIDs;

def parse_member_id(guild: discord.Guild | None, possibleID: str | None) -> int | None:
    if guild is None or possibleID is None:
        return None
    
    possibleID = possibleID.strip();
    try:
        if possibleID.startswith("<@") and possibleID.endswith(">"):
            userID: int = int(possibleID[2:len(possibleID) - 1])
            if guild_has_member(guild, userID):
                return None
            return userID
    except ValueError:
        return None

    return None

def chat_handle_from_id(handle: int | None) -> str:
    return f"<@{handle}>"

def guild_has_member(guild: discord.Guild, userID: int) -> bool:
    return get_member(guild, userID) is not None
def get_member(guild: discord.Guild | None, userID: int | None) -> discord.Member | None:
    if guild is None or userID is None:
        return None

    return guild.get_member(userID)