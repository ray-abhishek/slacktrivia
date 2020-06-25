from . import slash
from flask import  request
import  json
from quizcreation import quizCreation

@slash.route("/quiz",methods=["POST"])
def createQuiz():
    
    data=dict(request.form)

    if data["command"] == "/quiz" and data["text"] == "help":
        #responding with wiki/help/description of quizbot
        pass

    if data["command"] == "/quiz":
        quiz_message=quizCreation(data["channel_id"])

        message = quiz_message.get_message_payload()

        message["response_type"]="in_channel"

        return message
    
    return "Failure"