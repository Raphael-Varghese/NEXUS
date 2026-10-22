import os
from app import create_app
from app.extensions import db

config_name = os.environ.get('FLASK_CONFIG', 'config.DevelopmentConfig')
app = create_app(config_name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug_mode = app.config.get('DEBUG', False)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
