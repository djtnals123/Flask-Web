from app.app import db
from sqlalchemy import func


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    writer = db.Column(db.String(30), db.ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    writer_obj = db.relationship('Account')
    attachment = db.Column(db.String(87), nullable=True)
    content = db.Column(db.String(1000), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False, default=func.now())
    modified_date = db.Column(db.DateTime(), nullable=False, default=func.now())
