import os

from flask_mysqldb import MySQL

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from .secrets import my_db, my_secret_key, my_user, my_password


app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
	MYSQL_DB=my_db,
	SECRET_KEY=my_secret_key,
	MYSQL_USER=my_user,
	MYSQL_PASSWORD=my_password,
	MYSQL_CURSORCLASS='DictCursor'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

mysql = MySQL(app)


@app.route('/')
def sorteos():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM melate LIMIT 20")
	rv = cur.fetchall()
	for ja in rv:
		print(ja)
		
	return str(rv)

if __name__ == '__main__':
	app.run(debug=True)
