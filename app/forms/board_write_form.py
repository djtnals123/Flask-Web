from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import *


def FileNameLength(filename_length):
    def filename_length_check(form, field):
        if len(field.data.filename) > filename_length:
            raise ValidationError(f"파일이름은 {filename_length}글자를 넘을 수 없습니다.")
    return filename_length_check


class BoardWriteForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired('제목을 입력해주세요.'), Length(max=30)])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요.'), Length(max=1000)])
    attachment = FileField('첨부파일', validators=[FileNameLength(50)])


