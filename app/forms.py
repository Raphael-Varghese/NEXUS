from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User
from app import db


def strip_filter(x):
    return x.strip() if x else None


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], filters=[strip_filter])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)], filters=[strip_filter])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        with current_app.app_context():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')


class MessageForm(FlaskForm):
    receiver_id = SelectField('To', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()], filters=[strip_filter], render_kw={"rows": 3})
    submit = SubmitField('Send')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)], filters=[strip_filter])
    description = TextAreaField('Description', filters=[strip_filter], render_kw={"rows": 3})
    assigned_to = SelectField('Assign to', coerce=int)
    completed = BooleanField('Completed?')
    submit = SubmitField('Save')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PythonConsoleForm(FlaskForm):
    code = TextAreaField('Code', validators=[DataRequired()], render_kw={"placeholder": "Python code...", "rows": 6})
    submit = SubmitField('Run')


class TerminalConsoleForm(FlaskForm):
    cmd = TextAreaField('Command', validators=[DataRequired()], render_kw={"placeholder": "Enter command...", "rows": 4})
    submit = SubmitField('Run Command')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()], filters=[strip_filter], render_kw={"placeholder": "Search..."})
    submit = SubmitField('Search')
