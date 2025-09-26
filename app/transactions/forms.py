from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from app.models import Item, TransactionType

class CreateTransactionForm(FlaskForm):
    item_id = SelectField('Item (SSID)', coerce=int, validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', choices=[
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[])
    submit = SubmitField('Create Transaction')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        items = Item.query.all()
        self.item_id.choices = [(i.id, f"{i.ssid} - {i.name} (Stock: {i.current_stock})") for i in items]
    
    def validate_quantity(self, quantity):
        if self.transaction_type.data == 'out' and quantity.data <= 0:
            raise ValidationError('Quantity must be positive for stock out.')
        elif self.transaction_type.data == 'in' and quantity.data <= 0:
            raise ValidationError('Quantity must be positive for stock in.')
