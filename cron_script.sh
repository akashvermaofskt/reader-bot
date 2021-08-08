#!/bin/bash
cd /home/ubuntu/reader-bot
source reader_bot_env/bin/activate
python3 bot.py >> cron_runtime.log