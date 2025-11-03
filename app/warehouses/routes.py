from flask import render_template, redirect, url_for, flash, request
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
    # Allow managers to delete warehouses OR admins always
    if not (current_user.can_manage_warehouses() or getattr(current_user, 'can_manage_users', lambda: False)()):
        flash('Access denied. Manager or Admin privileges required.', 'danger')
        return redirect(url_for('warehouses.list_warehouses'))

    warehouse = Warehouse.query.get_or_404(id)
    # perform deletion (cascade settings as per models)
    db.session.delete(warehouse)
    db.session.commit()
    flash(f'Warehouse "{warehouse.name}" deleted.', 'success')
    return redirect(url_for('warehouses.list_warehouses'))