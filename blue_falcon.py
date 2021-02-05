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

conf_filename = "config.toml"

# Install the Slack app and get xoxb- token in advance
app = App(
    token=os.environ["SLACK_OAUTH"]
)

def load_welcome_config():
    """ loads the welcome message and channel from config.toml"""
    with open(conf_filename, 'r') as conf_file:
        config = tomlkit.loads(conf_file.read())
    return config["welcome"]


@app.command("/test-greet")
@app.event("team_join")
def greeter(ack, say, body, event):
    """
    Welcomes users when they first join the slack
    """
    # Needed for the slash command
    ack()

    # Slash Command and team_join events store user_id differently
    try:
        user_id = body["user_id"]
    except KeyError:
        user_id = event["user"]["id"]

    channel_id = welcome_config["channel"]

    replacement_dict = {'user_id' : user_id, 'channel_id' : channel_id}

    message_public = welcome_config["header"].format(**replacement_dict)
    message_reply = welcome_config["fold"].format(**replacement_dict)

    thread_ts = say(text=message_public, channel=channel_id)["ts"]
    say(text=message_reply, channel=channel_id, thread_ts=thread_ts)


welcome_config = load_welcome_config()
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).connect()

    app.client.conversations_join(channel=welcome_config["channel"])
    app.start()
