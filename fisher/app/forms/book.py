from wtforms import StringField, Form, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


# DataRequired防止传入空字符串
class SearchForm(Form):
    """
    控制请求的关键字，如果q为空在则会返回长度不满足要求
    page给定默认值
    """

    q = StringField(validators=[DataRequired(), Length(min=1, max=30, message="长度不满足要求")])
    page = IntegerField(default=1, validators=[NumberRange(min=1, max=99)])
