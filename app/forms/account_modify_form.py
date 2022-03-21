import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, BooleanField, FieldList, SelectMultipleField, \
    widgets
from wtforms.validators import Length, Email, DataRequired, EqualTo, Regexp

regexPassword = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
HOSPITAL_CHOICE = [('S', '서울대병원'), ('K', '고려대병원')]
ROLES_CHOICE = [('1', '환자'), ('2', '의사')]


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AccountModifyForm(FlaskForm):
    pw = PasswordField('비밀번호', validators=[Regexp(regex=regexPassword, message='비밀번호는 영문, 숫자, 특수문자를 조합한 8자리 이상만 허용합니다.')])
    confirm_pw = PasswordField('비밀번호 확인', validators=[EqualTo('pw', '비밀번호와 비밀번호확인이 일치하지 않습니다.')])
    email = EmailField('이메일', validators=[Email(message='유효하지않는 이메일 형식입니다.')])
    name = StringField('이름', validators=[DataRequired('이름을 입력해주세요.'), Length(max=25, message='이름은 최대 25글자까지 가능합니다.')])
    hospital = SelectField('병원', choices=HOSPITAL_CHOICE, validate_choice=True)
    roles = MultiCheckboxField('회원형태', choices=ROLES_CHOICE, validators=[DataRequired('회원형태를 선택해 주세요')])

