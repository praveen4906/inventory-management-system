from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure QR codes are saved under the Flask static directory so they can be served
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'qr_codes')
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import User after db is initialized to avoid circular import
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.warehouses import bp as warehouses_bp
    app.register_blueprint(warehouses_bp, url_prefix='/warehouses')
    
    from app.items import bp as items_bp
    app.register_blueprint(items_bp, url_prefix='/items')
    
    from app.transactions import bp as transactions_bp
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    
    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
