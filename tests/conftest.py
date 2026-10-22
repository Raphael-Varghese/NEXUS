import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(username='adminuser', is_admin=True)
        user.set_password('adminpass123')
        db.session.add(user)
        db.session.commit()
        return user.id

@pytest.fixture
def regular_user(app):
    with app.app_context():
        user = User(username='regularuser', is_admin=False)
        user.set_password('userpass123')
        db.session.add(user)
        db.session.commit()
        return user.id
