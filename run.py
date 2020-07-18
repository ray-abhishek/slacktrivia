import os
import logging
from flask import Flask, request
from app import create_app
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from app.slash.quizcreation import quizCreation
from app.models import db, Category, Question, Question_Category
import ssl as ssl_lib
import certifi
from greetings import Greetings
import json
from app.sendresult.function import getResult

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
config_name = 'development'
app = create_app(config_name)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# For simplicity we'll store our app data in-memory with the following data structure.
# quiz_sent = {"channel": {"user_id": OnboardingTutorial}}
#quiz_sent = {}
onboarding_tutorials_sent = {}


user_details={}

@slack_events_adapter.on("app_home_opened")
def welcomeMessage(payload):

    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    timestamp=event.get("event_ts")
    status=user_details.get((channel_id,user_id),None)

    if status == None:
        greeting=Greetings(channel_id)
        message=greeting.get_message_payload()
        user_details[(channel_id,user_id)]=timestamp
        return slack_web_client.chat_postMessage(**message)
    
    else:
        diff = float(timestamp)-float(status)
        if diff >= 15:
            greeting=Greetings(channel_id)
            message=greeting.get_message_payload()
            user_details[(channel_id,user_id)]=timestamp
            return slack_web_client.chat_postMessage(**message)
        else:
            pass            



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)