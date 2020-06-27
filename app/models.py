from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    setting=db.Column(db.String(100))
    flag=db.Column(db.Boolean,nullable=False)


class Question(db.Model):
    __tablename__="question"
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(300))
    option1=db.Column(db.String(100))
    option2=db.Column(db.String(100))
    option3=db.Column(db.String(100))
    option4=db.Column(db.String(100))
    answer=db.Column(db.String(100))


class Question_Category(db.Model):
    __tablename__="question_category"
    id=db.Column(db.Integer,primary_key=True)
    question_id=db.Column(db.Integer,db.ForeignKey("question.id"))
    category_id=db.Column(db.Integer,db.ForeignKey("category.id"))


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer,primary_key=True)
    channel_id = db.Column(db.String(100))
    author_id = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

class Quiz_Question(db.Model):
    __tablename__="quiz_question"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id = db.Column(db.Integer,db.ForeignKey("quiz.id"))
    question_id=db.Column(db.Integer,db.ForeignKey("question.id"))
    timestamp = db.Column(db.String(100))


class Attempt(db.Model):
    __tablename__ = "attempt"
    id = db.Column(db.Integer,primary_key=True)
    quiz_id = db.Column(db.Integer,db.ForeignKey("quiz.id"))
    user_id = db.Column(db.String(100))
    answer = db.Column(db.String(100))