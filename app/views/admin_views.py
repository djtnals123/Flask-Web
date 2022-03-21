from app.service import admin_service
from app.views.decorators import login_required, has_role
from flask import Blueprint, request, render_template

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/user_list')
@login_required
@has_role('ROLE_ADMIN')
def user_list():
    criteria = {
        'page': request.args.get('page'),
        'per_page': request.args.get('per_page')
    }
    result = admin_service.user_list(criteria)
    return render_template('admin/user_list.html', account_list=result.get('account_list'), criteria=criteria)
