from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from app.models import Item, Warehouse

class CreateItemForm(FlaskForm):
    ssid = StringField('SSID (Unique ID)', validators=[
        DataRequired(), 
        Length(min=3, max=50)
    ])
    name = StringField('Item Name', validators=[
        DataRequired(), 
        Length(min=3, max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    category = StringField('Category', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    unit = StringField('Unit', validators=[
        DataRequired(), 
        Length(min=1, max=20)
    ], default='pcs')
    initial_stock = IntegerField('Initial Stock', validators=[
        DataRequired(), 
        NumberRange(min=0)
    ], default=0)
    reorder_level = IntegerField('Reorder Level', validators=[
        DataRequired(), 
        NumberRange(min=0)
    ], default=10)
    unit_price = DecimalField('Unit Price', validators=[
        NumberRange(min=0)
    ], default=0)
    warehouse_id = SelectField('Warehouse', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Item')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.warehouse_id.choices = [(w.id, w.name) for w in Warehouse.query.all()]
    
    def validate_ssid(self, ssid):
        item = Item.query.filter_by(ssid=ssid.data).first()
        if item:
            raise ValidationError('SSID already exists. Please choose a different one.')

class EditItemForm(FlaskForm):
    name = StringField('Item Name', validators=[
        DataRequired(), 
        Length(min=3, max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    category = StringField('Category', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    unit = StringField('Unit', validators=[
        DataRequired(), 
        Length(min=1, max=20)
    ])
    reorder_level = IntegerField('Reorder Level', validators=[
        DataRequired(), 
        NumberRange(min=0)
    ])
    unit_price = DecimalField('Unit Price', validators=[
        NumberRange(min=0)
    ])
    warehouse_id = SelectField('Warehouse', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Item')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.warehouse_id.choices = [(w.id, w.name) for w in Warehouse.query.all()]
