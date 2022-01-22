from flask import *
import datetime
import secret_key
import psycopg2

from psycopg2 import extensions

import config

from contextlib import closing, contextmanager

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


class Cursor(extensions.cursor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


@contextmanager
def session_scope():
    connection = psycopg2.connect(
        user=config.DATABASE_USER,
        password=config.DATABASE_PASSWORD,
        host=config.DATABASE_HOST,
        cursor_factory=Cursor,
    )

    try:
        yield connection.cursor()
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()


with session_scope() as cursor:
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            "user"     text,
            password text,
            reg      date,
            upd      date
        )
        """
    )

    cursor.execute(
        """CREATE TABLE comments
            (
                "user" text,
                text text,
                time date
            )
        """
    )


# noinspection SqlDialectInspection
@main.route('/', methods=['POST', 'GET'])
def lobby():
    with session_scope() as cursor:
        if request.method == 'POST':
            if request.form.get('comment_text') and request.form['comment_text'].strip():
                sql = """
                INSERT INTO comments ("user", text, time) 
                VALUES ('%s', '%s', '%s');
                """ % (
                    session.get('auth'),
                    request.form['comment_text'].strip(),
                    datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                )

                for msg in cursor.execute(
                        sql
                ):
                    flash(msg[1], category=msg[0])

                return redirect(url_for("main.lobby"))

        cursor.execute('SELECT * FROM Comments')
        comments = reversed(cursor.fetchall())

        if session.get('auth'):
            sql = """
            UPDATE Users SET
            upd='%s'
            WHERE "user"='%s'
            """ % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), session['auth'])
            cursor.execute(sql)

    resp = make_response(render_template('base.html',
                                         auth=session.get('auth'),
                                         comments=comments))
    if not session.get('auth'):
        resp.set_cookie('password', '')
    return resp


@main.route('/login', methods=['POST', 'GET'])
def sign_in():
    if session.get('auth'):
        return redirect('')
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        with session_scope() as cursor:
            user = request.form['login']
            cursor.execute('SELECT * from Users WHERE "user"=%s', (user,))
            data = cursor.fetchone()
            if data and data[1] == request.form['password']:
                session['auth'] = user
                resp = redirect('/')
                return resp
            return render_template('signin.html', error='Wrong login or password')
    abort(418)


@main.route('/reg', methods=['POST', 'GET'])
def reg():
    if session.get('auth'):
        return redirect('')
    if request.method == 'GET':
        return render_template('reg.html')
    if request.method == 'POST':
        with session_scope() as cursor:
            user = request.form['login']
            password = request.form['password']
            key = request.form['key']

            if secret_key.check(key):
                sql = """
                INSERT INTO users ("user", password, reg) 
                VALUES (%s, %s, %s);
                """
                cursor.execute(sql, (user, password, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
                session['auth'] = user
                resp = redirect('/')
                return resp
        return render_template('reg.html', error='Bad key')

    abort(418)


@main.route('/profile')
def profile():
    if not request.args.get('user'):
        abort(404)
    user = request.args['user']
    with session_scope() as cursor:
        cursor.execute('SELECT * from Users WHERE "user"=%s', (user,))
        data = cursor.fetchone()
        if not data:
            abort(404)
    return render_template('pa.html', data=data)


@main.route('/logout')
def logout():
    if session.get('auth'):
        session.pop('auth')
    resp = redirect('/')
    resp.set_cookie('password', '')
    return resp


@main.errorhandler(500)
def internal_server_error(_):
    return render_template('500.html'), 500


@main.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
