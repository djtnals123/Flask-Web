import traceback

from app.app import db
from app.dao.error_message import ErrorMessage
from app.models.auth_model import Auth


def insert(username, role):
    role = 'ROLE_PATIENT' if role == '1' else 'ROLE_DOCTOR'
    auth = Auth(id=username, role=role)
    db.session.add(auth)


def delete(username):
    error_msg = None
    try:
        Auth.query.filter_by(id=username).delete()
        db.session.commit()
    except Exception as e:
        error_msg = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return error_msg
