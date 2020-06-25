import os
from flask import Flask, request
from . import sendquiz
from .. import db, Category, Question, Question_Category
from slack import WebClient
from .quizdisplay import QuizDisplay
import json

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
quiz_sent = {}
params = {}

@sendquiz.route("/actions",methods=['GET','POST'])
def parse_params():

    """
    This method gets called everytime User interacts with the Message Block Kit Components such as Button or Select Elements. Those choices are then stored here(sent through request body in POST), and upon clicking of Submit Button, provided all choices are made, control is then transferred to display_quiz function.
    """
    


    parsed_payload = json.loads(request.form["payload"])
    print(parsed_payload," is the parsed_payload")

    msg_ts = parsed_payload["container"]["message_ts"]
    msg_channel = parsed_payload["container"]["channel_id"]
    print(msg_ts," is msg_ts")
    print(msg_channel," is channel")
    print(quiz_sent," is quiz_sent")
    if msg_channel in quiz_sent and msg_ts in quiz_sent[msg_channel]:
        print("About to update message")
        prev_quiz_sent = quiz_sent[msg_channel][msg_ts]
        update_quiz(prev_quiz_sent)
        


    params["user_id"] = parsed_payload["user"]["id"]

    if parsed_payload["actions"][0]["type"] == "channels_select":
        print(parsed_payload["actions"][0]["type"]," is CHANNEL")
        params["channel"] = parsed_payload["actions"][0]["selected_channel"]

    elif parsed_payload["actions"][0]["type"] == "static_select":
        if parsed_payload["actions"][0]["placeholder"]["text"] == 'Select time':
            print(parsed_payload["actions"][0]["selected_option"]["value"]," is Time Limit ")
            params["time_limit"] = parsed_payload["actions"][0]["selected_option"]["value"]

        elif parsed_payload["actions"][0]["placeholder"]["text"] == 'Select a Category':
            print(parsed_payload["actions"][0]["selected_option"]["value"]," is Category ")
            params["category"] = parsed_payload["actions"][0]["selected_option"]["value"]

    elif parsed_payload["actions"][0]["value"] == "SUBMITBTN":
        print(params["channel"]," is channel")
        print(params["time_limit"]," is time_limit")
        print(params["category"]," category")
        if params["channel"] != "" and params["time_limit"] != "" and params["category"] != "":
            print("Calling display_quiz()")
            display_quiz(params["user_id"], params["channel"], params["time_limit"], params["category"])


    print("HELLO in CAPSLOC\n\n\n\n\n")
    return {"message":"hello"}



def display_quiz(user_id: str, channel: str, time_limit: str, category: str):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.

    raw_data = db.engine.execute('SELECT qq.question, qq.option1, qq.option2, qq.option3, qq.option4, qq.answer FROM question as qq JOIN question_category as qc ON qq.id = qc.question_id JOIN category as cc ON qc.category_id = cc.id WHERE cc.name="%s";'%(category))
    
    first_row = []
    for row in raw_data:
        first_row = row     
    print(first_row," is raw_data[0]")

    quiz_display = QuizDisplay(channel)

    quiz_display.init_message(first_row[0],first_row[1],first_row[2],first_row[3],first_row[4],first_row[5])

    # Get the onboarding message payload
    message = quiz_display.get_message_payload()
    

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    quiz_display.timestamp = response["ts"]
    print("----------------------",quiz_display.get_message_payload(),"----------------- is the message")
    # Store the message sent in quiz_sent
    if channel not in quiz_sent:
        quiz_sent[channel] = {}
    quiz_sent[channel][quiz_display.timestamp] = quiz_display

    print(quiz_sent," ARE THE QUIZ SENT SO FAR")


def update_quiz(prev_quiz_sent):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.

    
    # Get the onboarding message payload
    message = prev_quiz_sent.get_message_payload()
    prev_quiz_sent.inform_user()
    print("++++++++++",message,"+++++++++++")
    # Post the onboarding message in Slack
    response = slack_web_client.chat_update(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    """
    quiz_display.timestamp = response["ts"]
    print("----------------------",quiz_display.get_message_payload(),"----------------- is the message")
    # Store the message sent in quiz_sent
    if channel not in quiz_sent:
        quiz_sent[channel] = {}
    quiz_sent[channel][quiz_display.timestamp] = quiz_display

    print(quiz_sent," ARE THE QUIZ SENT SO FAR")
    """
