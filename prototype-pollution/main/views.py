from flask import *
import sqlite3

from contextlib import closing

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


class Cursor(sqlite3.Cursor):
    def __init__(self, database):
        super().__init__(database)

    def execute(self, sql, *args):
        msg = []
        for s in sql.split(';'):
            if s.strip():
                try:
                    super().execute(s, *args)
                    msg.append(('success', s))
                except Exception as ex:
                    print(ex)
                    msg.append(('error', s + '<br>' + str(ex)))
        if not len(msg):
            return []
        if msg[0][0] == 'error':
            return msg
        return msg[1:]


db = sqlite3.connect('prototype.sqlite', check_same_thread=False)


# noinspection SqlDialectInspection
@main.route('/', methods=['POST', 'GET'])
def lobby():
    resp = make_response(render_template('base.html', auth=session.get('auth')))
    return resp


# noinspection SqlDialectInspection
@main.route('/get_timetable', methods=['GET'])
def get_timetable():
    with closing(db.cursor(factory=Cursor)) as cursor:
        cursor.execute('SELECT * FROM timetable')
        return {'objects': cursor.fetchall()}


# noinspection SqlDialectInspection
@main.route('/insert_timetable', methods=['POST'])
def insert_timetable():
    if not session.get('auth'):
        abort(403)

    key = request.form.get('key')
    value = request.form.get('value')

    if len(key) > 30 or len(value) > 200:
        abort(400)

    with closing(db.cursor(factory=Cursor)) as cursor:
        sql = """
       INSERT INTO `timetable` (`key`, `value`, `user`) 
       VALUES (?, ?, ?);
       """
        cursor.execute(sql, (key, value, session.get('auth')))
        db.commit()

    return redirect('/')


@main.route('/login', methods=['POST', 'GET'])
def sign_in():
    if session.get('auth'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        cursor = db.cursor(factory=Cursor)
        user = request.form['login']
        cursor.execute('SELECT * from Users WHERE user=?', (user,))
        data = cursor.fetchone()
        if data and data[1] == request.form['password']:
            session['auth'] = user
            resp = redirect('/')
            return resp
        cursor.close()
        return render_template('signin.html', error='Wrong login or password')
    abort(418)


@main.route('/reg', methods=['POST', 'GET'])
def reg():
    if session.get('auth'):
        return redirect('')
    if request.method == 'GET':
        return render_template('reg.html')
    if request.method == 'POST':
        cursor = db.cursor(factory=Cursor)
        user = request.form['login']

        if len(user) > 30:
            abort(400)

        password = request.form['password']

        sql = """
        INSERT INTO `users` (`user`, `password`, `reg`) 
        VALUES (?, ?, ?);
        """
        cursor.execute(sql, (user, password))
        session['auth'] = user
        resp = redirect('/')
        db.commit()
        return resp

    abort(418)


@main.route('/profile')
def profile():
    if not request.args.get('user'):
        abort(404)
    user = request.args['user']
    with closing(db.cursor(factory=Cursor)) as cursor:
        cursor.execute('SELECT * from users WHERE user=?', (user,))
        data = cursor.fetchone()
        if not data:
            abort(404)
    return render_template('pa.html', data=data)


@main.route('/logout')
def logout():
    if session.get('auth'):
        session.pop('auth')
    resp = redirect('/')
    return resp


@main.errorhandler(500)
def internal_server_error(_):
    return render_template('500.html'), 500


@main.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
