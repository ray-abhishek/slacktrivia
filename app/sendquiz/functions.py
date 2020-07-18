import os
from flask import Flask, request
from . import sendquiz
from .. import db, Category, Question, Question_Category, Quiz, Quiz_Question, Attempt
from slack import WebClient
from .quizdisplay import QuizDisplay
import json
from ..sendquizconfirmation.sendconfirmation import sendConfirmation
from ..sendresult.function import getResult
import sched
import time
import random
from multiprocessing import Process

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
quiz_sent = {}
params = {}
scheduler = sched.scheduler(time.time, time.sleep)

create_quiz={}

@sendquiz.route("/actions",methods=['GET','POST'])
def parse_params():

    """
    This method gets called everytime User interacts with the Message Block Kit Components such as Button or Select Elements. Those choices are then stored here(sent through request body in POST), and upon clicking of Submit Button, provided all choices are made, control is then transferred to display_quiz function.
    """

    parsed_payload = json.loads(request.form["payload"])
    print("____________________",parsed_payload,"____________ IS PARSED PAYLOAD")
    if parsed_payload.get("view","")!="":
         if parsed_payload["view"]["type"] == "modal" or parsed_payload["type"] == "view_submission":
        
            if parsed_payload["type"] == "block_actions":
                create_quiz[(parsed_payload["user"]["team_id"],parsed_payload["user"]["id"])] = {}

                create_quiz[(parsed_payload["user"]["team_id"],parsed_payload["user"]["id"])]["channel"] = parsed_payload["actions"][0]["selected_channel"]
                params["channel"] = parsed_payload["actions"][0]["selected_channel"]

                return {"message":"stored successful"}

            else:
                
                obj_key = (parsed_payload["user"]["team_id"],parsed_payload["user"]["id"])

                blocks = parsed_payload["view"]["blocks"]

                data = parsed_payload["view"]["state"]["values"]

                category = data[blocks[1]["block_id"]][blocks[1]["element"]["action_id"]]["selected_option"]["value"]

                time = data[blocks[-2]["block_id"]][blocks[-2]["element"]["action_id"]]["selected_option"]["value"]

                question = data[blocks[2]["block_id"]][blocks[2]["element"]["action_id"]]["value"]

                answer = data[blocks[3]["block_id"]][blocks[3]["element"]["action_id"]]["value"]

                option2 = data[blocks[4]["block_id"]][blocks[4]["element"]["action_id"]]["value"]

                option3 = data[blocks[5]["block_id"]][blocks[5]["element"]["action_id"]]["value"]

                option4 = data[blocks[6]["block_id"]][blocks[6]["element"]["action_id"]]["value"]
            
                hash1 = parsed_payload["view"]["hash"]

                if create_quiz.get(obj_key,None) == None:
                    block_id = blocks[-2]["block_id"]

                    return {
                        "response_action": "errors",
                        "errors": {
                            str(block_id): "Please Select a channel to post quiz"
                        }
                    }
            
                create_quiz[obj_key]["time_limit"] = time
                create_quiz[obj_key]["category"] = category
                create_quiz[obj_key]["question"] = question
                create_quiz[obj_key]["answer"] = answer
                create_quiz[obj_key]["option2"] = option2
                create_quiz[obj_key]["option3"] = option3
                create_quiz[obj_key]["option4"] = option4
                create_quiz[obj_key]["hash"] = hash1
                data = create_quiz[obj_key]
                

                params["quiz_timestamp"] = hash1
                params["user_id"] = parsed_payload["user"]["id"]
                params["time_limit"] = time

                quiz_id = update_quiz_db(params["channel"], params["user_id"], params["quiz_timestamp"])
                new_question_id = add_question_db(question,answer,option2,option3,option4,answer)
                add_question_category_mapping(new_question_id, create_quiz[obj_key]["category"])
                time_stamp = display_quiz(params["user_id"], params["channel"], params["time_limit"], new_question_id, quiz_id, True)
            
                #logic for scheduling the quiz
                time = params["time_limit"].split(" ")
                if time[1] == "min":
                    duration = int(time[0]) * 60
                else:
                    duration = int(time[0])

                db.session.remove()
                db.engine.dispose()
                def modal_schedule():
                    scheduler.enter(duration,1,update_custom_quiz_timeout,(params["channel"],time_stamp,quiz_id))
                    scheduler.enter(duration+4,1,getResult,(quiz_id,))
                    scheduler.run()
                
                p = Process(target=modal_schedule)
                p.start()

            return {"response_action": "clear"}



    params["user_id"] = parsed_payload["user"]["id"]

    msg_ts = parsed_payload["container"]["message_ts"]
    msg_channel = parsed_payload["container"]["channel_id"]

    if msg_channel in quiz_sent and msg_ts in quiz_sent[msg_channel]:
        #Store Attempts 
        #We need quiz's timestamp because based on that we'll fetch the Quiz ID and store it in Attempt Table.
        already_present = checkDuplicate(params["quiz_id"],params["user_id"]) 
        if already_present == False:
            track_attempts(params["quiz_timestamp"], params["user_id"], parsed_payload["actions"][0]["value"])
            prev_quiz_sent = quiz_sent[msg_channel][msg_ts]
            update_quiz(prev_quiz_sent,params["user_id"])
        
  

    if parsed_payload["actions"][0]["type"] == "channels_select":
        params["channel"] = parsed_payload["actions"][0]["selected_channel"]

    elif parsed_payload["actions"][0]["type"] == "static_select":
        if parsed_payload["actions"][0]["placeholder"]["text"] == 'Select time':
            params["time_limit"] = parsed_payload["actions"][0]["selected_option"]["value"]

        elif parsed_payload["actions"][0]["placeholder"]["text"] == 'Select a Category':
            params["category"] = parsed_payload["actions"][0]["selected_option"]["value"]

    elif parsed_payload["actions"][0]["value"] == "SUBMITBTN":

        if params["channel"] != "" and params["time_limit"] != "" and params["category"] != "":
            params["quiz_timestamp"] = msg_ts
            quiz_id = update_quiz_db(params["channel"], params["user_id"], msg_ts)
            time_stamp = display_quiz(params["user_id"], params["channel"], params["time_limit"], params["category"], quiz_id, False)
            sendConfirmation(parsed_payload["response_url"],params["channel"])
            
            #logic for scheduling the quiz
            time = params["time_limit"].split(" ")
            if time[1] == "min":
                duration = int(time[0]) * 60
            else:
                duration = int(time[0])

            scheduler.enter(duration,1,update_quiz_timeout,(params["channel"],time_stamp,))
            scheduler.enter(duration+4,1,getResult,(quiz_id,))
            scheduler.run()

    return {"message":"hello"}



def display_quiz(user_id: str, channel: str, time_limit: str, temp , quiz_id, custom):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.
    if custom == True:
        raw_data = db.engine.execute('SELECT qq.id, qq.question, qq.option1, qq.option2, qq.option3, qq.option4, qq.answer FROM question as qq JOIN question_category as qc ON qq.id = qc.question_id JOIN category as cc ON qc.category_id = cc.id WHERE qq.id=%s;'%(temp))
    else:
        raw_data = db.engine.execute('SELECT qq.id, qq.question, qq.option1, qq.option2, qq.option3, qq.option4, qq.answer FROM question as qq JOIN question_category as qc ON qq.id = qc.question_id JOIN category as cc ON qc.category_id = cc.id WHERE cc.name="%s" ORDER BY RAND() LIMIT 1;'%(temp))
    
    first_row = []
    for row in raw_data:
        first_row = list(row)     

    shuffled_options = randomize(list(first_row[2:6]),4)

    quiz_display = QuizDisplay(channel,user_id,time_limit)

    quiz_display.init_message(first_row[1],shuffled_options[0],shuffled_options[1],shuffled_options[2],shuffled_options[3],first_row[6])

    # Get the QuizDisplay message payload
    message = quiz_display.get_message_payload()

    # Post the QuizDisplay message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message/keep score after a user
    # has clicked on an button.
    quiz_display.timestamp = response["ts"]

    add_quiz_question_mapping(first_row[0],quiz_id,quiz_display.timestamp)

    # Store the message sent in quiz_sent
    if channel not in quiz_sent:
        quiz_sent[channel] = {}
    quiz_sent[channel][quiz_display.timestamp] = quiz_display

    return response["ts"]





def add_question_category_mapping(qstn_id, category_name):

    category = Category.query.filter(Category.name == category_name).first()
    new_mapping = Question_Category(question_id = qstn_id, category_id = category.id)
    db.session.add(new_mapping)
    db.session.commit() 


def update_quiz(prev_quiz_sent,userID):
    # This method fetches questions and options from database according to the parameters and using them create a new QuizDisplay Object.
    prev_quiz_sent.submitted.append(userID)
    # Get the QuizDisplay Message Payload
    message = prev_quiz_sent.get_updated_payload() 
    # Post the updated Message Payload to Slack
    response = slack_web_client.chat_update(**message)



def update_quiz_db(channel_quiz, author_quiz, timestamp_quiz):

    new_quiz = Quiz(channel_id = channel_quiz, author_id = author_quiz, timestamp = timestamp_quiz )

    db.session.add(new_quiz)
    db.session.commit()

    raw_data = Quiz.query.filter(Quiz.timestamp == timestamp_quiz).all()
    for row in raw_data:
        new_quiz_id = row

    params["quiz_id"] = new_quiz_id.id
    return new_quiz_id.id


def add_quiz_question_mapping(questionID, quizID, quiz_display_ts):

    #Mapping Question to Quiz
    new_quiz_question_mapping = Quiz_Question(quiz_id = quizID, question_id = questionID, timestamp = quiz_display_ts)

    db.session.add(new_quiz_question_mapping)
    db.session.commit()

def add_question_db(qstn, op1, op2, op3, op4, ans):

    #Adding Entity to Question
    new_question = Question(question = qstn, option1 = op1, option2 = op2, option3 = op3, option4 = op4, answer = ans )

    db.session.add(new_question)
    db.session.commit()

    raw_data = Question.query.filter(Question.question == qstn).all()
    for row in raw_data:
        new_question = row

    return new_question.id


def track_attempts(msg_timestamp, userID, option_value):

    existing_quiz = Quiz.query.filter(Quiz.timestamp == msg_timestamp).first()
    new_attempt = Attempt(quiz_id = existing_quiz.id, user_id = userID, answer = option_value )
    db.session.add(new_attempt)
    db.session.commit()


def checkDuplicate(quizID,userID):

    existing_attempt = Attempt.query.filter(Attempt.quiz_id == quizID).filter(Attempt.user_id == userID).first()

    if existing_attempt:
        return True 
    else:
        return False

def update_quiz_timeout(channel,timestamp):

    quiz_message = quiz_sent[channel][timestamp]
    message = quiz_message.get_timeout_payload()
    response = slack_web_client.chat_update(**message)



def update_custom_quiz_timeout(channel, timestamp, quiz_id):

    quiz_message = quiz_sent[channel][timestamp]

    raw_data = db.engine.execute('SELECT user_id FROM attempt WHERE quiz_id=%s;'%(quiz_id))

    for row in raw_data:
        quiz_message.submitted.append(str(row[0]))

    message = quiz_message.get_timeout_payload()
    response = slack_web_client.chat_update(**message)



def randomize(arr, n): 
    for i in range(n-1,0,-1):
        j = random.randint(0,i+1)
        if j>3:
            j=3 
        arr[i],arr[j] = arr[j],arr[i] 
    return arr