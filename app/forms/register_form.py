from app.forms.account_modify_form import AccountModifyForm
from wtforms import StringField
from wtforms.validators import Length


class RegisterForm(AccountModifyForm):
    id = StringField('ID', validators=[Length(min=8, max=30, message='ID는 8글자이상 30글자 이하만 허용합니다.')])
