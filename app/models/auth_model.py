from app.app import db
from sqlalchemy import ForeignKey


class Auth(db.Model):
    id = db.Column(db.String(30), ForeignKey('account.id'), primary_key=True, nullable=False)
    role = db.Column(db.String(15), primary_key=True, nullable=False)
    user = db.relationship('Account', backref=db.backref('auth_set'))

