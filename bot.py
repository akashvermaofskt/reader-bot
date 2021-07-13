import os
import time
from datetime import date

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")
READING_CHANNEL_ID = int(os.getenv("DISCORD_READING_CHANNEL"))

client = discord.Client()
dir_name = "Books/Drive"


def get_offset_index():
    list_of_files = list(
        filter(
            lambda x: os.path.isfile(os.path.join("Books/Drive/OLD/", x)),
            os.listdir("Books/Drive/OLD/"),
        )
    )
    return len(list_of_files)


def get_all_ss_to_post():
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(dir_name, x))
        and x[0] != "."
        and len(x) > 4
        and x[-4:] == ".png",
        os.listdir(dir_name),
    )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(
        list_of_files, key=lambda x: os.path.getmtime(os.path.join(dir_name, x))
    )

    for file_name in list_of_files:
        file_path = os.path.join(dir_name, file_name)
        timestamp_str = time.strftime(
            "%m/%d/%Y :: %H:%M:%S", time.gmtime(os.path.getmtime(file_path))
        )
        print(timestamp_str, " -->", file_name)

    return list_of_files


@client.event
async def on_ready():
    print(client.guilds)
    for guild in client.guilds:
        if guild.name == GUILD:
            print(
                f"{client.user} is connected to the following guild:\n"
                f"{guild.name}(id: {guild.id})"
            )
            break

    channel = client.get_channel(READING_CHANNEL_ID)

    # sent_message = await channel.send("hello !!!")

    # await sent_message.add_reaction("⭐")

    # sent_message = await channel.send(file=discord.File("static/icon.jpeg"))
    # await sent_message.add_reaction("⭐")

    files = get_all_ss_to_post()
    if len(files) != 0:
        print("Posting Begins!")
        today = date.today().strftime("%d/%m/%Y")
        await channel.send("###")
        await channel.send(f"""`{today}`""")
        await channel.send("###")
        offset_index = get_offset_index()
        for idx, file_name in enumerate(files):
            await channel.send(f"Page no. {offset_index+idx}")
            sent_message = await channel.send(
                file=discord.File(dir_name + "/" + file_name)
            )
            await sent_message.add_reaction("⭐")
            await channel.send("---------------")
    else:
        print("Nothing to post")


client.run(TOKEN)
