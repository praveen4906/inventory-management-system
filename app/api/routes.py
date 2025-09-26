from flask import jsonify, request
from flask_login import login_required
from app.api import bp
from app.models import Item, Warehouse, User

@bp.route('/items')
@login_required
def get_items():
    warehouse_id = request.args.get('warehouse_id', type=int)
    
    query = Item.query
    if warehouse_id:
        query = query.filter(Item.warehouse_id == warehouse_id)
    
    items = query.all()
    
    return jsonify([{
        'id': item.id,
        'ssid': item.ssid,
        'name': item.name,
        'current_stock': item.current_stock,
        'warehouse_id': item.warehouse_id
    } for item in items])

@bp.route('/warehouses')
@login_required
def get_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'location': w.location
    } for w in warehouses])

@bp.route('/users')
@login_required
def get_users():
    users = User.query.filter(User.is_active == True).all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role': u.role.value
    } for u in users])

