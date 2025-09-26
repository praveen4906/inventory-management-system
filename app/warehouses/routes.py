from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.warehouses import bp
from app.models import Warehouse, db
from app.warehouses.forms import CreateWarehouseForm

@bp.route('/')
@login_required
def list_warehouses():
    warehouses = Warehouse.query.all()
    return render_template('warehouses/list.html', warehouses=warehouses)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_warehouse():
    if not current_user.can_create_warehouse():
        flash('Access denied. Admin privileges required to create warehouses.', 'danger')
        return redirect(url_for('warehouses.list_warehouses'))
    
    form = CreateWarehouseForm()
    if form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(warehouse)
        db.session.commit()
        flash(f'Warehouse "{warehouse.name}" created successfully!', 'success')
        return redirect(url_for('warehouses.list_warehouses'))
    
    return render_template('warehouses/create.html', form=form)

@bp.route('/delete/<int:id>')
@login_required
def delete_warehouse(id):
    if not current_user.can_create_warehouse():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('warehouses.list_warehouses'))
    
    warehouse = Warehouse.query.get_or_404(id)
    if warehouse.items:
        flash(f'Cannot delete warehouse "{warehouse.name}" - it contains items.', 'danger')
        return redirect(url_for('warehouses.list_warehouses'))
    
    db.session.delete(warehouse)
    db.session.commit()
    flash(f'Warehouse "{warehouse.name}" deleted successfully!', 'success')
    return redirect(url_for('warehouses.list_warehouses'))