from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Optional, NumberRange

class PaymentForm(FlaskForm):
    seller_id = SelectField('Seller', coerce=int, validators=[Optional()])
    amount = DecimalField('Amount', places=2, validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField('Currency', default='INR', validators=[Optional()])
    method = SelectField('Method', choices=[('card', 'Card'), ('bank', 'Bank Transfer'), ('cash', 'Cash')], validators=[Optional()])
    status = SelectField('Status', choices=[('pending','Pending'), ('completed','Completed'), ('refunded','Refunded')], default='pending')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Record Payment')