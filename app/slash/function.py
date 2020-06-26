from . import slash
from flask import  request
import  json
from quizcreation import quizCreation
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
        pass

    if data["command"] == "/quiz":
        quiz_message=quizCreation(data["channel_id"],category_list)

        message = quiz_message.get_message_payload()
        message["response_type"]= "in_channel"
        return message
    
    return "Failure"