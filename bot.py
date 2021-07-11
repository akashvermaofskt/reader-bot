import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
READING_CHANNEL_ID = int(os.getenv("DISCORD_READING_CHANNEL"))

client = discord.Client()


@client.event
async def on_ready():
    print(client.guilds)
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    channel = client.get_channel(READING_CHANNEL_ID)

    sent_message = await channel.send("hello !!!")
    emoji = "\N{THUMBS UP SIGN}"
    await sent_message.add_reaction(emoji)


client.run(TOKEN)
