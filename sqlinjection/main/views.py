from flask import *
import sqlite3
import datetime
import secret_key
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


db = sqlite3.connect('test.sqlite', check_same_thread=False)


@main.route('/', methods=['POST', 'GET'])
def lobby():
    with closing(db.cursor(factory=Cursor)) as cursor:
        if request.method == 'POST':
            if request.form.get('comment_text') and request.form['comment_text'].strip():
                sql = """
                INSERT INTO `comments` (`user`, `text`, `time`) 
                VALUES ("%s", "%s", "%s");
                """ % (session.get('auth'),
                       request.form['comment_text'].strip(),
                       datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

                for msg in cursor.execute(sql):
                    flash(msg[1], category=msg[0])
                return redirect(url_for("main.lobby"))

        cursor.execute('SELECT * FROM Comments')
        comments = reversed(cursor.fetchall())
        if session.get('auth'):
            sql = """
            UPDATE Users SET
            upd="%s"
            WHERE user="%s"
            """ % (datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), session['auth'])
            cursor.execute(sql)
        db.commit()
    resp = make_response(render_template('base.html',
                                         auth=session.get('auth'),
                                         comments=comments))
    if not session.get('auth'):
        resp.set_cookie('password', '')
    return resp


@main.route('/login', methods=['POST', 'GET'])
def sign_in():
    if session.get('auth'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        cursor = db.cursor(factory=Cursor)
        user = request.form['login']
        cursor.execute('SELECT * from Users WHERE user="%s"' % user)
        data = cursor.fetchone()
        if data and data[1] == request.form['password']:
            session['auth'] = user
            resp = redirect('/')
            resp.set_cookie('password', request.form['password'])
            return resp
        cursor.close()
        return render_template('signin.html', error='Wrong login or password')
    abort(418)


@main.route('/reg', methods=['POST', 'GET'])
def reg():
    if session.get('auth'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('reg.html')
    if request.method == 'POST':
        cursor = db.cursor(factory=Cursor)
        user = request.form['login']
        password = request.form['password']
        key = request.form['key']

        cursor.execute('SELECT * from Users WHERE user="%s"' % user)
        data = cursor.fetchone()

        if data:
            abort(409)

        if secret_key.check(key):
            sql = """
            INSERT INTO `users` (`user`, `password`, `reg`) 
            VALUES ('%s', '%s', '%s');
            """ % (user, password, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
            cursor.execute(sql)
            session['auth'] = user
            resp = redirect('/')
            resp.set_cookie('password', request.form['password'])
            db.commit()
            return resp
        cursor.close()
        return render_template('reg.html', error='Bad key')
    abort(418)


@main.route('/profile')
def profile():
    if not request.args.get('user'):
        abort(404)
    user = request.args['user']
    with closing(db.cursor(factory=Cursor)) as cursor:
        cursor.execute('SELECT * from Users WHERE user="%s"' % user)
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
