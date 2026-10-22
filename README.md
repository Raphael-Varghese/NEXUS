# NEXUS 2.0

A modern, secure, modular Flask web application for user management, messaging, and task assignment. Originally built at age 12 as a single-file Flask experiment, NEXUS has been completely re-architected into a production-ready blueprint-based platform with hardened security, Docker support, and a full test suite.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Security](#security)
- [Screenshots](#screenshots)
- [Quick Start](#quick-start)
- [Docker](#docker)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)
- [Credits](#credits)

---

## Features

### Authentication & Authorization
- Secure registration and login with Werkzeug password hashing
- First registered user is automatically promoted to Admin
- Role-based access control (Admin vs Standard User)
- Flask-Login session management
- Rate limiting on authentication endpoints

### Messaging System
- Send messages to any registered user
- Users see only messages they sent or received
- Admins can view all messages globally
- Paginated message history (10 per page)
- Full-text search through message content
- Timestamp formatting

### Task Management
- Admins can create, edit, and assign tasks to users
- Users can view tasks assigned to them
- Task completion tracking with status badges
- Search tasks by title or description
- Empty state handling

### Admin Panel
- Dedicated user management interface
- Promote standard users to admin
- Demote admins back to standard users (prevents demoting the last admin)
- Delete users with automatic cleanup of their messages and task assignments
- Admin-only Python and Terminal consoles

### Interactive Consoles
- **User Python Console:** Sandboxed execution environment with a restricted builtin whitelist
- **User Terminal:** Allowlist-based command execution with `shell=False` safety
- **Admin Python Console:** Full Python execution environment (admin only)
- **Admin Terminal:** System command execution via `subprocess` with `shell=False` (admin only)

### UI/UX
- Responsive Bootstrap 5 sidebar layout
- Bootstrap Icons throughout
- Color-coded flash messages with dismissible alerts
- Dark mode toggle with localStorage persistence
- Profile page with activity statistics
- Dashboard stat cards

---

## Architecture

NEXUS 2.0 follows the Flask application factory pattern with Blueprint-based modularity:

```
app/
  __init__.py          # Application factory
  extensions.py         # Shared extensions (db, login, csrf, limiter, migrate)
  models.py             # SQLAlchemy models (User, Message, Task)
  forms.py              # WTForms with validation
  decorators.py           # Custom route decorators
  auth/                 # Authentication blueprint
  main/                 # Dashboard, profile, consoles
  messages/             # Messaging blueprint
  tasks/                # Task management blueprint
  admin/                # Admin tools and user management
templates/              # Jinja2 HTML templates
tests/                  # pytest suite
config.py               # Environment-based configuration
run.py                  # Development entry point
setup.py                # One-command bootstrap script
```

---

## Security

NEXUS 2.0 was designed with security as a first-class concern, directly addressing the vulnerabilities present in the original codebase:

| Feature | Implementation |
|---------|---------------|
| CSRF Protection | Flask-WTF on all forms |
| Rate Limiting | Flask-Limiter (3/min register, 5/min login) |
| Password Policy | Minimum 6 characters with server-side validation |
| Secret Management | Environment variables via `python-dotenv` |
| Console Sandboxing | Restricted `__builtins__` whitelist for user Python; allowlist for user terminal |
| Shell Safety | `shell=False` with `shlex.split()` on all subprocess calls |
| SQL Injection Prevention | SQLAlchemy ORM throughout |
| Session Security | Flask-Login with configurable secret key |

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Linux / macOS

```bash
python setup.py
```

This installs dependencies, initializes the database, and opens the app in your default browser automatically.

### Windows

Gunicorn is not supported on Windows, so use the Windows-specific requirements file:

```bash
pip install -r requirements_win.txt
python run.py
```

Then visit `http://127.0.0.1:5000` in your browser.

### Environment Variables

Copy the example environment file and edit as needed:

```bash
cp .env.example .env
```

---

## Docker

Build and run with Docker Compose (Linux/macOS/WSL only):

```bash
docker-compose up --build
```

The app will be available at `http://localhost:5000`.

---

## Testing

Run the full test suite with pytest:

```bash
python -m pytest tests/ -v
```

Current coverage includes:
- Authentication (register, login, logout)
- First-user admin promotion
- Protected route redirects
- Task creation and completion
- Admin access control enforcement

---

## Project Structure

```
NEXUS/
  app/
    __init__.py
    extensions.py
    models.py
    forms.py
    decorators.py
    auth/
      __init__.py
      routes.py
    main/
      __init__.py
      routes.py
    messages/
      __init__.py
      routes.py
    tasks/
      __init__.py
      routes.py
    admin/
      __init__.py
      routes.py
  templates/
    base.html
    login.html
    register.html
    dashboard.html
    profile.html
    messages.html
    tasks.html
    create_task.html
    edit_task.html
    admin_users.html
    admin_python.html
    admin_terminal.html
    user_python.html
    user_terminal.html
  tests/
    conftest.py
    test_auth.py
    test_tasks.py
  config.py
  run.py
  setup.py
  requirements.txt
  requirements1.txt
  Dockerfile
  docker-compose.yml
  .env
  .dockerignore
  .gitignore
```

---

## Tech Stack

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Limiter, Flask-Migrate
- **Frontend:** Bootstrap 5, Bootstrap Icons, vanilla JavaScript
- **Database:** SQLite (development), PostgreSQL-compatible (production)
- **Security:** Werkzeug, CSRFProtect, python-dotenv
- **Testing:** pytest, pytest-flask
- **Deployment:** Docker, Gunicorn

---

## Roadmap

- [x] Security hardening (CSRF, rate limiting, sandboxed consoles)
- [x] Blueprint architecture
- [x] WTForms validation
- [x] Pagination and search
- [x] Flash categories and dismissible alerts
- [x] User profile with activity stats
- [x] Admin user management panel
- [x] Dark mode toggle
- [x] Docker support
- [x] pytest test suite
- [ ] WebSocket real-time chat
- [ ] File uploads
- [ ] Activity logs / audit trail
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] API endpoints (REST/JSON)

---

## Credits

Built by [Raphael Varghese](https://github.com/Raphael-Varghese).


---

## License

MIT License. See LICENSE for details.

## Disclaimer

The admin Python and Terminal consoles are powerful tools intended for local or trusted environments only. While NEXUS 2.0 includes significant security improvements over the original version, the admin consoles still execute code with the privileges of the running process. Use responsibly.
