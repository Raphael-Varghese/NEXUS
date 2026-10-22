import os
import sys

from flask import Flask
from flask_limiter import Limiter
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=lambda: "global")
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__, instance_relative_config=True)

    # Import config here to avoid circular issues
    from config import config as config_dict
    config_class = config_dict.get(config_name, config_dict['default'])
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

    # Ensure SQLite database directory exists
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
    print(f"[NEXUS] Database URI: {db_uri}", flush=True)

    if db_uri.startswith('sqlite://'):
        # Extract the actual file path from the URI
        # sqlite:////tmp/app.db  -> /tmp/app.db
        # sqlite:///data/app.db  -> data/app.db (relative, broken)
        path = db_uri.replace('sqlite://', '')
        if not path.startswith('/'):
            # Relative path - resolve against current working directory
            path = os.path.join(os.getcwd(), path)
            print(f"[NEXUS] Resolved relative path to: {path}", flush=True)

        db_dir = os.path.dirname(path)
        if db_dir:
            try:
                os.makedirs(db_dir, exist_ok=True)
                print(f"[NEXUS] Directory ready: {db_dir}", flush=True)
            except Exception as e:
                print(f"[NEXUS] WARNING: Could not create {db_dir}: {e}", flush=True)

    # Register blueprints
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

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("[NEXUS] db.create_all() SUCCESS", flush=True)
        except Exception as e:
            print(f"[NEXUS] db.create_all() FAILED: {e}", flush=True)
            raise

    return app
