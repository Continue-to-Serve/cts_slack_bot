#!/usr/bin/env python3

import os
import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
#from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.adapter.socket_mode import SocketModeHandler


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
    print("mention command")
    say("Hi there!")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
