import os
from flask import Flask, request
from . import sendquiz
from .. import db, Category, Question, Question_Category, Quiz, Quiz_Question, Attempt
from slack import WebClient
from .quizdisplay import QuizDisplay
import json
from ..sendquizconfirmation.sendconfirmation import sendConfirmation

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

    params["user_id"] = parsed_payload["user"]["id"]

    msg_ts = parsed_payload["container"]["message_ts"]
    msg_channel = parsed_payload["container"]["channel_id"]
    print(msg_ts," is msg_ts")
    print(msg_channel," is channel")
    print(quiz_sent," is quiz_sent")
    if msg_channel in quiz_sent and msg_ts in quiz_sent[msg_channel]:
        #Store Attempts 
        #We need quiz's timestamp because based on that we'll fetch the Quiz ID and store it in Attemp Table.
        already_present = checkDuplicate(params["quiz_id"],params["user_id"]) 
        if already_present == False:
            track_attempts(params["quiz_timestamp"], params["user_id"], parsed_payload["actions"][0]["value"])
            prev_quiz_sent = quiz_sent[msg_channel][msg_ts]
            update_quiz(prev_quiz_sent,params["user_id"])
        
  

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
            params["quiz_timestamp"] = msg_ts
            print("Calling display_quiz()")
            quiz_id = update_quiz_db(params["channel"], params["user_id"], msg_ts)
            display_quiz(params["user_id"], params["channel"], params["time_limit"], params["category"], quiz_id)
            sendConfirmation(parsed_payload["response_url"],params["channel"])


    print("HELLO in CAPSLOC\n\n\n\n\n")
    return {"message":"hello"}



def display_quiz(user_id: str, channel: str, time_limit: str, category: str, quiz_id):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.

    raw_data = db.engine.execute('SELECT qq.id, qq.question, qq.option1, qq.option2, qq.option3, qq.option4, qq.answer FROM question as qq JOIN question_category as qc ON qq.id = qc.question_id JOIN category as cc ON qc.category_id = cc.id WHERE cc.name="%s";'%(category))
    
    first_row = []
    for row in raw_data:
        first_row = row     
    print(first_row," is raw_data[0]")


    quiz_display = QuizDisplay(channel)

    quiz_display.init_message(first_row[1],first_row[2],first_row[3],first_row[4],first_row[5],first_row[6])

    # Get the QuizDisplay message payload
    message = quiz_display.get_message_payload()
    

    # Post the QuizDisplay message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message/keep score after a user
    # has clicked on an button.
    quiz_display.timestamp = response["ts"]

    add_quiz_question_mapping(first_row[0],quiz_id,quiz_display.timestamp)

    print("----------------------",quiz_display.get_message_payload(),"----------------- is the message")

    # Store the message sent in quiz_sent
    if channel not in quiz_sent:
        quiz_sent[channel] = {}
    quiz_sent[channel][quiz_display.timestamp] = quiz_display

    print(quiz_sent," ARE THE QUIZ SENT SO FAR")


def update_quiz(prev_quiz_sent,userID):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.
    print(userID," userID to be Appended after Submission.")
    prev_quiz_sent.submitted.append(userID)
    # Get the onboarding message payload
    message = prev_quiz_sent.get_updated_payload()
    #prev_quiz_sent.inform_user() # Issue : Object is not getting modified. 
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


def update_quiz_db(channel_quiz, author_quiz, timestamp_quiz):

    print("Adding Entity to Quiz")
    print("Adding TimeStamp %s to Quiz"%(timestamp_quiz))
    new_quiz = Quiz(channel_id = channel_quiz, author_id = author_quiz, timestamp = timestamp_quiz )

    db.session.add(new_quiz)
    db.session.commit()

    raw_data = Quiz.query.filter(Quiz.timestamp == timestamp_quiz).all()
    #print(raw_data[0]," is raw_data in quiz")
    for row in raw_data:
        new_quiz_id = row

    print(new_quiz_id.id," is the new quiz id")
    params["quiz_id"] = new_quiz_id.id
    return new_quiz_id.id


def add_quiz_question_mapping(questionID, quizID, quiz_display_ts):

    print("Mapping Question to Quiz")
    new_quiz_question_mapping = Quiz_Question(quiz_id = quizID, question_id = questionID, timestamp = quiz_display_ts)

    db.session.add(new_quiz_question_mapping)
    db.session.commit()



def track_attempts(msg_timestamp, userID, option_value):

    print("TRACKING ATTEMPTS")
    existing_quiz = Quiz.query.filter(Quiz.timestamp == msg_timestamp).first()
    print("EXISTING QUIZ ID ------> ",existing_quiz.id,"-------")
    new_attempt = Attempt(quiz_id = existing_quiz.id, user_id = userID, answer = option_value )

    db.session.add(new_attempt)
    db.session.commit()


def checkDuplicate(quizID,userID):

    print(quizID," is quizID\n",userID,"is userID\n")

    existing_attempt = Attempt.query.filter(Attempt.quiz_id == quizID).filter(Attempt.user_id == userID).first()

    print(existing_attempt," is the existing attempt")

    if existing_attempt:
        return True 
    else:
        return False 