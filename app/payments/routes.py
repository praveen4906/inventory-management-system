from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.payments import bp
from app.models import Payment, Seller, db
from app.payments.forms import PaymentForm

@bp.route('/')
@login_required
def index():
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    payments = Payment.query.order_by(Payment.created_at.desc()).limit(100).all()
    return render_template('payments/index.html', payments=payments)

@bp.route('/create', methods=['GET','POST'])
@login_required
def create():
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('payments.index'))
    form = PaymentForm()
    # populate sellers
    sellers = Seller.query.order_by(Seller.name).all()
    form.seller_id.choices = [(0, '— None —')] + [(s.id, s.name) for s in sellers]
    if form.validate_on_submit():
        seller_id = form.seller_id.data or None
        if seller_id == 0:
            seller_id = None
        p = Payment(amount=form.amount.data, currency=form.currency.data or 'USD',
                    method=form.method.data, status=form.status.data,
                    notes=form.notes.data, seller_id=seller_id, processed_by_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash('Payment recorded.', 'success')
        return redirect(url_for('payments.index'))
    return render_template('payments/create.html', form=form)