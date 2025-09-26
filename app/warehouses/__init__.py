from flask import Blueprint

bp = Blueprint('warehouses', __name__)

from app.warehouses import routes
