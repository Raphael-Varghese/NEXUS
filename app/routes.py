import traceback
import shlex
import subprocess

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Task, User, Message
from app.forms import PythonConsoleForm, TerminalConsoleForm, TaskForm, EmptyForm
from app.decorators import admin_required
from app.admin import bp

@bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_task():
    form = TaskForm()
    users = User.query.all()
    form.assigned_to.choices = [(0, '-- none --')] + [(u.id, u.username) for u in users]

    if form.validate_on_submit():
        assigned_to_id = form.assigned_to.data if form.assigned_to.data != 0 else None
        task = Task(
            title=form.title.data,
            description=form.description.data,
            assigned_to=assigned_to_id
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created.", "success")
        return redirect(url_for('tasks.tasks'))

    return render_template('create_task.html', form=form, title="Create Task")


@bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    users = User.query.all()
    form.assigned_to.choices = [(0, '-- none --')] + [(u.id, u.username) for u in users]

    if task.assigned_to:
        form.assigned_to.data = task.assigned_to
    else:
        form.assigned_to.data = 0

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assigned_to = form.assigned_to.data if form.assigned_to.data != 0 else None
        task.completed = form.completed.data
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for('tasks.tasks'))

    return render_template('edit_task.html', form=form, task=task, title="Edit Task")


@bp.route('/admin/python', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_python_console():
    form = PythonConsoleForm()
    output = ""
    if form.validate_on_submit():
        code = form.code.data
        try:
            local_vars = {}
            exec(code, globals(), local_vars)
            output = str(local_vars) if local_vars else "Executed."
        except Exception:
            output = traceback.format_exc()

    return render_template('admin_python.html', form=form, output=output, title="Admin Python Console")


@bp.route('/admin/terminal', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_terminal():
    form = TerminalConsoleForm()
    output = ""
    if form.validate_on_submit():
        cmd = form.cmd.data
        try:
            args = shlex.split(cmd)
            result = subprocess.run(args, shell=False, capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

    return render_template('admin_terminal.html', form=form, output=output, title="Admin Terminal")


@bp.route('/admin/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    action_form = EmptyForm()
    return render_template('admin_users.html', users=all_users, action_form=action_form, title="User Management")


@bp.route('/admin/users/<int:user_id>/promote', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("User is already an admin.", "info")
    else:
        user.is_admin = True
        db.session.commit()
        flash(f"Promoted {user.username} to admin.", "success")
    return redirect(url_for('admin.users'))


@bp.route('/admin/users/<int:user_id>/demote', methods=['POST'])
@login_required
@admin_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)

    if not user.is_admin:
        flash("User is not an admin.", "info")
        return redirect(url_for('admin.users'))

    if user.id == current_user.id:
        flash("You cannot demote yourself.", "danger")
        return redirect(url_for('admin.users'))

    admin_count = User.query.filter_by(is_admin=True).count()
    if admin_count <= 1:
        flash("Cannot demote the last admin.", "danger")
        return redirect(url_for('admin.users'))

    user.is_admin = False
    db.session.commit()
    flash(f"Demoted {user.username} from admin.", "success")
    return redirect(url_for('admin.users'))


@bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for('admin.users'))

    Message.query.filter(
        (Message.sender_id == user.id) | (Message.receiver_id == user.id)
    ).delete(synchronize_session=False)

    Task.query.filter_by(assigned_to=user.id).update({Task.assigned_to: None}, synchronize_session=False)

    db.session.delete(user)
    db.session.commit()
    flash(f"Deleted user {user.username}.", "success")
    return redirect(url_for('admin.users'))
