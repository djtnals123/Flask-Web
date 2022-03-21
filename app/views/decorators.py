import functools

from app.service import board_service
from flask import url_for, session, g, request, make_response
from werkzeug.utils import redirect


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index.login'))
        return view(**kwargs)
    return wrapped_view


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            session.clear()
        return view(**kwargs)
    return wrapped_view


def has_role(*roles):
    def wrapped_view(view):
        @functools.wraps(view)
        def decorator(**kwargs):
            permission = False
            for role in roles:
                print(role)
                for user_roles in g.user.auth_set:
                    print('user ' + user_roles.role)
                    if role == user_roles.role:
                        print('안녕')
                        permission = True
                        break
            if permission:
                return view(**kwargs)
            else:
                return redirect(url_for('index.choose_function'))
        return decorator
    return wrapped_view


def is_writer(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if request.method == 'GET':
            board_id = request.args.get('bid')
            board = board_service.read(board_id)
            if board.writer == g.user.id:
                return view(board, **kwargs)
            else:
                return redirect(url_for('board.read', bid=board_id))
        elif request.method == 'POST':
            board_id = request.form.get('bid')
            board = board_service.read(board_id)
            if board.writer == g.user.id:
                return view(board, **kwargs)
            else:
                return make_response(url_for('board.read', bid=board_id))

    return wrapped_view
