from app.forms.account_form import AgreeForm
from app.forms.account_modify_form import AccountModifyForm
from app.forms.register_form import RegisterForm
from app.service import account_service
from app.views.decorators import login_required, logout_required
from flask import Blueprint, url_for, request, render_template, make_response, session, g
from werkzeug.utils import redirect

bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/agree', methods=('GET', 'POST'))
@logout_required
def agree():
    form = AgreeForm()
    if request.method == 'GET':
        return render_template('account/agree.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('account.register', agree='on'))
        else:
            return render_template('account/agree.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
@logout_required
def register():
    form = RegisterForm()
    if request.method == 'GET':
        if request.args.get('agree') == "on":
            return render_template('account/join_form.html', form=form)
        else:
            return redirect(url_for('account.agree'))
    elif request.method == 'POST':
        if form.validate_on_submit():
            msg = account_service.register(form.id.data, form.pw.data, form.email.data, form.name.data,
                                           form.hospital.data, form.roles.data)
            if msg:
                return make_response(msg, 401)
            else:
                return make_response(url_for('index.index'))
        else:
            first_err_msg = list(form.errors.items())[0][1][0]
            return make_response({'msg': first_err_msg}, 401)


@bp.route('/modify', methods=('GET', 'POST'))
@login_required
def modify():
    form = AccountModifyForm()
    if g.user:
        if request.method == 'GET':
            return render_template('account/join_form.html', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                msg = account_service.modify(g.user, form.pw.data, form.email.data, form.name.data,
                                             form.hospital.data, form.roles.data)
                if msg:
                    return make_response(msg, 401)
                else:
                    return make_response(url_for('index.choose_function'))
            else:
                first_err_msg = list(form.errors.items())[0][1][0]
                return make_response({'msg': first_err_msg}, 401)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if '/static/' not in request.path:
        if user_id is None:
            g.user = None
        else:
            g.user = account_service.get_user(user_id)
