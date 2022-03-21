from app.app import db
from sqlalchemy import func
from wtforms.fields import datetime


class Account(db.Model):
    id = db.Column(db.String(30), primary_key=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    hospital = db.Column(db.String(1), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False, default=func.now())
    modified_date = db.Column(db.DateTime(), nullable=False, default=func.now())

