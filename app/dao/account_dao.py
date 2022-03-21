import traceback
from enum import Enum, auto

from app.app import db
from app.dao import auth_dao
from app.dao.error_message import ErrorMessage
from app.models.account_model import Account
from sqlalchemy import desc
from werkzeug.security import generate_password_hash


def insert(username, password, email, name, hospital, roles):
    hashed_password = generate_password_hash(password)
    result = {'err_msg': None, 'account': None}
    try:
        if Account.query.get(username) is not None:
            result['err_msg'] = ErrorMessage.DUPLICATED_ID
            return result
        elif Account.query.filter_by(email=email).first() is not None:
            result['err_msg'] = ErrorMessage.DUPLICATED_EMAIL
            return result
        result['account'] = Account(id=username, password=hashed_password, email=email, name=name, hospital=hospital)
        db.session.add(result.get('account'))
        for role in roles:
            auth_dao.insert(username, role)
        db.session.commit()
    except Exception as e:
        print(e)
    return result


def update(user, password, email, name, hospital, roles):
    hashed_password = generate_password_hash(password)
    result = {'error_msg': None}
    try:
        user.password = hashed_password
        user.email = email
        user.name = name
        user.hospital = hospital
        auth_dao.delete(user.id)
        for role in roles:
            auth_dao.insert(user.id, role)

        db.session.commit()
        result['account'] = user
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result


def find_one(username):
    return Account.query.get(username)


def find_list(criteria):
    result = {}
    try:
        tq = db.session.query(Account).order_by(desc(Account.id))
        paginated_board_list = tq.paginate(page=criteria.get('page'), per_page=criteria.get('per_page'),
                                           max_per_page=50)
        result['account_list'] = paginated_board_list
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result
