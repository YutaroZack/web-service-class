from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flaskext.mysql import MySQL
import sys
import random

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ci6glfn_af0'
app.config['MYSQL_DATABASE_PASSWORD'] = '4S83Wa9w'
app.config['MYSQL_DATABASE_DB'] = 'ci6glfn_af0'
app.config['MYSQL_DATABASE_HOST'] = '175.184.35.36'

mysql.init_app(app)

app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'


@app.before_request
def before_request():
    if session.get('uID') is not None:
        return
    if request.path == '/login':
        return
    #return redirect('/')


@app.route("/", methods=['GET'])
def index():
    session.pop('uID', None)
    return render_template("index.html")

@app.route("/index", methods=['GET'])
def index2():
    return render_template("index.html")


@app.route("/user_register", methods=["GET"])
def register():

    return render_template("user_register.html")


@app.route("/login", methods=["GET"])
def hello():
    if session.get('uID'):
        return redirect('/home')
    return render_template("host_login.html")


@app.route("/uEX_regist", methods=["get"])
def uEX_register():
    if session.get('uID'):
        return render_template("uEX_withdrawal.html")
    return render_template("uEX_register.html")


@app.route("/uEX_get", methods=["GET"])
def uEX_get():
    conn = mysql.connect()
    cursor = conn.cursor()

    uex = ''
    uexlen = int(8)
    s = 'abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456789'

    for i in range(uexlen):
        uex += random.choice(s)

    sql = 'UPDATE user_info SET uEX = "%s" WHERE uID = "%s"' % (uex, session.get('uID'))

    cursor.execute(sql)
    conn.commit()

    print uex

    session.pop('uID', None)

    return render_template("uEX_result.html", uex=uex)


@app.route("/uEX_withdrawal", methods=["GET"])
def uEX_withdrawal():
    if session.get('uID'):
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = 'UPDATE user_info SET uEX = 0 WHERE uID = "%s"' % session.get('uID')
        cursor.execute(sql)
        conn.commit()

        session['uEX'] = 0

    return redirect("home")


@app.route("/post_content", methods=["GET"])
def post_content():
    if session.get('uID'):
        return render_template("post_content.html")
    return redirect("login")


@app.route("/topic_add", methods=['POST'])
def topic_add():
    if request.form['title'] and request.form['main']:
        title = request.form['title']
        main = request.form['main']
        uName = session.get('uID')

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = 'INSERT INTO Contents (uName, TITLE, CONTENT) values("%s", "%s", "%s")' % (uName, title, main)

        cursor.execute(sql)
        conn.commit()

        content = cursor.fetchall()
        print(content)

    return redirect("home")


@app.route("/comment_add", methods=['POST'])
def comment_add():
    comment = request.form['comment']
    if session.get('uID'):
        uName = session.get('uID')
    else:
        uName = "No Name"
    cID = int(request.form['cID'])
    hName = request.form['hName']

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = 'INSERT INTO Comments (uName, cID, COMMENT, hName) values("%s", "%d", "%s", "%s")' % (uName, cID, comment, hName)

    cursor.execute(sql)
    conn.commit()

    comment = cursor.fetchall()
    print(comment)

    if session.get('uID'):
        return redirect("home")
    return redirect("all_topics")


@app.route("/store", methods=['POST'])
def store():

    if request.form['regist_uID'] and request.form['regist_uPASS']:

        conn = mysql.connect()
        cursor = conn.cursor()
        # cursorC = conn.cursor()

        uid = request.form['regist_uID']
        upass = request.form['regist_uPASS']
        # uex = request.form['regist_uEX']

        # check_sql = 'SELECT uID FROM user_info WHERE uID = "%s"' % (uid)
        # cursorC.execute(check_sql)
        # conn.commit()

        # check = cursorC.fetchone()
        # print(check)

        # return check

        # if check_sql != ' ':
        #     uid = ''
        #     upass = ''
        #     check_sql = ''

        #     return render_template('already_error.html')
            
        sql = 'INSERT INTO user_info (uID, uPASS) values("%s", "%s")' % (uid, upass)

        cursor.execute(sql)
        conn.commit()

        cursor.execute("SELECT * from user_info")
        data = cursor.fetchone()
        print(data)

        if data:
            session['uID'] = request.form['regist_uID']
            return redirect('uEX_get')
    return render_template('regist_error.html')


@app.route('/login_check', methods=['GET', 'POST'])
def login_check():

    conn = mysql.connect()
    cursor = conn.cursor()

    uid = request.form['login_uID']
    upass = request.form['login_uPASS']
    uex = request.form['login_uEX']

    sql = 'SELECT * FROM user_info WHERE uID = "%s" AND uPASS = "%s" AND uEX = "%s"' % (uid, upass, uex)
    
    if sql is None:
        return render_template('login_error.html')

    cursor.execute(sql)
    conn.commit()

    user = cursor.fetchone()
    print(user)

    if user:
        session['uID'] = request.form['login_uID']

        return redirect(url_for('home'))
    return render_template('login_error.html')


@app.route('/home', methods=['GET'])
def home():
    if session.get('uID'):

        uid = session.get('uID')

        conn = mysql.connect()
        cursorU = conn.cursor()
        cursorC = conn.cursor()
        cursorCom = conn.cursor()

        user_sql = 'SELECT * FROM user_info WHERE uID = "%s"' % (uid)
        Contents_sql = 'SELECT * FROM Contents WHERE uName = "%s"' % (uid)
        Comments_sql = 'SELECT * FROM Comments WHERE hName = "%s"' % (uid)

        cursorU.execute(user_sql)
        cursorC.execute(Contents_sql)
        cursorCom.execute(Comments_sql)
        conn.commit()

        user = cursorU.fetchone()
        contents = cursorC.fetchall()
        comments = cursorCom.fetchall()
        print(user)
        print(contents)
        print(comments)

        return render_template('home.html', user=user, contents=contents, comments=comments)
    return render_template('index.html')


@app.route('/all_topics', methods=['GET'])
def all_topics():

    uid = session.get('uID')

    conn = mysql.connect()
    cursorU = conn.cursor()
    cursorC = conn.cursor()
    cursorCom = conn.cursor()

    user_sql = 'SELECT * FROM user_info WHERE uID = "%s"' % (uid)
    Contents_sql = 'SELECT * FROM Contents'
    Comments_sql = 'SELECT * FROM Comments'

    cursorU.execute(user_sql)
    cursorC.execute(Contents_sql)
    cursorCom.execute(Comments_sql)
    conn.commit()

    user = cursorU.fetchone()
    contents = cursorC.fetchall()
    comments = cursorCom.fetchall()
    print(user)
    print(contents)
    print(comments)

    return render_template('all_topics.html', user=user, contents=contents, comments=comments)


@app.route("/change_user", methods=["GET"])
def change_user():
    session.pop('uID', None)
    return render_template('host_login.html')


@app.route("/logout", methods=["GET"])
def logout():
    session.pop('uID', None)
    return redirect("/")


if __name__ == '__main__':
    app.debug = True
    app.run()
