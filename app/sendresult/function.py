from ..models import db,Attempt,Quiz_Question,Question,Quiz
from .resultdisplay import resultDisplay
from slack import WebClient
import os

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def getResult(quiz_id):

    # Getting data of all attempts made to particular quiz identified by quiz id
    user_data = Attempt.query.filter_by(quiz_id=quiz_id).all()

    # Getting question id for particular quiz
    question_id_query = Quiz_Question.query.filter_by(quiz_id=quiz_id).first()
    question_id = question_id_query.question_id

    #Getting correct answer for the question in the given quiz
    question_query = Question.query.filter_by(id=question_id).first()
    answer = question_query.answer
    quiz_query = Quiz.query.filter_by(id=quiz_id).first()
    channel = quiz_query.channel_id

    #Login to save users_id with correct answer
    correct_answer_submission_data = {
        "users":[]
    }

    for x in user_data:
        if x.answer == answer:
            correct_answer_submission_data["users"].append(x.user_id)

    result = resultDisplay(channel , answer , correct_answer_submission_data["users"])

    message = result.get_message_payload()

    response = slack_web_client.chat_postMessage(**message)