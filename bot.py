import os
import time
from datetime import date, datetime
from dateutil import parser

import discord
from dotenv import load_dotenv
from localStoragePy import localStoragePy
from pdf_utils import get_page_groups

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_SERVER")
READING_CHANNEL_ID = int(os.getenv("DISCORD_READING_CHANNEL"))
BOOK_NAME = os.getenv("BOOK_NAME")
BOOK_START_PAGE = int(os.getenv("BOOK_START_PAGE"))
READING_SPEED_WPM = int(os.getenv("READING_SPEED_WPM"))
READING_TIME_IN_MINS = int(os.getenv("READING_TIME_IN_MINS"))
MASTER_FLAG = False


client = discord.Client()
localStorage = localStoragePy("reader_bot", "json")


def ensure_run():
    current_time = datetime.now()
    last_run = parser.parse(localStorage.getItem("last_run"))
    seconds_passed_since_last_run = (current_time - last_run).total_seconds()
    print("\n\n######")
    print(f"Time now: {str(current_time)}")
    print(f"Last Ran: {str(last_run)}")
    print(f"Seconds passed since last run: {seconds_passed_since_last_run}")

    if seconds_passed_since_last_run < 86400:
        return False
    else:
        return True


def get_offset_index():
    list_of_files = list(
        filter(
            lambda x: os.path.isfile(os.path.join(f"Books/{BOOK_NAME}/DONE/", x)),
            os.listdir(f"Books/{BOOK_NAME}/DONE/"),
        )
    )
    return len(list_of_files)


def get_all_ss_to_post_time_based_fixed():
    ss_dir_name = f"Books/{BOOK_NAME}/PENDING"
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(ss_dir_name, x))
        and x[0] != "."
        and len(x) > 4
        and x[-4:] == ".jpg",
        os.listdir(ss_dir_name),
    )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(
        list_of_files, key=lambda x: os.path.getmtime(os.path.join(ss_dir_name, x))
    )

    for file_name in list_of_files:
        file_path = os.path.join(ss_dir_name, file_name)
        timestamp_str = time.strftime(
            "%m/%d/%Y :: %H:%M:%S", time.gmtime(os.path.getmtime(file_path))
        )
        print(timestamp_str, " -->", file_name)

    return list_of_files[:5]


def get_all_ss_to_post_page_group_based():
    ss_dir_name = f"Books/{BOOK_NAME}/PENDING"
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(ss_dir_name, x))
        and x[0] != "."
        and len(x) > 4
        and x[-4:] == ".jpg",
        os.listdir(ss_dir_name),
    )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(
        list_of_files, key=lambda x: os.path.getmtime(os.path.join(ss_dir_name, x))
    )
    page_groups = get_page_groups(
        BOOK_NAME, BOOK_START_PAGE, READING_SPEED_WPM, READING_TIME_IN_MINS
    )

    starting_page = int(list_of_files[0].split(".")[0])
    current_page_group = []
    for page_group in page_groups:
        if starting_page in page_group:
            current_page_group.extend(page_group)
            break

    return [
        file_name
        for file_name in list_of_files
        if int(file_name.split(".")[0]) in current_page_group
    ]


@client.event
async def on_ready():
    if MASTER_FLAG is False:
        print("Master Flag is False, quiting!")
        quit()

    channel = client.get_channel(READING_CHANNEL_ID)
    ss_dir_name = f"Books/{BOOK_NAME}/PENDING"

    print("DONE Pages -> ", get_offset_index())
    files = get_all_ss_to_post_page_group_based()
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
                file=discord.File(ss_dir_name + "/" + file_name)
            )
            await sent_message.add_reaction("⭐")
            await channel.send("---------------")
            print(f"Posted {file_name}")
            os.rename(
                ss_dir_name + "/" + file_name, f"Books/{BOOK_NAME}/DONE/" + file_name
            )
            print(f"Moved {file_name}")
        await channel.send("<@&863534266843660288>")
    else:
        print("Nothing to post")

    localStorage.setItem("last_run", str(datetime.now()))
    print("All Done, quiting!")
    quit()


def main():
    bot_run_pending = ensure_run()
    if bot_run_pending:
        client.run(TOKEN)
    else:
        print("Bot not supposed to run")
        quit()


if __name__ == "__main__":
    main()
