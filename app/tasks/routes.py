from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import Task, User
from app.forms import EmptyForm
from app.tasks import bp

@bp.route('/tasks')
@login_required
def tasks():
    q = request.args.get('query', '').strip()

    if current_user.is_admin:
        all_tasks = Task.query
    else:
        all_tasks = Task.query.filter_by(assigned_to=current_user.id)

    if q:
        all_tasks = all_tasks.filter(
            or_(Task.title.ilike(f'%{q}%'), Task.description.ilike(f'%{q}%'))
        )

    all_tasks = all_tasks.all()
    users = User.query.all()
    complete_form = EmptyForm()
    return render_template('tasks.html', user=current_user, tasks=all_tasks, users=users, complete_form=complete_form, query=q, title="Tasks")

@bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    form = EmptyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "warning")
        return redirect(url_for('tasks.tasks'))

    task = Task.query.get_or_404(task_id)

    if not current_user.is_admin and task.assigned_to != current_user.id:
        flash("You are not allowed to complete this task.", "danger")
        return redirect(url_for('tasks.tasks'))

    task.completed = True
    db.session.commit()
    flash("Task marked as completed.", "success")
    return redirect(url_for('tasks.tasks'))
