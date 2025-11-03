from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.sellers import bp
from app.models import Seller, db
from app.sellers.forms import CreateSellerForm

@bp.route('/')
@login_required
def index():
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    sellers = Seller.query.order_by(Seller.name).all()
    form = CreateSellerForm()
    return render_template('sellers/index.html', sellers=sellers, form=form)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('sellers.index'))
    form = CreateSellerForm()
    if form.validate_on_submit():
        s = Seller(name=form.name.data.strip(), email=form.email.data.strip() or None, phone=form.phone.data.strip() or None)
        db.session.add(s)
        db.session.commit()
        flash('Seller created.', 'success')
    else:
        flash('Invalid seller data.', 'danger')
    return redirect(url_for('sellers.index'))