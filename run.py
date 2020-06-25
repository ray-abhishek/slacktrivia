import os
import logging
from flask import Flask, request
from app import create_app
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from quizcreation import quizCreation
from quizdisplay import QuizDisplay
import ssl as ssl_lib
import certifi
import json

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
params = {}

@app.route("/actions",methods=['GET','POST'])
def parse_params():

    """
    This method gets called everytime User interacts with the Message Block Kit Components such as Button or Select Elements. Those choices are then stored here(sent through request body in POST), and upon clicking of Submit Button, provided all choices are made, control is then transferred to display_quiz function.
    """
    
    parsed_payload = json.loads(request.form["payload"])
    print(parsed_payload," is the parsed_payload")


    if parsed_payload["actions"][0]["type"] == "channels_select":
        #print(parsed_payload["actions"][0]["type"]," is CHANNEL")
        params["channel"] = parsed_payload["actions"][0]["selected_channel"]

    elif parsed_payload["actions"][0]["type"] == "static_select":
        if parsed_payload["actions"][0]["placeholder"]["text"] == 'Select time':
            #print(parsed_payload["actions"][0]["selected_option"]["value"]," is Time Limit ")
            params["time_limit"] = parsed_payload["actions"][0]["selected_option"]["value"]

        elif parsed_payload["actions"][0]["placeholder"]["text"] == 'Select a Category':
            #print(parsed_payload["actions"][0]["selected_option"]["value"]," is Category ")
            params["category"] = parsed_payload["actions"][0]["selected_option"]["value"]

    elif parsed_payload["actions"][0]["value"] == "SUBMITBTN":
        print(params["channel"]," is channel")
        print(params["time_limit"]," is time_limit")
        print(params["category"]," category")
        if params["channel"] != "" and params["time_limit"] != "" and params["category"] != "":
            print("Calling display_quiz()")
            display_quiz(params["channel"], params["time_limit"], params["category"])


    print("HELLO in CAPSLOC\n\n\n\n\n")
    return {"message":"hello"}

def display_quiz(channel: str, time_limit: str, category: str):
    # Create a new QuizDisplay Object.

    quiz_display = QuizDisplay(channel)
    quiz_display.init_message("How many Moons does Saturn have?",4,164,29,57)
    # Get the onboarding message payload
    message = quiz_display.get_message_payload()
    
    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    quiz_display.timestamp = response["ts"]
    """
    # Store the message sent in quiz_sent
    if channel not in quiz_sent:
        quiz_sent[channel] = {}
    quiz_sent[channel][user_id] = quiz_display
    """

def start_onboarding(user_id: str, channel: str):
    # Create a new quizCreation.
    onboarding_tutorial = quizCreation(channel)

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

"""
# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack_events_adapter.on("team_join")
def onboarding_message(payload):

    event = payload.get("event", {})

    # Get the id of the Slack user associated with the incoming event
    user_id = event.get("user", {}).get("id")

    # Open a DM with the new user.
    response = slack_web_client.im_open(user=user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    start_onboarding(user_id, channel)


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack_events_adapter.on("reaction_added")
def update_emoji(payload):

    event = payload.get("event", {})

    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")

    if channel_id not in onboarding_tutorials_sent:
        return

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = slack_web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]


# =============== Pin Added Events ================ #
# When a users pins a message the type of the event will be 'pin_added'.
# Here we'll link the update_pin callback to the 'reaction_added' event.
@slack_events_adapter.on("pin_added")
def update_pin(payload):

    event = payload.get("event", {})

    channel_id = event.get("channel_id")
    user_id = event.get("user")

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the pin task as completed.
    onboarding_tutorial.pin_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = slack_web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]
"""

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and text.lower() == "start":
        return start_onboarding(user_id, channel_id)



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)