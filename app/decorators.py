from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in first.")
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash("Admin access required.")
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return wrapper
