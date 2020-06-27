from . import slash
from flask import  request
import  json
from .quizcreation import quizCreation
from .quizwiki import quizWiki
from ..models import db, Category, Question, Question_Category

@slash.route("/quiz",methods=["POST"])
def createQuiz():
    
    category_list = []
    raw_data = Category.query.with_entities(Category.name)
    for row in raw_data:
        print(row[0],' is row')
        category_list.append(row[0])

    print(category_list," ARE CATEGORIES")

    data=dict(request.form)

    category_list = []
    raw_data = Category.query.with_entities(Category.name)
    for row in raw_data:
        print(row[0],' is row')
        category_list.append(row[0])

    if data["command"] == "/quiz" and data["text"] == "help":
        #responding with wiki/help/description of quizbot
        quiz_wiki = quizWiki(data["channel_id"])

        quiz_wiki_message = quiz_wiki.get_message_payload()

        return quiz_wiki_message

    if data["command"] == "/quiz" and data["text"] == "start":
        quiz_message=quizCreation(data["channel_id"],category_list)

        message = quiz_message.get_message_payload()
        message["response_type"]= "in_channel"
        return message
    
    return "Please refer `/quiz help` to know how to use `/quiz` command"