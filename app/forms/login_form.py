from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired('아이디를 입력해주세요.')])
    pw = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력해주세요.')])
