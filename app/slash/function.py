from . import slash
from flask import  request
import  json
from .quizcreation import quizCreation
from .quizwiki import quizWiki
from .quizcustomdisplay import quizCustomDisplay
from ..models import db, Category, Question, Question_Category
from slack import WebClient
import os


slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

@slash.route("/quiz",methods=["POST"])
def createQuiz():
    
    category_list = []
    raw_data = Category.query.with_entities(Category.name)
    for row in raw_data:
        category_list.append(row[0])

    data=dict(request.form)

    if data["command"] == "/quiz" and data["text"] == "help":
        #responding with wiki/help/description of quizbot
        quiz_wiki = quizWiki(data["channel_id"])

        quiz_wiki_message = quiz_wiki.get_message_payload()

        return quiz_wiki_message

    if data["command"] == "/quiz" and data["text"] == "start":
        quiz_message=quizCreation(data["channel_id"],category_list)

        message = quiz_message.get_message_payload()
        return message

    if data["command"] == "/quiz" and data["text"] == "create":

        trigger_id = data["trigger_id"]

        quiz_modal = quizCustomDisplay(trigger_id , category_list)

        message = quiz_modal.get_message_payload()

        response = slack_web_client.views_open(**message)

        return ""

    return "Please refer `/quiz help` to know how to use `/quiz` command"