import os

print("[NEXUS CONFIG] Loading config.py v2 - PostgreSQL only", flush=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI') or 'memory://'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "instance", "app.db")}'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    # NO SQLITE FALLBACK. PostgreSQL only.
    db_url = os.environ.get('DATABASE_URL')
    print(f"[NEXUS CONFIG] DATABASE_URL found: {bool(db_url)}", flush=True)
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set! "
            "Add it to Netrun Secrets with your Neon connection string."
        )
    SQLALCHEMY_DATABASE_URI = db_url


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
