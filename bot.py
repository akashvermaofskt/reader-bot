import os
import time
from datetime import date, datetime
from dateutil import parser

import discord
from dotenv import load_dotenv
from localStoragePy import localStoragePy

localStorage = localStoragePy("reader_bot", "json")
current_time = datetime.now()
last_run = parser.parse(localStorage.getItem("last_run"))
seconds_passed_since_last_run = (current_time - last_run).total_seconds()
print("\n\n######")
print(f"Time now: {str(current_time)}")
print(f"Last Ran: {str(last_run)}")
print(f"Seconds passed since last run: {seconds_passed_since_last_run}")

if seconds_passed_since_last_run < 86400:
    print("24 hours didn't pass, quiting!")
    quit()
else:
    print("STARTING BOT!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")
READING_CHANNEL_ID = int(os.getenv("DISCORD_READING_CHANNEL"))
POSTED = False

client = discord.Client()
dir_name = "Books/Drive/PENDING"


def get_offset_index():
    list_of_files = list(
        filter(
            lambda x: os.path.isfile(os.path.join("Books/Drive/DONE/", x)),
            os.listdir("Books/Drive/DONE/"),
        )
    )
    return len(list_of_files)


def get_all_ss_to_post():
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(dir_name, x))
        and x[0] != "."
        and len(x) > 4
        and x[-4:] == ".jpg",
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
    if POSTED:
        print("Already posted for today, quiting!")
        quit()

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
    print("DONE Pages -> ", get_offset_index())
    files = get_all_ss_to_post()
    if len(files) != 0:
        print("Posting Begins!")
        today = date.today().strftime("%d/%m/%Y")
        await channel.send("###")
        await channel.send(f"""`{today}`""")
        await channel.send("###")
        offset_index = get_offset_index()
        for idx, file_name in enumerate(files[:5]):
            await channel.send(f"Page no. {offset_index+idx}")
            sent_message = await channel.send(
                file=discord.File(dir_name + "/" + file_name)
            )
            await sent_message.add_reaction("⭐")
            await channel.send("---------------")
            print(f"Posted {file_name}")
            os.rename(dir_name + "/" + file_name, "Books/Drive/DONE/" + file_name)
            print(f"Moved {file_name}")
    else:
        print("Nothing to post")

    localStorage.setItem("last_run", str(datetime.now()))
    print("All Done, quiting!")
    quit()


client.run(TOKEN)
