from app.forms.login_form import LoginForm
from app.service import index_service
from app.views.decorators import login_required
from flask import Blueprint, url_for, render_template, session, request, g
from werkzeug.utils import redirect

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('index.login'))
    else:
        return redirect(url_for('index.choose_function'))


@bp.route('/login', methods=('get', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login_form.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            msg = index_service.login(form.id.data, form.pw.data)
            if msg is None:
                return redirect(url_for('index.choose_function'))
            else:
                return render_template('login_form.html', form=form, error=msg)
        else:
            return render_template('login_form.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.login'))


@bp.route('/choose_function')
@login_required
def choose_function():
    return render_template('choose_function_form.html')