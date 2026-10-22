from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.profile import bp
from app.profile.forms import ProfileForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.email = form.email.data.strip() if form.email.data else None
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile.index'))
    return render_template('profile/index.html', form=form)


@bp.route('/delete', methods=['POST'])
@login_required
def delete_account():
    user = db.session.get(User, current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.', 'info')
    return redirect(url_for('auth.register'))
