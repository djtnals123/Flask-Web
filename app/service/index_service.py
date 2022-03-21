from app.dao.account_dao import find_one
from flask import session
from werkzeug.security import check_password_hash


def login(username, password):
    error = None
    user = find_one(username)
    if not user:
        error = "존재하지 않는 사용자입니다."
    elif not check_password_hash(user.password, password):
        error = "비밀번호가 올바르지 않습니다."
    if error is None:
        session.clear()
        session['user_id'] = user.id
    return error
