from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app.models import User, Role, db
from app.auth.forms import LoginForm, CreateUserForm
from urllib.parse import urlparse

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # Fix: use urlparse instead of url_parse
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/manage-users')
@login_required
def manage_users():
    if not current_user.can_manage_users():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.all()
    form = CreateUserForm()
    return render_template('auth/manage_users.html', users=users, form=form)

@bp.route('/create-user', methods=['POST'])
@login_required
def create_user():
    if not current_user.can_manage_users():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=Role(form.role.data)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} created successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
    return redirect(url_for('auth.manage_users'))

@bp.route('/toggle-user/<int:user_id>')
@login_required
def toggle_user(user_id):
    if not current_user.can_manage_users():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate your own account.', 'danger')
        return redirect(url_for('auth.manage_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    
    return redirect(url_for('auth.manage_users'))
