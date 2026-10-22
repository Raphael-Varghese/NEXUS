import os
import sys

from flask import Flask
from flask_limiter import Limiter
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=lambda: "global")
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__, instance_relative_config=True)

    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)

    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # DEBUG
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
    print(f"[NEXUS DEBUG] Database URI: {db_uri}", flush=True)

    # Ensure SQLite database directory exists - handles BOTH absolute and relative paths
    if db_uri.startswith('sqlite:///'):
        # Remove 'sqlite:///' prefix
        db_path = db_uri[10:]
        print(f"[NEXUS DEBUG] Raw database path: {db_path}", flush=True)

        # If it's an absolute path (starts with /), use it directly
        # If it's relative (no leading /), resolve it relative to app root
        if not db_path.startswith('/'):
            db_path = os.path.join(app.root_path, db_path)
            print(f"[NEXUS DEBUG] Resolved relative path to: {db_path}", flush=True)

        db_dir = os.path.dirname(db_path)
        print(f"[NEXUS DEBUG] Database directory: {db_dir}", flush=True)

        if db_dir:
            try:
                os.makedirs(db_dir, exist_ok=True)
                print(f"[NEXUS DEBUG] Directory ready: {db_dir}", flush=True)
            except Exception as e:
                print(f"[NEXUS DEBUG] FAILED to create {db_dir}: {e}", flush=True)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.messages import bp as messages_bp
    app.register_blueprint(messages_bp, url_prefix='/messages')

    from app.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    with app.app_context():
        try:
            db.create_all()
            print("[NEXUS DEBUG] db.create_all() succeeded", flush=True)
        except Exception as e:
            print(f"[NEXUS DEBUG] db.create_all() failed: {e}", flush=True)
            raise

    return app
