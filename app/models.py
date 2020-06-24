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