from app.models import Task, User
from app.extensions import db

def test_task_creation(client, app):
    with app.app_context():
        admin = User(username='taskadmin', is_admin=True)
        admin.set_password('adminpass123')
        db.session.add(admin)
        db.session.commit()

    client.post('/login', data={
        'username': 'taskadmin',
        'password': 'adminpass123'
    }, follow_redirects=True)

    response = client.post('/tasks/create', data={
        'title': 'Test Task',
        'description': 'Test Description',
        'assigned_to': 0
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None
        assert task.completed is False

def test_task_completion(client, app):
    with app.app_context():
        admin = User(username='completeadmin', is_admin=True)
        admin.set_password('adminpass123')
        db.session.add(admin)
        db.session.commit()

        task = Task(title='Complete Me', description='Do it', assigned_to=admin.id)
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    client.post('/login', data={
        'username': 'completeadmin',
        'password': 'adminpass123'
    }, follow_redirects=True)

    response = client.post(f'/tasks/{task_id}/complete', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.completed is True

def test_non_admin_cannot_create_task(client, app):
    with app.app_context():
        user = User(username='normaluser', is_admin=False)
        user.set_password('userpass123')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={
        'username': 'normaluser',
        'password': 'userpass123'
    }, follow_redirects=True)

    response = client.get('/tasks/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Admin access required' in response.data
