import os

# Paste your Neon connection string here between the quotes.
# Example: NEON_URL = "postgresql://neondb_owner:password@host/neondb?sslmode=require"
# all u hackers out there, dont worry, i dont care if u hack this bc it just has simple users table. go ahead.
NEON_URL = "postgresql+pg8000://neondb_owner:npg_QoPmpGl0qj1N@ep-long-queen-b4j8rvc0-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=true"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI') or 'memory://'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "app.db")}'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    # Hardcoded Neon PostgreSQL. No environment variable needed.
    SQLALCHEMY_DATABASE_URI = NEON_URL


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig,
}
