from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateWarehouseForm(FlaskForm):
    name = StringField('Warehouse Name', validators=[
        DataRequired(), 
        Length(min=3, max=100)
    ])
    location = StringField('Location', validators=[Length(max=200)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Create Warehouse')
