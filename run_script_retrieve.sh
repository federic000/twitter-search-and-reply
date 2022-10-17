#!/bin/bash
#shell script runs the bot from crontab, edit home-dir accordingly...
HOMEDIR=/home/user/twitter-bot
cd "$HOMEDIR"
./tweet_retrieve.py

