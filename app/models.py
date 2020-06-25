from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.Integer, unique=True)
    role = db.Column(db.String(50))
    orders = db.relationship('Order',backref='user',lazy=True)
    reviews = db.relationship('Review',backref='product',lazy=True)
'''

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