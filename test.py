#!/usr/bin/env python3
# my member id: U0196V8A137
# aron id: U01J9PT39K3
import logging
logging.basicConfig(level=logging.DEBUG)

from slack import WebClient
import os
from slack.errors import SlackApiError

slack_token = os.environ["SLACK_OAUTH"]
client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel='U01J9PT39K3',
        text="Testing the app! :tada:"
    )
except SlackApiError as e:
    assert e.response["error"]
