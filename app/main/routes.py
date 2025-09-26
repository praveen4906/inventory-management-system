from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.models import Item, Transaction, Warehouse, Category, TransactionType
from app.main.forms import SearchForm
from sqlalchemy import desc

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    # Get low stock items
    low_stock_items = Item.query.filter(Item.current_stock <= Item.reorder_level).all()
    
    # Get recent transactions
    recent_transactions = Transaction.query.order_by(desc(Transaction.created_at)).limit(10).all()
    
    # Get summary statistics
    total_items = Item.query.count()
    total_warehouses = Warehouse.query.count()
    total_transactions = Transaction.query.count()
    
    search_form = SearchForm()
    
    return render_template('main/dashboard.html',
                         low_stock_items=low_stock_items,
                         recent_transactions=recent_transactions,
                         total_items=total_items,
                         total_warehouses=total_warehouses,
                         total_transactions=total_transactions,
                         search_form=search_form)

@bp.route('/search')
@login_required
def search():
    ssid = request.args.get('ssid', '').strip()
    if not ssid:
        return jsonify({'error': 'SSID is required'}), 400
    
    item = Item.query.filter_by(ssid=ssid).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({
        'id': item.id,
        'ssid': item.ssid,
        'name': item.name,
        'warehouse': item.warehouse.name,
        'category': item.category.name,
        'current_stock': item.current_stock,
        'unit': item.unit,
        'reorder_level': item.reorder_level,
        'is_low_stock': item.is_low_stock
    })