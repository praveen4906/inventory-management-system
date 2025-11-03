from flask import Blueprint
bp = Blueprint('sellers', __name__, template_folder='templates')
from app.sellers import routes