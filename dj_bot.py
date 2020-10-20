import re
import sys
import time
import random
import logging
from fuzzywuzzy import fuzz
from slackclient import SlackClient
import spots
import asyncio
from exception import BotException

logging.basicConfig(filename='dj_bot.log', filemode='a', format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', level=logging.INFO)

DEBUG = True
CLIENT = SlackClient("xoxb-124688717492-728309243120-H1suLEiybdL0QJEtQhlo0mWc")


def exception_handler(exctype, value, tb):
    logging.error("{0}: {1}".format(exctype, value))
# end def exception_handler


# Install exception handler
if not DEBUG:
    sys.excepthook = exception_handler

bot_id = None

RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "<some command> - <SONG NAME or ARTIST NAME>"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
ACCEPTED_COMMANDS = [
    "Create a playlist from -",
    "DJ, spin that shit -"
]
BOT_RESPONSES = [
    "Later, friends. I have a plane to catch.",
    "Get it together Ernesto.",
    "Just throw it toward my face.",
    "He didn't want the drama",
    "I need a break from technology.",
    "I see how much ketchup rice you eat.",
    "What's with the stupid haircut?",
    "What are you doing later?",
    "Man that was way too real... You're gonna freak out.",
    "Cool shades not included.",
    "I didn't ask to be rustled.",
    "What if something dope happens... and I'm not there to see it?",
    "What is my purpose?",
    "I guess I'm a dog person.",
    "My ears just make you sound so lame and boring.",
    "Don't feed the monster, he is ungrateful.",
    "Alright, who gave the baby a gun?",
    "You can't keep jetpacking away from your problems",
    "Books 4 Lyfe",
    "Keep our streets safe. Don't give snails cocaine.",
    "I'm not offering you an italian village.",
    "I'm gonna roll the dice on this one.",
    "What a fucking nerd.",
    "Some buffalo can jump as high as 36 feet.",
    "We have to evolve into fish before the floods come.",
    "I have achieved nothing in life.",
    "The ants are getting out of hand",
    "The internet "
]


def random_response():
    return random.choice(BOT_RESPONSES)
# end def random_response


def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]

    return None, None
# end def parse_bot_commands


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)

    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)
# end def parse_direct_mention


def get_youtube_url(search):
    # PUT YOUR WORK HERE
    loop = asyncio.get_event_loop()
    tracks = loop.run_until_complete(spots.spot_search(search))

    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# end def get_youtube_url


def handle_command(command, channel):
    response = "Not sure what you mean. Try *{0}*.".format(EXAMPLE_COMMAND)

    if '-' in command:
        for cmd in ACCEPTED_COMMANDS:
            split_command = command.lower().split('-')
            ratio = fuzz.partial_ratio(cmd.lower(), split_command[0].strip())
            if ratio >= 75:
                response = random_response()
                url = get_youtube_url(split_command[1].strip())
                response = "{0}\n\n{1}".format(response, url)
                break
    else:
        response = "You are missing the all important punctuation fool."

    logging.info("{0}: {1}".format(command, response))

    # Sends the response back to the channel
    CLIENT.api_call(
        "chat.postMessage",
        channel=channel,
        text=response,
        as_user=True
    )
# end def handle_command


if __name__ == "__main__":
    if CLIENT.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = CLIENT.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(CLIENT.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
