from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, Length

class CreateSellerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=30)])
    submit = SubmitField('Create Seller')