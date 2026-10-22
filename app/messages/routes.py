from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Message, User
from app.forms import MessageForm, SearchForm
from app.messages import bp

@bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    form = MessageForm()
    search_form = SearchForm()
    users = User.query.filter(User.id != current_user.id).all()
    form.receiver_id.choices = [(u.id, f"{u.username}{' (Admin)' if u.is_admin else ''}") for u in users]

    if form.validate_on_submit():
        receiver = db.session.get(User, form.receiver_id.data)
        if not receiver:
            flash("Receiver not found.", "danger")
            return redirect(url_for('messages.messages'))

        msg = Message(
            sender_id=current_user.id,
            receiver_id=form.receiver_id.data,
            content=form.content.data
        )
        db.session.add(msg)
        db.session.commit()
        flash("Message sent.", "success")
        return redirect(url_for('messages.messages'))

    page = request.args.get('page', 1, type=int)

    if current_user.is_admin:
        msgs_query = Message.query
    else:
        msgs_query = Message.query.filter(
            (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
        )

    q = request.args.get('query', '').strip()
    if q:
        msgs_query = msgs_query.filter(Message.content.ilike(f'%{q}%'))

    msgs = msgs_query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=10, error_out=False)

    return render_template('messages.html', user=current_user, messages=msgs, form=form, search_form=search_form, query=q, title="Messages")
