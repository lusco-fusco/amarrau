from datetime import timedelta
from project.environment import get_env


env = get_env()


class ConfigFlask(object):
    DEBUG = env.get("DEBUG")
    CSRF_ENABLED = env.get("CSRF_ENABLED")
    HOST = env.get("HOST")
    PORT = env.get("PORT")
    SCOUTER_ENDPOINT = 'http://{}:{}/scan'.format(env.get("SCOUTER_HOST"), env.get("SCOUTER_PORT"))


class ConfigDB(object):
    SQLALCHEMY_DATABASE_URI = "postgres://{0}:{1}@{2}:{3}/{4}".format(
        env.get("DATABASE_USER"),
        env.get("DATABASE_PASSWORD"),
        env.get("DATABASE_HOST"),
        env.get("DATABASE_PORT"),
        env.get("DATABASE_NAME")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = env.get("TRACK_MODIFICATIONS")
    MIGRATION_PATH = env.get('MIGRATION_PATH')


class ConfigMail(object):
    MAIL_USERNAME = env.get("MAIL_USERNAME")
    MAIL_PASSWORD = env.get("MAIL_PASSWORD")
    MAIL_SERVER = env.get("MAIL_SERVER")
    MAIL_PORT = env.get("MAIL_PORT")
    MAIL_USE_SSL = env.get("MAIL_USE_SSL")


class ConfigJWT(object):
    JWT_SECRET_KEY = env.get('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=150)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class ConfigRedis(object):
    HOST = env.get('REDIS_HOST')
    PORT = env.get('REDIS_PORT')
    PASSWORD = env.get('REDIS_PASSWORD')
    DECODE_RESPONSES = True
