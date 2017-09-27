import datetime
import urllib.request
import shutil
import os

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

direccion_csv = 'http://pronosticos.gob.mx/Documentos/Historicos/Melate.csv'
archivo_destino = 'melate_historico.csv'

if not os.path.exists(archivo_destino):
    with urllib.request.urlopen(direccion_csv) as response, open(archivo_destino, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
else:
    print('El archivo ya existe')

registros = open(archivo_destino, 'r')
registros_lista = []

for r in reversed(list(registros.readlines())):
    r = r.replace('\n', '').split(',')
    try:
        r[-1] = datetime.datetime.strptime(r[-1], '%d/%m/%Y').date()
        registros_lista.append(r)
    except ValueError:
        pass


def llenar_tabla_vacia():
    clave_melate = 40
    for lista in registros_lista:
        concurso = int(lista[1])
        num1 = int(lista[2])
        num2 = int(lista[3])
        num3 = int(lista[4])
        num4 = int(lista[5])
        num5 = int(lista[6])
        num6 = int(lista[7])
        num7 = int(lista[8])
        bolsa = int(lista[9])
        fecha = lista[10]

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO melate2(producto, concurso, num1, num2, num3, num4, num5, num6, num7, bolsa, fecha)"
                query += " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (clave_melate, concurso, num1, num2, num3, num4, num5, num6, num7, bolsa, fecha))
                # Funcionará si le doy commit en el finally ?
                connection.commit()
        finally:
            pass


def get_concurso():
    try:
        with connection.cursor() as cursor:
            query = "SELECT concurso FROM melate2 ORDER BY concurso DESC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return False
            else:
                return result
    finally:
        pass


if get_concurso() == False:
    print('tabla vacía, se llenará con el último reporte.')
    llenar_tabla_vacia()
else:
    print(get_concurso())