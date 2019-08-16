#!/bin/bash

until python dj_bot.py; do
    echo "'dj_bot.py' crashed with exit code $?. Restarting in 5 seconds." >&2
    sleep 5
done