
from flask import *
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "CRUD"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# HOME PAGE


@app.route('/')
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    con.execute(sql)
    res = con.fetchall()

    return render_template('home.html', datas=res)


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "INSERT INTO users (NAME,AGE,CITY) VALUES(%s,%s,%s)"
        con.execute(sql, [name, age, city])
        mysql.connection.commit()
        con.close()
        flash(f"{name} detail added!")
        return redirect(url_for("home"))

    return render_template('adduser.html')


@app.route('/edituser/<int:id>', methods=["GET", "POST"])
def edituser(id):
    con = mysql.connection.cursor()
    sql = "SELECT * FROM users where ID = %s"
    con.execute(sql, [id])
    res = con.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "UPDATE users set NAME = %s, AGE =%s, CITY =%s where ID = %s"
        con.execute(sql, [name, age, city, id])
        mysql.connection.commit()
        con.close()
        flash(f"User {id} was updated!")
        return redirect(url_for('home'))
    return render_template("edituser.html", datas=res)


@app.route('/deleteuser/<int:id>/<string:name>', methods=['GET', 'POST'])
def deleteuser(id, name):
    con = mysql.connection.cursor()
    sql = "DELETE from users where ID = %s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    flash(f"{name} was deleted!")
    return redirect(url_for('home'))


if '__main__' == __name__:
    app.secret_key = "asde"
    app.run(debug=True)
