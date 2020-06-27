import os
import logging
from flask import Flask, request
from app import create_app
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from app.slash.quizcreation import quizCreation
from app.models import db, Category, Question, Question_Category
#from quizdisplay import QuizDisplay
import ssl as ssl_lib
import certifi
from greetings import Greetings
import json
from app.sendresult.function import getResult

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
config_name = 'development'
app = create_app(config_name)
#app = Flask(__name__)   --> This is now done inside the above create_app method. 
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# For simplicity we'll store our app data in-memory with the following data structure.
# quiz_sent = {"channel": {"user_id": OnboardingTutorial}}
#quiz_sent = {}
onboarding_tutorials_sent = {}

"""
def start_onboarding(user_id: str, channel: str, category_list: list):
    # Create a new quizCreation.
    onboarding_tutorial = quizCreation(channel, category_list)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial



# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):

    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    category_list = []
    raw_data = Category.query.with_entities(Category.name)
    for row in raw_data:
        print(row[0],' is row')
        category_list.append(row[0])

    print(category_list," ARE CATEGORIES")
    if text and text.lower() == "start":
        return start_onboarding(user_id, channel_id, category_list)
"""


user_details={}

@slack_events_adapter.on("app_home_opened")
def welcomeMessage(payload):

    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    timestamp=event.get("event_ts")
        
    status=user_details.get((channel_id,user_id),None)
    #getResult(16)
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