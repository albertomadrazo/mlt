import datetime
import urllib.request
from bs4 import BeautifulSoup

import pymysql
import pymysql.cursors

# Conecta a MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='melate',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

pagina_resultados = 'http://www.pronosticos.gob.mx/Paginas/Melate/historico-melate'
pagina = urllib.request.urlopen(pagina_resultados)
soup = BeautifulSoup(pagina, 'html.parser')

tabla_resultados = soup.find('table', attrs={'id':'MainContent_gvwHistoricosMelate'})

rowan = tabla_resultados.findAll('tr')

sorteos = []
for r in rowan:
    tede = r.findAll('td')
    sorteo = []
    for i, val in enumerate(tede):
        sorteo.append(val.text)

    sorteos.append(sorteo)


for s in sorteos:
    if len(s) > 0:
        print('Sorteo {}\tFecha: {}\tNúmeros: {}'.format(*s))

        # Formatea los numeros ganadores y los pone en un array
        s[2] = s[2].replace('-', ' ').split(' ')
        for i, num in enumerate(s[2]):
            if num[0] == '0':
                s[2][i] = num[1:]

        # Formatea la fecha para que sea aceptable por MySQL
        s[1] = datetime.datetime.strptime(s[1], '%d/%m/%Y').date()





def actualizaDB(listaConcursos):
    clave_melate = 40
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM melate LIMIT 10";
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()

    for lista in listaConcursos:
        concurso = lista[0]
        num1 = lista[1]
        num2 = lista[2]
        num3 = lista[3]
        num4 = lista[4]
        num5 = lista[5]
        num6 = lista[6]
        num7 = lista[7]
        bolsa = lista[]
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO melate(NPRODUCTO, CONCURSO, R1, R2, R3, R4, R5, R6, R7, BOLSA, FECHA_CONCURSO)"
                query += " VALUES(%d, %d, %d, %d, %d, %d, %d, %d, %d, %s, %s)"
                cursor.execute(query, (clave_melate, concurso, num1, num2, num3, num4, num5, num6, num7, bolsa, fecha))
                connection.commit()
        finally:
            connection.close()
actualizaDB(sorteos)

# for y in sorteos:
#     print(y)