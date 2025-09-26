from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.transactions import bp
from app.models import Transaction, Item, Warehouse, TransactionType, db
from app.transactions.forms import CreateTransactionForm

@bp.route('/')
@login_required
def list_transactions():
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('transactions/list.html', transactions=transactions)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_transaction():
    form = CreateTransactionForm()
    
    if form.validate_on_submit():
        item = Item.query.get(form.item_id.data)
        transaction_type = TransactionType(form.transaction_type.data)
        quantity = form.quantity.data
        
        # Check stock constraints
        if transaction_type == TransactionType.OUT:
            if item.current_stock < quantity and not current_user.can_override_stock():
                flash(f'Insufficient stock. Available: {item.current_stock}, Requested: {quantity}', 'danger')
                return render_template('transactions/create.html', form=form)
        elif transaction_type == TransactionType.ADJUSTMENT:
            new_stock = item.current_stock + quantity
            if new_stock < 0 and not current_user.can_override_stock():
                flash(f'Adjustment would result in negative stock: {new_stock}', 'danger')
                return render_template('transactions/create.html', form=form)
        
        # Create transaction
        transaction = Transaction(
            transaction_type=transaction_type,
            quantity=quantity,
            notes=form.notes.data,
            item_id=form.item_id.data,
            warehouse_id=item.warehouse_id,
            user_id=current_user.id
        )
        
        # Update stock
        if transaction_type == TransactionType.IN:
            item.current_stock += quantity
        elif transaction_type == TransactionType.OUT:
            item.current_stock -= quantity
        elif transaction_type == TransactionType.ADJUSTMENT:
            item.current_stock += quantity  # Adjustment can be positive or negative
        
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Transaction completed successfully! New stock: {item.current_stock}', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    return render_template('transactions/create.html', form=form)
