import os
import traceback
from app.dao.board_dao import insert, find_one, delete_one, update, find_list
from app.dao.error_message import ErrorMessage

path = 'D:/uploads/'


def write(title, content, writer, attachment):
    result = file_upload(attachment)
    if not result.get('msg'):
        result = insert(title, content, writer, result.get('new_filename'))
        if result.get('error_msg'):
            result['msg'] = '게시글 작성중 에러가 발생하였습니다.'
    return result


def modify(board, title, content, attachment):
    result = file_upload(attachment)
    if not result.get('msg'):
        if board.attachment:
            error = file_remove(board.attachment)
            if error:
                result['msg'] = '파일삭제중 에러가 발생하였습니다.'
                return result
        result = update(board, title, content, result.get('new_filename'))
        if result.get('error_msg'):
            result['msg'] = '파일 수정중 에러가 발생하였습니다.'
    return result


def read(board_id):
    result = find_one(board_id)
    return result.get('board')


def list(criteria):
    if (criteria.get('page') is None) or (not criteria.get('page').isdigit()):
        criteria['page'] = 1
    else:
        criteria['page'] = int(criteria.get('page'))

    if (criteria.get('per_page') is None) or (not criteria.get('per_page').isdigit()):
        criteria['per_page'] = 10
    else:
        criteria['per_page'] = int(criteria.get('per_page'))

    return find_list(criteria)


def delete(board_id):
    board = read(board_id)
    print(board.attachment)
    if board.attachment:
        error = file_remove(board.attachment)
        if error:
            return error
    return delete_one(board_id)


def file_remove(file_name):
    try:
        if os.path.isfile(path + file_name):
            os.remove(path + file_name)
        return None
    except Exception as e:
        print(traceback.format_exc())
        return ErrorMessage.UNKNOWN_ERROR


def file_upload(attachment):
    result = {}
    try:
        if attachment:
            import uuid
            result['new_filename'] = str(uuid.uuid4()) + '_' + attachment.filename
            attachment.save(path + result.get('new_filename'))
        else:
            attachment.filename = None
            result['new_filename'] = None
    except Exception as e:
        print(traceback.format_exc())
        result['msg'] = '파일 업로드중 에러가 발생하였습니다.'
    return result



