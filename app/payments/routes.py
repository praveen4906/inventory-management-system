from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_required, current_user
from app.payments import bp
from app.models import Payment, Seller, db
from app.payments.forms import PaymentForm
import csv
import io
from datetime import datetime

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


@bp.route('/export')
@login_required
def export():
    # Admin-only
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))

    fmt = request.args.get('format', 'csv').lower()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()

    # JSON export
    if fmt == 'json':
        data = []
        for p in payments:
            data.append({
                'id': p.id,
                'amount': str(p.amount),
                'currency': p.currency,
                'method': p.method,
                'status': p.status,
                'notes': p.notes,
                'seller': p.seller.name if p.seller else None,
                'processed_by_id': p.processed_by_id,
                'created_at': p.created_at.isoformat() if p.created_at else None,
            })
        return jsonify(data)

    # Default CSV export
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'amount', 'currency', 'method', 'status', 'notes', 'seller', 'processed_by_id', 'created_at'])
    for p in payments:
        cw.writerow([
            p.id,
            str(p.amount),
            p.currency,
            p.method,
            p.status,
            p.notes or '',
            p.seller.name if p.seller else '',
            p.processed_by_id or '',
            p.created_at.isoformat() if p.created_at else '',
        ])
    output = make_response(si.getvalue())
    stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    output.headers['Content-Disposition'] = f'attachment; filename=payments-{stamp}.csv'
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return output