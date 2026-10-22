from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.extensions import limiter, db
from app.models import User
from app.forms import LoginForm, RegisterForm
from app.auth import bp

@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        is_first_user = (User.query.count() == 0)
        user = User(username=form.username.data, is_admin=is_first_user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        if is_first_user:
            flash("First user registered — automatically granted ADMIN privileges.", "success")
        else:
            flash("User registered successfully.", "success")

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form, title="Register")

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html', form=form, title="Login")

@bp.route('/logout')
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('auth.login'))
