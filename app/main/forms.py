from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    ssid = StringField('Search by SSID', validators=[DataRequired()])
    submit = SubmitField('Search')
