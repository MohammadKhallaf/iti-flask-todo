from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType

from app import app

'''
Setup the database
'''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasklist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)



class Todo(db.Model):
    __tablename__ = 'todolist'
    types = [
        ('0', 'High Priority'),
        ('1', 'Mid Priority'),
        ('2', 'Low Priority')
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    status = db.Column(ChoiceType(types))  # !!?

    def __repr__(self):
        return '<Todo %r>' % self.id
