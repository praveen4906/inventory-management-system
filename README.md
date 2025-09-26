# Warehouse Inventory Management System

A comprehensive web-based warehouse inventory management system built with Flask, SQLAlchemy, and Bootstrap. This system provides role-based access control, real-time inventory tracking, QR code generation, and comprehensive reporting capabilities.

## Features

### 🔐 Authentication & Role-Based Access
- **Admin**: Full system access, user management, warehouse creation
- **Manager**: Inventory and transaction management, reporting
- **Staff**: Basic transactions and inventory viewing

### 📦 Core Functionality
- **Warehouse Management**: Create and manage multiple warehouses
- **Item Management**: Track items with unique SSIDs, categories, and stock levels
- **Transaction System**: Stock IN/OUT/Adjustment with full audit trail
- **QR Code Generation**: Dynamic QR codes with current item information
- **Search**: Quick SSID-based item lookup
- **Low Stock Alerts**: Automatic alerts when items fall below reorder levels

### 📊 Reporting & Export
- **Excel Export**: Transactions, inventory, and low stock reports
- **Filter Options**: Date range, warehouse, user, and item filters
- **Dashboard Analytics**: Real-time statistics and recent activity

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Create Project Structure
```bash
mkdir warehouse_inventory_system
cd warehouse_inventory_system
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
The database will be created automatically when you first run the application.

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at: http://127.0.0.1:5000

## Default Login Credentials

**Username:** admin  
**Password:** admin123  
**Role:** Admin

> ⚠️ **Important**: Change the default password after first login for production use.

## Usage Guide

### 1. Getting Started
1. Login with default credentials
2. Create additional users (Admin only)
3. Create your first warehouse (Admin only)
4. Add items to the warehouse
5. Start tracking transactions

### 2. Creating Items
- Each item must have a unique SSID
- Categories are created automatically when adding items
- Set reorder levels for low stock alerts
- Initial stock can be set during item creation

### 3. Managing Transactions
- **Stock IN**: Receiving new inventory
- **Stock OUT**: Items leaving warehouse
- **Adjustment**: Correct stock discrepancies (positive or negative)
- All transactions are logged with user, timestamp, and notes

### 4. QR Code System
- QR codes contain current item information including stock levels
- Regenerate QR codes after stock changes for accuracy
- Download QR codes for physical labeling
- QR data includes: SSID, name, warehouse, category, current stock, last updated

### 5. Reports & Analytics
- **Dashboard**: Overview with statistics and alerts
- **Transaction Reports**: Filterable by date, warehouse, user, or item
- **Inventory Reports**: Current stock levels across all warehouses
- **Low Stock Reports**: Items requiring attention
- **Excel Export**: All reports can be exported to Excel format

### 6. User Management (Admin Only)
- Create users with different roles
- Activate/deactivate user accounts
- Role-based access ensures security

## File Structure

```
warehouse_inventory_system/
├── app.py                    # Main application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── instance/
│   └── database.db          # SQLite database
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── utils.py             # Utility functions
│   ├── auth/                # Authentication module
│   ├── main/                # Dashboard module
│   ├── warehouses/          # Warehouse management
│   ├── items/               # Item management
│   ├── transactions/        # Transaction handling
│   ├── reports/             # Report generation
│   ├── api/                 # API endpoints
│   └── templates/           # HTML templates
└── static/
    ├── css/custom.css       # Custom styles
    ├── js/main.js          # JavaScript functions
    └── qr_codes/           # Generated QR codes
```

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Database
- Uses SQLite by default for easy setup
- Can be configured for PostgreSQL or MySQL in production
- Database file location: `instance/database.db`

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Secure session handling
- **Role-Based Access**: Granular permission system
- **CSRF Protection**: Forms protected against CSRF attacks
- **Input Validation**: Server-side validation on all forms

## Production Deployment

### 1. Security Checklist
- [ ] Change default admin password
- [ ] Set strong SECRET_KEY environment variable
- [ ] Use production database (PostgreSQL recommended)
- [ ] Enable HTTPS
- [ ] Configure proper logging
- [ ] Set up regular backups

### 2. Environment Setup
```bash
export SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/warehouse_db"
export FLASK_ENV="production"
```

### 3. WSGI Configuration
Use Gunicorn or similar WSGI server:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

## Troubleshooting

### Common Issues

**Database not found**
- Ensure the `instance` directory exists
- Check database permissions
- Run the application once to auto-create tables

**QR codes not generating**
- Verify `static/qr_codes` directory exists and is writable
- Check PIL/Pillow installation

**Permission errors**
- Verify user roles are assigned correctly
- Check login status
- Ensure database has proper permissions

**Excel export issues**
- Confirm openpyxl is installed
- Check file permissions for downloads

### Getting Help

For issues and questions:
1. Check the error logs in the console
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Check the troubleshooting section above

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.