from app.dao.account_dao import insert, find_one, update
from app.dao.error_message import ErrorMessage


def register(username, password, email, name, hospital, roles):
    result = insert(username, password, email, name, hospital, roles)
    if result.get('err_msg') is not None:
        if result.get('err_msg') == ErrorMessage.DUPLICATED_ID:
            return {'msg': '이미 존재하는 아이디입니다.'}
        elif result.get('err_msg') == ErrorMessage.DUPLICATED_EMAIL:
            return {'msg': '이미 존재하는 이메일입니다.'}
    return None


def modify(user, password, email, name, hospital, roles):
    result = update(user, password, email, name, hospital, roles)
    if result.get('err_msg') is not None:
        return {'msg': '회원정보 수정중 에러가 발생하였습니다.'}


def get_user(username):
    return find_one(username)