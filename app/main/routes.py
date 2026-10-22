import traceback
import shlex
import subprocess

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Task, Message
from app.forms import PythonConsoleForm, TerminalConsoleForm
from app.main import bp

@bp.route('/')
@login_required
def dashboard():
    pending_tasks = Task.query.filter_by(assigned_to=current_user.id, completed=False).count()
    total_tasks = Task.query.filter_by(assigned_to=current_user.id).count()
    unread_query = Message.query.filter_by(receiver_id=current_user.id)
    total_messages = unread_query.count()
    return render_template(
        'dashboard.html',
        user=current_user,
        pending_tasks=pending_tasks,
        total_tasks=total_tasks,
        total_messages=total_messages,
        title="Dashboard"
    )

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()
        if not new_username:
            flash("Username cannot be empty.", "warning")
            return redirect(url_for('main.profile'))

        from app.models import User
        existing = User.query.filter_by(username=new_username).first()
        if existing and existing.id != current_user.id:
            flash("Username already taken.", "danger")
            return redirect(url_for('main.profile'))

        current_user.username = new_username
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for('main.profile'))

    pending = Task.query.filter_by(assigned_to=current_user.id, completed=False).count()
    completed = Task.query.filter_by(assigned_to=current_user.id, completed=True).count()
    sent = Message.query.filter_by(sender_id=current_user.id).count()

    return render_template(
        'profile.html',
        user=current_user,
        pending=pending,
        completed=completed,
        sent=sent,
        title="Profile"
    )

@bp.route('/console/python', methods=['GET', 'POST'])
@login_required
def user_python_console():
    form = PythonConsoleForm()
    output = ""
    if form.validate_on_submit():
        code = form.code.data
        try:
            local_vars = {}
            safe_globals = {
                "__builtins__": {
                    "len": len, "str": str, "int": int, "float": float,
                    "range": range, "enumerate": enumerate, "zip": zip,
                    "list": list, "dict": dict, "tuple": tuple, "set": set,
                    "print": print, "sum": sum, "min": min, "max": max,
                    "abs": abs, "round": round, "sorted": sorted,
                    "map": map, "filter": filter, "bool": bool,
                    "type": type, "isinstance": isinstance,
                }
            }
            exec(code, safe_globals, local_vars)
            output = str(local_vars) if local_vars else "Executed."
        except Exception:
            output = traceback.format_exc()

    return render_template('user_python.html', form=form, output=output, title="User Python Console")

@bp.route('/console/terminal', methods=['GET', 'POST'])
@login_required
def user_terminal():
    form = TerminalConsoleForm()
    output = ""
    allowed = {
        'echo', 'python', 'python3', 'dir', 'ls', 'cat', 'type',
        'pwd', 'whoami', 'date', 'ping', 'tracert', 'nslookup',
        'ipconfig', 'hostname', 'cls', 'clear'
    }

    if form.validate_on_submit():
        cmd = form.cmd.data
        try:
            args = shlex.split(cmd)
            if not args:
                output = "No command entered."
            else:
                base = args[0].lower()
                if base not in allowed:
                    output = f"Command '{base}' is not in the allowed list."
                else:
                    result = subprocess.run(args, shell=False, capture_output=True, text=True)
                    output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

    return render_template('user_terminal.html', form=form, output=output, title="User Terminal")
