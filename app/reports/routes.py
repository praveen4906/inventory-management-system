from flask import render_template, request
from flask_login import login_required
from app.reports import bp
from app.models import Transaction, Item, Warehouse, User
from app.utils import create_excel_response
from datetime import datetime, timedelta
from sqlalchemy import and_

@bp.route('/')
@login_required
def index():
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    return render_template('reports/index.html', start_date=start_date)

@bp.route('/transactions-export')
@login_required
def export_transactions():
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    warehouse_id = request.args.get('warehouse_id', type=int)
    item_id = request.args.get('item_id', type=int)
    user_id = request.args.get('user_id', type=int)
    
    # Build query
    query = Transaction.query
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(Transaction.created_at >= start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(Transaction.created_at < end_date)
    
    if warehouse_id:
        query = query.filter(Transaction.warehouse_id == warehouse_id)
    
    if item_id:
        query = query.filter(Transaction.item_id == item_id)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    
    transactions = query.order_by(Transaction.created_at.desc()).all()
    
    # Prepare data for Excel
    data = []
    for t in transactions:
        data.append([
            t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            t.transaction_type.value.upper(),
            t.item.ssid,
            t.item.name,
            t.warehouse.name,
            t.quantity,
            t.user.username,
            t.notes or ''
        ])
    
    headers = [
        'Date/Time', 'Type', 'SSID', 'Item Name', 
        'Warehouse', 'Quantity', 'User', 'Notes'
    ]
    
    filename = f"transactions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return create_excel_response(data, filename, headers)

@bp.route('/inventory-export')
@login_required
def export_inventory():
    warehouse_id = request.args.get('warehouse_id', type=int)
    
    query = Item.query
    if warehouse_id:
        query = query.filter(Item.warehouse_id == warehouse_id)
    
    items = query.all()
    
    # Prepare data for Excel
    data = []
    for item in items:
        data.append([
            item.ssid,
            item.name,
            item.warehouse.name,
            item.category.name,
            item.current_stock,
            item.unit,
            item.reorder_level,
            'LOW STOCK' if item.is_low_stock else 'OK',
            float(item.unit_price),
            item.description or ''
        ])
    
    headers = [
        'SSID', 'Name', 'Warehouse', 'Category', 
        'Current Stock', 'Unit', 'Reorder Level', 'Status', 'Unit Price', 'Description'
    ]
    
    filename = f"inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return create_excel_response(data, filename, headers)

@bp.route('/low-stock-export')
@login_required
def export_low_stock():
    items = Item.query.filter(Item.current_stock <= Item.reorder_level).all()
    
    # Prepare data for Excel
    data = []
    for item in items:
        data.append([
            item.ssid,
            item.name,
            item.warehouse.name,
            item.category.name,
            item.current_stock,
            item.reorder_level,
            item.reorder_level - item.current_stock,
            item.unit,
            float(item.unit_price)
        ])
    
    headers = [
        'SSID', 'Name', 'Warehouse', 'Category', 
        'Current Stock', 'Reorder Level', 'Shortage', 'Unit', 'Unit Price'
    ]
    
    filename = f"low_stock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return create_excel_response(data, filename, headers)
