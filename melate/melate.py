import os
import locale
from time import strftime
import datetime

from flask_mysqldb import MySQL
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from secrets import my_db, my_secret_key, my_user, my_password

locale.setlocale(locale.LC_ALL, "es_MX.utf8")

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
	cur.execute("SELECT * FROM melate2 ORDER BY concurso DESC LIMIT 5")
	concursos = cur.fetchall()

	for c in concursos:
		fecha_formateada = strftime("%A %d de %B, %Y", c['fecha'].timetuple())
		c['fecha'] = fecha_formateada.decode('utf8')

	return render_template('index.html', concursos=concursos)


@app.route('/numero')
def numero():
	numero = request.args.get('n')
	cur = mysql.connection.cursor()
	ocurrencias = 0
	query = "SELECT COUNT(*) FROM melate2 WHERE num1='"+numero+ \
			"' OR num2='"+numero+"' OR num3='"+numero+"' OR num4='"+numero+ \
			"' OR num5='"+numero+"' OR num6='"+numero+"' OR num7='"+numero+"'"
	cur.execute(query)
	historia_numero = cur.fetchall()[0]['COUNT(*)']

	return str(historia_numero)


if __name__ == '__main__':
	app.run(debug=True)
