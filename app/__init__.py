import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf, limiter, migrate

def create_app(config_class=Config):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in first."

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.messages import bp as messages_bp
    app.register_blueprint(messages_bp)

    from app.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
