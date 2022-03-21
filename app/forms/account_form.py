from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired


class AgreeForm(FlaskForm):
    agree = BooleanField('동의', validators=[DataRequired('동의해주세요.')])
