from app.models import User

def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register_and_login(client, app):
    response = client.post('/register', data={
        'username': 'raphael',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post('/login', data={
        'username': 'raphael',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_protected_routes_redirect(client):
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302

def test_first_user_becomes_admin(client, app):
    client.post('/register', data={
        'username': 'firstuser',
        'password': 'password123'
    }, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username='firstuser').first()
        assert user is not None
        assert user.is_admin is True

def test_logout(client, app):
    client.post('/register', data={
        'username': 'logoutuser',
        'password': 'password123'
    }, follow_redirects=True)

    client.post('/login', data={
        'username': 'logoutuser',
        'password': 'password123'
    }, follow_redirects=True)

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
