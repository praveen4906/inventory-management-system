from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_required, current_user
from app.sellers import bp
from app.models import Seller, db
from app.sellers.forms import CreateSellerForm
import csv
import io
from datetime import datetime

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


@bp.route('/export')
@login_required
def export():
    # Admin-only
    if not getattr(current_user, 'can_manage_users', lambda: False)():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))

    fmt = request.args.get('format', 'csv').lower()
    sellers = Seller.query.order_by(Seller.name).all()

    if fmt == 'json':
        data = []
        for s in sellers:
            data.append({
                'id': s.id,
                'name': s.name,
                'email': s.email,
                'phone': s.phone,
                'created_at': s.created_at.isoformat() if getattr(s, 'created_at', None) else None,
            })
        return jsonify(data)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'name', 'email', 'phone', 'created_at'])
    for s in sellers:
        cw.writerow([
            s.id,
            s.name,
            s.email or '',
            s.phone or '',
            s.created_at.isoformat() if getattr(s, 'created_at', None) else '',
        ])
    output = make_response(si.getvalue())
    stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    output.headers['Content-Disposition'] = f'attachment; filename=sellers-{stamp}.csv'
    output.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return output