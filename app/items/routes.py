from flask import render_template, redirect, url_for, flash, send_file, current_app, request
from flask_login import login_required, current_user
from app.items import bp
from app.models import Item, Warehouse, Category, db
from app.items.forms import CreateItemForm, EditItemForm
from app.utils import generate_qr_code
import os

@bp.route('/')
@login_required
def list_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('items/list.html', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_item():
    if not current_user.can_create_items():
        flash('Access denied. Manager or Admin privileges required.', 'danger')
        return redirect(url_for('items.list_items'))
    
    form = CreateItemForm()
    if form.validate_on_submit():
        # Create category if it doesn't exist
        category = Category.query.filter_by(name=form.category.data).first()
        if not category:
            category = Category(name=form.category.data)
            db.session.add(category)
            db.session.flush()  # Get the ID
        
        item = Item(
            ssid=form.ssid.data,
            name=form.name.data,
            description=form.description.data,
            unit=form.unit.data,
            current_stock=form.initial_stock.data,
            reorder_level=form.reorder_level.data,
            unit_price=form.unit_price.data,
            warehouse_id=form.warehouse_id.data,
            category_id=category.id
        )
        db.session.add(item)
        db.session.commit()
        flash(f'Item "{item.ssid}" created successfully!', 'success')
        return redirect(url_for('items.list_items'))
    
    return render_template('items/create.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    if not current_user.can_create_items():
        flash('Access denied. Manager or Admin privileges required.', 'danger')
        return redirect(url_for('items.list_items'))
    
    item = Item.query.get_or_404(id)
    form = EditItemForm(obj=item)
    
    if form.validate_on_submit():
        # Handle category
        category = Category.query.filter_by(name=form.category.data).first()
        if not category:
            category = Category(name=form.category.data)
            db.session.add(category)
            db.session.flush()
        
        item.name = form.name.data
        item.description = form.description.data
        item.unit = form.unit.data
        item.reorder_level = form.reorder_level.data
        item.unit_price = form.unit_price.data
        item.warehouse_id = form.warehouse_id.data
        item.category_id = category.id
        
        db.session.commit()
        flash(f'Item "{item.ssid}" updated successfully!', 'success')
        return redirect(url_for('items.list_items'))
    
    # Pre-populate category field
    form.category.data = item.category.name
    
    return render_template('items/edit.html', form=form, item=item)

@bp.route('/qr/<int:id>')
@login_required
def generate_qr(id):
    item = Item.query.get_or_404(id)
    filename = generate_qr_code(item)
    
    return render_template('items/qr_code.html', 
                         item=item, 
                         qr_filename=filename)

@bp.route('/download-qr/<filename>')
@login_required
def download_qr(filename):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('QR code file not found.', 'danger')
        return redirect(url_for('items.list_items'))

@bp.route('/delete/<int:id>')
@login_required
def delete_item(id):
    if not current_user.can_create_items():
        flash('Access denied. Manager or Admin privileges required.', 'danger')
        return redirect(url_for('items.list_items'))
    
    item = Item.query.get_or_404(id)
    # Deleting the item will cascade delete its transactions (configured in models)
    db.session.delete(item)
    db.session.commit()
    flash(f'Item "{item.ssid}" and all related transactions were deleted.', 'success')
    return redirect(url_for('items.list_items'))