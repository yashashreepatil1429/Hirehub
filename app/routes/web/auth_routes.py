from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.services.auth_service import AuthService


auth_bp = Blueprint('auth', __name__, url_prefix='')


@auth_bp.route('/')
def home():
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            AuthService().login(request.form.get('email', ''), request.form.get('password', ''))
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard.index'))
        except InvalidCredentialsError as exc:
            flash(str(exc), 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = dict(request.form)
        try:
            AuthService().register(data)
            flash('Registration successful', 'success')
            return redirect(url_for('dashboard.index'))
        except (UserAlreadyExistsError, ValueError) as exc:
            flash(str(exc), 'danger')
    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    AuthService().logout()
    return redirect(url_for('auth.login'))
