import os

from environs import Env
from os import path


def get_env():
    if path.exists(os.getcwd() + '/.env'):
        # Load env file
        env = Env()
        env.read_env(os.getcwd() + '/.env')
        # Flask application
        env.bool("CSRF_ENABLED")
        env.bool("DEBUG")
        env.str("HOST")
        env.int("PORT")
        env.str("MIGRATION_PATH")
        env.bool("SQLALCHEMY_ECHO")
        env.str("TRACK_MODIFICATIONS")
        # Postgres database
        env.str("DATABASE_USER")
        env.str("DATABASE_PASSWORD")
        env.str("DATABASE_HOST")
        env.str("DATABASE_PORT")
        env.str("DATABASE_NAME")
        # JWT
        env.str("JWT_SECRET_KEY")
        # Mail
        env.str("MAIL_USERNAME")
        env.str("MAIL_PASSWORD")
        env.str("MAIL_SERVER")
        env.str("MAIL_PORT")
        env.str("MAIL_USE_SSL")
        # Redis
        env.str("REDIS_PORT")
        env.str("REDIS_HOST")
        env.str("REDIS_PASSWORD")
        # Scouter
        env.str("SCOUTER_HOST")
        env.str("SCOUTER_PORT")
        env.str("SCOUTER_X_API_KEY")
        return env.dump()
    env = dict()
    # Flask application
    env['DEBUG'] = bool(os.getenv('DEBUG')) or None
    env['CSRF_ENABLED'] = bool(os.getenv('CSRF_ENABLED')) or None
    env['HOST'] = os.getenv('HOST') or None
    env['PORT'] = int(os.getenv('PORT') or 5000)
    env['MIGRATION_PATH'] = os.getenv('MIGRATION_PATH') or ''
    env['SQLALCHEMY_ECHO'] = bool(os.getenv('SQLALCHEMY_ECHO')) or None
    env['TRACK_MODIFICATIONS'] = os.getenv("TRACK_MODIFICATIONS") or True
    # Postgres database
    env['DATABASE_USER'] = os.getenv('DATABASE_USER') or None
    env['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD') or None
    env['DATABASE_HOST'] = os.getenv('DATABASE_HOST') or None
    env['DATABASE_PORT'] = os.getenv('DATABASE_PORT') or None
    env['DATABASE_NAME'] = os.getenv('DATABASE_NAME') or None
    # JWT
    env['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or None
    # Mail
    env['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME") or None
    env['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD") or None
    env['MAIL_SERVER'] = os.getenv("MAIL_SERVER") or None
    env['MAIL_PORT'] = os.getenv("MAIL_PORT") or None
    env['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL") or None
    # Redis
    env['REDIS_PORT'] = os.getenv("REDIS_PORT") or None
    env['REDIS_HOST'] = os.getenv("REDIS_HOST") or None
    env['REDIS_PASSWORD'] = os.getenv("REDIS_PASSWORD") or None
    # Scouter
    env['SCOUTER_HOST'] = os.getenv("SCOUTER_HOST") or None
    env['SCOUTER_PORT'] = os.getenv("SCOUTER_PORT") or None
    env['SCOUTER_X_API_KEY'] = os.getenv("SCOUTER_X_API_KEY") or None
    return env
