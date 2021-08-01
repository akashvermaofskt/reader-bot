import os
import discord
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")
WORD_CHAIN_CHANNEL_ID = int(os.getenv("DISCORD_WORD_CHAIN_CHANNEL"))


client = discord.Client()


@client.event
async def on_ready():
    data = pd.DataFrame(columns=["author", "username", "content", "time"])
    channel = client.get_channel(WORD_CHAIN_CHANNEL_ID)
    limit = 10000
    async for msg in channel.history(limit=limit):
        if (
            not (len(msg.content) >= 3 and msg.content[:3] == "xw!")
            and not (len(msg.content) > 0 and msg.content[0] == ".")
            and not len(msg.content) == 0
            and not msg.author.name == "XerWord"
        ):
            # print(type(msg.author))
            data = data.append(
                {
                    "content": msg.content,
                    "time": msg.created_at,
                    "author": msg.author.display_name,
                    "username": msg.author.name,
                },
                ignore_index=True,
            )

        if len(data) == limit:
            break

    file_location = (
        "data.csv"  # Set the string to where you want the file to be saved to
    )
    data.to_csv(file_location)
    print("Done!")


client.run(TOKEN)
