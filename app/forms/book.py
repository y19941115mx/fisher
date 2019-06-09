from wtforms import StringField, Form, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=100)], default=1)
