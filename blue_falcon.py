#!/usr/bin/env python3
"""
A Slack bot using the slack bot api and socket mode
credentials are loaded from environment variables

welcome message / welcome channel are stored in TOML
"""

import os
import logging
import tomlkit

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#conf_file =

# Install the Slack app and get xoxb- token in advance
app = App(
    token=os.environ["SLACK_OAUTH"]
)

@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")

@app.message("test")
@app.event("app_mention")
def event_test(say):
    say("Hi there!")


@app.command("/test-greet")
@app.event("team_join")
def greeter(ack, say, body, event):
    """
    Welcomes users when they first join the slack
    """
    # Needed for the slash command
    ack()

    # Slash Command and team_join events are formatted differently
    try:
        user_id = body["user_id"]
    except KeyError:
        user_id = event["user"]["id"]
    # Fixed Channel ID
    #channel_id = "C0195S27CP5"
    channel_id = "G01K8MJ7TP1"

    message_public = f"Give a warm welcome to <#{channel_id}> <@{user_id}>!"
    message_reply = (f"Welcome to the team, <@{user_id}>! please reply here with your name, branch of service, the state you're from, and anything else about you! It's good to have you here :relaxed:"
                     "\nPlease be sure to add yourself to other channels! If you need assistance, view the message pinned to this one, at the top.")

    thread_ts = say(text=message_public, channel=channel_id)["ts"]
    say(text=message_reply, channel=channel_id, thread_ts=thread_ts)



if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
