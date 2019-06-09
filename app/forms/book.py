from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length, NumberRange


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = StringField(validators=[NumberRange(min=1, max=100)], default=1)