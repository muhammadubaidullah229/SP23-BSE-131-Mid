from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        reg_number = request.form.get('reg_number', '').strip().upper()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'Student')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validation
        if not full_name or not username or not email or not password or not reg_number:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Username is already taken. Please choose another.', 'warning')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Email is already registered. Please log in.', 'warning')
            return render_template('auth/register.html')

        # Create new user
        new_user = User(
            full_name=full_name,
            reg_number=reg_number,
            username=username,
            email=email,
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in to the Student Portal.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if not user or not user.check_password(password):
            flash('Invalid credentials. Please verify your username/email and password.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    flash('You have been logged out of the portal.', 'info')
    return redirect(url_for('main.home'))
