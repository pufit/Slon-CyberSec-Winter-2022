

class Configuration(object):
    SECRET_KEY = '100000'
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_NAME = 'flask_session'


VERSION = '1.0a'

# ---------------------------- #
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'toor'
MYSQL_DATABASE_DB = 'CTF'
MYSQL_DATABASE_HOST = 'localhost'
# ---------------------------- #


# ---------------------------- #
HTTP_PORT = 8001
HTTP_IP = '0.0.0.0'
# ---------------------------- #

# ---------------------------- #
WIN_SCORE = 999
SHEET_NAME = 'test'
SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET = 'client_secret.json'
UPDATE_DELAY = 60
COMMANDS_NAME_START = (2, 2)
COMMANDS_SCORE_START = (2, 6)
# ---------------------------- #
