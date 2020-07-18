import requests
import json
from .factpayload import factPayload
from slack import WebClient
import os

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def facts(user_info):
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    data = data.json()
    message_payload = factPayload(user_info["channel_id"], data["text"])
    message = message_payload.get_message_payload()
    response = slack_web_client.chat_postMessage(**message)
