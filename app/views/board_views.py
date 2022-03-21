import os

from app.forms.board_write_form import BoardWriteForm
from app.service import board_service
from app.views.decorators import has_role, login_required, is_writer
from flask import Blueprint, render_template, request, g, make_response, url_for, send_file, redirect

bp = Blueprint('board', __name__, url_prefix='/board')


@bp.route('/list')
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
def _list():
    print('gd')
    criteria = {
        'page': request.args.get('page'),
        'per_page': request.args.get('per_page'),
        'option': request.args.get('option'),
        'keyword': request.args.get('keyword')
    }
    result = board_service.list(criteria)
    return render_template('board/board_list.html', board_list=result.get('board_list'), criteria=criteria)


@bp.route('/read')
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
def read():
    board_id = request.args.get('bid')
    board = board_service.read(board_id)
    if board:
        return render_template('board/board_read.html', board=board)
    else:
        return redirect(url_for('board._list'))


@bp.route('/write', methods=('GET', 'POST'))
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
def write():
    form = BoardWriteForm()
    if request.method == 'GET':
        return render_template('board/board_write.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            result = board_service.write(form.title.data, form.content.data, g.user.id, form.attachment.data)
            if result.get('msg'):
                return make_response({'msg': result.get('msg')}, 401)
            else:
                return make_response(url_for('board.read', bid=result.get('board').board_id))
        else:
            first_err_msg = list(form.errors.items())[0][1][0]
            return make_response({'msg': first_err_msg}, 401)


@bp.route('/modify', methods=('GET', 'POST'))
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
@is_writer
def modify(board):
    if request.method == 'GET':
        form = BoardWriteForm(obj=board)
        return render_template('board/board_write.html', form=form, bid=board.board_id)
    elif request.method == 'POST':
        form = BoardWriteForm()
        if form.validate_on_submit():
            result = board_service.modify(board, form.title.data, form.content.data, form.attachment.data)
            if result.get('msg'):
                return make_response({'msg': result.get('msg')}, 401)
            else:
                return make_response(url_for('board.read', bid=result.get('board').board_id))
        else:
            first_err_msg = list(form.errors.items())[0][1][0]
            return make_response({'msg': first_err_msg}, 401)


@bp.route('/delete')
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
@is_writer
def delete(board):
    error_msg = board_service.delete(board.board_id)
    if error_msg:
        return redirect(url_for('board.read', bid=board.board_id))
    else:
        return redirect(url_for('board._list'))


@bp.route('/download/<attachment>')
@login_required
@has_role('ROLE_DOCTOR', 'ROLE_ADMIN')
def download(attachment):
    print(attachment[37:])
    sw = 0
    path = "D:/uploads/"
    files = os.listdir(path)
    for x in files:
        if x == attachment:
            sw = 1

    return send_file(path + attachment, attachment_filename=attachment[37:], as_attachment=True)


@bp.errorhandler(413)
def large_file_error(e):
    if request.is_xhr:
        return make_response({'msg': '파일은 최대 10MB까지 업로드 가능합니다.'}, 413)
