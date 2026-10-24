from functools import wraps

from flask import redirect, render_template, session, url_for


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if session.get('role') != role:
                return render_template('errors/404.html'), 403
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
