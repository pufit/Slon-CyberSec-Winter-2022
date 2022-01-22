from flask import *
from main.views import main
from config import *

app = Flask(__name__, static_folder=None, template_folder=None)
app.register_blueprint(main)

app.config.from_object(Configuration)


@app.route('/debug')
def debug_page():
    raise Exception('Debug')


if __name__ == '__main__':
    app.run(HTTP_IP, port=HTTP_PORT)
