import traceback
from datetime import datetime
from app.app import db
from app.dao.error_message import ErrorMessage
from app.models.board_model import Board
from sqlalchemy import desc


def insert(title, content, writer, attachment):
    result = {'error_msg': None}
    try:
        result['board'] = Board(title=title, content=content, writer=writer, attachment=attachment)
        db.session.add(result['board'])
        db.session.commit()
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result


def update(board, title, content, attachment):
    result = {'error_msg': None}
    try:
        board.title = title
        board.content = content
        board.modified_date = datetime.now()
        if attachment:
            board.attachment = attachment
        db.session.commit()
        result['board'] = board
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result


def find_one(board_id):
    result = {}
    try:
        result['board'] = Board.query.get(board_id)
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result


def find_list(criteria):
    result = {}
    try:
        tq = db.session.query(Board).order_by(desc(Board.board_id))
        option = criteria.get('option')
        keyword = criteria.get('keyword')
        keyword = '%%{}%%'.format(keyword)

        if option and keyword:
            if option == 'title':
                tq = tq.filter(Board.title.ilike(keyword))
            elif option == 'content':
                tq = tq.filter(Board.content.ilike(keyword))
            elif option == 'title+content':
                tq = tq.filter(Board.title.ilike(keyword) |
                               Board.content.ilike(keyword))
            elif option == 'writer':
                tq = tq.filter(Board.writer.ilike(keyword))

        # board_list = Board.query.order_by(Board.board_id.desc())
        paginated_board_list = tq.paginate(page=criteria.get('page'), per_page=criteria.get('per_page'),
                                           max_per_page=50)
        result['board_list'] = paginated_board_list
    except Exception as e:
        result['error_msg'] = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return result


def delete_one(board_id):
    error_msg = None
    try:
        Board.query.filter_by(board_id=board_id).delete()
        db.session.commit()
    except Exception as e:
        error_msg = ErrorMessage.UNKNOWN_ERROR
        print(traceback.format_exc())
    return error_msg
