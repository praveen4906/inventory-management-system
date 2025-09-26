from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Role(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    STAFF = 'staff'

class TransactionType(Enum):
    IN = 'in'
    OUT = 'out'
    ADJUSTMENT = 'adjustment'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.STAFF)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        return self.role == role
    
    def can_create_warehouse(self):
        return self.role == Role.ADMIN
    
    def can_manage_users(self):
        return self.role == Role.ADMIN
    
    def can_create_items(self):
        return self.role in [Role.ADMIN, Role.MANAGER]
    
    def can_override_stock(self):
        return self.role == Role.ADMIN
    
    def __repr__(self):
        return f'<User {self.username}>'

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('Item', backref='warehouse', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='warehouse', lazy=True)
    
    def __repr__(self):
        return f'<Warehouse {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    items = db.relationship('Item', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit = db.Column(db.String(20), nullable=False, default='pcs')
    current_stock = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    unit_price = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Relationships
    transactions = db.relationship(
        'Transaction',
        backref='item',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level
    
    def get_qr_data(self):
        """Generate QR code data with current item information"""
        return {
            'ssid': self.ssid,
            'name': self.name,
            'warehouse': self.warehouse.name,
            'category': self.category.name,
            'current_stock': self.current_stock,
            'unit': self.unit,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Item {self.ssid}: {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type.value}: {self.quantity} of {self.item.ssid}>'
