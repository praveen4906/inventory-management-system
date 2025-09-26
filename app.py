from app import create_app
from app.models import db, User, Role

app = create_app()

@app.before_request
def create_tables():
    """Create database tables and initial data if they don't exist"""
    db.create_all()
    
    # Create default admin user if no users exist
    if not User.query.first():
        admin_user = User(
            username='admin',
            email='admin@warehouse.com',
            role=Role.ADMIN
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: username='admin', password='admin123'")

if __name__ == '__main__':
    app.run(debug=True)