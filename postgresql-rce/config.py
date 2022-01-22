

class Configuration(object):
    SECRET_KEY = '00000000000000000000000000000000'
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_NAME = 'flask_session'


VERSION = '1.0a'

# ---------------------------- #
DATABASE_USER = 'docker'
DATABASE_PASSWORD = 'sososecret'
DATABASE_DB = 'docker'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
# ---------------------------- #


# ---------------------------- #
HTTP_PORT = 8003
HTTP_IP = '0.0.0.0'
# ---------------------------- #
